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
    result = _safe_execute(_do, fallback=row_data)
    # Auto-update any tracking goals (best-effort, non-blocking)
    try:
        _fasted = bool(row_data.get("fasted"))
        auto_update_goals(
            prayer_minutes=prayer_minutes,
            chapters_count=len(chapters_read or []),
            fasted=_fasted,
            entry_date=entry_date,
        )
    except Exception:
        pass
    return result


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
                       additional_thoughts: str,
                       tags: list = None) -> dict:
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
        "tags": [sanitize_html(t) for t in (tags or [])],
    }).execute()
    return result.data[0] if result.data else {}


def update_sermon_note(note_id: int, title: str, speaker: str, sermon_date: str,
                       notes_text: str, bible_references: list,
                       learnings: str, key_takeaways: str,
                       additional_thoughts: str,
                       tags: list = None) -> dict:
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
            "tags": [sanitize_html(t) for t in (tags or [])],
        }) \
        .eq("id", note_id) \
        .eq("user_id", _uid()) \
        .execute()
    return result.data[0] if result.data else {}


def toggle_sermon_starred(note_id: int, current: bool) -> None:
    _clear_cache("all_sermon_notes")
    _safe_execute(
        lambda: _client().table("sermon_notes")
            .update({"is_starred": not current})
            .eq("id", note_id)
            .eq("user_id", _uid())
            .execute(),
        fallback=None,
    )


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


# --- Prayer Sharing ---

def share_prayer_with_pastor(prayer_id: int):
    """Mark a prayer as shared with the user's pastor."""
    client = _client()
    from datetime import datetime
    client.table("prayer_entries") \
        .update({"shared_with_pastor": True, "shared_at": datetime.now().isoformat()}) \
        .eq("id", prayer_id) \
        .eq("user_id", _uid()) \
        .execute()


def unshare_prayer(prayer_id: int):
    """Remove sharing from a prayer."""
    client = _client()
    client.table("prayer_entries") \
        .update({"shared_with_pastor": False, "shared_at": None}) \
        .eq("id", prayer_id) \
        .eq("user_id", _uid()) \
        .execute()


def get_shared_prayers_for_pastor(pastor_id: str) -> list[dict]:
    """Get all prayers shared by members of a specific pastor."""
    admin = get_admin_client()
    # Get member IDs for this pastor
    members = admin.table("user_profiles") \
        .select("user_id") \
        .eq("pastor_id", pastor_id) \
        .execute()
    member_ids = [m["user_id"] for m in (members.data or [])]
    if not member_ids:
        return []

    result = admin.table("prayer_entries") \
        .select("*") \
        .in_("user_id", member_ids) \
        .eq("shared_with_pastor", True) \
        .order("shared_at", desc=True) \
        .execute()

    # Enrich with member names
    prayers = result.data or []
    for p in prayers:
        try:
            u = admin.auth.admin.get_user_by_id(p["user_id"]).user
            meta = u.user_metadata or {}
            p["member_name"] = meta.get("preferred_name") or meta.get("first_name", "Member")
        except Exception:
            p["member_name"] = "Member"
    return prayers


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


# --- Pastor Notes ---

def get_pastor_notes(pastor_id: str, member_id: str) -> list[dict]:
    """Get all notes a pastor has written about a member."""
    admin = get_admin_client()
    result = admin.table("pastor_notes") \
        .select("*") \
        .eq("pastor_id", pastor_id) \
        .eq("member_id", member_id) \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


def add_pastor_note(pastor_id: str, member_id: str, note_text: str) -> dict:
    admin = get_admin_client()
    result = admin.table("pastor_notes").insert({
        "pastor_id": pastor_id,
        "member_id": member_id,
        "note_text": sanitize_html(note_text),
    }).execute()
    return result.data[0] if result.data else {}


def delete_pastor_note(note_id: int):
    admin = get_admin_client()
    admin.table("pastor_notes").delete().eq("id", note_id).execute()


# --- Member History (for Pastor/Bishop view) ---

def get_member_entries(member_id: str, limit: int = 30) -> list[dict]:
    """Get recent daily entries for a specific member (admin client bypasses RLS)."""
    admin = get_admin_client()
    result = admin.table("daily_entries") \
        .select("*") \
        .eq("user_id", member_id) \
        .order("date", desc=True) \
        .limit(limit) \
        .execute()
    return result.data or []


def get_member_entry_dates(member_id: str) -> list[str]:
    """Get all entry dates for a member."""
    admin = get_admin_client()
    result = admin.table("daily_entries") \
        .select("date") \
        .eq("user_id", member_id) \
        .order("date") \
        .execute()
    return [r["date"] for r in (result.data or [])]


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


# --- Testimonies ---

def create_testimony(title: str, testimony: str, is_anonymous: bool = False) -> dict:
    client = _client()
    result = client.table("testimonies").insert({
        "user_id": _uid(),
        "title": sanitize_html(title),
        "testimony": sanitize_html(testimony),
        "is_anonymous": is_anonymous,
    }).execute()
    return result.data[0] if result.data else {}


def get_testimonies(approved_only: bool = True) -> list[dict]:
    admin = get_admin_client()
    query = admin.table("testimonies").select("*").order("created_at", desc=True)
    if approved_only:
        query = query.eq("is_approved", True)
    result = query.execute()
    # Enrich with names
    for t in (result.data or []):
        if t.get("is_anonymous"):
            t["author_name"] = "Anonymous"
        else:
            try:
                u = admin.auth.admin.get_user_by_id(t["user_id"]).user
                t["author_name"] = (u.user_metadata or {}).get("preferred_name", "Member")
            except Exception:
                t["author_name"] = "Member"
    return result.data or []


