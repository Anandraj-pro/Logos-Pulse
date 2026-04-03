import streamlit as st
from datetime import date, timedelta
import calendar
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_login, require_password_changed
from modules import db

require_login()
require_password_changed()
inject_styles()

page_header("\U0001f374", "Fasting Tracker", "Track your fasting journey")

fasting_dates = db.get_fasting_dates()
fasting_log = db.get_fasting_log(limit=60)

# Stats
total_fasts = len(fasting_dates)
this_month = sum(1 for d in fasting_dates if d.startswith(date.today().strftime("%Y-%m")))

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#5B4FC4;">{total_fasts}</div>
        <div class="stat-label">Total Fasting Days</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#D4853A;">{this_month}</div>
        <div class="stat-label">This Month</div>
    </div>
    """, unsafe_allow_html=True)

spacer()

tab_log, tab_calendar = st.tabs(["\U0001f374 Log Fast", "\U0001f4c5 Calendar"])

# ==================== LOG FAST ====================
with tab_log:
    with st.form("log_fast_form"):
        f_date = st.date_input("Date", value=date.today(), max_value=date.today())
        f_type = st.selectbox("Fast Type", ["Full Day", "Partial", "Daniel Fast"])
        f_notes = st.text_input("Notes (optional)", placeholder="e.g., Prayed for healing during fast")
        f_submit = st.form_submit_button("Log Fast", type="primary", use_container_width=True)

    if f_submit:
        db.log_fast(f_date.isoformat(), f_type, f_notes.strip())
        st.success(f"Fast logged for {f_date.isoformat()}!")
        st.rerun()

    # Recent fasts
    spacer()
    section_label("Recent Fasts")

    if not fasting_log:
        empty_state("\U0001f374", "No fasts logged yet", "Log your first fast above!")
    else:
        type_colors = {"Full Day": "#5B4FC4", "Partial": "#D4853A", "Daniel Fast": "#3A8F5C"}
        for f in fasting_log[:15]:
            fc = type_colors.get(f.get("fast_type", ""), "#5B4FC4")
            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-family:'DM Serif Display',Georgia,serif; color:#2A2438;">{f['date']}</span>
                    <span style="background:{fc}20; color:{fc}; padding:2px 10px;
                                 border-radius:10px; font-size:11px; font-weight:600;">
                        {f.get('fast_type', 'Fast')}
                    </span>
                </div>
                {"<div style='font-size:13px; color:#6B6580; margin-top:4px;'>" + f['notes'] + "</div>" if f.get('notes') else ""}
            </div>
            """, unsafe_allow_html=True)

# ==================== CALENDAR ====================
with tab_calendar:
    fasting_dates_set = set(fasting_dates)

    today = date.today()
    year = today.year
    month = today.month

    month_name = calendar.month_name[month]
    st.markdown(f"<h3 style='text-align:center;'>{month_name} {year}</h3>", unsafe_allow_html=True)

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_cols = st.columns(7)
    for i, name in enumerate(day_names):
        header_cols[i].markdown(f"<div class='cal-header'>{name}</div>", unsafe_allow_html=True)

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)

    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown("<div class='heatmap-day'>&nbsp;</div>", unsafe_allow_html=True)
                else:
                    d = date(year, month, day)
                    d_str = d.isoformat()
                    if d_str in fasting_dates_set:
                        st.markdown(f"<div class='heatmap-day' style='background:linear-gradient(135deg, #D4853A, #E85D3A); color:white; font-weight:700;'>{day}</div>", unsafe_allow_html=True)
                    elif d <= today:
                        st.markdown(f"<div class='heatmap-day cal-empty'>{day}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='heatmap-day heatmap-future'>{day}</div>", unsafe_allow_html=True)
