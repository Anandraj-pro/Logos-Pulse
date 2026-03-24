import streamlit as st
from datetime import date, timedelta
import calendar
import json
from modules import db
from modules.utils import format_prayer_duration

db.init_db()

st.markdown("""
<style>
    .log-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        color: white;
    }
    .log-title { font-size: 24px; font-weight: 700; }
    .log-sub { font-size: 13px; color: rgba(255,255,255,0.7); margin-top: 4px; }
    .cal-day {
        text-align: center;
        border-radius: 8px;
        padding: 6px 4px;
        font-size: 13px;
        font-weight: 500;
        margin: 2px;
        cursor: pointer;
    }
    .cal-done {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: 700;
    }
    .cal-empty { color: #ccc; }
    .cal-header {
        text-align: center;
        font-size: 11px;
        color: #999;
        font-weight: 600;
        text-transform: uppercase;
        padding: 4px;
    }
    .entry-card {
        background: white;
        border: 1px solid #F0EBF8;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)

all_dates = db.get_all_entry_dates()

st.markdown(f"""
<div class="log-header">
    <div class="log-title">\U0001f4c5 Daily Log</div>
    <div class="log-sub">{len(all_dates)} entries recorded</div>
</div>
""", unsafe_allow_html=True)

view_mode = st.segmented_control("View", ["Calendar", "List"], default="Calendar", label_visibility="collapsed")

if view_mode == "Calendar":
    if "journal_year" not in st.session_state:
        st.session_state.journal_year = date.today().year
    if "journal_month" not in st.session_state:
        st.session_state.journal_month = date.today().month

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("\u25c0 Prev", use_container_width=True):
            if st.session_state.journal_month == 1:
                st.session_state.journal_month = 12
                st.session_state.journal_year -= 1
            else:
                st.session_state.journal_month -= 1
            st.rerun()
    with col2:
        month_name = calendar.month_name[st.session_state.journal_month]
        st.markdown(f"<h3 style='text-align:center; color:#2C2C2C;'>{month_name} {st.session_state.journal_year}</h3>", unsafe_allow_html=True)
    with col3:
        if st.button("Next \u25b6", use_container_width=True):
            if st.session_state.journal_month == 12:
                st.session_state.journal_month = 1
                st.session_state.journal_year += 1
            else:
                st.session_state.journal_month += 1
            st.rerun()

    year = st.session_state.journal_year
    month = st.session_state.journal_month

    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    entries = db.get_entries_in_range(first_day.isoformat(), last_day.isoformat())
    entry_dates = {e["date"] for e in entries}
    entry_map = {e["date"]: e for e in entries}

    # Calendar header
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_cols = st.columns(7)
    for i, name in enumerate(day_names):
        header_cols[i].markdown(f"<div class='cal-header'>{name}</div>", unsafe_allow_html=True)

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)

    selected_date = None
    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown("<div class='cal-day'>&nbsp;</div>", unsafe_allow_html=True)
                else:
                    d = date(year, month, day)
                    d_str = d.isoformat()
                    if d_str in entry_dates:
                        if st.button(f"{day}", key=f"cal_{d_str}", use_container_width=True, type="primary"):
                            selected_date = d_str
                    else:
                        st.markdown(f"<div class='cal-day cal-empty'>{day}</div>", unsafe_allow_html=True)

    if selected_date and selected_date in entry_map:
        entry = entry_map[selected_date]
        st.markdown(f"""
        <div class="entry-card" style="margin-top:16px;">
            <div style="font-size:16px; font-weight:600; color:#4A3728; margin-bottom:8px;">
                {selected_date}
            </div>
            <div style="font-size:14px; color:#555; line-height:1.8;">
                \U0001f64f <b>Prayer:</b> {format_prayer_duration(entry['prayer_minutes'])}<br/>
                \U0001f4d6 <b>Reading:</b> {entry.get('chapters_display', 'N/A')}<br/>
                {"\U0001f3a7 <b>Sermon:</b> " + entry['sermon_title'] + (" - " + entry['sermon_speaker'] if entry.get('sermon_speaker') else "") + "<br/>" if entry.get('sermon_title') else ""}
                {"\U0001f517 " + entry['youtube_link'] + "<br/>" if entry.get('youtube_link') else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # List view
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("From", value=date.today() - timedelta(days=30))
    with col2:
        end = st.date_input("To", value=date.today())

    entries = db.get_entries_in_range(start.isoformat(), end.isoformat())

    if not entries:
        st.markdown("""
        <div style="text-align:center; padding:40px; color:#ccc;">
            <div style="font-size:48px; margin-bottom:8px;">\U0001f4c5</div>
            <div style="font-size:16px; color:#999;">No entries found</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for entry in entries:
            duration = format_prayer_duration(entry["prayer_minutes"])
            reading = entry.get("chapters_display", "N/A")
            report_icon = "\u2705" if entry.get("report_copied") else "\u23f3"

            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:600; color:#4A3728;">{entry['date']}</span>
                    <span style="font-size:12px; color:#999;">{report_icon} Report</span>
                </div>
                <div style="font-size:14px; color:#666; margin-top:6px; line-height:1.6;">
                    Prayer: {duration} &bull; Reading: {reading}
                    {"&bull; " + entry['sermon_title'] if entry.get('sermon_title') else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