def approve_testimony(testimony_id: int):
    admin = get_admin_client()
    admin.table("testimonies") \
        .update({"is_approved": True, "approved_by": _uid()}) \
        .eq("id", testimony_id) \
        .execute()


def react_to_testimony(testimony_id: int, reaction: str):
    admin = get_admin_client()
    t = admin.table("testimonies").select("reactions").eq("id", testimony_id).execute()
    if t.data:
        reactions = t.data[0].get("reactions") or {"pray": 0, "amen": 0, "hallelujah": 0}
        reactions[reaction] = reactions.get(reaction, 0) + 1
        admin.table("testimonies").update({"reactions": reactions}).eq("id", testimony_id).execute()


# --- Personal Goals ---

def create_personal_goal(title: str, description: str, goal_type: str,
                         target_value: int = None, target_date: str = None,
                         tracking_mode: str = "manual", unit: str = None) -> dict:
    client = _client()
    result = client.table("personal_goals").insert({
        "user_id": _uid(),
        "title": sanitize_html(title),
        "description": sanitize_html(description),
        "goal_type": goal_type,
        "target_value": target_value,
        "target_date": target_date,
        "tracking_mode": tracking_mode,
        "unit": unit,
    }).execute()
    return result.data[0] if result.data else {}


def get_personal_goals(status: str = "active") -> list[dict]:
    client = _client()
    result = client.table("personal_goals") \
        .select("*") \
        .eq("user_id", _uid()) \
        .eq("status", status) \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


def update_goal_progress(goal_id: int, current_value: int, status: str = None):
    client = _client()
    data = {"current_value": current_value}
    if status:
        data["status"] = status
    client.table("personal_goals").update(data).eq("id", goal_id).eq("user_id", _uid()).execute()


def auto_update_goals(prayer_minutes: int, chapters_count: int, fasted: bool,
                      entry_date: str) -> None:
    """Increment auto-tracking active goals based on today's entry. Skips if already counted today."""
    from datetime import date as _date
    uid = _uid()
    client = _client()
    goals_result = client.table("personal_goals") \
        .select("*") \
        .eq("user_id", uid) \
        .eq("status", "active") \
        .neq("tracking_mode", "manual") \
        .execute()
    goals = goals_result.data or []
    for g in goals:
        if g.get("last_tracked_date") == entry_date:
            continue  # already counted today
        mode = g["tracking_mode"]
        delta = 0
        if mode == "auto_prayer":
            delta = prayer_minutes
        elif mode == "auto_reading":
            delta = chapters_count
        elif mode == "auto_fasting":
            delta = 1 if fasted else 0
        if delta == 0:
            continue
        new_val = (g.get("current_value") or 0) + delta
        target = g.get("target_value") or 0
        new_status = "completed" if target > 0 and new_val >= target else None
        update_data: dict = {
            "current_value": new_val,
            "last_tracked_date": entry_date,
        }
        if new_status:
            update_data["status"] = new_status
        client.table("personal_goals").update(update_data) \
            .eq("id", g["id"]).eq("user_id", uid).execute()


# --- Fasting Log ---

def log_fast(fast_date: str, fast_type: str, notes: str = "") -> dict:
    client = _client()
    result = client.table("fasting_log").upsert({
        "user_id": _uid(),
        "date": fast_date,
        "fast_type": fast_type,
        "notes": sanitize_html(notes),
    }, on_conflict="user_id,date").execute()
    return result.data[0] if result.data else {}


def get_fasting_log(limit: int = 30) -> list[dict]:
    client = _client()
    result = client.table("fasting_log") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("date", desc=True) \
        .limit(limit) \
        .execute()
    return result.data or []


def get_fasting_dates() -> list[str]:
    client = _client()
    result = client.table("fasting_log") \
        .select("date") \
        .eq("user_id", _uid()) \
        .order("date") \
        .execute()
    return [r["date"] for r in (result.data or [])]


# --- Audit Log ---

def log_audit(action: str, target_type: str = None, target_id: str = None, details: dict = None):
    admin = get_admin_client()
    admin.table("audit_log").insert({
        "actor_id": _uid(),
        "action": action,
        "target_type": target_type,
        "target_id": target_id,
        "details": details,
    }).execute()


def get_audit_log(limit: int = 50) -> list[dict]:
    admin = get_admin_client()
    result = admin.table("audit_log") \
        .select("*") \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()
    # Enrich with actor names
    for entry in (result.data or []):
        try:
            u = admin.auth.admin.get_user_by_id(entry["actor_id"]).user
            entry["actor_name"] = (u.user_metadata or {}).get("preferred_name", u.email)
        except Exception:
            entry["actor_name"] = "System"
    return result.data or []


# --- Announcements ---

def create_announcement(title: str, message: str, target_role: str = "all",
                        expires_at: str = None) -> dict:
    client = _client()
    result = client.table("announcements").insert({
        "created_by": _uid(),
        "title": sanitize_html(title),
        "message": sanitize_html(message),
        "target_role": target_role,
        "expires_at": expires_at,
    }).execute()
    return result.data[0] if result.data else {}


def get_active_announcements(role: str = None) -> list[dict]:
    admin = get_admin_client()
    uid = _uid()
    result = admin.table("announcements") \
        .select("*") \
        .eq("is_active", True) \
        .order("created_at", desc=True) \
        .execute()

    # Filter by role and remove dismissed
    dismissed = admin.table("announcement_dismissals") \
        .select("announcement_id") \
        .eq("user_id", uid) \
        .execute()
    dismissed_ids = {d["announcement_id"] for d in (dismissed.data or [])}

    announcements = []
    for a in (result.data or []):
        if a["id"] in dismissed_ids:
            continue
        if a.get("target_role") and a["target_role"] != "all" and a["target_role"] != role:
            continue
        announcements.append(a)
    return announcements


