import html as _html
import streamlit as st
from datetime import date, timedelta
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id, get_current_role
from modules.rbac import get_members_for_pastor
from modules.supabase_client import get_admin_client
from modules.bible_data import get_book_names, get_chapter_count
from modules.chapter_splitter import split_chapters
from modules.utils import get_next_monday
from modules.db import (
    create_group_assignment, get_group_assignments,
    get_inactive_members, create_care_task, get_care_tasks, complete_care_task,
    get_reading_plans, enroll_in_plan, get_members_plan_progress,
)

require_role(["admin", "bishop", "pastor"])

inject_styles()

role = get_current_role()
my_id = get_current_user_id()

# If admin or bishop, let them pick which pastor to view
if role in ("admin", "bishop"):
    from modules.rbac import get_pastors_list, get_pastors_for_bishop

    if role == "admin":
        pastors = get_pastors_list()
    else:
        pastors = get_pastors_for_bishop(my_id)

    if not pastors:
        page_header("\U0001f9d1\u200d\U0001f91d\u200d\U0001f9d1", "Pastor Dashboard", "No pastors found")
        st.stop()

    pastor_options = {p["display_name"] + f" ({p['email']})": p["user_id"] for p in pastors}
    selected = st.selectbox("Select Pastor", options=list(pastor_options.keys()))
    viewing_pastor_id = pastor_options[selected]
    pastor_name = selected.split(" (")[0]
else:
    viewing_pastor_id = my_id
    pastor_name = st.session_state.get("preferred_name", "Pastor")

page_header("\U0001f9d1\u200d\U0001f91d\u200d\U0001f9d1", f"{pastor_name}'s Group", "Member progress and group assignments")

# Get members
members = get_members_for_pastor(viewing_pastor_id)

if not members:
    empty_state("\U0001f465", "No members assigned yet", "Prayer Warriors will appear here once assigned to this pastor")
    st.stop()

# ==================== TABS ====================
tab_members, tab_followup, tab_leaderboard, tab_prayers, tab_assign, tab_history, tab_confessions, tab_care, tab_plans, tab_digest, tab_wall = st.tabs([
    "\U0001f465 Members", "\U0001f514 Follow-Up", "\U0001f3c6 Leaderboard", "\U0001f64f Shared Prayers",
    "\U0001f4d6 Create Assignment", "\U0001f4c1 Assignment History", "\u2720\ufe0f Confessions",
    "\U0001f6a8 Care Alerts", "\U0001f4da Reading Plans", "\U0001f4f2 Group Report", "\U0001f64c Prayer Wall"
])

# ==================== MEMBERS TAB ====================
with tab_members:
    admin = get_admin_client()
    today_str = date.today().isoformat()
    member_ids = [m["user_id"] for m in members]

    today_entries = admin.table("daily_entries") \
        .select("user_id, prayer_minutes, chapters_display, report_copied") \
        .eq("date", today_str) \
        .in_("user_id", member_ids) \
        .execute()

    logged_user_ids = {e["user_id"] for e in (today_entries.data or [])}
    entry_map = {e["user_id"]: e for e in (today_entries.data or [])}

    logged_count = len(logged_user_ids)
    total_count = len(members)
    pct = int(logged_count / total_count * 100) if total_count > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:#5B4FC4;">{total_count}</div>
            <div class="stat-label">Total Members</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        color = "#3A8F5C" if pct >= 70 else "#D4853A" if pct >= 40 else "#C44B5B"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:{color};">{logged_count}/{total_count}</div>
            <div class="stat-label">Logged Today</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        reports_copied = sum(1 for e in (today_entries.data or []) if e.get("report_copied"))
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="color:#D4853A;">{reports_copied}</div>
            <div class="stat-label">Reports Sent</div>
        </div>
        """, unsafe_allow_html=True)

    spacer()
    section_label("Members")

    # Search + filter row
    _search_col, _filter_col = st.columns([2, 2])
    with _search_col:
        _member_search = st.text_input("Search", placeholder="Search by name…", label_visibility="collapsed", key="pd_member_search")
    with _filter_col:
        view_mode = st.segmented_control("Filter", ["All", "Logged Today", "Not Logged", "Inactive 7d"], default="All", label_visibility="collapsed", key="pd_view_mode")

    # Inactive 7-day set (for filter)
    if view_mode == "Inactive 7d":
        from modules.db import get_inactive_members as _get_inactive
        _inactive_ids = {m["user_id"] for m in _get_inactive(viewing_pastor_id, threshold_days=7)}
    else:
        _inactive_ids = set()

    for member in members:
        uid = member["user_id"]
        logged = uid in logged_user_ids
        entry = entry_map.get(uid)

        if _member_search and _member_search.lower() not in member["display_name"].lower():
            continue
        if view_mode == "Logged Today" and not logged:
            continue
        if view_mode == "Not Logged" and logged:
            continue
        if view_mode == "Inactive 7d" and uid not in _inactive_ids:
            continue

        status_icon = "\u2705" if logged else "\u274c"
        status_color = "#3A8F5C" if logged else "#C44B5B"
        status_bg = "#E8F5E9" if logged else "#FFEBEE"

        details = ""
        if entry:
            details = f"Prayer: {entry.get('prayer_minutes', 0)} min | Reading: {entry.get('chapters_display', 'N/A')}"
            if entry.get("report_copied"):
                details += " | Report sent"

        card_id_text = f" | Card: {member['membership_card_id']}" if member.get("membership_card_id") else ""

        st.markdown(f"""
        <div class="entry-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">
                        {status_icon} {member['display_name']}
                    </span>
                    <span style="font-size:12px; color:#9E96AB; margin-left:8px;">
                        {member['email']}{card_id_text}
                    </span>
                </div>
                <span style="background:{status_bg}; color:{status_color}; padding:2px 10px;
                             border-radius:10px; font-size:11px; font-weight:600;">
                    {"Logged" if logged else "Pending"}
                </span>
            </div>
            {"<div style='font-size:13px; color:#6B6580; margin-top:6px;'>" + details + "</div>" if details else ""}
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"View {member['display_name']}", key=f"view_{uid}", use_container_width=True):
            st.session_state["viewing_member_id"] = uid
            st.rerun()

