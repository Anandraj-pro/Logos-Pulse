import streamlit as st
from datetime import date, timedelta
import calendar
import json
from modules import db
from modules.utils import format_prayer_duration
from modules.styles import inject_styles, page_header, empty_state, spacer
from modules.auth import require_login, require_password_changed

require_login()
require_password_changed()

db.init_db()

inject_styles()

all_dates = db.get_all_entry_dates()

page_header("\U0001f4c5", "Daily Log", f"{len(all_dates)} entries recorded")

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
        st.markdown(f"<h3 style='text-align:center;'>{month_name} {st.session_state.journal_year}</h3>", unsafe_allow_html=True)
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
            <div style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438; margin-bottom:8px;">
                {selected_date}
            </div>
            <div style="font-size:14px; color:#6B6580; line-height:1.8;">
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
        empty_state("\U0001f4c5", "No entries found")
    else:
        for entry in entries:
            duration = format_prayer_duration(entry["prayer_minutes"])
            reading = entry.get("chapters_display", "N/A")
            report_icon = "\u2705" if entry.get("report_copied") else "\u23f3"

            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-family:'DM Serif Display',Georgia,serif; font-weight:400; color:#2A2438;">{entry['date']}</span>
                    <span style="font-size:12px; color:#9E96AB;">{report_icon} Report</span>
                </div>
                <div style="font-size:14px; color:#6B6580; margin-top:6px; line-height:1.6;">
                    Prayer: {duration} &bull; Reading: {reading}
                    {"&bull; " + entry['sermon_title'] if entry.get('sermon_title') else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)