def dismiss_announcement(announcement_id: int):
    client = _client()
    client.table("announcement_dismissals").insert({
        "announcement_id": announcement_id,
        "user_id": _uid(),
    }).execute()


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


# ─── Prayer Engine ───────────────────────────────────────────────────

def get_confession_categories(tier: int = None) -> list[dict]:
    key = _cache_key("confession_categories", tier or "all")
    cached = _get_cached(key)
    if cached is not None:
        return cached

    def op():
        client = _client()
        q = client.table("confession_categories").select("*").eq("is_active", True).order("sort_order")
        if tier:
            q = q.eq("tier", tier)
        return q.execute()
    result = _safe_execute(op, fallback=None)
    return _set_cached(key, result.data if result and result.data else [])


def get_confession_templates(category_id: int = None, published_only: bool = True) -> list[dict]:
    key = _cache_key("confession_templates", category_id or "all", published_only)
    cached = _get_cached(key)
    if cached is not None:
        return cached

    def op():
        client = _client()
        q = client.table("confession_templates").select("*, confession_categories(name, icon, color)")
        if published_only:
            q = q.eq("is_published", True).eq("is_pastor_custom", False)
        if category_id:
            q = q.eq("category_id", category_id)
        return q.order("sort_order").execute()
    result = _safe_execute(op, fallback=None)
    return _set_cached(key, result.data if result and result.data else [])


def get_confession_template(template_id: int) -> dict | None:
    def op():
        client = _client()
        return client.table("confession_templates").select(
            "*, confession_categories(name, icon, color)"
        ).eq("id", template_id).single().execute()
    result = _safe_execute(op, fallback=None)
    return result.data if result else None


def create_confession_template(data: dict) -> dict | None:
    for field in ("name", "description", "short_form_text"):
        if field in data and data[field]:
            data[field] = sanitize_html(data[field])
    data["created_by"] = _uid()

    def op():
        client = _client()
        return client.table("confession_templates").insert(data).execute()
    result = _safe_execute(op, fallback=None)
    _clear_cache("confession_templates")
    return result.data[0] if result and result.data else None


def update_confession_template(template_id: int, data: dict) -> dict | None:
    for field in ("name", "description", "short_form_text"):
        if field in data and data[field]:
            data[field] = sanitize_html(data[field])

    def op():
        admin = get_admin_client()
        return admin.table("confession_templates").update(data).eq("id", template_id).execute()
    result = _safe_execute(op, fallback=None)
    _clear_cache("confession_templates")
    return result.data[0] if result and result.data else None


# --- Confession of the Week ---

def get_confession_of_the_week() -> dict | None:
    key = _cache_key("cotw")
    cached = _get_cached(key)
    if cached is not None:
        return cached

    from datetime import date
    today = date.today().isoformat()

    def op():
        client = _client()
        return client.table("confession_of_the_week").select(
            "*, confession_templates(*, confession_categories(name, icon, color))"
        ).eq("is_active", True).lte("start_date", today).gte("end_date", today).order(
            "created_at", desc=True
        ).limit(1).execute()
    result = _safe_execute(op, fallback=None)
    data = result.data[0] if result and result.data else None
    return _set_cached(key, data)


def set_confession_of_the_week(template_id: int, start_date: str, end_date: str,
                                sermon_theme: str = None, sermon_reference: str = None) -> dict | None:
    admin = get_admin_client()
    # Deactivate previous
    try:
        admin.table("confession_of_the_week").update({"is_active": False}).eq("is_active", True).execute()
    except Exception:
        pass

    row = {
        "template_id": template_id,
        "start_date": start_date,
        "end_date": end_date,
        "sermon_theme": sanitize_html(sermon_theme) if sermon_theme else None,
        "sermon_reference": sanitize_html(sermon_reference) if sermon_reference else None,
        "set_by": _uid(),
        "is_active": True,
    }

    def op():
        return admin.table("confession_of_the_week").insert(row).execute()
    result = _safe_execute(op, fallback=None)
    _clear_cache("cotw")
    return result.data[0] if result and result.data else None


# --- Member Confession Plans ---

def get_my_confession_plans(status: str = "active") -> list[dict]:
    key = _cache_key("my_plans", status)
    cached = _get_cached(key)
    if cached is not None:
        return cached

    def op():
        client = _client()
        q = client.table("member_confession_plans").select(
            "*, confession_templates(id, name, short_form_text, confessions, declarations, prayers, scriptures, "
            "time_of_day, maturity_warning, confession_categories(name, icon, color))"
        ).eq("user_id", _uid())
        if status:
            q = q.eq("status", status)
        return q.order("created_at", desc=True).execute()
    result = _safe_execute(op, fallback=None)
    return _set_cached(key, result.data if result and result.data else [])


def add_to_my_plan(template_id: int, plan_type: str = "ongoing", time_slot: str = "anytime",
                   is_new_believer: bool = False) -> dict | None:
    from datetime import date, timedelta
    start = date.today()
    end = None
    if plan_type == "7_days":
        end = (start + timedelta(days=6)).isoformat()
    elif plan_type == "21_days":
        end = (start + timedelta(days=20)).isoformat()

    row = {
        "user_id": _uid(),
        "template_id": template_id,
        "plan_type": plan_type,
        "time_slot": time_slot,
        "start_date": start.isoformat(),
        "end_date": end,
        "status": "active",
        "is_new_believer_track": is_new_believer,
    }

    def op():
        client = _client()
        return client.table("member_confession_plans").insert(row).execute()
    result = _safe_execute(op, fallback=None)
    _clear_cache("my_plans")
    return result.data[0] if result and result.data else None


