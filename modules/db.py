"""
Database module for Logos Pulse — Supabase edition.
All functions use the authenticated user's session via RLS.
Function signatures are preserved from the SQLite version for page compatibility.
"""

import json
import streamlit as st
from typing import Optional
from modules.supabase_client import get_supabase_client, get_admin_client
from modules.sanitize import sanitize_html


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
    """Wrap a Supabase operation with error handling and retry on token expiry."""
    try:
        return operation()
    except Exception as e:
        error_msg = str(e)

        # Token expired — try refreshing and retrying once
        if "JWT" in error_msg or "token" in error_msg.lower() or "401" in error_msg:
            refresh = st.session_state.get("refresh_token")
            if refresh:
                try:
                    client = get_supabase_client()
                    response = client.auth.refresh_session(refresh)
                    if response and response.session:
                        st.session_state["access_token"] = response.session.access_token
                        st.session_state["refresh_token"] = response.session.refresh_token
                        return operation()  # Retry
                except Exception:
                    pass
            st.session_state["authenticated"] = False
            st.error("Your session has expired. Please log in again.")
            st.stop()

        elif "violates row-level security" in error_msg.lower():
            st.error("You don't have permission to perform this action.")
            return fallback

        elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            st.error("Could not reach the server. Please check your connection and try again.")
            return fallback

        else:
            st.error("Something went wrong. Please try again.")
            return fallback


def init_db():
    """No-op for Supabase — schema is managed via migrations."""
    pass


# --- Session-scoped cache ---
# Caches read results per Streamlit rerun to avoid duplicate API calls
# within the same page render. Cleared automatically on each rerun
# and explicitly on write operations.

def _cache_key(name: str, *args) -> str:
    return f"_db_cache_{_uid()}_{name}_{'_'.join(str(a) for a in args)}"


def _get_cached(key: str):
    return st.session_state.get(key)


def _set_cached(key: str, value):
    st.session_state[key] = value
    return value


def _clear_cache(prefix: str = ""):
    """Clear cached queries. If prefix given, only clear matching keys."""
    uid = _uid()
    keys_to_clear = [
        k for k in st.session_state
        if k.startswith(f"_db_cache_{uid}_{prefix}")
    ]
    for k in keys_to_clear:
        del st.session_state[k]


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
        "bible_book": sanitize_html(bible_book),
        "chapters_read": chapters_read,
        "chapters_display": sanitize_html(chapters_display),
        "sermon_title": sanitize_html(sermon_title),
        "sermon_speaker": sanitize_html(sermon_speaker),
        "youtube_link": sanitize_html(youtube_link),
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

    _clear_cache("daily_entries")
    _clear_cache("entry_dates")
    return _safe_execute(_do, fallback=row_data)


def get_entry_by_date(entry_date: str) -> Optional[dict]:
    key = _cache_key("daily_entries", entry_date)
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("daily_entries") \
        .select("*") \
        .eq("user_id", _uid()) \
        .eq("date", entry_date) \
        .execute()
    value = result.data[0] if result.data else None
    return _set_cached(key, value)


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
    key = _cache_key("entry_dates")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("daily_entries") \
        .select("date") \
        .eq("user_id", _uid()) \
        .order("date") \
        .execute()
    return _set_cached(key, [r["date"] for r in (result.data or [])])


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
    _clear_cache("active_assignment")
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
    key = _cache_key("active_assignment")
    cached = _get_cached(key)
    if cached is not None:
        return cached if cached != "__none__" else None
    client = _client()
    result = client.table("weekly_assignments") \
        .select("*") \
        .eq("user_id", _uid()) \
        .eq("status", "ACTIVE") \
        .order("id", desc=True) \
        .limit(1) \
        .execute()
    value = result.data[0] if result.data else None
    _set_cached(key, value if value else "__none__")
    return value


def get_assignment_history() -> list[dict]:
    client = _client()
    result = client.table("weekly_assignments") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("id", desc=True) \
        .execute()
    return result.data or []


def create_group_assignment(pastor_id: str, member_ids: list[str],
                            book: str, start_chapter: int, end_chapter: int,
                            week_start: str, week_end: str,
                            daily_breakdown: dict) -> dict:
    """Create a weekly assignment for all members in a pastor's group.
    Uses admin client to bypass RLS (pastor inserts rows for other users).
    """
    admin = get_admin_client()
    total = end_chapter - start_chapter + 1
    created = 0

    for member_id in member_ids:
        # Mark existing active assignments as completed for this member
        admin.table("weekly_assignments") \
            .update({"status": "COMPLETED"}) \
            .eq("user_id", member_id) \
            .eq("status", "ACTIVE") \
            .execute()

        admin.table("weekly_assignments").insert({
            "user_id": member_id,
            "assigned_by": pastor_id,
            "book": sanitize_html(book),
            "start_chapter": start_chapter,
            "end_chapter": end_chapter,
            "total_chapters": total,
            "week_start_date": week_start,
            "week_end_date": week_end,
            "daily_breakdown": daily_breakdown,
            "status": "ACTIVE",
        }).execute()
        created += 1

    return {"success": True, "count": created}


