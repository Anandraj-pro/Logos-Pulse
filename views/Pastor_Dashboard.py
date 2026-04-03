import streamlit as st
from datetime import date, timedelta
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id, get_current_role
from modules.rbac import get_members_for_pastor
from modules.supabase_client import get_admin_client
from modules.bible_data import get_book_names, get_chapter_count
from modules.chapter_splitter import split_chapters
from modules.utils import get_next_monday
from modules.db import create_group_assignment, get_group_assignments

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
tab_members, tab_leaderboard, tab_assign, tab_history = st.tabs([
    "\U0001f465 Members", "\U0001f3c6 Leaderboard", "\U0001f4d6 Create Assignment", "\U0001f4c1 Assignment History"
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

    view_mode = st.segmented_control("Filter", ["All", "Logged Today", "Not Logged"], default="All", label_visibility="collapsed")

    for member in members:
        uid = member["user_id"]
        logged = uid in logged_user_ids
        entry = entry_map.get(uid)

        if view_mode == "Logged Today" and not logged:
            continue
        if view_mode == "Not Logged" and logged:
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