def update_plan_status(plan_id: int, status: str) -> None:
    def op():
        client = _client()
        return client.table("member_confession_plans").update(
            {"status": status, "updated_at": "now()"}
        ).eq("id", plan_id).eq("user_id", _uid()).execute()
    _safe_execute(op)
    _clear_cache("my_plans")


def assign_confession_to_member(member_id: str, template_id: int, plan_type: str = "21_days",
                                 note: str = None) -> dict | None:
    from datetime import date, timedelta
    start = date.today()
    end = None
    if plan_type == "7_days":
        end = (start + timedelta(days=6)).isoformat()
    elif plan_type == "21_days":
        end = (start + timedelta(days=20)).isoformat()

    row = {
        "user_id": member_id,
        "template_id": template_id,
        "assigned_by": _uid(),
        "assignment_note": sanitize_html(note) if note else None,
        "plan_type": plan_type,
        "start_date": start.isoformat(),
        "end_date": end,
        "status": "active",
    }

    def op():
        admin = get_admin_client()
        return admin.table("member_confession_plans").insert(row).execute()
    result = _safe_execute(op, fallback=None)
    return result.data[0] if result and result.data else None


def get_pastor_assigned_plans(pastor_id: str = None) -> list[dict]:
    pid = pastor_id or _uid()

    def op():
        admin = get_admin_client()
        return admin.table("member_confession_plans").select(
            "*, confession_templates(name, recommended_duration), user:user_id(id)"
        ).eq("assigned_by", pid).eq("status", "active").order("created_at", desc=True).execute()
    result = _safe_execute(op, fallback=None)
    plans = result.data if result and result.data else []

    # Enrich with member names
    if plans:
        member_ids = list({p["user_id"] for p in plans})
        admin = get_admin_client()
        profiles = admin.table("user_profiles").select("user_id, preferred_name, full_name").in_(
            "user_id", member_ids
        ).execute()
        name_map = {p["user_id"]: p.get("preferred_name") or p.get("full_name", "Member")
                    for p in (profiles.data or [])}
        for p in plans:
            p["member_name"] = name_map.get(p["user_id"], "Member")
    return plans


# --- Confession Completions ---

def mark_confession_complete(plan_id: int, time_slot: str = None,
                              reflection_note: str = None) -> dict | None:
    from datetime import date
    row = {
        "user_id": _uid(),
        "plan_id": plan_id,
        "completed_date": date.today().isoformat(),
        "time_slot": time_slot,
        "reflection_note": sanitize_html(reflection_note) if reflection_note else None,
    }

    def op():
        client = _client()
        return client.table("confession_completions").insert(row).execute()
    result = _safe_execute(op, fallback=None)
    _clear_cache("completions")
    _clear_cache("my_plans")
    return result.data[0] if result and result.data else None


def get_today_completions() -> list[dict]:
    from datetime import date
    key = _cache_key("completions", date.today().isoformat())
    cached = _get_cached(key)
    if cached is not None:
        return cached

    def op():
        client = _client()
        return client.table("confession_completions").select("*").eq(
            "user_id", _uid()
        ).eq("completed_date", date.today().isoformat()).execute()
    result = _safe_execute(op, fallback=None)
    return _set_cached(key, result.data if result and result.data else [])


def get_completions_for_plan(plan_id: int) -> list[dict]:
    def op():
        client = _client()
        return client.table("confession_completions").select("completed_date, time_slot").eq(
            "plan_id", plan_id
        ).order("completed_date").execute()
    result = _safe_execute(op, fallback=None)
    return result.data if result and result.data else []


def get_member_completion_stats(member_id: str, plan_id: int) -> dict:
    """Get completion stats for a pastor-prescribed plan (pastor view)."""
    def op():
        admin = get_admin_client()
        return admin.table("confession_completions").select(
            "completed_date"
        ).eq("user_id", member_id).eq("plan_id", plan_id).execute()
    result = _safe_execute(op, fallback=None)
    completions = result.data if result and result.data else []
    dates = [c["completed_date"] for c in completions]
    return {
        "total_days_completed": len(set(dates)),
        "last_completed": max(dates) if dates else None,
    }


# --- New Believer Track ---

def get_new_believer_track() -> list[dict]:
    key = _cache_key("nb_track")
    cached = _get_cached(key)
    if cached is not None:
        return cached

    def op():
        client = _client()
        return client.table("new_believer_track").select(
            "*, confession_templates(id, name, description, short_form_text, confessions, declarations, "
            "prayers, scriptures)"
        ).eq("is_active", True).order("day_number").execute()
    result = _safe_execute(op, fallback=None)
    return _set_cached(key, result.data if result and result.data else [])


def seed_new_believer_plan(user_id: str) -> None:
    """Auto-assign 7-day New Believer Track to a new user. Uses admin client."""
    from datetime import date, timedelta
    track = get_new_believer_track()
    if not track:
        return

    admin = get_admin_client()
    start = date.today()
    end = (start + timedelta(days=6)).isoformat()

    for item in track:
        try:
            admin.table("member_confession_plans").insert({
                "user_id": user_id,
                "template_id": item["template_id"],
                "plan_type": "7_days",
                "time_slot": "morning",
                "start_date": start.isoformat(),
                "end_date": end,
                "status": "active",
                "is_new_believer_track": True,
            }).execute()
        except Exception:
            pass


def get_confession_count_today() -> int:
    """Quick count of today's completions for dashboard card."""
    completions = get_today_completions()
    return len(completions)


