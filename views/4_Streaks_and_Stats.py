import streamlit as st
from datetime import date, timedelta
import calendar
import json
from modules import db
from modules.utils import calculate_streaks, format_prayer_duration
from modules.styles import inject_styles, section_label, spacer
from modules.auth import require_login, require_password_changed

require_login()
require_password_changed()
inject_styles()

# --- Data ---
all_dates = db.get_all_entry_dates()
current_streak, longest_streak = calculate_streaks(all_dates)

# ==================== STREAK HERO ====================
col1, col2 = st.columns(2)
with col1:
    streak_emoji = "\U0001f525" if current_streak >= 7 else "\u2b50" if current_streak >= 3 else "\U0001f331"
    st.markdown(f"""
    <div class="streak-hero" style="background:linear-gradient(135deg, #E85D3A 0%, #D4A843 100%);">
        <div style="font-size:40px; margin-bottom:4px;">{streak_emoji}</div>
        <div class="streak-num">{current_streak}</div>
        <div class="streak-label">Day Streak</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="streak-hero" style="background:linear-gradient(135deg, #5B4FC4, #9B5FA8);">
        <div style="font-size:40px; margin-bottom:4px;">\U0001f3c6</div>
        <div class="streak-num">{longest_streak}</div>
        <div class="streak-label">Best Streak</div>
    </div>
    """, unsafe_allow_html=True)

if current_streak in [7, 30, 50, 100, 365]:
    st.balloons()
    st.success(f"Congratulations! {current_streak}-day streak!")

# ==================== MONTHLY HEATMAP ====================
section_label("Monthly Activity")

if "stats_year" not in st.session_state:
    st.session_state.stats_year = date.today().year
if "stats_month" not in st.session_state:
    st.session_state.stats_month = date.today().month

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("\u25c0 Prev", key="stats_prev", use_container_width=True):
        if st.session_state.stats_month == 1:
            st.session_state.stats_month = 12
            st.session_state.stats_year -= 1
        else:
            st.session_state.stats_month -= 1
        st.rerun()
with col2:
    month_name = calendar.month_name[st.session_state.stats_month]
    st.markdown(f"<h3 style='text-align:center;'>{month_name} {st.session_state.stats_year}</h3>", unsafe_allow_html=True)
with col3:
    if st.button("Next \u25b6", key="stats_next", use_container_width=True):
        if st.session_state.stats_month == 12:
            st.session_state.stats_month = 1
            st.session_state.stats_year += 1
        else:
            st.session_state.stats_month += 1
        st.rerun()

year = st.session_state.stats_year
month = st.session_state.stats_month

first_day = date(year, month, 1)
last_day = date(year, month, calendar.monthrange(year, month)[1])
entries = db.get_entries_in_range(first_day.isoformat(), last_day.isoformat())
entry_dates = {e["date"] for e in entries}

# Calendar header
day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
header_cols = st.columns(7)
for i, name in enumerate(day_names):
    header_cols[i].markdown(f"<div class='heatmap-header'>{name}</div>", unsafe_allow_html=True)

# Calendar grid
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
                if d_str in entry_dates:
                    st.markdown(f"<div class='heatmap-day heatmap-done'>{day}</div>", unsafe_allow_html=True)
                elif d <= date.today():
                    st.markdown(f"<div class='heatmap-day heatmap-missed'>{day}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='heatmap-day heatmap-future'>{day}</div>", unsafe_allow_html=True)

# ==================== MONTHLY SUMMARY ====================
section_label("Monthly Summary")

days_in_month = calendar.monthrange(year, month)[1]
days_passed = min(date.today().day, days_in_month) if year == date.today().year and month == date.today().month else days_in_month
days_logged = len(entries)
completion_pct = int(days_logged / days_passed * 100) if days_passed > 0 else 0

total_prayer_minutes = sum(e["prayer_minutes"] for e in entries)
total_prayer_hours = round(total_prayer_minutes / 60, 1)

total_chapters = 0
for e in entries:
    if e.get("chapters_read"):
        chs = json.loads(e["chapters_read"]) if isinstance(e["chapters_read"], str) else e["chapters_read"]
        total_chapters += len(chs)

col1, col2, col3, col4 = st.columns(4)

with col1:
    pct_color = "#3A8F5C" if completion_pct >= 80 else "#D4853A" if completion_pct >= 50 else "#C44B5B"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:{pct_color};">{completion_pct}%</div>
        <div class="stat-label">Completion</div>
        <div style="font-size:11px; color:#C0B8CC; margin-top:2px;">{days_logged}/{days_passed} days</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#5B4FC4;">{total_prayer_hours}</div>
        <div class="stat-label">Prayer Hours</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#9B5FA8;">{total_chapters}</div>
        <div class="stat-label">Chapters Read</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    sermons_count = sum(1 for e in entries if e.get("sermon_title"))
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#D4853A;">{sermons_count}</div>
        <div class="stat-label">Sermons</div>
    </div>
    """, unsafe_allow_html=True)