import streamlit as st
from datetime import date, timedelta
import json
from modules import db
from modules.bible_data import get_book_names, get_chapter_count
from modules.chapter_splitter import split_chapters
from modules.utils import get_next_monday

db.init_db()

st.markdown("""
<style>
    .wa-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        color: white;
    }
    .wa-title { font-size: 24px; font-weight: 700; }
    .wa-sub { font-size: 13px; color: rgba(255,255,255,0.7); margin-top: 4px; }
    .day-row {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        margin: 4px 0;
        border-radius: 10px;
        font-size: 15px;
    }
    .day-done { background: #E8F5E9; }
    .day-pending { background: #FFF3E0; }
    .day-name { font-weight: 600; width: 100px; }
    .day-chapters { flex: 1; color: #555; }
    .day-status { font-size: 18px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="wa-header">
    <div class="wa-title">\U0001f4d6 Weekly Assignment</div>
    <div class="wa-sub">Bible reading goals from your pastor</div>
</div>
""", unsafe_allow_html=True)

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
            <span style="font-size:13px; color:#999; text-transform:uppercase; letter-spacing:2px;">
                {assignment['week_start_date']} \u2014 {assignment['week_end_date']}
            </span><br/>
            <span style="font-size:28px; font-weight:700; color:#4A3728;">
                {assignment['book']} {assignment['start_chapter']}\u2013{assignment['end_chapter']}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.markdown(f"""
        <div style="margin:12px 0;">
            <div style="background:#F0EBF8; border-radius:8px; height:12px; overflow:hidden;">
                <div style="width:{progress_pct}%; height:100%; border-radius:8px;
                            background:linear-gradient(90deg, #667eea, #764ba2);"></div>
            </div>
            <div style="text-align:center; font-size:13px; color:#999; margin-top:6px;">
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
        st.markdown("""
        <div style="text-align:center; padding:40px; color:#ccc;">
            <div style="font-size:48px; margin-bottom:8px;">\U0001f4d6</div>
            <div style="font-size:16px; color:#999;">No active assignment</div>
            <div style="font-size:13px; color:#bbb;">Create one in the "New Assignment" tab</div>
        </div>
        """, unsafe_allow_html=True)

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
        st.markdown("""
        <div style="font-size:12px; color:#999; text-transform:uppercase;
                    letter-spacing:1.5px; font-weight:600; margin:16px 0 8px 0;">
            Daily Breakdown Preview
        </div>
        """, unsafe_allow_html=True)

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

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
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
        st.markdown("""
        <div style="text-align:center; padding:40px; color:#ccc;">
            <div style="font-size:48px; margin-bottom:8px;">\U0001f4c1</div>
            <div style="font-size:16px; color:#999;">No history yet</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for a in history:
            status_config = {
                "COMPLETED": ("#4CAF50", "#E8F5E9", "\u2705"),
                "ACTIVE": ("#FF9800", "#FFF3E0", "\U0001f7e1"),
            }
            s_color, s_bg, s_icon = status_config.get(a["status"], ("#888", "#F5F5F5", "\u26aa"))

            st.markdown(f"""
            <div style="background:white; border:1px solid #F0EBF8; border-radius:12px;
                        padding:14px 18px; margin-bottom:8px;
                        box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-weight:600; color:#4A3728; font-size:15px;">
                            {s_icon} {a['book']} {a['start_chapter']}\u2013{a['end_chapter']}
                        </span>
                        <span style="font-size:12px; color:#999; margin-left:8px;">
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
                <div style="font-size:12px; color:#aaa; margin-top:4px;">
                    Week of {a['week_start_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)
