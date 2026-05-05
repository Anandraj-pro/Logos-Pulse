import streamlit as st
from datetime import date, timedelta
import calendar
import json
import plotly.graph_objects as go
from modules import db
from modules.utils import calculate_streaks, format_prayer_duration
from modules.styles import inject_styles, section_label, spacer
from modules.auth import require_login, require_password_changed

from modules.auth import get_current_user_id

require_login()
require_password_changed()
inject_styles()

# ==================== GROWTH SCORE ====================
try:
    from modules.growth_score import calculate_growth_score
    score = calculate_growth_score(get_current_user_id())

    st.markdown(f"""
    <div class="entry-card" style="text-align:center; padding:24px; border:2px solid #D4A843;">
        <span style="font-size:48px;">{score['level_emoji']}</span>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:36px; color:#2A2438; margin:8px 0;">
            {score['total']}<span style="font-size:16px; color:#9E96AB;">/100</span>
        </div>
        <div style="font-size:16px; color:#D4A843; font-weight:600;">{score['level_name']}</div>
        <div style="font-size:13px; color:#9E96AB; margin-top:4px;">{score['level_desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    spacer()

    # Component breakdown
    section_label("Score Breakdown")
    components = [
        ("Consistency", score["consistency"], "#5B4FC4", "40%"),
        ("Quantity", score["quantity"], "#3A8F5C", "30%"),
        ("Diversity", score["diversity"], "#9B5FA8", "20%"),
        ("Engagement", score["engagement"], "#D4853A", "10%"),
    ]

    for name, value, color, weight in components:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
            <div style="width:100px; font-size:13px; color:#6B6580; font-weight:500;">{name} <span style="color:#C0B8CC;">({weight})</span></div>
            <div style="flex:1;">
                <div class="progress-bar-bg" style="height:8px;">
                    <div style="height:100%; width:{value}%; background:{color}; border-radius:8px;"></div>
                </div>
            </div>
            <div style="width:40px; text-align:right; font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:{color};">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    spacer()
except Exception:
    pass

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

# ── Bible Annotations ──
try:
    from modules.db import get_bookmark_count, get_highlight_count
    _bm_count = get_bookmark_count()
    _hl_count = get_highlight_count()
    if _bm_count > 0 or _hl_count > 0:
        spacer(4)
        _bm_col, _hl_col = st.columns(2)
        with _bm_col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color:#2196F3;">{_bm_count}</div>
                <div class="stat-label">Verses Bookmarked</div>
            </div>
            """, unsafe_allow_html=True)
        with _hl_col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color:#F4C430;">{_hl_count}</div>
                <div class="stat-label">Verses Highlighted</div>
            </div>
            """, unsafe_allow_html=True)
except Exception:
    pass

# ==================== CHARTS ====================
spacer()

# Fetch last 30 days of data for charts
chart_start = (date.today() - timedelta(days=29)).isoformat()
chart_end = date.today().isoformat()
chart_entries = db.get_entries_in_range(chart_start, chart_end)

if chart_entries:
    # Build daily data map
    entry_by_date = {e["date"]: e for e in chart_entries}

    # --- Prayer Time Trend (30 days) ---
    section_label("Prayer Time \u2014 Last 30 Days")

    dates_30 = []
    prayer_mins = []
    for i in range(30):
        d = date.today() - timedelta(days=29 - i)
        d_str = d.isoformat()
        dates_30.append(d.strftime("%b %d"))
        e = entry_by_date.get(d_str)
        prayer_mins.append(e["prayer_minutes"] if e else 0)

    fig_prayer = go.Figure()
    fig_prayer.add_trace(go.Bar(
        x=dates_30,
        y=prayer_mins,
        marker_color=["#5B4FC4" if m > 0 else "#EDE8F5" for m in prayer_mins],
        marker_line_width=0,
        hovertemplate="%{x}<br>%{y} min<extra></extra>",
    ))
    # Add goal line
    prayer_goal = int(db.get_all_settings().get("default_prayer_minutes", "60"))
    fig_prayer.add_hline(
        y=prayer_goal, line_dash="dot", line_color="#D4853A",
        annotation_text=f"Goal: {prayer_goal} min",
        annotation_position="top right",
        annotation_font_color="#D4853A",
    )
    fig_prayer.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#9E96AB"), dtick=5),
        yaxis=dict(showgrid=True, gridcolor="#EDE8F5", tickfont=dict(size=10, color="#9E96AB"), title="Minutes"),
        bargap=0.3,
    )
    st.plotly_chart(fig_prayer, use_container_width=True)

    # --- Chapters Read Per Week (4 weeks) ---
    section_label("Chapters Read \u2014 Weekly")

    week_labels = []
    week_chapters = []
    for w in range(4):
        w_end = date.today() - timedelta(days=w * 7)
        w_start = w_end - timedelta(days=6)
        label = f"{w_start.strftime('%b %d')}"
        week_labels.append(label)

        ch_count = 0
        for i in range(7):
            d = w_start + timedelta(days=i)
            e = entry_by_date.get(d.isoformat())
            if e and e.get("chapters_read"):
                chs = json.loads(e["chapters_read"]) if isinstance(e["chapters_read"], str) else e["chapters_read"]
                ch_count += len(chs)
        week_chapters.append(ch_count)

    week_labels.reverse()
    week_chapters.reverse()

    fig_chapters = go.Figure()
    fig_chapters.add_trace(go.Bar(
        x=week_labels,
        y=week_chapters,
        marker_color="#9B5FA8",
        marker_line_width=0,
        text=week_chapters,
        textposition="outside",
        textfont=dict(size=12, color="#9B5FA8", family="DM Sans"),
        hovertemplate="%{x}<br>%{y} chapters<extra></extra>",
    ))
    fig_chapters.update_layout(
        height=220,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color="#9E96AB")),
        yaxis=dict(showgrid=True, gridcolor="#EDE8F5", tickfont=dict(size=10, color="#9E96AB"), title="Chapters"),
        bargap=0.4,
    )
    st.plotly_chart(fig_chapters, use_container_width=True)

    # --- Weekly Consistency (donut) ---
    section_label("This Week's Consistency")

    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    days_so_far = min(today.weekday() + 1, 6)  # Mon-Sat
    days_logged_week = sum(
        1 for i in range(days_so_far)
        if (week_start + timedelta(days=i)).isoformat() in entry_by_date
    )
    days_missed = days_so_far - days_logged_week

    fig_donut = go.Figure()
    fig_donut.add_trace(go.Pie(
        values=[days_logged_week, days_missed],
        labels=["Logged", "Missed"],
        hole=0.65,
        marker=dict(colors=["#5B4FC4", "#EDE8F5"]),
        textinfo="none",
        hovertemplate="%{label}: %{value} day(s)<extra></extra>",
    ))
    fig_donut.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        annotations=[dict(
            text=f"<b>{days_logged_week}/{days_so_far}</b>",
            x=0.5, y=0.5, font_size=22, font_color="#5B4FC4",
            font_family="DM Serif Display, Georgia, serif",
            showarrow=False,
        )],
    )

    col_donut, col_legend = st.columns([1, 2])
    with col_donut:
        st.plotly_chart(fig_donut, use_container_width=True)
    with col_legend:
        pct_week = int(days_logged_week / days_so_far * 100) if days_so_far > 0 else 0
        pct_color = "#3A8F5C" if pct_week >= 80 else "#D4853A" if pct_week >= 50 else "#C44B5B"
        st.markdown(f"""
        <div style="padding-top:24px;">
            <div style="font-family:'DM Serif Display',Georgia,serif; font-size:32px; color:{pct_color};">
                {pct_week}%
            </div>
            <div style="font-size:13px; color:#9E96AB; margin-top:4px;">
                {days_logged_week} of {days_so_far} days logged this week
            </div>
            <div style="font-size:12px; color:#C0B8CC; margin-top:8px;">
                {"Keep it up!" if pct_week >= 80 else "You can do it \u2014 stay consistent!" if pct_week >= 50 else "Don't give up \u2014 every day counts!"}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    spacer()
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">\U0001f4ca</div>
        <div class="empty-state-title">No data yet for charts</div>
        <div class="empty-state-sub">Start logging daily entries to see your trends</div>
    </div>
    """, unsafe_allow_html=True)