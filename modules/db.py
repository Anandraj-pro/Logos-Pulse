"""
Database module for Logos Pulse — Supabase edition.
All functions use the authenticated user's session via RLS.
Function signatures are preserved from the SQLite version for page compatibility.
"""

import json
import streamlit as st
from typing import Optional
from modules.supabase_client import get_supabase_client, get_admin_client


def _uid() -> str:
    """Get the current authenticated user's ID."""
    return st.session_state.get("user_id", "")


def _client():
    """Get authenticated Supabase client with user's session.
    Handles token refresh if the access token has expired.
    """
    client = get_supabase_client()
    token = st.session_state.get("access_token")
    refresh = st.session_state.get("refresh_token")
    if token and refresh:
        try:
            client.auth.set_session(token, refresh)
        except Exception:
            # Token may have expired — try refreshing
            try:
                response = client.auth.refresh_session(refresh)
                if response and response.session:
                    st.session_state["access_token"] = response.session.access_token
                    st.session_state["refresh_token"] = response.session.refresh_token
                    client.auth.set_session(
                        response.session.access_token,
                        response.session.refresh_token,
                    )
                else:
                    # Refresh failed — user needs to re-login
                    st.session_state["authenticated"] = False
            except Exception:
                st.session_state["authenticated"] = False
    return client


def _safe_execute(operation, fallback=None):
    """Wrap a Supabase operation with error handling."""
    try:
        return operation()
    except Exception as e:
        error_msg = str(e)
        if "JWT" in error_msg or "token" in error_msg.lower() or "401" in error_msg:
            st.session_state["authenticated"] = False
            st.error("Your session has expired. Please log in again.")
            st.stop()
        elif "violates row-level security" in error_msg.lower():
            st.error("You don't have permission to perform this action.")
            return fallback
        else:
            st.error(f"Something went wrong. Please try again.")
            return fallback


def init_db():
    """No-op for Supabase — schema is managed via migrations."""
    pass


# --- Daily Entries ---

def upsert_daily_entry(entry_date: str, prayer_minutes: int, bible_book: str,
                       chapters_read: list[int], chapters_display: str,
                       sermon_title: str, sermon_speaker: str,
                       youtube_link: str) -> dict:
    user_id = _uid()
    client = _client()

    row_data = {
        "user_id": user_id,
        "date": entry_date,
        "prayer_minutes": prayer_minutes,
        "bible_book": bible_book,
        "chapters_read": chapters_read,
        "chapters_display": chapters_display,
        "sermon_title": sermon_title,
        "sermon_speaker": sermon_speaker,
        "youtube_link": youtube_link,
    }

    def _do():
        existing = client.table("daily_entries") \
            .select("id") \
            .eq("user_id", user_id) \
            .eq("date", entry_date) \
            .execute()

        if existing.data:
            result = client.table("daily_entries") \
                .update(row_data) \
                .eq("user_id", user_id) \
                .eq("date", entry_date) \
                .execute()
        else:
            result = client.table("daily_entries") \
                .insert(row_data) \
                .execute()
        return result.data[0] if result.data else row_data

    return _safe_execute(_do, fallback=row_data)


def get_entry_by_date(entry_date: str) -> Optional[dict]:
    client = _client()
    result = client.table("daily_entries") \
        .select("*") \
        .eq("user_id", _uid()) \
        .eq("date", entry_date) \
        .execute()
    return result.data[0] if result.data else None


def get_entries_in_range(start_date: str, end_date: str) -> list[dict]:
    client = _client()
    result = client.table("daily_entries") \
        .select("*") \
        .eq("user_id", _uid()) \
        .gte("date", start_date) \
        .lte("date", end_date) \
        .order("date", desc=True) \
        .execute()
    return result.data or []


def get_all_entry_dates() -> list[str]:
    client = _client()
    result = client.table("daily_entries") \
        .select("date") \
        .eq("user_id", _uid()) \
        .order("date") \
        .execute()
    return [r["date"] for r in (result.data or [])]


def mark_report_copied(entry_date: str):
    client = _client()
    client.table("daily_entries") \
        .update({"report_copied": True}) \
        .eq("user_id", _uid()) \
        .eq("date", entry_date) \
        .execute()


# --- Weekly Assignments ---

