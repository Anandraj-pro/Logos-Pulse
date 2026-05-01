"""Weekly digest data builder for Logos Pulse."""
from datetime import date, timedelta
from modules.supabase_client import get_admin_client
from modules.utils import calculate_streaks


def _week_bounds() -> tuple[str, str]:
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    saturday = monday + timedelta(days=5)
    return monday.isoformat(), saturday.isoformat()


def build_member_digest(user_id: str, display_name: str, email: str) -> dict:
    """Gather one Prayer Warrior's weekly stats. Uses admin client."""
    admin = get_admin_client()
    monday, saturday = _week_bounds()

    # Streak
    all_dates_resp = admin.table("daily_entries") \
        .select("date") \
        .eq("user_id", user_id) \
        .order("date") \
        .execute()
    all_dates = [r["date"] for r in (all_dates_resp.data or [])]
    current_streak, _ = calculate_streaks(all_dates)

    # This-week entries
    week_resp = admin.table("daily_entries") \
        .select("date, chapters_read") \
        .eq("user_id", user_id) \
        .gte("date", monday) \
        .lte("date", saturday) \
        .execute()
    week_entries = week_resp.data or []
    days_logged = len(week_entries)

    import json as _json
    chapters_read = 0
    for e in week_entries:
        raw = e.get("chapters_read")
        if raw:
            try:
                ch = _json.loads(raw) if isinstance(raw, str) else raw
                chapters_read += len(ch) if isinstance(ch, list) else 0
            except Exception:
                pass

    # This-week confessions
    conf_resp = admin.table("confession_completions") \
        .select("completed_date") \
        .eq("user_id", user_id) \
        .gte("completed_date", monday) \
        .lte("completed_date", saturday) \
        .execute()
    confession_days = len({r["completed_date"] for r in (conf_resp.data or [])})

    return {
        "user_id": user_id,
        "display_name": display_name,
        "email": email,
        "current_streak": current_streak,
        "days_logged": days_logged,
        "chapters_read": chapters_read,
        "confession_days": confession_days,
        "week_start": monday,
        "week_end": saturday,
    }


def build_all_digests(pastor_id: str = None) -> list[dict]:
    """Build digests for all Prayer Warriors (or those under a specific pastor)."""
    admin = get_admin_client()

    query = admin.table("user_profiles").select("user_id, pastor_id").eq("role", "prayer_warrior")
    if pastor_id:
        query = query.eq("pastor_id", pastor_id)
    profiles = query.execute().data or []

    digests = []
    for p in profiles:
        try:
            u = admin.auth.admin.get_user_by_id(p["user_id"]).user
            meta = u.user_metadata or {}
            name = meta.get("preferred_name") or meta.get("first_name") or u.email
            digests.append(build_member_digest(p["user_id"], name, u.email))
        except Exception:
            pass
    return digests


def format_digest_email(d: dict) -> tuple[str, str]:
    """Return (subject, plain-text body) for one member digest."""
    week_label = f"{d['week_start']} to {d['week_end']}"
    streak_note = (
        f"🔥 You're on a {d['current_streak']}-day streak — keep it going!"
        if d["current_streak"] >= 3
        else f"Current streak: {d['current_streak']} day(s)"
    )
    subject = f"Logos Pulse — Your weekly summary ({d['week_start']})"
    body = f"""Hello {d['display_name']},

Here is your spiritual disciplines summary for the week of {week_label}.

📅 Days logged:       {d['days_logged']} / 6
📖 Chapters read:    {d['chapters_read']}
✝️  Confession days:  {d['confession_days']}
{streak_note}

Keep pressing forward in your walk with God.

— Logos Pulse
"""
    return subject, body