# ─── System Settings ─────────────────────────────────────────────────────────

def get_system_setting(key: str) -> str | None:
    admin = get_admin_client()
    result = admin.table("system_settings").select("value").eq("key", key).execute()
    return result.data[0]["value"] if result.data else None


def set_system_setting(key: str, value: str) -> None:
    admin = get_admin_client()
    admin.table("system_settings").upsert(
        {"key": key, "value": value, "updated_at": "now()"},
        on_conflict="key"
    ).execute()


# ─── Care Tasks ──────────────────────────────────────────────────────────────

def get_inactive_members(pastor_id: str, threshold_days: int = 3) -> list[dict]:
    admin = get_admin_client()
    result = admin.table("inactive_members_view") \
        .select("*") \
        .eq("pastor_id", pastor_id) \
        .gte("days_since_last_entry", threshold_days) \
        .execute()
    return result.data or []


def create_care_task(pastor_id: str, member_id: str, care_type: str,
                     note: str, due_date: str = None) -> dict:
    admin = get_admin_client()
    result = admin.table("care_tasks").insert({
        "pastor_id": pastor_id,
        "member_id": member_id,
        "care_type": care_type,
        "note": sanitize_html(note) if note else None,
        "due_date": due_date,
        "status": "open",
    }).execute()
    log_audit("care_task.created", target_type="care_tasks",
              target_id=str(result.data[0]["id"]) if result.data else None,
              details={"member_id": member_id, "care_type": care_type})
    return result.data[0] if result.data else {}


def get_care_tasks(pastor_id: str, status: str = None) -> list[dict]:
    admin = get_admin_client()
    q = admin.table("care_tasks").select("*").eq("pastor_id", pastor_id)
    if status:
        q = q.eq("status", status)
    result = q.order("due_date").order("created_at", desc=True).execute()
    tasks = result.data or []

    # Enrich with member names
    if tasks:
        member_ids = list({t["member_id"] for t in tasks})
        profiles = admin.table("user_profiles") \
            .select("user_id") \
            .in_("user_id", member_ids) \
            .execute()
        name_map = {}
        for p in (profiles.data or []):
            try:
                u = admin.auth.admin.get_user_by_id(p["user_id"]).user
                name_map[p["user_id"]] = (u.user_metadata or {}).get("preferred_name", u.email)
            except Exception:
                name_map[p["user_id"]] = "Member"
        for t in tasks:
            t["member_name"] = name_map.get(t["member_id"], "Member")
    return tasks


def complete_care_task(task_id: int) -> None:
    from datetime import datetime
    admin = get_admin_client()
    admin.table("care_tasks").update({
        "status": "done",
        "completed_at": datetime.utcnow().isoformat(),
    }).eq("id", task_id).execute()
    log_audit("care_task.completed", target_type="care_tasks", target_id=str(task_id))


def get_bishop_care_overview(bishop_id: str) -> dict:
    admin = get_admin_client()
    pastor_ids_result = admin.table("user_profiles") \
        .select("user_id") \
        .eq("bishop_id", bishop_id) \
        .eq("role", "pastor") \
        .execute()
    pastor_ids = [p["user_id"] for p in (pastor_ids_result.data or [])]
    if not pastor_ids:
        return {"open_tasks": 0, "inactive_7d": 0}

    open_tasks = admin.table("care_tasks") \
        .select("id", count="exact") \
        .in_("pastor_id", pastor_ids) \
        .eq("status", "open") \
        .execute()

    inactive_7d = admin.table("inactive_members_view") \
        .select("user_id", count="exact") \
        .in_("pastor_id", pastor_ids) \
        .gte("days_since_last_entry", 7) \
        .execute()

    return {
        "open_tasks": open_tasks.count or 0,
        "inactive_7d": inactive_7d.count or 0,
    }


# ─── Reading Plans ────────────────────────────────────────────────────────────

def get_reading_plans() -> list[dict]:
    key = _cache_key("reading_plans")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("reading_plans").select("*").order("id").execute()
    return _set_cached(key, result.data or [])


def get_plan_days(plan_id: int) -> list[dict]:
    key = _cache_key("plan_days", plan_id)
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("reading_plan_days") \
        .select("*") \
        .eq("plan_id", plan_id) \
        .order("day_number") \
        .execute()
    return _set_cached(key, result.data or [])


def get_member_active_plan(user_id: str = None) -> dict | None:
    uid = user_id or _uid()
    key = _cache_key("active_plan", uid)
    cached = _get_cached(key)
    if cached is not None:
        return cached if cached != "__none__" else None
    admin = get_admin_client()
    result = admin.table("reading_plan_progress") \
        .select("*, reading_plans(name, description, total_days)") \
        .eq("user_id", uid) \
        .eq("status", "active") \
        .order("enrolled_at", desc=True) \
        .limit(1) \
        .execute()
    value = result.data[0] if result.data else None
    _set_cached(key, value if value else "__none__")
    return value


def get_member_completed_plan_ids(user_id: str = None) -> set[int]:
    uid = user_id or _uid()
    admin = get_admin_client()
    result = admin.table("reading_plan_progress") \
        .select("plan_id") \
        .eq("user_id", uid) \
        .eq("status", "completed") \
        .execute()
    return {r["plan_id"] for r in (result.data or [])}


def abandon_active_plan(user_id: str, except_plan_id: int = None) -> None:
    """Mark all active plans for user as abandoned (except the given plan_id)."""
    admin = get_admin_client()
    query = admin.table("reading_plan_progress") \
        .update({"status": "abandoned"}) \
        .eq("user_id", user_id) \
        .eq("status", "active")
    if except_plan_id:
        query = query.neq("plan_id", except_plan_id)
    query.execute()
    _clear_cache("active_plan")