def create_assignment(book: str, start_chapter: int, end_chapter: int,
                      week_start: str, week_end: str,
                      daily_breakdown: dict) -> dict:
    user_id = _uid()
    client = _client()

    # Mark existing active assignments as completed
    client.table("weekly_assignments") \
        .update({"status": "COMPLETED"}) \
        .eq("user_id", user_id) \
        .eq("status", "ACTIVE") \
        .execute()

    result = client.table("weekly_assignments").insert({
        "user_id": user_id,
        "book": book,
        "start_chapter": start_chapter,
        "end_chapter": end_chapter,
        "total_chapters": end_chapter - start_chapter + 1,
        "week_start_date": week_start,
        "week_end_date": week_end,
        "daily_breakdown": daily_breakdown,
        "status": "ACTIVE",
    }).execute()

    return result.data[0] if result.data else {}


def get_active_assignment() -> Optional[dict]:
    client = _client()
    result = client.table("weekly_assignments") \
        .select("*") \
        .eq("user_id", _uid()) \
        .eq("status", "ACTIVE") \
        .order("id", desc=True) \
        .limit(1) \
        .execute()
    return result.data[0] if result.data else None


def get_assignment_history() -> list[dict]:
    client = _client()
    result = client.table("weekly_assignments") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("id", desc=True) \
        .execute()
    return result.data or []


# --- Settings ---

def get_setting(key: str) -> Optional[str]:
    client = _client()
    result = client.table("app_settings") \
        .select("value") \
        .eq("user_id", _uid()) \
        .eq("key", key) \
        .execute()
    return result.data[0]["value"] if result.data else None


def get_all_settings() -> dict:
    client = _client()
    uid = _uid()
    if not uid:
        return {}
    result = client.table("app_settings") \
        .select("key, value") \
        .eq("user_id", uid) \
        .execute()
    return {r["key"]: r["value"] for r in (result.data or [])}


def save_setting(key: str, value: str):
    user_id = _uid()
    client = _client()
    # Upsert
    existing = client.table("app_settings") \
        .select("id") \
        .eq("user_id", user_id) \
        .eq("key", key) \
        .execute()

    if existing.data:
        client.table("app_settings") \
            .update({"value": value}) \
            .eq("user_id", user_id) \
            .eq("key", key) \
            .execute()
    else:
        client.table("app_settings").insert({
            "user_id": user_id,
            "key": key,
            "value": value,
        }).execute()


def save_settings(settings: dict):
    for key, value in settings.items():
        save_setting(key, str(value))


# --- Sermon Notes ---

def create_sermon_note(title: str, speaker: str, sermon_date: str,
                       notes_text: str, bible_references: list,
                       learnings: str, key_takeaways: str,
                       additional_thoughts: str) -> dict:
    client = _client()
    result = client.table("sermon_notes").insert({
        "user_id": _uid(),
        "title": title,
        "speaker": speaker,
        "sermon_date": sermon_date,
        "notes_text": notes_text,
        "bible_references": bible_references,
        "learnings": learnings,
        "key_takeaways": key_takeaways,
        "additional_thoughts": additional_thoughts,
    }).execute()
    return result.data[0] if result.data else {}


def update_sermon_note(note_id: int, title: str, speaker: str, sermon_date: str,
                       notes_text: str, bible_references: list,
                       learnings: str, key_takeaways: str,
                       additional_thoughts: str) -> dict:
    client = _client()
    result = client.table("sermon_notes") \
        .update({
            "title": title,
            "speaker": speaker,
            "sermon_date": sermon_date,
            "notes_text": notes_text,
            "bible_references": bible_references,
            "learnings": learnings,
            "key_takeaways": key_takeaways,
            "additional_thoughts": additional_thoughts,
        }) \
        .eq("id", note_id) \
        .eq("user_id", _uid()) \
        .execute()
    return result.data[0] if result.data else {}


def get_sermon_note(note_id: int) -> Optional[dict]:
    client = _client()
    result = client.table("sermon_notes") \
        .select("*") \
        .eq("id", note_id) \
        .eq("user_id", _uid()) \
        .execute()
    return result.data[0] if result.data else None


def get_all_sermon_notes() -> list[dict]:
    client = _client()
    result = client.table("sermon_notes") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("sermon_date", desc=True) \
        .order("id", desc=True) \
        .execute()
    return result.data or []