def get_group_assignments(pastor_id: str) -> list[dict]:
    """Get all assignments created by a pastor for their group."""
    admin = get_admin_client()
    result = admin.table("weekly_assignments") \
        .select("*") \
        .eq("assigned_by", pastor_id) \
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
    cache_k = _cache_key("all_settings")
    cached = _get_cached(cache_k)
    if cached is not None:
        return cached
    client = _client()
    uid = _uid()
    if not uid:
        return {}
    result = client.table("app_settings") \
        .select("key, value") \
        .eq("user_id", uid) \
        .execute()
    return _set_cached(cache_k, {r["key"]: r["value"] for r in (result.data or [])})


def save_setting(key: str, value: str):
    _clear_cache("all_settings")
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
    _clear_cache("all_sermon_notes")
    client = _client()
    result = client.table("sermon_notes").insert({
        "user_id": _uid(),
        "title": sanitize_html(title),
        "speaker": sanitize_html(speaker),
        "sermon_date": sermon_date,
        "notes_text": sanitize_html(notes_text),
        "bible_references": bible_references,
        "learnings": sanitize_html(learnings),
        "key_takeaways": sanitize_html(key_takeaways),
        "additional_thoughts": sanitize_html(additional_thoughts),
    }).execute()
    return result.data[0] if result.data else {}