def enroll_in_plan(user_id: str, plan_id: int, assigned_by: str = None) -> dict | None:
    admin = get_admin_client()
    # Abandon any other currently active plan first
    abandon_active_plan(user_id, except_plan_id=plan_id)
    row = {
        "user_id": user_id,
        "plan_id": plan_id,
        "current_day": 1,
        "status": "active",
        "completed_at": None,
        "last_completed_date": None,
        "enrolled_at": "now()",
    }
    if assigned_by:
        row["assigned_by"] = assigned_by
    result = admin.table("reading_plan_progress").upsert(
        row, on_conflict="user_id,plan_id"
    ).execute()
    _clear_cache("active_plan")
    log_audit("reading_plan_self_enrolled", target_type="reading_plan_progress",
              target_id=str(plan_id), details={"plan_id": plan_id})
    return result.data[0] if result.data else None


def mark_plan_day_complete(progress_id: int, total_days: int) -> dict:
    from datetime import date
    admin = get_admin_client()
    prog = admin.table("reading_plan_progress") \
        .select("current_day") \
        .eq("id", progress_id) \
        .single() \
        .execute()
    if not prog.data:
        return {}
    next_day = prog.data["current_day"] + 1
    updates: dict = {
        "current_day": next_day,
        "last_completed_date": date.today().isoformat(),
    }
    if next_day > total_days:
        from datetime import datetime
        updates["completed_at"] = datetime.utcnow().isoformat()
        log_audit("reading_plan_completed", target_type="reading_plan_progress",
                  target_id=str(progress_id))
    result = admin.table("reading_plan_progress").update(updates).eq("id", progress_id).execute()
    _clear_cache("active_plan")
    return result.data[0] if result.data else {}


def get_members_plan_progress(pastor_id: str) -> list[dict]:
    admin = get_admin_client()
    members_result = admin.table("user_profiles") \
        .select("user_id") \
        .eq("pastor_id", pastor_id) \
        .execute()
    member_ids = [m["user_id"] for m in (members_result.data or [])]
    if not member_ids:
        return []
    result = admin.table("reading_plan_progress") \
        .select("*, reading_plans(name, total_days)") \
        .in_("user_id", member_ids) \
        .is_("completed_at", "null") \
        .execute()
    rows = result.data or []
    # Enrich with member names
    for r in rows:
        try:
            u = admin.auth.admin.get_user_by_id(r["user_id"]).user
            r["member_name"] = (u.user_metadata or {}).get("preferred_name", u.email)
        except Exception:
            r["member_name"] = "Member"
    return rows


# ─── Bible Bookmarks & Highlights ────────────────────────────────────────────

def get_bookmarks_for_chapter(book: str, chapter: int) -> list[dict]:
    uid = _uid()
    key = _cache_key("bookmarks_chapter", book, chapter)
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("bible_bookmarks") \
        .select("*") \
        .eq("user_id", uid) \
        .eq("book", book) \
        .eq("chapter", chapter) \
        .execute()
    return _set_cached(key, result.data or [])


def get_all_bookmarks() -> list[dict]:
    key = _cache_key("all_bookmarks")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("bible_bookmarks") \
        .select("*") \
        .eq("user_id", _uid()) \
        .order("created_at", desc=True) \
        .execute()
    return _set_cached(key, result.data or [])


def toggle_bookmark(book: str, chapter: int, verse_number: int) -> bool:
    """Add bookmark if absent, remove if present. Returns True if now bookmarked."""
    uid = _uid()
    client = _client()
    existing = client.table("bible_bookmarks") \
        .select("id") \
        .eq("user_id", uid) \
        .eq("book", book) \
        .eq("chapter", chapter) \
        .eq("verse_number", verse_number) \
        .execute()
    _clear_cache("bookmarks_chapter")
    _clear_cache("all_bookmarks")
    _clear_cache("bookmark_count")
    if existing.data:
        client.table("bible_bookmarks").delete().eq("id", existing.data[0]["id"]).execute()
        # Also remove any highlight for this verse
        client.table("bible_highlights") \
            .delete() \
            .eq("user_id", uid) \
            .eq("book", book) \
            .eq("chapter", chapter) \
            .eq("verse_number", verse_number) \
            .execute()
        _clear_cache("highlights_chapter")
        return False
    else:
        client.table("bible_bookmarks").insert({
            "user_id": uid,
            "book": book,
            "chapter": chapter,
            "verse_number": verse_number,
            "note": "",
        }).execute()
        return True


def update_bookmark_note(book: str, chapter: int, verse_number: int, note: str) -> None:
    client = _client()
    client.table("bible_bookmarks") \
        .update({"note": sanitize_html(note)}) \
        .eq("user_id", _uid()) \
        .eq("book", book) \
        .eq("chapter", chapter) \
        .eq("verse_number", verse_number) \
        .execute()
    _clear_cache("all_bookmarks")
    _clear_cache("bookmarks_chapter")


def delete_bookmark(bookmark_id: int) -> None:
    client = _client()
    # Get the bookmark to also remove highlight
    bm = client.table("bible_bookmarks").select("book,chapter,verse_number") \
        .eq("id", bookmark_id).eq("user_id", _uid()).execute()
    client.table("bible_bookmarks").delete().eq("id", bookmark_id).eq("user_id", _uid()).execute()
    if bm.data:
        b = bm.data[0]
        client.table("bible_highlights").delete() \
            .eq("user_id", _uid()) \
            .eq("book", b["book"]) \
            .eq("chapter", b["chapter"]) \
            .eq("verse_number", b["verse_number"]) \
            .execute()
        _clear_cache("highlights_chapter")
    _clear_cache("all_bookmarks")
    _clear_cache("bookmarks_chapter")
    _clear_cache("bookmark_count")


