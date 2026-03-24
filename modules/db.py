import sqlite3
import json
import os
from contextlib import contextmanager
from typing import Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tracker.db")

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS daily_entries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT NOT NULL UNIQUE,
    prayer_minutes  INTEGER NOT NULL DEFAULT 60,
    bible_book      TEXT,
    chapters_read   TEXT,
    chapters_display TEXT,
    sermon_title    TEXT,
    sermon_speaker  TEXT,
    youtube_link    TEXT,
    report_copied   INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_daily_entries_date ON daily_entries(date);

CREATE TABLE IF NOT EXISTS weekly_assignments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    book            TEXT NOT NULL,
    start_chapter   INTEGER NOT NULL,
    end_chapter     INTEGER NOT NULL,
    total_chapters  INTEGER NOT NULL,
    week_start_date TEXT NOT NULL,
    week_end_date   TEXT NOT NULL,
    daily_breakdown TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_weekly_assignments_dates
    ON weekly_assignments(week_start_date, week_end_date);
CREATE INDEX IF NOT EXISTS idx_weekly_assignments_status
    ON weekly_assignments(status);

CREATE TABLE IF NOT EXISTS app_settings (
    key             TEXT PRIMARY KEY,
    value           TEXT NOT NULL
);

INSERT OR IGNORE INTO app_settings (key, value) VALUES ('greeting_name', 'Anna');
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('pastor_name', 'Ps. Deepak');
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('default_prayer_minutes', '60');
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('omit_empty_sermon', 'false');

-- Sermon Notes
CREATE TABLE IF NOT EXISTS sermon_notes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT NOT NULL,
    speaker             TEXT NOT NULL,
    sermon_date         TEXT NOT NULL,
    notes_text          TEXT,
    bible_references    TEXT,
    learnings           TEXT,
    key_takeaways       TEXT,
    additional_thoughts TEXT,
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_sermon_notes_date ON sermon_notes(sermon_date);

-- Prayer Journal Categories
CREATE TABLE IF NOT EXISTS prayer_categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    icon        TEXT DEFAULT '',
    color       TEXT DEFAULT '#7B68EE',
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO prayer_categories (name, icon, color) VALUES ('Personal', '\U0001f64f', '#7B68EE');
INSERT OR IGNORE INTO prayer_categories (name, icon, color) VALUES ('Finance & Breakthroughs', '\U0001f4b0', '#4CAF50');
INSERT OR IGNORE INTO prayer_categories (name, icon, color) VALUES ('Spouse', '\u2764\ufe0f', '#E91E63');
INSERT OR IGNORE INTO prayer_categories (name, icon, color) VALUES ('Job & Career', '\U0001f4bc', '#FF9800');

-- Prayer Entries
CREATE TABLE IF NOT EXISTS prayer_entries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id     INTEGER NOT NULL,
    title           TEXT NOT NULL,
    prayer_text     TEXT,
    scriptures      TEXT,
    confessions     TEXT,
    declarations    TEXT,
    status          TEXT NOT NULL DEFAULT 'ongoing',
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (category_id) REFERENCES prayer_categories(id)
);

CREATE INDEX IF NOT EXISTS idx_prayer_entries_category ON prayer_entries(category_id);
CREATE INDEX IF NOT EXISTS idx_prayer_entries_status ON prayer_entries(status);
"""


@contextmanager
def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL)


# --- Daily Entries ---

def upsert_daily_entry(entry_date: str, prayer_minutes: int, bible_book: str,
                       chapters_read: list[int], chapters_display: str,
                       sermon_title: str, sermon_speaker: str,
                       youtube_link: str) -> dict:
    now = datetime.now().isoformat()
    chapters_json = json.dumps(chapters_read)
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM daily_entries WHERE date = ?", (entry_date,)
        ).fetchone()
        if existing:
            conn.execute("""
                UPDATE daily_entries SET
                    prayer_minutes = ?, bible_book = ?, chapters_read = ?,
                    chapters_display = ?, sermon_title = ?, sermon_speaker = ?,
                    youtube_link = ?, updated_at = ?
                WHERE date = ?
            """, (prayer_minutes, bible_book, chapters_json, chapters_display,
                  sermon_title, sermon_speaker, youtube_link, now, entry_date))
        else:
            conn.execute("""
                INSERT INTO daily_entries
                    (date, prayer_minutes, bible_book, chapters_read, chapters_display,
                     sermon_title, sermon_speaker, youtube_link, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (entry_date, prayer_minutes, bible_book, chapters_json,
                  chapters_display, sermon_title, sermon_speaker, youtube_link, now, now))
        row = conn.execute(
            "SELECT * FROM daily_entries WHERE date = ?", (entry_date,)
        ).fetchone()
        return dict(row)


