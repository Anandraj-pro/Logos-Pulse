"""
One-time migration: SQLite -> Supabase.
Migrates all data from data/tracker.db into Supabase under a specified user.

Usage:
    python migrations/migrate_sqlite.py <user_email>

Example:
    python migrations/migrate_sqlite.py anandrajpandiri@gmail.com
"""

import sys
import os
import sqlite3
import json
import toml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

secrets_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ".streamlit", "secrets.toml"
)
secrets = toml.load(secrets_path)

from supabase import create_client

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tracker.db")


def migrate(user_email: str):
    url = secrets["supabase"]["url"]
    key = secrets["supabase"]["service_role_key"]
    client = create_client(url, key)

    # Find user by email
    users = client.auth.admin.list_users()
    user = next((u for u in users if u.email == user_email), None)
    if not user:
        print(f"ERROR: No user found with email {user_email}")
        sys.exit(1)

    user_id = user.id
    print(f"Migrating data for: {user_email} (ID: {user_id})")

    if not os.path.exists(DB_PATH):
        print(f"ERROR: SQLite database not found at {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # 1. Daily Entries
    rows = conn.execute("SELECT * FROM daily_entries ORDER BY date").fetchall()
    print(f"\nDaily entries: {len(rows)}")
    for row in rows:
        data = {
            "user_id": user_id,
            "date": row["date"],
            "prayer_minutes": row["prayer_minutes"],
            "bible_book": row["bible_book"],
            "chapters_read": json.loads(row["chapters_read"]) if row["chapters_read"] else None,
            "chapters_display": row["chapters_display"],
            "sermon_title": row["sermon_title"],
            "sermon_speaker": row["sermon_speaker"],
            "youtube_link": row["youtube_link"],
            "report_copied": bool(row["report_copied"]),
        }
        try:
            client.table("daily_entries").upsert(data, on_conflict="user_id,date").execute()
            print(f"  {row['date']}: OK")
        except Exception as e:
            print(f"  {row['date']}: FAILED - {e}")

    # 2. Weekly Assignments
    rows = conn.execute("SELECT * FROM weekly_assignments ORDER BY id").fetchall()
    print(f"\nWeekly assignments: {len(rows)}")
    for row in rows:
        data = {
            "user_id": user_id,
            "book": row["book"],
            "start_chapter": row["start_chapter"],
            "end_chapter": row["end_chapter"],
            "total_chapters": row["total_chapters"],
            "week_start_date": row["week_start_date"],
            "week_end_date": row["week_end_date"],
            "daily_breakdown": json.loads(row["daily_breakdown"]) if isinstance(row["daily_breakdown"], str) else row["daily_breakdown"],
            "status": row["status"],
        }
        try:
            client.table("weekly_assignments").insert(data).execute()
            print(f"  {row['book']} {row['start_chapter']}-{row['end_chapter']}: OK")
        except Exception as e:
            print(f"  {row['book']}: FAILED - {e}")

    # 3. Settings
    rows = conn.execute("SELECT * FROM app_settings").fetchall()
    print(f"\nSettings: {len(rows)}")
    for row in rows:
        data = {"user_id": user_id, "key": row["key"], "value": row["value"]}
        try:
            client.table("app_settings").upsert(data, on_conflict="user_id,key").execute()
            print(f"  {row['key']}: OK")
        except Exception as e:
            print(f"  {row['key']}: FAILED - {e}")

    # 4. Sermon Notes
    rows = conn.execute("SELECT * FROM sermon_notes ORDER BY id").fetchall()
    print(f"\nSermon notes: {len(rows)}")
    for row in rows:
        data = {
            "user_id": user_id,
            "title": row["title"],
            "speaker": row["speaker"],
            "sermon_date": row["sermon_date"],
            "notes_text": row["notes_text"],
            "bible_references": json.loads(row["bible_references"]) if row["bible_references"] else None,
            "learnings": row["learnings"],
            "key_takeaways": row["key_takeaways"],
            "additional_thoughts": row["additional_thoughts"],
        }
        try:
            client.table("sermon_notes").insert(data).execute()
            print(f"  {row['title']}: OK")
        except Exception as e:
            print(f"  {row['title']}: FAILED - {e}")

    # 5. Prayer Categories + Entries
    old_categories = conn.execute("SELECT * FROM prayer_categories ORDER BY id").fetchall()
    print(f"\nPrayer categories: {len(old_categories)}")
    old_to_new_cat_id = {}

    for cat in old_categories:
        data = {
            "user_id": user_id,
            "name": cat["name"],
            "icon": cat["icon"],
            "color": cat["color"],
        }
        try:
            result = client.table("prayer_categories").upsert(
                data, on_conflict="user_id,name"
            ).execute()
            if result.data:
                old_to_new_cat_id[cat["id"]] = result.data[0]["id"]
            print(f"  {cat['name']}: OK (new_id={old_to_new_cat_id.get(cat['id'])})")
        except Exception as e:
            print(f"  {cat['name']}: FAILED - {e}")

    # Prayer Entries
    prayer_rows = conn.execute("SELECT * FROM prayer_entries ORDER BY id").fetchall()
    print(f"\nPrayer entries: {len(prayer_rows)}")
    for row in prayer_rows:
        new_cat_id = old_to_new_cat_id.get(row["category_id"])
        if not new_cat_id:
            print(f"  {row['title']}: SKIPPED (category not found)")
            continue
        data = {
            "user_id": user_id,
            "category_id": new_cat_id,
            "title": row["title"],
            "prayer_text": row["prayer_text"],
            "scriptures": json.loads(row["scriptures"]) if row["scriptures"] else None,
            "confessions": row["confessions"],
            "declarations": row["declarations"],
            "status": row["status"],
        }
        try:
            client.table("prayer_entries").insert(data).execute()
            print(f"  {row['title']}: OK")
        except Exception as e:
            print(f"  {row['title']}: FAILED - {e}")

    conn.close()
    print("\n=== MIGRATION COMPLETE ===")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python migrations/migrate_sqlite.py <user_email>")
        sys.exit(1)
    migrate(sys.argv[1])