def get_highlights_for_chapter(book: str, chapter: int) -> list[dict]:
    key = _cache_key("highlights_chapter", book, chapter)
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("bible_highlights") \
        .select("*") \
        .eq("user_id", _uid()) \
        .eq("book", book) \
        .eq("chapter", chapter) \
        .execute()
    return _set_cached(key, result.data or [])


def cycle_highlight(book: str, chapter: int, verse_number: int) -> str | None:
    """Cycle highlight: none → yellow → green → none. Returns new color or None."""
    uid = _uid()
    client = _client()
    existing = client.table("bible_highlights") \
        .select("id, color") \
        .eq("user_id", uid) \
        .eq("book", book) \
        .eq("chapter", chapter) \
        .eq("verse_number", verse_number) \
        .execute()
    _clear_cache("highlights_chapter")
    _clear_cache("highlight_count")
    if not existing.data:
        client.table("bible_highlights").insert({
            "user_id": uid, "book": book, "chapter": chapter,
            "verse_number": verse_number, "color": "yellow",
        }).execute()
        return "yellow"
    current = existing.data[0]["color"]
    row_id = existing.data[0]["id"]
    if current == "yellow":
        client.table("bible_highlights").update({"color": "green"}).eq("id", row_id).execute()
        return "green"
    # green → remove
    client.table("bible_highlights").delete().eq("id", row_id).execute()
    return None


def get_bookmark_count() -> int:
    key = _cache_key("bookmark_count")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("bible_bookmarks").select("id", count="exact").eq("user_id", _uid()).execute()
    return _set_cached(key, result.count or 0)


def get_highlight_count() -> int:
    key = _cache_key("highlight_count")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    client = _client()
    result = client.table("bible_highlights").select("id", count="exact").eq("user_id", _uid()).execute()
    return _set_cached(key, result.count or 0)


def get_confession_count_this_week() -> int:
    """Count distinct confession days completed in the current Mon–Sat window."""
    from datetime import date as _date
    today = _date.today()
    monday = (today - __import__("datetime").timedelta(days=today.weekday())).isoformat()
    saturday = (__import__("datetime").date.fromisoformat(monday) + __import__("datetime").timedelta(days=5)).isoformat()

    def op():
        client = _client()
        return client.table("confession_completions") \
            .select("completed_date") \
            .gte("completed_date", monday) \
            .lte("completed_date", saturday) \
            .execute()
    result = _safe_execute(op, fallback=None)
    rows = result.data if result else []
    return len({r["completed_date"] for r in rows})


# ============================================================
# Sprint 8 — Prayer Requests
# ============================================================

def get_prayer_requests() -> list[dict]:
    uid = _uid()
    result = _safe_execute(
        lambda: _client().table("prayer_requests")
            .select("*, prayer_request_prays(user_id), user_profiles(display_name)")
            .eq("status", "active")
            .order("created_at", desc=True)
            .execute(),
        fallback=None,
    )
    rows = result.data if result else []
    for r in rows:
        prays = r.pop("prayer_request_prays", []) or []
        profile = r.pop("user_profiles", {}) or {}
        r["display_name"] = profile.get("display_name", "Member")
        r["pray_count"] = len(prays)
        r["has_prayed"] = any(p["user_id"] == uid for p in prays)
    return rows


def get_all_prayer_requests_for_moderation() -> list[dict]:
    """Admin/pastor: all requests including hidden/answered."""
    admin = get_admin_client()
    result = admin.table("prayer_requests") \
        .select("*, user_profiles(display_name)") \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


def create_prayer_request(title: str, body: str, is_anonymous: bool) -> None:
    uid = _uid()
    _safe_execute(
        lambda: _client().table("prayer_requests").insert({
            "user_id": uid,
            "title": sanitize_html(title),
            "body": sanitize_html(body) if body else None,
            "is_anonymous": is_anonymous,
        }).execute(),
        fallback=None,
    )


def toggle_pray_for(request_id: str) -> bool:
    """Returns True if now praying, False if un-prayed."""
    uid = _uid()
    existing = _safe_execute(
        lambda: _client().table("prayer_request_prays")
            .select("id")
            .eq("request_id", request_id)
            .eq("user_id", uid)
            .execute(),
        fallback=None,
    )
    if existing and existing.data:
        _safe_execute(
            lambda: _client().table("prayer_request_prays")
                .delete()
                .eq("request_id", request_id)
                .eq("user_id", uid)
                .execute(),
            fallback=None,
        )
        return False
    else:
        _safe_execute(
            lambda: _client().table("prayer_request_prays")
                .insert({"request_id": request_id, "user_id": uid})
                .execute(),
            fallback=None,
        )
        return True


def moderate_prayer_request(request_id: str, new_status: str) -> None:
    """Admin/pastor: hide or mark answered."""
    get_admin_client().table("prayer_requests") \
        .update({"status": new_status}) \
        .eq("id", request_id) \
        .execute()


def mark_prayer_answered(request_id: str) -> None:
    uid = _uid()
    _safe_execute(
        lambda: _client().table("prayer_requests")
            .update({"status": "answered"})
            .eq("id", request_id)
            .eq("user_id", uid)
            .execute(),
        fallback=None,
    )


# ============================================================
# Sprint 8 — Notifications
# ============================================================