def get_entry_by_date(entry_date: str) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM daily_entries WHERE date = ?", (entry_date,)
        ).fetchone()
        return dict(row) if row else None


def get_entries_in_range(start_date: str, end_date: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM daily_entries WHERE date BETWEEN ? AND ? ORDER BY date DESC",
            (start_date, end_date)
        ).fetchall()
        return [dict(r) for r in rows]


def get_all_entry_dates() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT date FROM daily_entries ORDER BY date"
        ).fetchall()
        return [r["date"] for r in rows]


def mark_report_copied(entry_date: str):
    with get_connection() as conn:
        conn.execute(
            "UPDATE daily_entries SET report_copied = 1 WHERE date = ?", (entry_date,)
        )


# --- Weekly Assignments ---

def create_assignment(book: str, start_chapter: int, end_chapter: int,
                      week_start: str, week_end: str,
                      daily_breakdown: dict) -> dict:
    with get_connection() as conn:
        conn.execute(
            "UPDATE weekly_assignments SET status = 'COMPLETED' WHERE status = 'ACTIVE'"
        )
        conn.execute("""
            INSERT INTO weekly_assignments
                (book, start_chapter, end_chapter, total_chapters,
                 week_start_date, week_end_date, daily_breakdown, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'ACTIVE')
        """, (book, start_chapter, end_chapter,
              end_chapter - start_chapter + 1,
              week_start, week_end, json.dumps(daily_breakdown)))
        row = conn.execute(
            "SELECT * FROM weekly_assignments WHERE status = 'ACTIVE' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row)


def get_active_assignment() -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM weekly_assignments WHERE status = 'ACTIVE' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row) if row else None


def get_assignment_history() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM weekly_assignments ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


# --- Settings ---

def get_setting(key: str) -> Optional[str]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM app_settings WHERE key = ?", (key,)
        ).fetchone()
        return row["value"] if row else None


def get_all_settings() -> dict:
    with get_connection() as conn:
        rows = conn.execute("SELECT key, value FROM app_settings").fetchall()
        return {r["key"]: r["value"] for r in rows}


def save_setting(key: str, value: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)",
            (key, value)
        )


def save_settings(settings: dict):
    with get_connection() as conn:
        for key, value in settings.items():
            conn.execute(
                "INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)",
                (key, str(value))
            )


# --- Sermon Notes ---