def update_sermon_note(note_id: int, title: str, speaker: str, sermon_date: str,
                       notes_text: str, bible_references: list,
                       learnings: str, key_takeaways: str,
                       additional_thoughts: str) -> dict:
    _clear_cache("all_sermon_notes")
    client = _client()
    result = client.table("sermon_notes") \
        .update({
            "title": sanitize_html(title),
            "speaker": sanitize_html(speaker),
            "sermon_date": sermon_date,
            "notes_text": sanitize_html(notes_text),
            "bible_references": bible_references,
            "learnings": sanitize_html(learnings),
            "key_takeaways": sanitize_html(key_takeaways),
            "additional_thoughts": sanitize_html(additional_thoughts),
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
    key = _cache_key("all_sermon_notes")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("sermon_notes") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("sermon_date", desc=True) \
        .order("id", desc=True) \
        .execute()
    return _set_cached(key, result.data or [])


def delete_sermon_note(note_id: int):
    _clear_cache("all_sermon_notes")
    client = _client()
    client.table("sermon_notes") \
        .delete() \
        .eq("id", note_id) \
        .eq("user_id", _uid()) \
        .execute()


# --- Prayer Categories ---

def get_prayer_categories() -> list[dict]:
    key = _cache_key("prayer_categories")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("prayer_categories") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("id") \
        .execute()
    return _set_cached(key, result.data or [])


def create_prayer_category(name: str, icon: str = "", color: str = "#5B4FC4") -> dict:
    _clear_cache("prayer_categories")
    client = _client()
    result = client.table("prayer_categories").insert({
        "user_id": _uid(),
        "name": sanitize_html(name),
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
        "title": sanitize_html(title),
        "prayer_text": sanitize_html(prayer_text),
        "scriptures": scriptures,
        "confessions": sanitize_html(confessions),
        "declarations": sanitize_html(declarations),
        "status": "ongoing",
    }).execute()
    return result.data[0] if result.data else {}


def update_prayer_entry(entry_id: int, title: str, prayer_text: str,
                        scriptures: list, confessions: str,
                        declarations: str, status: str) -> dict:
    client = _client()
    result = client.table("prayer_entries") \
        .update({
            "title": sanitize_html(title),
            "prayer_text": sanitize_html(prayer_text),
            "scriptures": scriptures,
            "confessions": sanitize_html(confessions),
            "declarations": sanitize_html(declarations),
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

# --- Prayer Templates (REQ-4) ---

def get_prayer_templates() -> list[dict]:
    """Get all standard + user's custom prayer templates."""
    key = _cache_key("prayer_templates")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("prayer_templates") \
        .select("*") \
        .eq("is_archived", False) \
        .order("sort_order") \
        .order("name") \
        .execute()
    return _set_cached(key, result.data or [])


def get_prayer_template(template_id: int) -> Optional[dict]:
    client = _client()
    result = client.table("prayer_templates") \
        .select("*") \
        .eq("id", template_id) \
        .execute()
    return result.data[0] if result.data else None


def create_prayer_template(name: str, description: str, confessions: str,
                           prayers: str, declarations: str,
                           scriptures: list = None, template_type: str = "custom") -> dict:
    _clear_cache("prayer_templates")
    client = _client()
    result = client.table("prayer_templates").insert({
        "name": sanitize_html(name),
        "description": sanitize_html(description),
        "template_type": template_type,
        "created_by": _uid(),
        "confessions": sanitize_html(confessions),
        "prayers": sanitize_html(prayers),
        "declarations": sanitize_html(declarations),
        "scriptures": scriptures,
    }).execute()
    return result.data[0] if result.data else {}


# --- Wizard Assignments (REQ-5) ---

def create_wizard_assignment(title: str, description: str, created_by: str,
                             target_user_ids: list[str], start_date: str,
                             end_date: str, components: list[dict]) -> dict:
    """Create a composite wizard assignment with components and targets."""
    admin = get_admin_client()

    # Create the assignment
    result = admin.table("wizard_assignments").insert({
        "title": sanitize_html(title),
        "description": sanitize_html(description),
        "created_by": created_by,
        "target_type": "specific",
        "start_date": start_date,
        "end_date": end_date,
        "is_published": True,
    }).execute()

    if not result.data:
        return {"success": False, "error": "Failed to create assignment"}

    assignment_id = result.data[0]["id"]

    # Add targets
    targets = [{"wizard_assignment_id": assignment_id, "user_id": uid} for uid in target_user_ids]
    if targets:
        admin.table("wizard_assignment_targets").insert(targets).execute()

    # Add components
    for i, comp in enumerate(components):
        admin.table("wizard_components").insert({
            "wizard_assignment_id": assignment_id,
            "component_type": comp["type"],
            "config": comp["config"],
            "sort_order": i,
        }).execute()

    return {"success": True, "id": assignment_id}


def get_my_wizard_assignments() -> list[dict]:
    """Get wizard assignments assigned to the current user."""
    client = _client()
    uid = _uid()
    # Get assignment IDs for this user
    targets = client.table("wizard_assignment_targets") \
        .select("wizard_assignment_id") \
        .eq("user_id", uid) \
        .execute()
    if not targets.data:
        return []

    assignment_ids = [t["wizard_assignment_id"] for t in targets.data]
    result = client.table("wizard_assignments") \
        .select("*") \
        .in_("id", assignment_ids) \
        .eq("is_published", True) \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


def get_wizard_components(assignment_id: int) -> list[dict]:
    """Get components for a wizard assignment."""
    client = _client()
    result = client.table("wizard_components") \
        .select("*") \
        .eq("wizard_assignment_id", assignment_id) \
        .order("sort_order") \
        .execute()
    return result.data or []


def get_wizard_progress(component_id: int, user_id: str = None) -> Optional[dict]:
    """Get progress for a specific component."""
    admin = get_admin_client()
    uid = user_id or _uid()
    result = admin.table("wizard_component_progress") \
        .select("*") \
        .eq("wizard_component_id", component_id) \
        .eq("user_id", uid) \
        .execute()
    return result.data[0] if result.data else None


def update_wizard_progress(component_id: int, status: str, progress_data: dict = None):
    """Update progress on a wizard component."""
    admin = get_admin_client()
    uid = _uid()
    existing = admin.table("wizard_component_progress") \
        .select("id") \
        .eq("wizard_component_id", component_id) \
        .eq("user_id", uid) \
        .execute()

    data = {"wizard_component_id": component_id, "user_id": uid, "status": status}
    if progress_data:
        data["progress_data"] = progress_data

    if existing.data:
        admin.table("wizard_component_progress") \
            .update({"status": status, "progress_data": progress_data}) \
            .eq("wizard_component_id", component_id) \
            .eq("user_id", uid) \
            .execute()
    else:
        admin.table("wizard_component_progress").insert(data).execute()


def get_sermon_series_list() -> list[dict]:
    """Get all sermon series."""
    client = _client()
    result = client.table("sermon_series") \
        .select("*") \
        .order("title") \
        .execute()
    return result.data or []


def get_wizard_assignments_by_creator(creator_id: str) -> list[dict]:
    """Get all wizard assignments created by a specific user."""
    admin = get_admin_client()
    result = admin.table("wizard_assignments") \
        .select("*") \
        .eq("created_by", creator_id) \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


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