def get_unread_notification_count() -> int:
    key = _cache_key("notif_unread_count")
    cached = _get_cached(key)
    if cached is not None:
        return cached
    result = _safe_execute(
        lambda: _client().table("notifications")
            .select("id", count="exact")
            .eq("user_id", _uid())
            .eq("is_read", False)
            .execute(),
        fallback=None,
    )
    return _set_cached(key, result.count if result else 0)


def get_notifications(limit: int = 30) -> list[dict]:
    result = _safe_execute(
        lambda: _client().table("notifications")
            .select("*")
            .eq("user_id", _uid())
            .order("created_at", desc=True)
            .limit(limit)
            .execute(),
        fallback=None,
    )
    return result.data if result else []


def mark_all_notifications_read() -> None:
    _safe_execute(
        lambda: _client().table("notifications")
            .update({"is_read": True})
            .eq("user_id", _uid())
            .eq("is_read", False)
            .execute(),
        fallback=None,
    )
    _clear_cache("notif_unread_count")


def create_notification_for_user(user_id: str, notif_type: str, title: str, body: str = None) -> None:
    """Service-role: push a notification to any user."""
    try:
        get_admin_client().table("notifications").insert({
            "user_id": user_id,
            "type": notif_type,
            "title": sanitize_html(title),
            "body": sanitize_html(body) if body else None,
        }).execute()
    except Exception:
        pass


# ============================================================
# Sprint 8 — Check-in Requests
# ============================================================

def create_checkin_request(message: str = None) -> None:
    uid = _uid()
    profile = _safe_execute(
        lambda: _client().table("user_profiles")
            .select("pastor_id")
            .eq("user_id", uid)
            .execute(),
        fallback=None,
    )
    pastor_id = None
    if profile and profile.data:
        pastor_id = profile.data[0].get("pastor_id")

    _safe_execute(
        lambda: _client().table("checkin_requests").insert({
            "member_id": uid,
            "pastor_id": pastor_id,
            "message": sanitize_html(message) if message else None,
        }).execute(),
        fallback=None,
    )
    if pastor_id:
        create_notification_for_user(
            pastor_id, "checkin_request",
            "Check-in Requested",
            f"A member has requested a pastoral check-in.",
        )


def get_my_checkin_requests() -> list[dict]:
    result = _safe_execute(
        lambda: _client().table("checkin_requests")
            .select("*")
            .eq("member_id", _uid())
            .order("created_at", desc=True)
            .execute(),
        fallback=None,
    )
    return result.data if result else []


def get_pastor_checkin_requests(pastor_id: str = None) -> list[dict]:
    uid = pastor_id or _uid()
    admin = get_admin_client()
    result = admin.table("checkin_requests") \
        .select("*, user_profiles!checkin_requests_member_id_fkey(display_name)") \
        .eq("pastor_id", uid) \
        .order("created_at", desc=True) \
        .execute()
    return result.data or []


def acknowledge_checkin_request(request_id: int) -> None:
    get_admin_client().table("checkin_requests") \
        .update({"status": "acknowledged"}) \
        .eq("id", request_id) \
        .execute()


# ============================================================
# Sprint 8 — Analytics Export
# ============================================================

def get_member_activity_export(start_date: str, end_date: str) -> list[dict]:
    admin = get_admin_client()
    entries = admin.table("daily_entries") \
        .select("user_id, date, prayer_minutes, chapters_display, sermons_count") \
        .gte("date", start_date) \
        .lte("date", end_date) \
        .order("date", desc=False) \
        .execute()
    rows = entries.data or []

    profiles = admin.table("user_profiles") \
        .select("user_id, display_name, role") \
        .execute()
    profile_map = {p["user_id"]: p for p in (profiles.data or [])}

    for r in rows:
        p = profile_map.get(r["user_id"], {})
        r["display_name"] = p.get("display_name", r["user_id"])
        r["role"] = p.get("role", "")
    return rows


def get_reading_completions_export() -> list[dict]:
    admin = get_admin_client()
    result = admin.table("reading_plan_progress") \
        .select("user_id, plan_id, current_day, status, enrolled_at, completed_at, reading_plans(name, total_days)") \
        .neq("status", "abandoned") \
        .order("enrolled_at", desc=True) \
        .execute()
    rows = result.data or []

    profiles = admin.table("user_profiles") \
        .select("user_id, display_name") \
        .execute()
    profile_map = {p["user_id"]: p["display_name"] for p in (profiles.data or [])}

    for r in rows:
        r["display_name"] = profile_map.get(r["user_id"], r["user_id"])
        plan = r.pop("reading_plans", {}) or {}
        r["plan_name"] = plan.get("name", "")
        r["total_days"] = plan.get("total_days", 0)
    return rows


def get_prayer_hours_export(start_date: str, end_date: str) -> list[dict]:
    admin = get_admin_client()
    entries = admin.table("daily_entries") \
        .select("user_id, prayer_minutes") \
        .gte("date", start_date) \
        .lte("date", end_date) \
        .execute()
    rows = entries.data or []

    totals: dict[str, int] = {}
    for r in rows:
        totals[r["user_id"]] = totals.get(r["user_id"], 0) + (r.get("prayer_minutes") or 0)

    profiles = admin.table("user_profiles") \
        .select("user_id, display_name, role") \
        .execute()
    profile_map = {p["user_id"]: p for p in (profiles.data or [])}

    result = []
    for uid, mins in sorted(totals.items(), key=lambda x: -x[1]):
        p = profile_map.get(uid, {})
        result.append({
            "user_id": uid,
            "display_name": p.get("display_name", uid),
            "role": p.get("role", ""),
            "total_minutes": mins,
            "total_hours": round(mins / 60, 2),
        })
    return result