def create_sermon_note(title: str, speaker: str, sermon_date: str,
                       notes_text: str, bible_references: list,
                       learnings: str, key_takeaways: str,
                       additional_thoughts: str) -> dict:
    now = datetime.now().isoformat()
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO sermon_notes
                (title, speaker, sermon_date, notes_text, bible_references,
                 learnings, key_takeaways, additional_thoughts, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, speaker, sermon_date, notes_text,
              json.dumps(bible_references), learnings, key_takeaways,
              additional_thoughts, now, now))
        row = conn.execute(
            "SELECT * FROM sermon_notes ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row)


def update_sermon_note(note_id: int, title: str, speaker: str, sermon_date: str,
                       notes_text: str, bible_references: list,
                       learnings: str, key_takeaways: str,
                       additional_thoughts: str) -> dict:
    now = datetime.now().isoformat()
    with get_connection() as conn:
        conn.execute("""
            UPDATE sermon_notes SET
                title = ?, speaker = ?, sermon_date = ?, notes_text = ?,
                bible_references = ?, learnings = ?, key_takeaways = ?,
                additional_thoughts = ?, updated_at = ?
            WHERE id = ?
        """, (title, speaker, sermon_date, notes_text,
              json.dumps(bible_references), learnings, key_takeaways,
              additional_thoughts, now, note_id))
        row = conn.execute(
            "SELECT * FROM sermon_notes WHERE id = ?", (note_id,)
        ).fetchone()
        return dict(row)


def get_sermon_note(note_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM sermon_notes WHERE id = ?", (note_id,)
        ).fetchone()
        return dict(row) if row else None


def get_all_sermon_notes() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM sermon_notes ORDER BY sermon_date DESC, id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def delete_sermon_note(note_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM sermon_notes WHERE id = ?", (note_id,))


# --- Prayer Categories ---

def get_prayer_categories() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM prayer_categories ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


def create_prayer_category(name: str, icon: str = "", color: str = "#7B68EE") -> dict:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO prayer_categories (name, icon, color) VALUES (?, ?, ?)",
            (name, icon, color)
        )
        row = conn.execute(
            "SELECT * FROM prayer_categories ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row)


# --- Prayer Entries ---

def create_prayer_entry(category_id: int, title: str, prayer_text: str,
                        scriptures: list, confessions: str,
                        declarations: str) -> dict:
    now = datetime.now().isoformat()
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO prayer_entries
                (category_id, title, prayer_text, scriptures,
                 confessions, declarations, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'ongoing', ?, ?)
        """, (category_id, title, prayer_text, json.dumps(scriptures),
              confessions, declarations, now, now))
        row = conn.execute(
            "SELECT * FROM prayer_entries ORDER BY id DESC LIMIT 1"
        ).fetchone()
        return dict(row)


def update_prayer_entry(entry_id: int, title: str, prayer_text: str,
                        scriptures: list, confessions: str,
                        declarations: str, status: str) -> dict:
    now = datetime.now().isoformat()
    with get_connection() as conn:
        conn.execute("""
            UPDATE prayer_entries SET
                title = ?, prayer_text = ?, scriptures = ?,
                confessions = ?, declarations = ?, status = ?, updated_at = ?
            WHERE id = ?
        """, (title, prayer_text, json.dumps(scriptures),
              confessions, declarations, status, now, entry_id))
        row = conn.execute(
            "SELECT * FROM prayer_entries WHERE id = ?", (entry_id,)
        ).fetchone()
        return dict(row)


def get_prayers_by_category(category_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM prayer_entries WHERE category_id = ? ORDER BY created_at DESC",
            (category_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_prayer_entry(entry_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM prayer_entries WHERE id = ?", (entry_id,)
        ).fetchone()
        return dict(row) if row else None


def delete_prayer_entry(entry_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM prayer_entries WHERE id = ?", (entry_id,))


# --- Export/Import ---

def export_all_data() -> dict:
    with get_connection() as conn:
        entries = conn.execute("SELECT * FROM daily_entries ORDER BY date").fetchall()
        assignments = conn.execute("SELECT * FROM weekly_assignments ORDER BY id").fetchall()
        settings = conn.execute("SELECT * FROM app_settings").fetchall()
        return {
            "daily_entries": [dict(r) for r in entries],
            "weekly_assignments": [dict(r) for r in assignments],
            "app_settings": {r["key"]: r["value"] for r in settings},
        }


def import_all_data(data: dict):
    with get_connection() as conn:
        if "daily_entries" in data:
            for entry in data["daily_entries"]:
                conn.execute("""
                    INSERT OR REPLACE INTO daily_entries
                        (date, prayer_minutes, bible_book, chapters_read, chapters_display,
                         sermon_title, sermon_speaker, youtube_link, report_copied,
                         created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (entry["date"], entry["prayer_minutes"], entry.get("bible_book"),
                      entry.get("chapters_read"), entry.get("chapters_display"),
                      entry.get("sermon_title"), entry.get("sermon_speaker"),
                      entry.get("youtube_link"), entry.get("report_copied", 0),
                      entry.get("created_at", ""), entry.get("updated_at", "")))
        if "app_settings" in data:
            for key, value in data["app_settings"].items():
                conn.execute(
                    "INSERT OR REPLACE INTO app_settings (key, value) VALUES (?, ?)",
                    (key, value)
                )
