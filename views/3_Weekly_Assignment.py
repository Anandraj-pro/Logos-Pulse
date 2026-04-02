import streamlit as st
from datetime import date, timedelta
import json
from modules import db
from modules.bible_data import get_book_names, get_chapter_count
from modules.chapter_splitter import split_chapters
from modules.utils import get_next_monday
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_login, require_password_changed

require_login()
require_password_changed()
inject_styles()

page_header("\U0001f4d6", "Weekly Assignment", "Bible reading goals from your pastor")

tab1, tab2, tab3 = st.tabs(["\U0001f4ca Current", "\u2795 New Assignment", "\U0001f4c1 History"])

# ==================== CURRENT ====================
with tab1:
    assignment = db.get_active_assignment()
    if assignment:
        breakdown = json.loads(assignment["daily_breakdown"]) if isinstance(
            assignment["daily_breakdown"], str
        ) else assignment["daily_breakdown"]

        week_entries = db.get_entries_in_range(assignment["week_start_date"], assignment["week_end_date"])
        chapters_done = set()
        for entry in week_entries:
            if entry.get("bible_book") == assignment["book"] and entry.get("chapters_read"):
                read = json.loads(entry["chapters_read"]) if isinstance(entry["chapters_read"], str) else entry["chapters_read"]
                chapters_done.update(read)

        all_assigned = []
        for chs in breakdown.values():
            all_assigned.extend(chs)
        total = len(all_assigned)
        done_count = len(chapters_done.intersection(set(all_assigned)))
        progress_pct = int(done_count / total * 100) if total > 0 else 0

        # Book title
        st.markdown(f"""
        <div style="text-align:center; padding:8px 0;">
            <span style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:2px;">
                {assignment['week_start_date']} \u2014 {assignment['week_end_date']}
            </span><br/>
            <span style="font-family:'DM Serif Display',Georgia,serif; font-size:28px; color:#2A2438;">
                {assignment['book']} {assignment['start_chapter']}\u2013{assignment['end_chapter']}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.markdown(f"""
        <div style="margin:12px 0;">
            <div class="progress-bar-bg" style="height:12px;">
                <div class="progress-bar-fill" style="width:{progress_pct}%;"></div>
            </div>
            <div style="text-align:center; font-size:13px; color:#9E96AB; margin-top:6px;">
                {done_count}/{total} chapters ({progress_pct}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Daily breakdown
        day_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_keys = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]

        for label, key in zip(day_labels, day_keys):
            chapters = breakdown.get(key, [])
            if not chapters:
                continue
            done = all(c in chapters_done for c in chapters)
            ch_range = f"Ch {chapters[0]}\u2013{chapters[-1]}" if len(chapters) > 1 else f"Ch {chapters[0]}"
            css_class = "day-done" if done else "day-pending"
            icon = "\u2705" if done else "\u23f3"

            st.markdown(f"""
            <div class="day-row {css_class}">
                <span class="day-name">{label}</span>
                <span class="day-chapters">{ch_range} ({len(chapters)} ch)</span>
                <span class="day-status">{icon}</span>
            </div>
            """, unsafe_allow_html=True)

        if done_count >= total:
            st.balloons()
            st.success("Assignment completed! Praise the Lord!")
    else:
        empty_state("\U0001f4d6", "No active assignment", 'Create one in the "New Assignment" tab')

# ==================== NEW ====================
with tab2:
    with st.form("new_assignment"):
        book_names = get_book_names()
        book = st.selectbox("Bible Book", options=book_names, index=book_names.index("Luke") if "Luke" in book_names else 0)
        max_ch = get_chapter_count(book)

        col1, col2 = st.columns(2)
        with col1:
            start_ch = st.number_input("From Chapter", min_value=1, max_value=max_ch, value=1)
        with col2:
            end_ch = st.number_input("To Chapter", min_value=1, max_value=max_ch, value=max_ch)

        today = date.today()
        default_monday = today if today.weekday() == 0 else get_next_monday(today)
        week_start = st.date_input("Week starting (Monday)", value=default_monday)

        generate = st.form_submit_button("Preview Breakdown", use_container_width=True)

    if generate:
        if start_ch > end_ch:
            st.error("'From Chapter' must be less than or equal to 'To Chapter'.")
        else:
            breakdown = split_chapters(start_ch, end_ch, num_days=6)
            st.session_state["preview_breakdown"] = breakdown
            st.session_state["preview_book"] = book
            st.session_state["preview_start"] = start_ch
            st.session_state["preview_end"] = end_ch
            st.session_state["preview_week_start"] = week_start

    if "preview_breakdown" in st.session_state:
        section_label("Daily Breakdown Preview")

        breakdown = st.session_state["preview_breakdown"]
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
        if st.button("Confirm Assignment", type="primary", use_container_width=True):
            ws = st.session_state["preview_week_start"]
            week_end = ws + timedelta(days=5)
            db.create_assignment(
                book=st.session_state["preview_book"],
                start_chapter=st.session_state["preview_start"],
                end_chapter=st.session_state["preview_end"],
                week_start=ws.isoformat(),
                week_end=week_end.isoformat(),
                daily_breakdown=breakdown,
            )
            for k in ["preview_breakdown", "preview_book", "preview_start", "preview_end", "preview_week_start"]:
                st.session_state.pop(k, None)
            st.success("Assignment created!")
            st.rerun()

# ==================== HISTORY ====================
with tab3:
    history = db.get_assignment_history()
    if not history:
        empty_state("\U0001f4c1", "No history yet")
    else:
        for a in history:
            status_config = {
                "COMPLETED": ("#3A8F5C", "#E8F5E9", "\u2705"),
                "ACTIVE": ("#D4853A", "#FFF3E0", "\U0001f7e1"),
            }
            s_color, s_bg, s_icon = status_config.get(a["status"], ("#888", "#F5F5F5", "\u26aa"))

            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-weight:400; color:#2A2438; font-size:15px;">
                            {s_icon} {a['book']} {a['start_chapter']}\u2013{a['end_chapter']}
                        </span>
                        <span style="font-size:12px; color:#9E96AB; margin-left:8px;">
                            {a['total_chapters']} chapters
                        </span>
                    </div>
                    <div>
                        <span style="background:{s_bg}; color:{s_color}; padding:3px 10px;
                                     border-radius:12px; font-size:11px; font-weight:600;">
                            {a['status']}
                        </span>
                    </div>
                </div>
                <div style="font-size:12px; color:#9E96AB; margin-top:4px;">
                    Week of {a['week_start_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)