def delete_sermon_note(note_id: int):
    client = _client()
    client.table("sermon_notes") \
        .delete() \
        .eq("id", note_id) \
        .eq("user_id", _uid()) \
        .execute()


# --- Prayer Categories ---

def get_prayer_categories() -> list[dict]:
    client = _client()
    result = client.table("prayer_categories") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("id") \
        .execute()
    return result.data or []


def create_prayer_category(name: str, icon: str = "", color: str = "#5B4FC4") -> dict:
    client = _client()
    result = client.table("prayer_categories").insert({
        "user_id": _uid(),
        "name": name,
        "icon": icon,
        "color": color,
    }).execute()
    return result.data[0] if result.data else {}


# --- Prayer Entries ---

def create_prayer_entry(category_id: int, title: str, prayer_text: str,
                        scriptures: list, confessions: str,
                        declarations: str) -> dict:
    client = _client()
    result = client.table("prayer_entries").insert({
        "user_id": _uid(),
        "category_id": category_id,
        "title": title,
        "prayer_text": prayer_text,
        "scriptures": scriptures,
        "confessions": confessions,
        "declarations": declarations,
        "status": "ongoing",
    }).execute()
    return result.data[0] if result.data else {}


def update_prayer_entry(entry_id: int, title: str, prayer_text: str,
                        scriptures: list, confessions: str,
                        declarations: str, status: str) -> dict:
    client = _client()
    result = client.table("prayer_entries") \
        .update({
            "title": title,
            "prayer_text": prayer_text,
            "scriptures": scriptures,
            "confessions": confessions,
            "declarations": declarations,
            "status": status,
        }) \
        .eq("id", entry_id) \
        .eq("user_id", _uid()) \
        .execute()
    return result.data[0] if result.data else {}


def get_prayers_by_category(category_id: int) -> list[dict]:
    client = _client()
    result = client.table("prayer_entries") \
        .select("*") \
        .eq("user_id", _uid()) \
        .eq("category_id", category_id) \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


def get_prayer_entry(entry_id: int) -> Optional[dict]:
    client = _client()
    result = client.table("prayer_entries") \
        .select("*") \
        .eq("id", entry_id) \
        .eq("user_id", _uid()) \
        .execute()
    return result.data[0] if result.data else None


def delete_prayer_entry(entry_id: int):
    client = _client()
    client.table("prayer_entries") \
        .delete() \
        .eq("id", entry_id) \
        .eq("user_id", _uid()) \
        .execute()


# --- Export/Import ---

def export_all_data() -> dict:
    client = _client()
    uid = _uid()

    entries = client.table("daily_entries").select("*").eq("user_id", uid).order("date").execute()
    assignments = client.table("weekly_assignments").select("*").eq("user_id", uid).order("id").execute()
    settings = client.table("app_settings").select("key, value").eq("user_id", uid).execute()
    sermons = client.table("sermon_notes").select("*").eq("user_id", uid).order("id").execute()
    categories = client.table("prayer_categories").select("*").eq("user_id", uid).order("id").execute()
    prayers = client.table("prayer_entries").select("*").eq("user_id", uid).order("id").execute()

    return {
        "daily_entries": entries.data or [],
        "weekly_assignments": assignments.data or [],
        "app_settings": {r["key"]: r["value"] for r in (settings.data or [])},
        "sermon_notes": sermons.data or [],
        "prayer_categories": categories.data or [],
        "prayer_entries": prayers.data or [],
    }


def import_all_data(data: dict):
    """Import data from a JSON backup. Merges with existing data."""
    client = _client()
    uid = _uid()

    if "daily_entries" in data:
        for entry in data["daily_entries"]:
            entry.pop("id", None)
            entry["user_id"] = uid
            # Convert SQLite boolean
            if "report_copied" in entry:
                entry["report_copied"] = bool(entry["report_copied"])
            # Convert chapters_read from string to list if needed
            if isinstance(entry.get("chapters_read"), str):
                entry["chapters_read"] = json.loads(entry["chapters_read"])
            try:
                client.table("daily_entries").upsert(
                    entry, on_conflict="user_id,date"
                ).execute()
            except Exception:
                pass

    if "app_settings" in data:
        for key, value in data["app_settings"].items():
            save_setting(key, value)