# ==================== FOLLOW-UP TAB ====================
with tab_followup:
    from modules.utils import calculate_streaks

    section_label("Members Needing Follow-Up")
    st.caption("Members who haven't logged in 3+ days")

    admin_fu = get_admin_client()
    needs_followup = []

    for member in members:
        m_entries = admin_fu.table("daily_entries") \
            .select("date") \
            .eq("user_id", member["user_id"]) \
            .order("date", desc=True) \
            .limit(1) \
            .execute()

        if m_entries.data:
            last_date = m_entries.data[0]["date"]
            days_since = (date.today() - date.fromisoformat(last_date)).days
        else:
            days_since = 999  # Never logged

        if days_since >= 3:
            needs_followup.append({**member, "days_since": days_since, "last_date": last_date if m_entries.data else "Never"})

    needs_followup.sort(key=lambda x: x["days_since"], reverse=True)

    if not needs_followup:
        st.markdown("""
        <div class="goal-banner" style="text-align:center;">
            \u2705 All members are active! No follow-up needed.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"{len(needs_followup)} member(s) need follow-up")

        for m in needs_followup:
            urgency_color = "#C44B5B" if m["days_since"] >= 7 else "#D4853A"
            st.markdown(f"""
            <div class="entry-card" style="border-left:3px solid {urgency_color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">
                        {m['display_name']}
                    </span>
                    <span style="background:#FFEBEE; color:{urgency_color}; padding:2px 10px;
                                 border-radius:10px; font-size:11px; font-weight:600;">
                        {m['days_since']} days inactive
                    </span>
                </div>
                <div style="font-size:12px; color:#9E96AB; margin-top:4px;">
                    Last logged: {m['last_date']} | {m['email']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_note, col_log = st.columns([3, 1])
            with col_note:
                fu_note = st.text_input("Follow-up note", placeholder="e.g., Called and encouraged",
                                        key=f"fu_{m['user_id']}", label_visibility="collapsed")
            with col_log:
                if st.button("Log", key=f"fu_log_{m['user_id']}", use_container_width=True):
                    if fu_note.strip():
                        admin_fu.table("follow_up_log").insert({
                            "pastor_id": viewing_pastor_id,
                            "member_id": m["user_id"],
                            "action": "follow_up",
                            "notes": fu_note.strip(),
                        }).execute()
                        st.success(f"Follow-up logged for {m['display_name']}")
                        st.rerun()

    # Recent follow-up history
    spacer()
    section_label("Recent Follow-Up Log")
    fu_log = admin_fu.table("follow_up_log") \
        .select("*") \
        .eq("pastor_id", viewing_pastor_id) \
        .order("created_at", desc=True) \
        .limit(10) \
        .execute()

    if fu_log.data:
        for log in fu_log.data:
            try:
                fu_user = admin_fu.auth.admin.get_user_by_id(log["member_id"]).user
                fu_name = (fu_user.user_metadata or {}).get("preferred_name", fu_user.email)
            except Exception:
                fu_name = "Member"
            log_date = (log.get("created_at") or "")[:10]
            st.markdown(f"""
            <div style="font-size:13px; color:#6B6580; padding:6px 0; border-bottom:1px solid #EDE8F5;">
                <b>{fu_name}</b> \u2014 {log.get('notes', '')} <span style="color:#9E96AB; font-size:11px;">({log_date})</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No follow-up logs yet")

# ==================== LEADERBOARD TAB ====================
with tab_leaderboard:
    from modules.utils import calculate_streaks

    admin = get_admin_client()
    member_streaks = []

    for member in members:
        # Get all entry dates for this member
        member_entries = admin.table("daily_entries") \
            .select("date") \
            .eq("user_id", member["user_id"]) \
            .order("date") \
            .execute()
        member_dates = [e["date"] for e in (member_entries.data or [])]
        streak, best = calculate_streaks(member_dates)
        member_streaks.append({
            **member,
            "current_streak": streak,
            "best_streak": best,
            "total_entries": len(member_dates),
        })

    # Sort by current streak descending
    member_streaks.sort(key=lambda x: x["current_streak"], reverse=True)

    section_label("Streak Leaderboard")

    for rank, ms in enumerate(member_streaks, 1):
        medal = "\U0001f947" if rank == 1 else "\U0001f948" if rank == 2 else "\U0001f949" if rank == 3 else f"#{rank}"
        streak = ms["current_streak"]
        streak_color = "#3A8F5C" if streak >= 7 else "#D4853A" if streak >= 3 else "#C44B5B" if streak == 0 else "#5B4FC4"
        streak_emoji = "\U0001f525" if streak >= 7 else "\u2b50" if streak >= 3 else ""

        st.markdown(f"""
        <div class="entry-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:20px; min-width:32px; text-align:center;">{medal}</span>
                    <div>
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">
                            {ms['display_name']}
                        </span>
                        <div style="font-size:12px; color:#9E96AB;">
                            Best: {ms['best_streak']} days | Total: {ms['total_entries']} entries
                        </div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:{streak_color};">
                        {streak}
                    </span>
                    <span style="font-size:14px;"> {streak_emoji}</span>
                    <div style="font-size:10px; color:#9E96AB; text-transform:uppercase; letter-spacing:1px;">day streak</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== SHARED PRAYERS TAB ====================
with tab_prayers:
    shared_prayers = db.get_shared_prayers_for_pastor(viewing_pastor_id)

    if not shared_prayers:
        empty_state("\U0001f64f", "No shared prayer requests yet",
                    "Members can share prayers from their Prayer Journal")
    else:
        section_label(f"{len(shared_prayers)} Shared Prayer Request(s)")

        for prayer in shared_prayers:
            status_config = {
                "ongoing": ("#D4853A", "#FFF3E0", "Ongoing"),
                "answered": ("#3A8F5C", "#E8F5E9", "Answered"),
                "standing_in_faith": ("#5B4FC4", "#EDEBFA", "Standing in Faith"),
            }
            p_status = prayer.get("status", "ongoing")
            s_color, s_bg, s_label = status_config.get(p_status, ("#888", "#F5F5F5", p_status))
            shared_date = (prayer.get("shared_at") or "")[:10]

            st.markdown(f"""
            <div class="entry-card" style="border-left:3px solid {s_color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">
                            {prayer['title']}
                        </span>
                        <span style="font-size:12px; color:#9E96AB; margin-left:8px;">
                            from {prayer.get('member_name', 'Member')}
                        </span>
                    </div>
                    <span style="background:{s_bg}; color:{s_color}; padding:2px 10px;
                                 border-radius:10px; font-size:11px; font-weight:600;">
                        {s_label}
                    </span>
                </div>
                {"<div style='font-size:14px; color:#6B6580; margin-top:8px; line-height:1.6; font-style:italic;'>" + prayer['prayer_text'][:200].replace(chr(10), '<br/>') + ('...' if len(prayer.get('prayer_text','')) > 200 else '') + "</div>" if prayer.get('prayer_text') else ""}
                <div style="font-size:11px; color:#C0B8CC; margin-top:6px;">
                    Shared on {shared_date}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== CREATE ASSIGNMENT TAB ====================
with tab_assign:
    section_label("Assign Bible Reading to Group")

    st.markdown(f"""
    <div style="font-size:13px; color:#9E96AB; margin-bottom:16px;">
        This assignment will be pushed to all <b>{len(members)}</b> member(s) in your group.
        It replaces any active assignment they currently have.
    </div>
    """, unsafe_allow_html=True)

    # REQ-2: Multi-book assignment support
    st.caption("You can add multiple book ranges (e.g., Hebrews 7-13 + 1 Corinthians 7-11)")

    if "grp_books" not in st.session_state:
        st.session_state["grp_books"] = []

    with st.form("add_book_form"):
        book_names = get_book_names()
        book = st.selectbox("Bible Book", options=book_names,
                            index=book_names.index("Luke") if "Luke" in book_names else 0)
        max_ch = get_chapter_count(book)

        col1, col2 = st.columns(2)
        with col1:
            start_ch = st.number_input("From Chapter", min_value=1, max_value=max_ch, value=1)
        with col2:
            end_ch = st.number_input("To Chapter", min_value=1, max_value=max_ch, value=min(max_ch, 10))

        add_book = st.form_submit_button("Add Book Range", use_container_width=True)

    if add_book:
        if start_ch > end_ch:
            st.error("'From Chapter' must be less than or equal to 'To Chapter'.")
        else:
            st.session_state["grp_books"].append({"book": book, "start": start_ch, "end": end_ch})
            st.rerun()

    # Show added books
    if st.session_state["grp_books"]:
        section_label("Reading Plan")
        for i, b in enumerate(st.session_state["grp_books"]):
            col_book, col_del = st.columns([5, 1])
            with col_book:
                st.markdown(f"\U0001f4d6 **{b['book']}** {b['start']}\u2013{b['end']} ({b['end'] - b['start'] + 1} chapters)")
            with col_del:
                if st.button("\u274c", key=f"del_book_{i}"):
                    st.session_state["grp_books"].pop(i)
                    st.rerun()

        today = date.today()
        default_monday = today if today.weekday() == 0 else get_next_monday(today)
        week_start = st.date_input("Week starting (Monday)", value=default_monday)

        if st.button("Preview Breakdown", use_container_width=True):
            # Calculate total chapters across all books
            total_chapters = sum(b["end"] - b["start"] + 1 for b in st.session_state["grp_books"])
            breakdown = split_chapters(1, total_chapters, num_days=6)
            st.session_state["grp_preview"] = breakdown
            st.session_state["grp_book"] = " + ".join(f"{b['book']} {b['start']}-{b['end']}" for b in st.session_state["grp_books"])
            st.session_state["grp_start"] = st.session_state["grp_books"][0]["start"]
            st.session_state["grp_end"] = st.session_state["grp_books"][-1]["end"]
            st.session_state["grp_week_start"] = week_start
            st.session_state["grp_reading_plan"] = st.session_state["grp_books"]
    else:
        st.info("Add at least one book range to create an assignment.")

    if "grp_preview" in st.session_state:
        section_label("Daily Breakdown Preview")

        breakdown = st.session_state["grp_preview"]
        day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

        for label, key in zip(day_labels, day_keys):
            chapters = breakdown.get(key, [])
            if chapters:
                ch_range = f"Ch {chapters[0]}\u2013{chapters[-1]}" if len(chapters) > 1 else f"Ch {chapters[0]}"
                st.markdown(f"""
                <div class="day-row day-pending">
                    <span class="day-name">{label}</span>
                    <span class="day-chapters">{ch_range} ({len(chapters)} ch)</span>
                </div>
                """, unsafe_allow_html=True)

        spacer(12)

        st.markdown(f"""
        <div class="goal-banner">
            \U0001f465 This will be assigned to <b>{len(members)}</b> member(s):
            {', '.join(m['display_name'] for m in members[:5])}{'...' if len(members) > 5 else ''}
        </div>
        """, unsafe_allow_html=True)

        if st.button("Assign to Group", type="primary", use_container_width=True):
            ws = st.session_state["grp_week_start"]
            week_end = ws + timedelta(days=5)

            with st.spinner(f"Assigning to {len(members)} members..."):
                result = create_group_assignment(
                    pastor_id=viewing_pastor_id,
                    member_ids=[m["user_id"] for m in members],
                    book=st.session_state["grp_book"],
                    start_chapter=st.session_state["grp_start"],
                    end_chapter=st.session_state["grp_end"],
                    week_start=ws.isoformat(),
                    week_end=week_end.isoformat(),
                    daily_breakdown=breakdown,
                )

            if result.get("success"):
                for k in ["grp_preview", "grp_book", "grp_start", "grp_end", "grp_week_start"]:
                    st.session_state.pop(k, None)
                st.success(f"Assignment pushed to {result['count']} members!")
                st.rerun()

# ==================== ASSIGNMENT HISTORY TAB ====================
with tab_history:
    assignments = get_group_assignments(viewing_pastor_id)

    if not assignments:
        empty_state("\U0001f4c1", "No group assignments yet", "Create one in the 'Create Assignment' tab")
    else:
        # Group by unique assignment (same book, dates, assigned_by)
        seen = set()
        unique_assignments = []
        for a in assignments:
            key = f"{a['book']}_{a['start_chapter']}_{a['end_chapter']}_{a['week_start_date']}"
            if key not in seen:
                seen.add(key)
                unique_assignments.append(a)

        for a in unique_assignments:
            # Count how many members have this assignment
            admin = get_admin_client()
            same_assignment = admin.table("weekly_assignments") \
                .select("user_id, status", count="exact") \
                .eq("assigned_by", viewing_pastor_id) \
                .eq("book", a["book"]) \
                .eq("start_chapter", a["start_chapter"]) \
                .eq("week_start_date", a["week_start_date"]) \
                .execute()

            member_count = same_assignment.count or 0
            active_count = sum(1 for r in (same_assignment.data or []) if r["status"] == "ACTIVE")

            status_config = {
                "ACTIVE": ("#D4853A", "#FFF3E0", "\U0001f7e1"),
                "COMPLETED": ("#3A8F5C", "#E8F5E9", "\u2705"),
            }
            s_color, s_bg, s_icon = status_config.get(
                "ACTIVE" if active_count > 0 else "COMPLETED",
                ("#888", "#F5F5F5", "\u26aa")
            )

            assign_key = f"{a['book']}_{a['start_chapter']}_{a['week_start_date']}"

            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-weight:400; color:#2A2438; font-size:15px;">
                            {s_icon} {a['book']} {a['start_chapter']}\u2013{a['end_chapter']}
                        </span>
                        <span style="font-size:12px; color:#9E96AB; margin-left:8px;">
                            {a['total_chapters']} chapters | {member_count} members
                        </span>
                    </div>
                    <span style="background:{s_bg}; color:{s_color}; padding:3px 10px;
                                 border-radius:12px; font-size:11px; font-weight:600;">
                        {active_count} active
                    </span>
                </div>
                <div style="font-size:12px; color:#9E96AB; margin-top:4px;">
                    Week of {a['week_start_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Cancel button for active assignments
            if active_count > 0:
                if st.button("Cancel Assignment", key=f"cancel_{assign_key}", use_container_width=True):
                    st.session_state[f"confirm_cancel_{assign_key}"] = True

                if st.session_state.get(f"confirm_cancel_{assign_key}"):
                    st.warning(f"Cancel **{a['book']} {a['start_chapter']}-{a['end_chapter']}** for all members?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Yes, Cancel", key=f"yes_cancel_{assign_key}", type="primary"):
                            admin.table("weekly_assignments") \
                                .update({"status": "COMPLETED"}) \
                                .eq("assigned_by", viewing_pastor_id) \
                                .eq("book", a["book"]) \
                                .eq("start_chapter", a["start_chapter"]) \
                                .eq("week_start_date", a["week_start_date"]) \
                                .eq("status", "ACTIVE") \
                                .execute()
                            st.session_state.pop(f"confirm_cancel_{assign_key}", None)
                            st.success("Assignment cancelled for all members.")
                            st.rerun()
                    with c2:
                        if st.button("No", key=f"no_cancel_{assign_key}"):
                            st.session_state.pop(f"confirm_cancel_{assign_key}", None)
                            st.rerun()

# ==================== CONFESSIONS TAB ====================
with tab_confessions:
    section_label("Confession Assignments")

    try:
        # Show active assignments
        assigned_plans = db.get_pastor_assigned_plans(viewing_pastor_id)

        if assigned_plans:
            st.markdown(f"""
            <div class="stat-card" style="text-align:center;">
                <div class="stat-value">{len(assigned_plans)}</div>
                <div class="stat-label">Active Confession Assignments</div>
            </div>
            """, unsafe_allow_html=True)
            spacer()

            for plan in assigned_plans:
                tpl = plan.get("confession_templates", {})
                member_name = plan.get("member_name", "Member")
                stats = db.get_member_completion_stats(plan["user_id"], plan["id"])

                # Calculate progress
                progress_text = ""
                if plan.get("start_date") and plan.get("end_date"):
                    start_d = date.fromisoformat(plan["start_date"])
                    end_d = date.fromisoformat(plan["end_date"])
                    total_days = (end_d - start_d).days + 1
                    days_done = stats["total_days_completed"]
                    progress_text = f"Day {days_done}/{total_days}"
                    pct = min(days_done / total_days * 100, 100) if total_days > 0 else 0
                else:
                    days_done = stats["total_days_completed"]
                    progress_text = f"{days_done} days"
                    pct = 0

                last_active = stats.get("last_completed") or "Never"
                days_since = ""
                if stats.get("last_completed"):
                    delta = (date.today() - date.fromisoformat(stats["last_completed"])).days
                    if delta == 0:
                        days_since = "Today"
                    elif delta == 1:
                        days_since = "Yesterday"
                    else:
                        days_since = f"{delta} days ago"
                        if delta >= 3:
                            days_since = f"&#9888;&#65039; {days_since}"
                else:
                    days_since = "Not started"

                st.markdown(f"""
                <div class="entry-card" style="padding:16px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <strong>{member_name}</strong>
                            <span style="color:#6B6580; font-size:13px;"> &mdash; {tpl.get('name', 'Confession')}</span>
                        </div>
                        <span style="font-size:12px; color:#6B6580;">{progress_text}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:8px;">
                        <span style="font-size:12px; color:#9E96AB;">Last active: {days_since}</span>
                        <span style="font-size:12px; color:#9E96AB;">{plan.get('plan_type', '').replace('_', ' ').title()}</span>
                    </div>
                    <div style="height:4px; background:#EDE8F5; border-radius:2px; margin-top:8px; overflow:hidden;">
                        <div style="height:100%; width:{pct:.0f}%; background:#5B4FC4; border-radius:2px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("✝️", "No Confession Assignments", "Assign confessions to members below.")

        # --- Assign New Confession ---
        spacer()
        section_label("Assign Confession to Member")

        if members:
            member_options = {m["user_id"]: m.get("preferred_name") or m.get("full_name", "Member") for m in members}
            selected_member = st.selectbox(
                "Select Member",
                options=list(member_options.keys()),
                format_func=lambda uid: member_options[uid],
                key="conf_assign_member"
            )

            # Load available templates
            all_templates = db.get_confession_templates(published_only=True)
            # Filter out new believer track
            available_templates = [t for t in all_templates if t.get("sort_order", 0) < 100]

            if available_templates:
                template_options = {t["id"]: t["name"] for t in available_templates}
                selected_template = st.selectbox(
                    "Select Confession",
                    options=list(template_options.keys()),
                    format_func=lambda tid: template_options[tid],
                    key="conf_assign_template"
                )

                col_dur, col_note = st.columns(2)
                with col_dur:
                    duration = st.selectbox(
                        "Duration",
                        ["21_days", "7_days", "ongoing"],
                        format_func=lambda x: {"21_days": "21 Days", "7_days": "7 Days", "ongoing": "Ongoing"}[x],
                        key="conf_assign_duration"
                    )
                with col_note:
                    note = st.text_input("Note for member (optional)", key="conf_assign_note")

                if st.button("Assign Confession", type="primary", key="conf_assign_btn"):
                    result = db.assign_confession_to_member(
                        member_id=selected_member,
                        template_id=selected_template,
                        plan_type=duration,
                        note=note if note else None
                    )
                    if result:
                        st.success(f"Confession assigned to {member_options[selected_member]}!")
                        st.rerun()
                    else:
                        st.error("Failed to assign confession. Please try again.")
            else:
                st.info("No confession templates available yet. Ask your admin to add templates.")
        else:
            st.info("No members found in your group.")

    except Exception as e:
        st.info("Confession assignments will be available once the Prayer Engine is set up.")
        if st.session_state.get("debug_mode"):
            st.exception(e)

# ==================== CARE ALERTS TAB ====================
with tab_care:
    CARE_TYPES = ["Check-In Call", "Prayer Visit", "Message", "Escalate to Bishop"]

    # ── Inactive Members (no entry in 3+ days) ──
    section_label("\U0001f6a8 Inactive Members (3+ days)")
    try:
        inactive = get_inactive_members(viewing_pastor_id, threshold_days=3)
    except Exception:
        inactive = []

    # Build a set of member_ids that already have an open task
    try:
        open_tasks = get_care_tasks(viewing_pastor_id, status="open")
    except Exception:
        open_tasks = []

    tasked_member_ids = {t["member_id"] for t in open_tasks}

    # Get member name map
    admin_c = get_admin_client()
    member_name_map: dict = {}
    for m in members:
        try:
            u = admin_c.auth.admin.get_user_by_id(m["user_id"]).user
            member_name_map[m["user_id"]] = (u.user_metadata or {}).get("preferred_name", u.email)
        except Exception:
            member_name_map[m["user_id"]] = "Member"

    untasked_inactive = [i for i in inactive if i["user_id"] not in tasked_member_ids]

    if not untasked_inactive:
        st.success("No inactive members without a care task. Great work!")
    else:
        for row in untasked_inactive:
            m_name = member_name_map.get(row["user_id"], "Member")
            days = row.get("days_since_last_entry", "?")
            with st.expander(f"{m_name} — {days} day(s) inactive", expanded=False):
                with st.form(key=f"care_form_{row['user_id']}"):
                    care_type = st.selectbox("Care Type", CARE_TYPES,
                                             key=f"ct_{row['user_id']}")
                    note = st.text_area("Care Note (optional, max 500 chars)", max_chars=500,
                                        key=f"cn_{row['user_id']}")
                    due = st.date_input("Follow-up Due Date", value=date.today() + timedelta(days=2),
                                        key=f"cd_{row['user_id']}")
                    if st.form_submit_button("Create Care Task", type="primary",
                                             use_container_width=True):
                        create_care_task(
                            pastor_id=viewing_pastor_id,
                            member_id=row["user_id"],
                            care_type=care_type,
                            note=note,
                            due_date=due.isoformat(),
                        )
                        st.success(f"Care task created for {m_name}.")
                        st.rerun()

    spacer()

    # ── Open Tasks ──
    section_label("\U0001f4cb Open Care Tasks")

    if not open_tasks:
        st.info("No open care tasks.")
    else:
        # Sort by due_date ascending (nulls last)
        open_tasks.sort(key=lambda t: t.get("due_date") or "9999-99-99")
        for task in open_tasks:
            m_name = task.get("member_name", member_name_map.get(task["member_id"], "Member"))
            due_str = task.get("due_date") or "—"
            overdue = task.get("due_date") and task["due_date"] < date.today().isoformat()
            badge_color = "#C44B5B" if overdue else "#D4853A"
            badge_label = "OVERDUE" if overdue else task["care_type"]

            st.markdown(f"""
            <div class="entry-card" style="border-left:4px solid {badge_color};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-weight:600; color:#2A2438;">{m_name}</span>
                        <span style="background:{badge_color}20; color:{badge_color};
                                     padding:2px 8px; border-radius:8px; font-size:11px;
                                     font-weight:600; margin-left:8px;">
                            {badge_label}
                        </span>
                    </div>
                    <div style="font-size:12px; color:#9E96AB;">Due: {due_str}</div>
                </div>
                {f'<div style="font-size:13px; color:#6B6580; margin-top:4px;">{task["note"]}</div>' if task.get("note") else ''}
            </div>
            """, unsafe_allow_html=True)

            if st.button("Mark Done", key=f"done_{task['id']}", use_container_width=False):
                complete_care_task(task["id"])
                st.success("Task marked as done.")
                st.rerun()

    spacer()

    # ── Completed Tasks (last 10) ──
    with st.expander("Completed Tasks (recent 10)"):
        try:
            done_tasks = get_care_tasks(viewing_pastor_id, status="done")
        except Exception:
            done_tasks = []
        done_tasks = sorted(done_tasks, key=lambda t: t.get("completed_at") or "", reverse=True)[:10]
        if not done_tasks:
            st.caption("No completed tasks yet.")
        else:
            for task in done_tasks:
                m_name = task.get("member_name", member_name_map.get(task["member_id"], "Member"))
                done_at = (task.get("completed_at") or "")[:10]
                st.markdown(f"✅ **{m_name}** — {task['care_type']} (completed {done_at})")

# ==================== READING PLANS TAB ====================
with tab_plans:
    plans = get_reading_plans()

    if not plans:
        st.info("No reading plans available yet. Ask your admin to seed the built-in plans.")
    else:
        # ── Assign a plan ──
        section_label("\U0001f4e5 Assign a Reading Plan")
        member_options = {m["display_name"]: m["user_id"] for m in members}
        plan_options = {p["name"]: p["id"] for p in plans}

        col_m, col_p = st.columns(2)
        with col_m:
            selected_member = st.selectbox("Member", options=list(member_options.keys()),
                                           key="rp_member")
        with col_p:
            selected_plan = st.selectbox("Plan", options=list(plan_options.keys()),
                                         key="rp_plan")

        chosen_plan = next((p for p in plans if p["name"] == selected_plan), None)
        if chosen_plan:
            st.caption(chosen_plan.get("description", ""))

        if st.button("\U0001f4e5 Assign Plan", type="primary", key="assign_plan_btn"):
            enroll_in_plan(
                user_id=member_options[selected_member],
                plan_id=plan_options[selected_plan],
                assigned_by=viewing_pastor_id,
            )
            st.success(f"Assigned **{selected_plan}** to {selected_member}.")
            st.rerun()

        spacer()

        # ── Members' progress ──
        section_label("\U0001f4ca Members' Reading Progress")
        try:
            progress_rows = get_members_plan_progress(viewing_pastor_id)
        except Exception:
            progress_rows = []

        if not progress_rows:
            st.info("No members are currently enrolled in a reading plan.")
        else:
            for row in progress_rows:
                rp = row.get("reading_plans") or {}
                total = rp.get("total_days", 1)
                current = row.get("current_day", 1)
                done = current - 1
                pct = int(done / total * 100) if total > 0 else 0
                pct_color = "#3A8F5C" if pct >= 70 else "#D4853A" if pct >= 30 else "#5B4FC4"
                m_name = row.get("member_name", "Member")

                st.markdown(f"""
                <div class="entry-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <div>
                            <span style="font-weight:600; color:#2A2438;">{m_name}</span>
                            <span style="font-size:12px; color:#9E96AB; margin-left:8px;">{rp.get('name', '')}</span>
                        </div>
                        <span style="font-size:12px; color:{pct_color}; font-weight:600;">
                            Day {done}/{total} ({pct}%)
                        </span>
                    </div>
                    <div class="progress-bar-bg" style="height:6px;">
                        <div class="progress-bar-fill" style="width:{pct}%; background:{pct_color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ==================== GROUP REPORT TAB ====================
with tab_digest:
    from modules.utils import format_prayer_duration

    section_label("\U0001f4f2 Weekly Group WhatsApp Report")
    st.caption("Generate a WhatsApp-ready summary of your group's activity this week. Copy and paste into your group chat.")

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=5)
    week_label = f"{week_start.strftime('%b %d')} – {week_end.strftime('%b %d, %Y')}"

    if st.button("\U0001f504 Generate Report", type="primary", use_container_width=True, key="gen_digest"):
        st.session_state["digest_ready"] = True

    if st.session_state.get("digest_ready"):
        admin_d = get_admin_client()
        member_ids_d = [m["user_id"] for m in members]

        # Fetch all entries for this week across the group
        week_entries_raw = admin_d.table("daily_entries") \
            .select("user_id, date, prayer_minutes, chapters_read, chapters_display") \
            .in_("user_id", member_ids_d) \
            .gte("date", week_start.isoformat()) \
            .lte("date", week_end.isoformat()) \
            .execute()
        week_entries_map: dict = {}
        for e in (week_entries_raw.data or []):
            week_entries_map.setdefault(e["user_id"], []).append(e)

        # Build name map
        name_map_d: dict = {}
        for m in members:
            try:
                u = admin_d.auth.admin.get_user_by_id(m["user_id"]).user
                name_map_d[m["user_id"]] = (u.user_metadata or {}).get("preferred_name", u.email.split("@")[0])
            except Exception:
                name_map_d[m["user_id"]] = "Member"

        lines = [
            f"\U0001f4ca *Group Report — {week_label}*",
            f"Pastor {pastor_name}'s Group • {len(members)} members",
            "",
        ]

        total_prayer_min = 0
        total_chapters = 0
        members_logged = 0

        import json as _json
        for m in members:
            uid = m["user_id"]
            name = name_map_d.get(uid, "Member")
            entries = week_entries_map.get(uid, [])
            days_logged = len(entries)
            prayer_min = sum(e.get("prayer_minutes", 0) for e in entries)
            ch_count = 0
            for e in entries:
                if e.get("chapters_read"):
                    chs = _json.loads(e["chapters_read"]) if isinstance(e["chapters_read"], str) else e["chapters_read"]
                    ch_count += len(chs)

            total_prayer_min += prayer_min
            total_chapters += ch_count
            if days_logged > 0:
                members_logged += 1

            if days_logged == 0:
                lines.append(f"❌ {name} — No entries this week")
            else:
                prayer_str = format_prayer_duration(prayer_min)
                streak_icon = "\U0001f525" if days_logged >= 5 else "⭐" if days_logged >= 3 else "✅"
                lines.append(f"{streak_icon} {name} — {days_logged}/6 days | Prayer: {prayer_str} | Chapters: {ch_count}")

        lines += [
            "",
            f"\U0001f4ca *Group Totals:*",
            f"\U0001f64f Total prayer: {format_prayer_duration(total_prayer_min)}",
            f"\U0001f4d6 Total chapters: {total_chapters}",
            f"\U0001f465 Members active: {members_logged}/{len(members)}",
            "",
            "_Generated by Logos Pulse_",
        ]

        report_text = "\n".join(lines)

        st.text_area("Copy the report below:", value=report_text, height=320, key="digest_text")
        st.caption("Select all → Copy → Paste into WhatsApp group chat.")

# ==================== PRAYER WALL (MODERATION) ====================
with tab_wall:
    from modules.db import (
        get_all_prayer_requests_for_moderation, moderate_prayer_request,
        get_pastor_checkin_requests, acknowledge_checkin_request,
    )

    section_label("\U0001f64c Prayer Request Moderation")
    all_reqs = get_all_prayer_requests_for_moderation()

    status_filter = st.selectbox("Show", ["active", "answered", "hidden", "all"], index=0, key="wall_filter")
    if status_filter != "all":
        all_reqs = [r for r in all_reqs if r.get("status") == status_filter]

    if not all_reqs:
        st.caption("No prayer requests matching this filter.")
    else:
        for req in all_reqs:
            profile_info = req.pop("user_profiles", {}) or {}
            author = "Anonymous" if req.get("is_anonymous") else profile_info.get("display_name", "Member")
            status_badge_color = {"active": "#3A8F5C", "answered": "#5B4FC4", "hidden": "#9E96AB"}.get(req.get("status"), "#9E96AB")

            _req_title = _html.escape(req['title'])
            _req_body = _html.escape(req['body']) if req.get('body') else ""
            _req_author = _html.escape(author)
            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div style="flex:1;">
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">
                            {_req_title}
                        </span>
                        {"<div style='font-size:13px; color:#6B6580; margin-top:4px;'>" + _req_body + "</div>" if _req_body else ""}
                    </div>
                    <div style="text-align:right; margin-left:12px; flex-shrink:0;">
                        <div style="font-size:11px; color:#9E96AB;">{_req_author}</div>
                        <span style="background:{status_badge_color}20; color:{status_badge_color};
                                     padding:2px 8px; border-radius:8px; font-size:11px; font-weight:600;">
                            {req.get('status','active')}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if req.get("status") == "active":
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Mark Answered", key=f"ans_mod_{req['id']}", use_container_width=True):
                        moderate_prayer_request(req["id"], "answered")
                        st.rerun()
                with c2:
                    if st.button("Hide", key=f"hide_mod_{req['id']}", use_container_width=True):
                        moderate_prayer_request(req["id"], "hidden")
                        st.rerun()
            elif req.get("status") in ("hidden", "answered"):
                if st.button("Restore to Active", key=f"restore_mod_{req['id']}", use_container_width=True):
                    moderate_prayer_request(req["id"], "active")
                    st.rerun()

    spacer()
    section_label("\U0001f4cb Check-in Requests from Members")
    checkin_reqs = get_pastor_checkin_requests(pastor_id=viewing_pastor_id)
    if not checkin_reqs:
        st.caption("No pending check-in requests.")
    else:
        for cr in checkin_reqs:
            profile_info = cr.pop("user_profiles", {}) or {}
            member_name = _html.escape(profile_info.get("display_name", "Member"))
            _cr_msg = _html.escape(cr['message']) if cr.get('message') else ""
            st.markdown(f"""
            <div class="entry-card" style="border-left:3px solid #D4853A;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:13px; font-weight:600; color:#2A2438;">{member_name}</span>
                        {"<div style='font-size:12px; color:#6B6580; margin-top:2px;'>" + _cr_msg + "</div>" if _cr_msg else ""}
                    </div>
                    <span style="font-size:11px; color:#9E96AB; white-space:nowrap; margin-left:8px;">{cr['created_at'][:10]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if cr.get("status") == "pending":
                if st.button("Acknowledge", key=f"ack_cr_{cr['id']}", use_container_width=True):
                    acknowledge_checkin_request(cr["id"])
                    st.rerun()