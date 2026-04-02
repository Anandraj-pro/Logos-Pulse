# Architecture Document
# Spiritual Growth Daily Tracker

**Document Version:** 1.0
**Date:** 2026-03-23
**Author:** BMAD Architect
**Status:** Implementation-Ready
**Based on:** PRD v1.0

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Database Schema](#4-database-schema)
5. [Page Architecture](#5-page-architecture)
6. [Component Design](#6-component-design)
7. [Data Flow](#7-data-flow)
8. [Copy-to-Clipboard Implementation](#8-copy-to-clipboard-implementation)
9. [Chapter Splitting Algorithm](#9-chapter-splitting-algorithm)
10. [Bible Reference Data](#10-bible-reference-data)
11. [Streamlit Configuration](#11-streamlit-configuration)
12. [Deployment](#12-deployment)
13. [Error Handling Strategy](#13-error-handling-strategy)
14. [Performance Considerations](#14-performance-considerations)

---

## 1. System Overview

### High-Level Architecture

```
+-------------------------------------------------------+
|              Streamlit Community Cloud                  |
|                                                        |
|  +--------------------------------------------------+  |
|  |            Streamlit Application (Python)         |  |
|  |                                                   |  |
|  |  +-------------+  +------------+  +------------+  |  |
|  |  |   Pages/    |  | Components |  |  Modules   |  |  |
|  |  |             |  |            |  |            |  |  |
|  |  | Dashboard   |  | Forms      |  | db.py      |  |  |
|  |  | Daily_Entry |  | Calendar   |  | models.py  |  |  |
|  |  | Journal     |  | Charts     |  | utils.py   |  |  |
|  |  | Assignment  |  | Clipboard  |  | bible.py   |  |  |
|  |  | Stats       |  | Message    |  | message.py |  |  |
|  |  | Settings    |  | Preview    |  |            |  |  |
|  |  +------+------+  +-----+------+  +-----+------+  |  |
|  |         |                |               |         |  |
|  |         +--------+-------+-------+-------+         |  |
|  |                  |                                  |  |
|  |           +------v------+                           |  |
|  |           |   SQLite    |                           |  |
|  |           |  Database   |                           |  |
|  |           | (tracker.db)|                           |  |
|  |           +-------------+                           |  |
|  +--------------------------------------------------+  |
+-------------------------------------------------------+
         |                              |
         v                              v
  +-------------+              +-----------------+
  | User Browser|              | Clipboard API   |
  | (Mobile/    |              | (JS injection   |
  |  Desktop)   |              |  for WhatsApp   |
  +-------------+              |  message copy)  |
                               +-----------------+
```

### Architecture Principles

1. **Server-side rendering** -- Streamlit handles all UI rendering; the browser is a thin client.
2. **Single-file database** -- SQLite file (`tracker.db`) lives alongside the app on the server.
3. **No authentication for MVP** -- Single user; the unlisted Streamlit Cloud URL provides access control.
4. **Stateless page renders** -- Each Streamlit rerun reads from the database; `st.session_state` is used only for transient form state within a single session.
5. **Modular code** -- Business logic in Python modules; pages are thin wrappers calling modules.

---

## 2. Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Framework | Streamlit | >=1.32.0 | Application framework, UI rendering |
| Language | Python | 3.10+ | Application language |
| Database | SQLite3 | Built-in | Persistent data storage |
| Charts | Plotly | >=5.18.0 | Heatmaps, progress charts |
| Date Handling | Python datetime, calendar | Built-in | Date formatting, ordinals, calendar views |
| Clipboard | st.components.v1.html | Built-in | JavaScript injection for clipboard copy |
| Hosting | Streamlit Community Cloud | N/A | Free hosting, auto-deploy from GitHub |

### Dependencies (requirements.txt)

```
streamlit>=1.32.0
plotly>=5.18.0
```

No other external dependencies required. SQLite3, datetime, calendar, json, and dataclasses are all part of the Python standard library.

---

## 3. Project Structure

```
spiritual-growth-tracker/
|
+-- .streamlit/
|   +-- config.toml              # Streamlit theme and server config
|
+-- app.py                        # Main entry point (home/dashboard)
|
+-- pages/
|   +-- 1_Daily_Entry.py          # Daily entry form + report generation
|   +-- 2_Prayer_Journal.py       # Calendar view + list view of entries
|   +-- 3_Weekly_Assignment.py    # Weekly assignment setup + progress
|   +-- 4_Streaks_and_Stats.py    # Streak tracking + monthly heatmap
|   +-- 5_Settings.py             # App configuration
|
+-- modules/
|   +-- __init__.py
|   +-- db.py                     # Database connection, schema init, CRUD
|   +-- models.py                 # Dataclass definitions
|   +-- utils.py                  # Date helpers, duration formatting
|   +-- message.py                # WhatsApp message formatting
|   +-- bible_data.py             # Bible books with chapter counts
|   +-- chapter_splitter.py       # Weekly-to-daily chapter distribution
|   +-- clipboard.py              # JS clipboard component
|
+-- data/
|   +-- tracker.db                # SQLite database (auto-created)
|
+-- requirements.txt              # Python dependencies
+-- .gitignore                    # Exclude tracker.db, __pycache__, etc.
```

### File Naming Convention

Streamlit multi-page apps use the `pages/` directory. Files are prefixed with numbers (`1_`, `2_`, etc.) to control sidebar ordering. The prefix number and underscores are stripped from the display name in the sidebar.

---

## 4. Database Schema

### 4.1 Full DDL

```sql
-- ============================================================
-- Database: tracker.db
-- Engine: SQLite 3
-- ============================================================

-- Daily spiritual activity entries
CREATE TABLE IF NOT EXISTS daily_entries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    date            TEXT NOT NULL UNIQUE,          -- ISO format: YYYY-MM-DD
    prayer_minutes  INTEGER NOT NULL DEFAULT 60,   -- Duration in minutes
    bible_book      TEXT,                           -- e.g., "Luke"
    chapters_read   TEXT,                           -- JSON array: [1,2,3,4]
    chapters_display TEXT,                          -- Human-readable: "Luke 1-4"
    sermon_title    TEXT,                           -- Nullable
    sermon_speaker  TEXT,                           -- Nullable
    youtube_link    TEXT,                           -- Nullable
    report_copied   INTEGER NOT NULL DEFAULT 0,    -- Boolean: 0=false, 1=true
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index for fast date lookups (calendar view, streak calc)
CREATE INDEX IF NOT EXISTS idx_daily_entries_date ON daily_entries(date);

-- Weekly Bible reading assignments
CREATE TABLE IF NOT EXISTS weekly_assignments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    book            TEXT NOT NULL,                  -- e.g., "Luke"
    start_chapter   INTEGER NOT NULL,              -- e.g., 1
    end_chapter     INTEGER NOT NULL,              -- e.g., 24
    total_chapters  INTEGER NOT NULL,              -- Derived: end - start + 1
    week_start_date TEXT NOT NULL,                 -- ISO: YYYY-MM-DD (Monday)
    week_end_date   TEXT NOT NULL,                 -- ISO: YYYY-MM-DD (Saturday)
    daily_breakdown TEXT NOT NULL,                 -- JSON: {"monday":[1,2,3,4], ...}
    status          TEXT NOT NULL DEFAULT 'ACTIVE', -- ACTIVE | COMPLETED | PARTIAL
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index for finding the active assignment
CREATE INDEX IF NOT EXISTS idx_weekly_assignments_dates
    ON weekly_assignments(week_start_date, week_end_date);
CREATE INDEX IF NOT EXISTS idx_weekly_assignments_status
    ON weekly_assignments(status);

-- App-wide key-value settings
CREATE TABLE IF NOT EXISTS app_settings (
    key             TEXT PRIMARY KEY,
    value           TEXT NOT NULL
);

-- Seed default settings on first run
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('greeting_name', 'Anna');
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('pastor_name', 'Ps. Deepak');
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('default_prayer_minutes', '60');
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('omit_empty_sermon', 'false');
INSERT OR IGNORE INTO app_settings (key, value) VALUES ('reminder_time', '07:00');
```

### 4.2 Table Details

#### `daily_entries`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Unique row ID |
| date | TEXT | NOT NULL, UNIQUE | Entry date in YYYY-MM-DD format |
| prayer_minutes | INTEGER | NOT NULL, DEFAULT 60 | Prayer duration in minutes |
| bible_book | TEXT | Nullable | Bible book name |
| chapters_read | TEXT | Nullable | JSON array of chapter numbers, e.g., `[1,2,3,4]` |
| chapters_display | TEXT | Nullable | Human-readable string, e.g., `"Luke 1-4"` |
| sermon_title | TEXT | Nullable | Sermon title (optional) |
| sermon_speaker | TEXT | Nullable | Speaker name (optional) |
| youtube_link | TEXT | Nullable | YouTube URL (optional) |
| report_copied | INTEGER | NOT NULL, DEFAULT 0 | Whether message was copied (0/1) |
| created_at | TEXT | NOT NULL | ISO datetime of creation |
| updated_at | TEXT | NOT NULL | ISO datetime of last update |

#### `weekly_assignments`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Unique row ID |
| book | TEXT | NOT NULL | Bible book name |
| start_chapter | INTEGER | NOT NULL | First chapter in range |
| end_chapter | INTEGER | NOT NULL | Last chapter in range |
| total_chapters | INTEGER | NOT NULL | Total chapters (end - start + 1) |
| week_start_date | TEXT | NOT NULL | Monday of the week (YYYY-MM-DD) |
| week_end_date | TEXT | NOT NULL | Saturday of the week (YYYY-MM-DD) |
| daily_breakdown | TEXT | NOT NULL | JSON object mapping day names to chapter arrays |
| status | TEXT | NOT NULL, DEFAULT 'ACTIVE' | ACTIVE, COMPLETED, or PARTIAL |
| created_at | TEXT | NOT NULL | ISO datetime of creation |

**`daily_breakdown` JSON format:**
```json
{
    "monday":    [1, 2, 3, 4],
    "tuesday":   [5, 6, 7, 8],
    "wednesday": [9, 10, 11, 12],
    "thursday":  [13, 14, 15, 16],
    "friday":    [17, 18, 19, 20],
    "saturday":  [21, 22, 23, 24]
}
```

#### `app_settings`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| key | TEXT | PK | Setting identifier |
| value | TEXT | NOT NULL | Setting value (stored as string, cast as needed) |

**Default settings:**

| Key | Default Value | Description |
|-----|---------------|-------------|
| `greeting_name` | `"Anna"` | Name in WhatsApp greeting |
| `pastor_name` | `"Ps. Deepak"` | Pastor's name |
| `default_prayer_minutes` | `"60"` | Default prayer duration |
| `omit_empty_sermon` | `"false"` | If `"true"`, omit sermon line when empty; if `"false"`, show "None" |
| `reminder_time` | `"07:00"` | Reminder time (informational only in MVP -- no push notifications in Streamlit) |

---

## 5. Page Architecture

### 5.1 Navigation Structure

Streamlit multi-page apps automatically create sidebar navigation from the `pages/` directory. The main `app.py` serves as the home/dashboard page.

```
Sidebar Navigation:
  [Dashboard]            <-- app.py
  [Daily Entry]          <-- pages/1_Daily_Entry.py
  [Prayer Journal]       <-- pages/2_Prayer_Journal.py
  [Weekly Assignment]    <-- pages/3_Weekly_Assignment.py
  [Streaks and Stats]    <-- pages/4_Streaks_and_Stats.py
  [Settings]             <-- pages/5_Settings.py
```

### 5.2 Page Specifications

#### Page: Dashboard (`app.py`)

**Purpose:** Home screen with quick status overview and call-to-action.

**Data needed:**
- Today's entry (or lack thereof) from `daily_entries`
- Current streak (calculated from `daily_entries`)
- Active weekly assignment from `weekly_assignments`
- Weekly completion count

**Layout:**
```
st.title("Spiritual Growth Daily Tracker")
st.subheader("Good Morning, {user_name}")

col1, col2, col3 = st.columns(3)
  col1: st.metric("Current Streak", "{n} days")
  col2: st.metric("Longest Streak", "{n} days")
  col3: st.metric("This Week", "{n}/6 days")

if not today_entry:
    st.button("Log Today's Entry") --> navigate to Daily Entry
else:
    st.success("Today's entry is complete!")
    if not today_entry.report_copied:
        st.warning("Report not yet copied to clipboard")

# Weekly reading progress bar
st.subheader("Weekly Bible Reading")
st.progress(chapters_read / total_chapters)
st.caption("{chapters_read}/{total_chapters} chapters of {book}")
```

**Session state used:** None persistent. Reads from DB on every render.

---

#### Page: Daily Entry (`pages/1_Daily_Entry.py`)

**Purpose:** Single form for logging all daily spiritual activities. After save, shows message preview and copy button.

**Data needed:**
- Active weekly assignment (for suggested chapters)
- Existing entry for selected date (for edit mode)
- App settings (greeting name, sermon display preference)

**Layout and Flow:**

```
# Step 1: Date selection
entry_date = st.date_input("Date", value=today, max_value=today)

# Step 2: Check if entry exists for this date
existing = db.get_entry_by_date(entry_date)

# Step 3: Form
with st.form("daily_entry_form"):

    st.subheader("Prayer")
    prayer_minutes = st.select_slider(
        "Duration",
        options=[15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180],
        value=existing.prayer_minutes if existing else default_prayer
    )

    st.subheader("Bible Reading")
    # Show suggested chapters from weekly assignment
    suggested = chapter_splitter.get_today_suggestion(entry_date)
    if suggested:
        st.info(f"Today's goal: {suggested['book']} {suggested['range']}")

    bible_book = st.selectbox("Book", options=bible_data.get_book_names(),
                              index=suggested_book_index)
    chapters = st.multiselect("Chapters read",
                              options=range(1, max_chapters+1),
                              default=suggested_chapters)

    st.subheader("Listening to the Word (optional)")
    sermon_title = st.text_input("Sermon Title", value=existing.sermon_title or "")
    sermon_speaker = st.text_input("Speaker", value=existing.sermon_speaker or "")
    youtube_link = st.text_input("YouTube Link", value=existing.youtube_link or "")

    submitted = st.form_submit_button("Save & Generate Report")

# Step 4: On submit
if submitted:
    # Validate
    if prayer_minutes <= 0:
        st.error("Prayer duration must be greater than 0")
    elif not chapters:
        st.error("Please select at least one chapter")
    else:
        # Save to DB (insert or update)
        entry = db.upsert_daily_entry(...)

        # Generate message
        message = message.format_whatsapp_message(entry, settings)

        # Show preview
        st.subheader("Report Preview")
        st.code(message, language=None)

        # Copy button
        clipboard.copy_button(message)
```

**Validation rules:**
- `prayer_minutes` must be > 0
- At least one chapter must be selected in Bible Reading
- YouTube link, if provided, must match YouTube URL patterns
- Sermon title and speaker are required if YouTube link is provided

---

#### Page: Prayer Journal (`pages/2_Prayer_Journal.py`)

**Purpose:** Browse historical entries via calendar and list views.

**Data needed:**
- All entries (dates for calendar highlighting)
- Filtered entries for list view

**Layout:**

```
view_mode = st.radio("View", ["Calendar", "List"], horizontal=True)

if view_mode == "Calendar":
    # Month navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    col1: st.button("<<")    # Previous month
    col2: st.subheader(f"{month_name} {year}")
    col3: st.button(">>")    # Next month

    # Render calendar grid using st.columns(7)
    # Highlight dates that have entries
    # On date click (using st.button for each date), show entry detail

elif view_mode == "List":
    # Search/filter controls
    search = st.text_input("Search")
    date_range = st.date_input("Date range", value=(start, end))

    # Display entries as expandable cards
    entries = db.get_entries_filtered(search, date_range)
    for entry in entries:
        with st.expander(f"{entry.date} - Prayer: {duration}, {entry.chapters_display}"):
            # Full entry detail
```

---

#### Page: Weekly Assignment (`pages/3_Weekly_Assignment.py`)

**Purpose:** Create new assignments and track progress.

**Layout:**

```
tab1, tab2 = st.tabs(["Current Assignment", "New Assignment"])

with tab1:  # Current Assignment
    assignment = db.get_active_assignment()
    if assignment:
        st.subheader(f"{assignment.book} {assignment.start_chapter}-{assignment.end_chapter}")
        st.progress(completed / total)

        # Show daily breakdown with completion status
        for day, chapters in breakdown.items():
            col1, col2 = st.columns([3, 1])
            col1: st.write(f"{day.title()}: Ch {chapters[0]}-{chapters[-1]}")
            col2: st.write("Done" or "Pending")
    else:
        st.info("No active assignment. Create one in the 'New Assignment' tab.")

with tab2:  # New Assignment
    with st.form("new_assignment"):
        book = st.selectbox("Bible Book", bible_data.get_book_names())
        max_ch = bible_data.get_chapter_count(book)
        start_ch = st.number_input("From Chapter", min_value=1, max_value=max_ch, value=1)
        end_ch = st.number_input("To Chapter", min_value=start_ch, max_value=max_ch, value=max_ch)
        week_start = st.date_input("Week starting (Monday)", value=next_monday())

        if st.form_submit_button("Generate Breakdown"):
            breakdown = chapter_splitter.split_chapters(start_ch, end_ch, 6)
            # Store in session_state for preview

    # Show breakdown preview (outside form, from session_state)
    if "preview_breakdown" in st.session_state:
        st.subheader("Daily Breakdown Preview")
        # Render editable breakdown
        st.button("Confirm Assignment") --> save to DB
```

---

#### Page: Streaks and Stats (`pages/4_Streaks_and_Stats.py`)

**Purpose:** Motivational statistics and visual progress.

**Data needed:**
- All entry dates for streak calculation
- Monthly entry data for heatmap

**Layout:**

```
# Streak metrics
col1, col2 = st.columns(2)
col1: st.metric("Current Streak", f"{current_streak} days")
col2: st.metric("Longest Streak", f"{longest_streak} days")

# Milestone celebration
if current_streak in [7, 30, 50, 100, 365]:
    st.balloons()
    st.success(f"Congratulations! {current_streak}-day streak!")

# Monthly heatmap (Plotly)
st.subheader("Monthly Activity")
fig = create_heatmap(year, month, entry_dates)
st.plotly_chart(fig, use_container_width=True)

# Monthly summary stats
st.subheader("This Month")
col1, col2, col3 = st.columns(3)
col1: st.metric("Days Logged", f"{days_logged}/{days_in_month}")
col2: st.metric("Total Prayer", f"{total_hours} hrs")
col3: st.metric("Bible Chapters", f"{total_chapters}")
```

---

#### Page: Settings (`pages/5_Settings.py`)

**Purpose:** Configure app behavior.

**Layout:**

```
st.title("Settings")

with st.form("settings_form"):
    greeting_name = st.text_input("Greeting Name", value=current_greeting)
    pastor_name = st.text_input("Pastor's Name", value=current_pastor)
    default_prayer = st.select_slider("Default Prayer Duration (minutes)",
                                       options=[15,30,45,60,75,90,105,120],
                                       value=current_default)
    omit_sermon = st.checkbox("Omit 'Listening to the Word' when empty",
                              value=current_omit)

    if st.form_submit_button("Save Settings"):
        db.save_settings(...)
        st.success("Settings saved!")

st.divider()
st.subheader("Data Management")
col1, col2 = st.columns(2)
col1: st.download_button("Export Data (JSON)", data=export_json(), file_name="backup.json")
col2: uploaded = st.file_uploader("Import Data (JSON)")
```

---

## 6. Component Design

### 6.1 `modules/db.py` -- Database Layer

```python
"""
Database connection management and CRUD operations.
All database access goes through this module.
"""
import sqlite3
import json
import os
from contextlib import contextmanager
from typing import Optional
from datetime import date, datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tracker.db")

@contextmanager
def get_connection():
    """Context manager for database connections."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Create tables and seed defaults. Safe to call on every app start."""
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL)  # Full DDL from Section 4

# --- Daily Entries ---

def upsert_daily_entry(entry_date: str, prayer_minutes: int, bible_book: str,
                        chapters_read: list[int], chapters_display: str,
                        sermon_title: str, sermon_speaker: str,
                        youtube_link: str) -> dict:
    """Insert or update a daily entry. Returns the saved entry."""

def get_entry_by_date(entry_date: str) -> Optional[dict]:
    """Fetch a single entry by date string (YYYY-MM-DD)."""

def get_entries_in_range(start_date: str, end_date: str) -> list[dict]:
    """Fetch all entries between two dates, inclusive."""

def get_all_entry_dates() -> list[str]:
    """Return list of all dates that have entries. Used for streaks and calendar."""

def mark_report_copied(entry_date: str):
    """Set report_copied=1 for the given date."""

# --- Weekly Assignments ---

def create_assignment(book: str, start_chapter: int, end_chapter: int,
                      week_start: str, week_end: str,
                      daily_breakdown: dict) -> dict:
    """Create a new weekly assignment. Deactivates any prior active assignment."""

def get_active_assignment() -> Optional[dict]:
    """Get the currently active weekly assignment."""

def get_assignment_history() -> list[dict]:
    """Get all past assignments, newest first."""

def update_assignment_status(assignment_id: int, status: str):
    """Update status to COMPLETED or PARTIAL."""

# --- Settings ---

def get_setting(key: str) -> Optional[str]:
    """Get a single setting value by key."""

def get_all_settings() -> dict:
    """Get all settings as a dict."""

def save_setting(key: str, value: str):
    """Insert or update a setting."""

def save_settings(settings: dict):
    """Bulk save multiple settings."""

# --- Export/Import ---

def export_all_data() -> dict:
    """Export all tables as a JSON-serializable dict."""

def import_all_data(data: dict):
    """Import data from a backup dict. Replaces existing data."""
```

### 6.2 `modules/models.py` -- Data Classes

```python
"""
Data classes for type safety and IDE support.
These are not ORM models -- they are simple containers.
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import date

@dataclass
class DailyEntry:
    id: Optional[int] = None
    date: str = ""                          # YYYY-MM-DD
    prayer_minutes: int = 60
    bible_book: Optional[str] = None
    chapters_read: list[int] = field(default_factory=list)
    chapters_display: Optional[str] = None
    sermon_title: Optional[str] = None
    sermon_speaker: Optional[str] = None
    youtube_link: Optional[str] = None
    report_copied: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "DailyEntry":
        """Create from a sqlite3.Row dict."""
        import json
        return cls(
            id=row["id"],
            date=row["date"],
            prayer_minutes=row["prayer_minutes"],
            bible_book=row["bible_book"],
            chapters_read=json.loads(row["chapters_read"]) if row["chapters_read"] else [],
            chapters_display=row["chapters_display"],
            sermon_title=row["sermon_title"],
            sermon_speaker=row["sermon_speaker"],
            youtube_link=row["youtube_link"],
            report_copied=bool(row["report_copied"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

@dataclass
class WeeklyAssignment:
    id: Optional[int] = None
    book: str = ""
    start_chapter: int = 1
    end_chapter: int = 1
    total_chapters: int = 0
    week_start_date: str = ""               # YYYY-MM-DD
    week_end_date: str = ""                 # YYYY-MM-DD
    daily_breakdown: dict = field(default_factory=dict)
    status: str = "ACTIVE"
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row: dict) -> "WeeklyAssignment":
        import json
        return cls(
            id=row["id"],
            book=row["book"],
            start_chapter=row["start_chapter"],
            end_chapter=row["end_chapter"],
            total_chapters=row["total_chapters"],
            week_start_date=row["week_start_date"],
            week_end_date=row["week_end_date"],
            daily_breakdown=json.loads(row["daily_breakdown"]),
            status=row["status"],
            created_at=row["created_at"],
        )

@dataclass
class AppSettings:
    greeting_name: str = "Anna"
    pastor_name: str = "Ps. Deepak"
    default_prayer_minutes: int = 60
    omit_empty_sermon: bool = False
    reminder_time: str = "07:00"
```

### 6.3 `modules/utils.py` -- Utility Functions

```python
"""
Date formatting, duration formatting, and general helpers.
"""
from datetime import date, datetime, timedelta
import calendar
import re

# --- Date Helpers ---

def format_ordinal_date(d: date) -> str:
    """Format date as '23rd March' with ordinal suffix."""
    day = d.day
    suffix = _ordinal_suffix(day)
    month_name = d.strftime("%B")
    return f"{day}{suffix} {month_name}"

def _ordinal_suffix(day: int) -> str:
    """Return ordinal suffix for a day number."""
    if 11 <= day <= 13:
        return "th"
    last_digit = day % 10
    if last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    return "th"

def get_next_monday(from_date: date = None) -> date:
    """Return the next Monday from the given date (or today)."""
    d = from_date or date.today()
    days_ahead = 0 - d.weekday()  # Monday = 0
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)

def get_day_of_week(d: date) -> str:
    """Return lowercase day name: 'monday', 'tuesday', etc."""
    return d.strftime("%A").lower()

def get_week_dates(monday: date) -> list[date]:
    """Return Mon-Sat dates for a week starting on the given Monday."""
    return [monday + timedelta(days=i) for i in range(6)]

# --- Duration Formatting ---

def format_prayer_duration(minutes: int) -> str:
    """
    Format minutes into human-readable duration.
    60 -> "1 Hour"
    90 -> "1 Hour 30 Minutes"
    120 -> "2 Hours"
    45 -> "45 Minutes"
    """
    if minutes <= 0:
        return "0 Minutes"
    hours = minutes // 60
    remaining_minutes = minutes % 60

    parts = []
    if hours == 1:
        parts.append("1 Hour")
    elif hours > 1:
        parts.append(f"{hours} Hours")
    if remaining_minutes > 0:
        parts.append(f"{remaining_minutes} Minutes")

    return " ".join(parts)

# --- Chapter Display ---

def format_chapters_display(book: str, chapters: list[int]) -> str:
    """
    Format chapters into display string.
    ("Luke", [1,2,3,4]) -> "Luke 1-4"
    ("Luke", [5]) -> "Luke 5"
    ("Luke", [1,3,5]) -> "Luke 1, 3, 5"
    """
    if not chapters:
        return ""
    if not book:
        return ""

    chapters_sorted = sorted(chapters)

    # Check if chapters are consecutive
    if _is_consecutive(chapters_sorted):
        if len(chapters_sorted) == 1:
            return f"{book} {chapters_sorted[0]}"
        return f"{book} {chapters_sorted[0]}-{chapters_sorted[-1]}"
    else:
        chapter_str = ", ".join(str(c) for c in chapters_sorted)
        return f"{book} {chapter_str}"

def _is_consecutive(nums: list[int]) -> bool:
    """Check if a sorted list of integers is consecutive."""
    if len(nums) <= 1:
        return True
    return nums[-1] - nums[0] == len(nums) - 1

# --- YouTube Validation ---

def is_valid_youtube_url(url: str) -> bool:
    """Validate that a string looks like a YouTube URL."""
    if not url:
        return True  # Empty is valid (field is optional)
    patterns = [
        r'https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'https?://youtu\.be/[\w-]+',
        r'https?://(www\.)?youtube\.com/shorts/[\w-]+',
    ]
    return any(re.match(p, url) for p in patterns)

# --- Streak Calculation ---

def calculate_streaks(entry_dates: list[str]) -> tuple[int, int]:
    """
    Calculate current streak and longest streak from a sorted list of date strings.
    Returns (current_streak, longest_streak).
    """
    if not entry_dates:
        return 0, 0

    dates = sorted(set(date.fromisoformat(d) for d in entry_dates), reverse=True)
    today = date.today()

    # Current streak: count backwards from today (or yesterday)
    current_streak = 0
    check_date = today
    if dates and dates[0] < today:
        check_date = today - timedelta(days=1)

    for d in dates:
        if d == check_date:
            current_streak += 1
            check_date -= timedelta(days=1)
        elif d < check_date:
            break

    # Longest streak: scan all dates
    dates_asc = sorted(dates)
    longest_streak = 1
    current_run = 1
    for i in range(1, len(dates_asc)):
        if (dates_asc[i] - dates_asc[i-1]).days == 1:
            current_run += 1
            longest_streak = max(longest_streak, current_run)
        else:
            current_run = 1

    return current_streak, longest_streak
```

### 6.4 `modules/message.py` -- WhatsApp Message Formatter

```python
"""
WhatsApp message generation from daily entry data.
"""
from datetime import date
from modules.utils import format_ordinal_date, format_prayer_duration

def format_whatsapp_message(
    entry_date: date,
    prayer_minutes: int,
    chapters_display: str,
    sermon_title: str | None,
    sermon_speaker: str | None,
    youtube_link: str | None,
    greeting_name: str,
    omit_empty_sermon: bool,
) -> str:
    """
    Generate the formatted WhatsApp report message.

    Output format:
        Good Morning {greeting_name},
        Praise the Lord!

        Date: {ordinal_date}
        Prayer: {duration}
        Bible Reading: {chapters}
        Listening to the Word: {sermon} - {speaker}
        {youtube_link}
    """
    date_str = format_ordinal_date(entry_date)
    duration_str = format_prayer_duration(prayer_minutes)

    lines = [
        f"Good Morning {greeting_name},",
        "Praise the Lord!",
        "",
        f"Date: {date_str}",
        f"Prayer: {duration_str}",
        f"Bible Reading: {chapters_display}",
    ]

    # Sermon line
    has_sermon = sermon_title and sermon_title.strip()
    if has_sermon:
        speaker_part = f" - {sermon_speaker}" if sermon_speaker else ""
        lines.append(f"Listening to the Word: {sermon_title}{speaker_part}")
        if youtube_link and youtube_link.strip():
            lines.append(youtube_link.strip())
    elif not omit_empty_sermon:
        lines.append("Listening to the Word: None")
    # If omit_empty_sermon is True and no sermon, we skip the line entirely

    return "\n".join(lines)
```

### 6.5 `modules/bible_data.py` -- Bible Reference Data

```python
"""
Complete Bible reference data: all 66 books with chapter counts.
"""

BIBLE_BOOKS = [
    # Old Testament (39 books)
    {"name": "Genesis",        "chapters": 50, "testament": "Old",  "order": 1},
    {"name": "Exodus",         "chapters": 40, "testament": "Old",  "order": 2},
    {"name": "Leviticus",      "chapters": 27, "testament": "Old",  "order": 3},
    {"name": "Numbers",        "chapters": 36, "testament": "Old",  "order": 4},
    {"name": "Deuteronomy",    "chapters": 34, "testament": "Old",  "order": 5},
    {"name": "Joshua",         "chapters": 24, "testament": "Old",  "order": 6},
    {"name": "Judges",         "chapters": 21, "testament": "Old",  "order": 7},
    {"name": "Ruth",           "chapters": 4,  "testament": "Old",  "order": 8},
    {"name": "1 Samuel",       "chapters": 31, "testament": "Old",  "order": 9},
    {"name": "2 Samuel",       "chapters": 24, "testament": "Old",  "order": 10},
    {"name": "1 Kings",        "chapters": 22, "testament": "Old",  "order": 11},
    {"name": "2 Kings",        "chapters": 25, "testament": "Old",  "order": 12},
    {"name": "1 Chronicles",   "chapters": 29, "testament": "Old",  "order": 13},
    {"name": "2 Chronicles",   "chapters": 36, "testament": "Old",  "order": 14},
    {"name": "Ezra",           "chapters": 10, "testament": "Old",  "order": 15},
    {"name": "Nehemiah",       "chapters": 13, "testament": "Old",  "order": 16},
    {"name": "Esther",         "chapters": 10, "testament": "Old",  "order": 17},
    {"name": "Job",            "chapters": 42, "testament": "Old",  "order": 18},
    {"name": "Psalms",         "chapters": 150,"testament": "Old",  "order": 19},
    {"name": "Proverbs",       "chapters": 31, "testament": "Old",  "order": 20},
    {"name": "Ecclesiastes",   "chapters": 12, "testament": "Old",  "order": 21},
    {"name": "Song of Solomon","chapters": 8,  "testament": "Old",  "order": 22},
    {"name": "Isaiah",         "chapters": 66, "testament": "Old",  "order": 23},
    {"name": "Jeremiah",       "chapters": 52, "testament": "Old",  "order": 24},
    {"name": "Lamentations",   "chapters": 5,  "testament": "Old",  "order": 25},
    {"name": "Ezekiel",        "chapters": 48, "testament": "Old",  "order": 26},
    {"name": "Daniel",         "chapters": 12, "testament": "Old",  "order": 27},
    {"name": "Hosea",          "chapters": 14, "testament": "Old",  "order": 28},
    {"name": "Joel",           "chapters": 3,  "testament": "Old",  "order": 29},
    {"name": "Amos",           "chapters": 9,  "testament": "Old",  "order": 30},
    {"name": "Obadiah",        "chapters": 1,  "testament": "Old",  "order": 31},
    {"name": "Jonah",          "chapters": 4,  "testament": "Old",  "order": 32},
    {"name": "Micah",          "chapters": 7,  "testament": "Old",  "order": 33},
    {"name": "Nahum",          "chapters": 3,  "testament": "Old",  "order": 34},
    {"name": "Habakkuk",       "chapters": 3,  "testament": "Old",  "order": 35},
    {"name": "Zephaniah",      "chapters": 3,  "testament": "Old",  "order": 36},
    {"name": "Haggai",         "chapters": 2,  "testament": "Old",  "order": 37},
    {"name": "Zechariah",      "chapters": 14, "testament": "Old",  "order": 38},
    {"name": "Malachi",        "chapters": 4,  "testament": "Old",  "order": 39},

    # New Testament (27 books)
    {"name": "Matthew",        "chapters": 28, "testament": "New",  "order": 40},
    {"name": "Mark",           "chapters": 16, "testament": "New",  "order": 41},
    {"name": "Luke",           "chapters": 24, "testament": "New",  "order": 42},
    {"name": "John",           "chapters": 21, "testament": "New",  "order": 43},
    {"name": "Acts",           "chapters": 28, "testament": "New",  "order": 44},
    {"name": "Romans",         "chapters": 16, "testament": "New",  "order": 45},
    {"name": "1 Corinthians",  "chapters": 16, "testament": "New",  "order": 46},
    {"name": "2 Corinthians",  "chapters": 13, "testament": "New",  "order": 47},
    {"name": "Galatians",      "chapters": 6,  "testament": "New",  "order": 48},
    {"name": "Ephesians",      "chapters": 6,  "testament": "New",  "order": 49},
    {"name": "Philippians",    "chapters": 4,  "testament": "New",  "order": 50},
    {"name": "Colossians",     "chapters": 4,  "testament": "New",  "order": 51},
    {"name": "1 Thessalonians","chapters": 5,  "testament": "New",  "order": 52},
    {"name": "2 Thessalonians","chapters": 3,  "testament": "New",  "order": 53},
    {"name": "1 Timothy",      "chapters": 6,  "testament": "New",  "order": 54},
    {"name": "2 Timothy",      "chapters": 4,  "testament": "New",  "order": 55},
    {"name": "Titus",          "chapters": 3,  "testament": "New",  "order": 56},
    {"name": "Philemon",       "chapters": 1,  "testament": "New",  "order": 57},
    {"name": "Hebrews",        "chapters": 13, "testament": "New",  "order": 58},
    {"name": "James",          "chapters": 5,  "testament": "New",  "order": 59},
    {"name": "1 Peter",        "chapters": 5,  "testament": "New",  "order": 60},
    {"name": "2 Peter",        "chapters": 3,  "testament": "New",  "order": 61},
    {"name": "1 John",         "chapters": 5,  "testament": "New",  "order": 62},
    {"name": "2 John",         "chapters": 1,  "testament": "New",  "order": 63},
    {"name": "3 John",         "chapters": 1,  "testament": "New",  "order": 64},
    {"name": "Jude",           "chapters": 1,  "testament": "New",  "order": 65},
    {"name": "Revelation",     "chapters": 22, "testament": "New",  "order": 66},
]

def get_book_names() -> list[str]:
    """Return ordered list of all Bible book names."""
    return [b["name"] for b in BIBLE_BOOKS]

def get_chapter_count(book_name: str) -> int:
    """Return the number of chapters in a given book. Returns 0 if not found."""
    for b in BIBLE_BOOKS:
        if b["name"].lower() == book_name.lower():
            return b["chapters"]
    return 0

def get_book_info(book_name: str) -> dict | None:
    """Return full info dict for a book, or None."""
    for b in BIBLE_BOOKS:
        if b["name"].lower() == book_name.lower():
            return b
    return None

def get_testament_books(testament: str) -> list[dict]:
    """Return all books in a testament ('Old' or 'New')."""
    return [b for b in BIBLE_BOOKS if b["testament"] == testament]
```

### 6.6 `modules/chapter_splitter.py` -- Chapter Distribution Algorithm

```python
"""
Algorithm for splitting a weekly Bible reading assignment into daily targets.
"""
import json
from datetime import date, timedelta
from modules import db
from modules.utils import get_day_of_week, get_week_dates

READING_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

def split_chapters(start_chapter: int, end_chapter: int, num_days: int = 6) -> dict:
    """
    Distribute chapters across reading days as evenly as possible.

    Algorithm:
        total = end - start + 1
        base = total // num_days
        remainder = total % num_days

        Days 1..remainder get (base + 1) chapters.
        Days (remainder+1)..num_days get base chapters.

    Args:
        start_chapter: First chapter number (inclusive)
        end_chapter:   Last chapter number (inclusive)
        num_days:      Number of reading days (default 6 for Mon-Sat)

    Returns:
        dict mapping day names to lists of chapter numbers.
        Example: {"monday": [1,2,3,4], "tuesday": [5,6,7,8], ...}
    """
    total = end_chapter - start_chapter + 1
    if total <= 0:
        return {day: [] for day in READING_DAYS[:num_days]}
    if num_days <= 0:
        return {}

    base_per_day = total // num_days
    remainder = total % num_days

    breakdown = {}
    current_chapter = start_chapter

    for i, day in enumerate(READING_DAYS[:num_days]):
        count = base_per_day + (1 if i < remainder else 0)
        day_chapters = list(range(current_chapter, current_chapter + count))
        breakdown[day] = day_chapters
        current_chapter += count

    return breakdown


def get_today_suggestion(entry_date: date) -> dict | None:
    """
    Get the suggested Bible reading for a given date from the active assignment.

    Returns:
        dict with keys: book, chapters (list[int]), range (str like "1-4")
        or None if no active assignment or date is outside the assignment week.
    """
    assignment = db.get_active_assignment()
    if not assignment:
        return None

    week_start = date.fromisoformat(assignment["week_start_date"])
    week_end = date.fromisoformat(assignment["week_end_date"])

    if not (week_start <= entry_date <= week_end):
        return None

    day_name = get_day_of_week(entry_date)
    breakdown = json.loads(assignment["daily_breakdown"]) if isinstance(
        assignment["daily_breakdown"], str
    ) else assignment["daily_breakdown"]

    chapters = breakdown.get(day_name, [])
    if not chapters:
        return None

    range_str = f"{chapters[0]}-{chapters[-1]}" if len(chapters) > 1 else str(chapters[0])

    return {
        "book": assignment["book"],
        "chapters": chapters,
        "range": range_str,
    }


def recalculate_remaining(
    assignment_id: int,
    book: str,
    end_chapter: int,
    chapters_completed: list[int],
    today: date,
    week_end: date,
) -> dict:
    """
    Recalculate the daily breakdown for remaining days when the user
    reads ahead or falls behind.

    Args:
        assignment_id:     ID of the active assignment
        book:              Bible book name
        end_chapter:       Last chapter in the assignment
        chapters_completed: All chapters read so far this week
        today:             Current date
        week_end:          Saturday of the assignment week

    Returns:
        Updated daily_breakdown dict
    """
    all_chapters = set(range(min(chapters_completed or [1]), end_chapter + 1))
    remaining = sorted(all_chapters - set(chapters_completed))

    if not remaining:
        return {}

    # Calculate remaining reading days (today through Saturday)
    remaining_days = []
    d = today
    while d <= week_end:
        day_name = get_day_of_week(d)
        if day_name in READING_DAYS:
            remaining_days.append(day_name)
        d += timedelta(days=1)

    if not remaining_days:
        return {}

    # Re-split remaining chapters across remaining days
    base = len(remaining) // len(remaining_days)
    extra = len(remaining) % len(remaining_days)

    new_breakdown = {}
    idx = 0
    for i, day in enumerate(remaining_days):
        count = base + (1 if i < extra else 0)
        new_breakdown[day] = remaining[idx:idx + count]
        idx += count

    return new_breakdown
```

### 6.7 `modules/clipboard.py` -- Clipboard Component

```python
"""
Clipboard copy functionality using Streamlit's HTML component with JavaScript.
"""
import streamlit as st
import streamlit.components.v1 as components

def copy_button(text: str, button_label: str = "Copy to Clipboard"):
    """
    Render a copy-to-clipboard button using injected JavaScript.

    This uses st.menu_style.v1.html() to inject a small HTML/JS snippet
    that copies text to the clipboard when clicked.

    Args:
        text: The text to copy to clipboard
        button_label: Label for the button
    """
    # Escape text for safe embedding in JavaScript
    escaped_text = (
        text
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("$", "\\$")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )

    html_code = f"""
    <div style="text-align: center;">
        <button id="copyBtn" style="
            background-color: #FF6B6B;
            color: white;
            border: none;
            padding: 12px 32px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            max-width: 400px;
            transition: background-color 0.3s;
        " onclick="copyToClipboard()">
            {button_label}
        </button>
        <p id="copyStatus" style="
            color: #28a745;
            font-weight: bold;
            margin-top: 8px;
            display: none;
        ">Copied! Now paste in WhatsApp</p>
    </div>

    <script>
    function copyToClipboard() {{
        const text = `{escaped_text}`;

        if (navigator.clipboard && navigator.clipboard.writeText) {{
            navigator.clipboard.writeText(text).then(function() {{
                showCopied();
            }}).catch(function() {{
                fallbackCopy(text);
            }});
        }} else {{
            fallbackCopy(text);
        }}
    }}

    function fallbackCopy(text) {{
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        textarea.select();
        try {{
            document.execCommand('copy');
            showCopied();
        }} catch (err) {{
            alert('Copy failed. Please manually select and copy the text above.');
        }}
        document.body.removeChild(textarea);
    }}

    function showCopied() {{
        const btn = document.getElementById('copyBtn');
        const status = document.getElementById('copyStatus');
        btn.style.backgroundColor = '#28a745';
        btn.textContent = 'Copied!';
        status.style.display = 'block';
        setTimeout(function() {{
            btn.style.backgroundColor = '#FF6B6B';
            btn.textContent = '{button_label}';
        }}, 3000);
    }}
    </script>
    """
    components.html(html_code, height=100)
```

---

## 7. Data Flow

### 7.1 Main Use Case: Log Entry and Generate Report

```
User opens app
    |
    v
[Dashboard Page]
    |  User clicks "Log Today's Entry"
    v
[Daily Entry Page]
    |
    v
st.date_input() --> entry_date
    |
    v
db.get_entry_by_date(entry_date) --> existing entry or None
    |
    +-- If existing: pre-fill form fields
    +-- If new: apply defaults
    |
    v
chapter_splitter.get_today_suggestion(entry_date)
    |
    +-- Queries db.get_active_assignment()
    +-- Looks up today's day in daily_breakdown JSON
    +-- Returns suggested chapters
    |
    v
[User fills form]
  - Prayer duration (slider)
  - Bible chapters (multiselect, pre-filled with suggestion)
  - Sermon info (optional text inputs)
    |
    v
st.form_submit_button("Save & Generate Report")
    |
    v
[Validation]
  - prayer_minutes > 0?
  - len(chapters) > 0?
  - YouTube URL valid (if provided)?
    |
    +-- FAIL: st.error() with message
    |
    +-- PASS:
        |
        v
    utils.format_chapters_display(book, chapters) --> "Luke 1-4"
        |
        v
    db.upsert_daily_entry(
        date, prayer_minutes, book, chapters_json,
        chapters_display, sermon_title, speaker, youtube_link
    )
        |
        v
    db.get_all_settings() --> {greeting_name, omit_empty_sermon, ...}
        |
        v
    message.format_whatsapp_message(
        entry_date, prayer_minutes, chapters_display,
        sermon_title, speaker, youtube_link,
        greeting_name, omit_empty_sermon
    ) --> formatted_message string
        |
        v
    st.code(formatted_message)  # Preview
        |
        v
    clipboard.copy_button(formatted_message)
        |
        v
    [User clicks "Copy to Clipboard"]
        |
        v
    JavaScript: navigator.clipboard.writeText(text)
        |
        v
    "Copied!" confirmation shown
        |
        v
    db.mark_report_copied(entry_date)
        |
        v
    User switches to WhatsApp, pastes, sends
```

### 7.2 Weekly Assignment Creation Flow

```
User navigates to Weekly Assignment page
    |
    v
[New Assignment tab]
    |
    v
st.selectbox("Book") --> book name
    |
    v
bible_data.get_chapter_count(book) --> max_chapters
    |
    v
st.number_input("From") --> start_chapter
st.number_input("To") --> end_chapter
st.date_input("Week starting") --> week_start (Monday)
    |
    v
st.form_submit_button("Generate Breakdown")
    |
    v
chapter_splitter.split_chapters(start_chapter, end_chapter, 6)
    |
    v
--> {"monday": [1,2,3,4], "tuesday": [5,6,7,8], ...}
    |
    v
Store in st.session_state["preview_breakdown"]
    |
    v
[Display breakdown for review]
    |
    v
st.button("Confirm Assignment")
    |
    v
db.create_assignment(book, start, end, week_start, week_end, breakdown)
    |  (also deactivates any previous ACTIVE assignment)
    v
st.success("Assignment created!")
```

---

## 8. Copy-to-Clipboard Implementation

### Why JavaScript Injection?

Streamlit does not have a native clipboard API. The standard approach is to use `st.components.v1.html()` to inject a small HTML/JS snippet into the page.

### Implementation Strategy

The clipboard module (`modules/clipboard.py`, defined in Section 6.7) uses a three-tier approach:

1. **Primary:** `navigator.clipboard.writeText()` -- Modern Clipboard API (works in all modern browsers over HTTPS, which Streamlit Cloud provides).
2. **Fallback:** `document.execCommand('copy')` with a hidden textarea -- For older browsers.
3. **Last resort:** Display the message in a selectable text area with instructions to manually select-all and copy.

### Key Considerations

- **HTTPS required:** The modern Clipboard API requires a secure context. Streamlit Community Cloud serves over HTTPS by default, so this works.
- **Component height:** The `components.html()` call needs an explicit height parameter. Set to `100` pixels to accommodate the button and status text.
- **Text escaping:** The message text must be properly escaped for embedding inside a JavaScript template literal. Newlines, backticks, dollar signs, and quotes all need escaping.
- **No cross-frame communication:** The JS runs inside an iframe created by `st.components.v1.html()`. There is no way to notify Streamlit Python code that the copy succeeded. Instead, after the copy button is rendered, we call `db.mark_report_copied()` immediately (assumes intent to copy).

### Alternative: streamlit-clipboard Package

The `streamlit-clipboard` third-party package could also be used. However, relying on the built-in `st.components.v1.html()` avoids an external dependency and gives full control over styling and behavior.

---

## 9. Chapter Splitting Algorithm

### Algorithm: Even Distribution with Remainder Front-Loading

```
FUNCTION split_chapters(start_chapter, end_chapter, num_days=6):
    total_chapters = end_chapter - start_chapter + 1
    base_per_day = total_chapters DIV num_days
    remainder = total_chapters MOD num_days

    current = start_chapter
    breakdown = {}

    FOR i = 0 TO num_days - 1:
        day_name = READING_DAYS[i]   -- ["monday", "tuesday", ..., "saturday"]

        IF i < remainder THEN
            count = base_per_day + 1   -- Extra chapter for first 'remainder' days
        ELSE
            count = base_per_day
        END IF

        breakdown[day_name] = [current, current+1, ..., current+count-1]
        current = current + count
    END FOR

    RETURN breakdown
END FUNCTION
```

### Worked Examples

**Example 1: Luke (24 chapters, 6 days)**
```
total = 24, base = 24 / 6 = 4, remainder = 24 % 6 = 0
Every day gets exactly 4 chapters.

Monday:    Ch 1-4
Tuesday:   Ch 5-8
Wednesday: Ch 9-12
Thursday:  Ch 13-16
Friday:    Ch 17-20
Saturday:  Ch 21-24
```

**Example 2: Romans (16 chapters, 6 days)**
```
total = 16, base = 16 / 6 = 2, remainder = 16 % 6 = 4
Days 1-4 get 3 chapters (base + 1), Days 5-6 get 2 chapters (base).

Monday:    Ch 1-3     (3 chapters)
Tuesday:   Ch 4-6     (3 chapters)
Wednesday: Ch 7-9     (3 chapters)
Thursday:  Ch 10-12   (3 chapters)
Friday:    Ch 13-14   (2 chapters)
Saturday:  Ch 15-16   (2 chapters)
```

**Example 3: Philemon (1 chapter, 6 days)**
```
total = 1, base = 0, remainder = 1
Only Monday gets 1 chapter. All other days get 0.

Monday:    Ch 1       (1 chapter)
Tuesday:   (none)
Wednesday: (none)
Thursday:  (none)
Friday:    (none)
Saturday:  (none)
```

### Dynamic Recalculation

When the user reads more or fewer chapters than suggested on a given day:

```
FUNCTION recalculate_remaining(chapters_completed, end_chapter, today, week_end):
    all_assigned = {start_chapter ... end_chapter}
    remaining = all_assigned - chapters_completed
    remaining_days = count_reading_days(today, week_end)

    IF remaining is empty:
        RETURN {}   -- Assignment complete

    RETURN split_chapters(
        min(remaining), max(remaining), remaining_days
    )
END FUNCTION
```

This is called when loading the daily entry form to update suggestions. The recalculated breakdown is saved back to the assignment record.

---

## 10. Bible Reference Data

The complete list of 66 books with chapter counts is defined as a Python list in `modules/bible_data.py` (see Section 6.5 for the full implementation).

### Summary Statistics

| Testament | Books | Total Chapters |
|-----------|-------|----------------|
| Old Testament | 39 | 929 |
| New Testament | 27 | 260 |
| **Total** | **66** | **1,189** |

### Data Access Patterns

| Function | Purpose | Used By |
|----------|---------|---------|
| `get_book_names()` | Populate dropdown selectors | Daily Entry, Weekly Assignment |
| `get_chapter_count(book)` | Set max value for chapter inputs | Daily Entry, Weekly Assignment |
| `get_book_info(book)` | Full metadata for a book | Stats page |
| `get_testament_books(testament)` | Filter by testament | Future: filtered dropdowns |

---

## 11. Streamlit Configuration

### `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#FFF5F5"
textColor = "#333333"
font = "sans serif"

[server]
headless = true
maxUploadSize = 5

[browser]
gatherUsageStats = false
```

### Theme Rationale

| Setting | Value | Reason |
|---------|-------|--------|
| primaryColor | `#FF6B6B` | Warm coral/salmon -- spiritual, warm, not clinical |
| backgroundColor | `#FFFFFF` | Clean white background |
| secondaryBackgroundColor | `#FFF5F5` | Very light pink tint for sidebar and containers |
| textColor | `#333333` | Dark gray for readability (softer than pure black) |
| font | `sans serif` | Clean, modern, mobile-friendly |

### Page Configuration in `app.py`

```python
import streamlit as st

st.set_page_config(
    page_title="Spiritual Growth Tracker",
    page_icon="cross_mark",
    layout="centered",
    initial_sidebar_state="collapsed",  # Collapsed on mobile for more space
)
```

---

## 12. Deployment

### 12.1 Prerequisites

1. A GitHub repository containing the project code.
2. A Streamlit Community Cloud account (free at share.streamlit.io).

### 12.2 Repository Structure for Deployment

```
Repository root:
  app.py                  # Entry point (Streamlit looks for this)
  requirements.txt        # Dependencies
  .streamlit/
    config.toml           # Theme config
  pages/
    1_Daily_Entry.py
    2_Prayer_Journal.py
    3_Weekly_Assignment.py
    4_Streaks_and_Stats.py
    5_Settings.py
  modules/
    __init__.py
    db.py
    models.py
    utils.py
    message.py
    bible_data.py
    chapter_splitter.py
    clipboard.py
  data/
    .gitkeep              # Keep the directory in git; tracker.db is gitignored
```

### 12.3 `requirements.txt`

```
streamlit>=1.32.0
plotly>=5.18.0
```

### 12.4 `.gitignore`

```
data/tracker.db
__pycache__/
*.pyc
.DS_Store
```

### 12.5 Deployment Steps

1. **Push code to GitHub.**
2. **Go to** [share.streamlit.io](https://share.streamlit.io) and sign in.
3. **Click "New app"** and select:
   - Repository: `your-username/spiritual-growth-tracker`
   - Branch: `main`
   - Main file path: `app.py`
4. **Click "Deploy."** Streamlit Cloud will install requirements and launch.
5. **Access the app** at `https://your-app-name.streamlit.app`.

### 12.6 SQLite Persistence on Streamlit Cloud

Streamlit Community Cloud persists files between app reboots. The SQLite database at `data/tracker.db` will survive app restarts. However:

- **Risk:** If Streamlit Cloud reprovisioned the container entirely (rare), data could be lost.
- **Mitigation:** The app includes a JSON export feature (Settings page). Users should periodically download a backup.
- **Future:** Migrate to a cloud database (Supabase, Neon PostgreSQL) for guaranteed durability.

### 12.7 Secrets Management

For MVP, no secrets are required (no auth, no API keys). If password protection is added later:

```toml
# .streamlit/secrets.toml (local only, never committed)
[passwords]
app_password = "your-secure-password"
```

On Streamlit Cloud, secrets are configured in the app settings dashboard, not in files.

---

## 13. Error Handling Strategy

### Database Errors

```python
# In db.py - all operations use the context manager
@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Database error: {e}")
        raise
    finally:
        conn.close()
```

### Form Validation Errors

Handled inline in the page code using `st.error()`, `st.warning()`:
- Empty required fields shown with `st.error("Please enter...")`
- Invalid YouTube URLs shown with `st.warning("Invalid YouTube URL format")`

### Graceful Degradation

| Scenario | Behavior |
|----------|----------|
| No active assignment | Daily Entry shows manual chapter input (no suggestions) |
| Clipboard copy fails | Fallback to `execCommand`, then to selectable text area |
| Database file missing | Auto-created on first `init_db()` call |
| Empty database | Dashboard shows zero state with call-to-action |

---

## 14. Performance Considerations

### Database

- **WAL mode enabled** (`PRAGMA journal_mode=WAL`) for better concurrent read performance during Streamlit reruns.
- **Indexes** on `daily_entries.date` and `weekly_assignments` dates for fast lookups.
- **Data volume is tiny:** A single user generating one entry per day produces roughly 365 rows/year. SQLite handles this effortlessly.

### Streamlit Caching

```python
@st.cache_data(ttl=60)
def get_bible_book_names():
    """Cache the static Bible book list -- never changes."""
    return bible_data.get_book_names()

@st.cache_data(ttl=10)
def get_streak_data():
    """Cache streak calculation for 10 seconds to avoid recomputing on every rerun."""
    dates = db.get_all_entry_dates()
    return utils.calculate_streaks(dates)
```

Use `@st.cache_data` for:
- Bible book list (static data, long TTL)
- Streak calculations (short TTL, recompute after new entry)

Do NOT cache:
- Form data (must reflect current state)
- Current entry lookup (must be real-time)

### Page Load Targets

| Operation | Target | Approach |
|-----------|--------|----------|
| Page render | < 3 seconds | Streamlit Cloud + lightweight SQLite queries |
| Form save | < 500ms | Single SQLite INSERT/UPDATE |
| Message generation | < 200ms | Pure string formatting |
| Clipboard copy | < 100ms | Client-side JavaScript |

---

*End of Architecture Document*
*Prepared by BMAD Architect*
*This document is implementation-ready. A developer can begin coding directly from these specifications.*
