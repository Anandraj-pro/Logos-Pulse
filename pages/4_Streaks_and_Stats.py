import streamlit as st
from datetime import date, timedelta
import calendar
import json
from modules import db
from modules.utils import calculate_streaks, format_prayer_duration

db.init_db()

# ==================== CSS ====================
st.markdown("""
<style>
    .streak-hero {
        background: linear-gradient(135deg, #FF6B35 0%, #F7C948 100%);
        border-radius: 16px;
        padding: 32px 28px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    .streak-num {
        font-size: 64px;
        font-weight: 800;
        line-height: 1;
    }
    .streak-label {
        font-size: 14px;
        color: rgba(255,255,255,0.8);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }
    .stat-card {
        background: white;
        border: 1px solid #F0EBF8;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        line-height: 1;
    }
    .stat-label {
        font-size: 12px;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
    }
    .heatmap-day {
        text-align: center;
        border-radius: 8px;
        padding: 6px 4px;
        font-size: 13px;
        font-weight: 500;
        margin: 2px;
    }
    .heatmap-done {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: 700;
    }
    .heatmap-missed {
        background: #FFEBEE;
        color: #FFAB91;
    }
    .heatmap-future {
        color: #ddd;
    }
    .heatmap-header {
        text-align: center;
        font-size: 11px;
        color: #999;
        font-weight: 600;
        text-transform: uppercase;
        padding: 4px;
    }
</style>
""", unsafe_allow_html=True)

# --- Data ---
all_dates = db.get_all_entry_dates()
current_streak, longest_streak = calculate_streaks(all_dates)

# ==================== STREAK HERO ====================
col1, col2 = st.columns(2)
with col1:
    streak_emoji = "\U0001f525" if current_streak >= 7 else "\u2b50" if current_streak >= 3 else "\U0001f331"
    st.markdown(f"""
    <div class="streak-hero">
        <div style="font-size:40px; margin-bottom:4px;">{streak_emoji}</div>
        <div class="streak-num">{current_streak}</div>
        <div class="streak-label">Day Streak</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="streak-hero" style="background:linear-gradient(135deg, #667eea, #764ba2);">
        <div style="font-size:40px; margin-bottom:4px;">\U0001f3c6</div>
        <div class="streak-num">{longest_streak}</div>
        <div class="streak-label">Best Streak</div>
    </div>
    """, unsafe_allow_html=True)

if current_streak in [7, 30, 50, 100, 365]:
    st.balloons()
    st.success(f"Congratulations! {current_streak}-day streak!")

# ==================== MONTHLY HEATMAP ====================
st.markdown("""
<div style="font-size:12px; color:#999; text-transform:uppercase; letter-spacing:1.5px;
            font-weight:600; margin:16px 0 8px 0;">
    Monthly Activity
</div>
""", unsafe_allow_html=True)

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
    st.markdown(f"<h3 style='text-align:center; color:#2C2C2C;'>{month_name} {st.session_state.stats_year}</h3>", unsafe_allow_html=True)
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
st.markdown("""
<div style="font-size:12px; color:#999; text-transform:uppercase; letter-spacing:1.5px;
            font-weight:600; margin:24px 0 12px 0;">
    Monthly Summary
</div>
""", unsafe_allow_html=True)

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
    pct_color = "#4CAF50" if completion_pct >= 80 else "#FF9800" if completion_pct >= 50 else "#E91E63"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:{pct_color};">{completion_pct}%</div>
        <div class="stat-label">Completion</div>
        <div style="font-size:11px; color:#bbb; margin-top:2px;">{days_logged}/{days_passed} days</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#667eea;">{total_prayer_hours}</div>
        <div class="stat-label">Prayer Hours</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#764ba2;">{total_chapters}</div>
        <div class="stat-label">Chapters Read</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    sermons_count = sum(1 for e in entries if e.get("sermon_title"))
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#FF9800;">{sermons_count}</div>
        <div class="stat-label">Sermons</div>
    </div>
    """, unsafe_allow_html=True)
