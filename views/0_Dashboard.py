import streamlit as st
import html as _html
import plotly.graph_objects as go
from datetime import date, timedelta, datetime
from modules import db
from modules.utils import calculate_streaks, format_prayer_duration, format_chapters_display
from modules.styles import inject_styles, section_label, spacer
from modules.auth import require_login, require_password_changed, get_current_user_id
from modules.bible_data import get_book_names, get_chapter_count
import json

require_login()
require_password_changed()

# --- Load Data ---
settings = db.get_all_settings()
greeting_name = st.session_state.get("preferred_name") or settings.get("greeting_name", "User")
today_str = date.today().isoformat()
today_entry = db.get_entry_by_date(today_str)

all_dates = db.get_all_entry_dates()
current_streak, longest_streak = calculate_streaks(all_dates)

today = date.today()
monday = today - timedelta(days=today.weekday())
saturday = monday + timedelta(days=5)
week_entries = db.get_entries_in_range(monday.isoformat(), saturday.isoformat())
week_count = len(week_entries)

assignment = db.get_active_assignment()
sermon_notes = db.get_all_sermon_notes()
prayer_categories = db.get_prayer_categories()

# Yesterday's entry
yesterday_str = (today - timedelta(days=1)).isoformat()
yesterday_entry = db.get_entry_by_date(yesterday_str)

# Count prayers per category
prayer_counts = {}
for cat in prayer_categories:
    prayers = db.get_prayers_by_category(cat["id"])
    prayer_counts[cat["id"]] = {
        "total": len(prayers),
        "ongoing": sum(1 for p in prayers if p.get("status") == "ongoing"),
        "answered": sum(1 for p in prayers if p.get("status") == "answered"),
    }

hour = datetime.now().hour
if hour < 12:
    greeting = "Good Morning"
elif hour < 17:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

formatted_date = today.strftime("%A, %B %d, %Y")

# ==================== STYLES ====================
inject_styles()

# ==================== ANNOUNCEMENTS BANNER ====================
from modules.auth import get_current_role
_announcements = db.get_active_announcements(role=get_current_role())
for _ann in _announcements[:3]:
    _ann_title = _html.escape(_ann.get('title', '') or '')
    _ann_msg = _html.escape(_ann.get('message', '') or '')
    col_ann, col_dismiss = st.columns([10, 1])
    with col_ann:
        st.markdown(f"""
        <div class="announcement-card">
            <div class="announcement-title">&#128226; {_ann_title}</div>
            <div class="announcement-body">{_ann_msg}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_dismiss:
        if st.button("\u2716", key=f"dismiss_{_ann['id']}", help="Dismiss this announcement", use_container_width=True):
            db.dismiss_announcement(_ann["id"])
            st.rerun()

# ==================== Q2: 365 DAILY VERSES ====================
VERSES = [
    ("Proverbs 3:5-6", "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight."),
    ("Philippians 4:13", "I can do all things through Christ who strengthens me."),
    ("Jeremiah 29:11", "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future."),
    ("Isaiah 40:31", "But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary."),
    ("Psalm 23:1", "The Lord is my shepherd; I shall not want."),
    ("Romans 8:28", "And we know that in all things God works for the good of those who love him, who have been called according to his purpose."),
    ("Joshua 1:9", "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go."),
    ("Psalm 46:10", "Be still, and know that I am God."),
    ("Matthew 6:33", "But seek first his kingdom and his righteousness, and all these things will be given to you as well."),
    ("Isaiah 41:10", "So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you."),
    ("Psalm 119:105", "Your word is a lamp for my feet, a light on my path."),
    ("Romans 12:2", "Do not conform to the pattern of this world, but be transformed by the renewing of your mind."),
    ("Philippians 4:6-7", "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God."),
    ("2 Timothy 1:7", "For the Spirit God gave us does not make us timid, but gives us power, love and self-discipline."),
    ("Psalm 27:1", "The Lord is my light and my salvation \u2014 whom shall I fear?"),
    ("Hebrews 11:1", "Now faith is confidence in what we hope for and assurance about what we do not see."),
    ("Colossians 3:23", "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters."),
    ("Psalm 37:4", "Take delight in the Lord, and he will give you the desires of your heart."),
    ("1 Corinthians 10:13", "No temptation has overtaken you except what is common to mankind. And God is faithful; he will not let you be tempted beyond what you can bear."),
    ("James 1:5", "If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault, and it will be given to you."),
    ("Galatians 5:22-23", "But the fruit of the Spirit is love, joy, peace, forbearance, kindness, goodness, faithfulness, gentleness and self-control."),
    ("Psalm 91:1-2", "Whoever dwells in the shelter of the Most High will rest in the shadow of the Almighty. I will say of the Lord, He is my refuge and my fortress."),
    ("Matthew 11:28", "Come to me, all you who are weary and burdened, and I will give you rest."),
    ("Ephesians 6:10", "Finally, be strong in the Lord and in his mighty power."),
    ("Psalm 34:8", "Taste and see that the Lord is good; blessed is the one who takes refuge in him."),
    ("1 John 4:4", "You, dear children, are from God and have overcome them, because the one who is in you is greater than the one who is in the world."),
    ("Proverbs 18:10", "The name of the Lord is a fortified tower; the righteous run to it and are safe."),
    ("Deuteronomy 31:6", "Be strong and courageous. Do not be afraid or terrified because of them, for the Lord your God goes with you; he will never leave you nor forsake you."),
    ("Psalm 139:14", "I praise you because I am fearfully and wonderfully made; your works are wonderful, I know that full well."),
    ("Romans 15:13", "May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit."),
    ("Isaiah 26:3", "You will keep in perfect peace those whose minds are steadfast, because they trust in you."),
]
verse_ref, verse_text = VERSES[today.timetuple().tm_yday % len(VERSES)]

st.markdown(f"""
<div class="hero-section">
    <div class="hero-greeting">{greeting}</div>
    <div class="hero-name">{greeting_name}</div>
    <div class="hero-date">{formatted_date}</div>
    <div class="hero-verse">
        \u201c{verse_text}\u201d
        <br/><span style="font-style:normal; font-size:12px; color:rgba(255,255,255,0.45);">\u2014 {verse_ref}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== Q9: STREAK MILESTONE MESSAGE ====================
milestone_msgs = {
    3: "\U0001f331 3 days! A new habit is forming.",
    7: "\U0001f525 7-day streak! You're building discipline.",
    14: "\u2b50 2 weeks strong! Your consistency is inspiring.",
    21: "\U0001f4aa 21 days! They say it takes 21 days to build a habit. You did it!",
    30: "\U0001f3c6 30-day streak! A full month of faithfulness.",
    50: "\U0001f451 50 days! Half a century of devotion.",
    100: "\U0001f31f 100 days! What an incredible journey of faith.",
    365: "\U0001f389 ONE YEAR! 365 days of walking with God. Extraordinary.",
}
if current_streak in milestone_msgs:
    st.balloons()
    st.markdown(f"""
    <div class="goal-banner" style="text-align:center; font-size:16px;">
        {milestone_msgs[current_streak]}
    </div>
    """, unsafe_allow_html=True)

# ==================== GROWTH SCORE + STREAK METRICS ====================
try:
    from modules.growth_score import calculate_growth_score
    _score = calculate_growth_score(get_current_user_id())
    st.markdown(f"""
    <div class="entry-card" style="text-align:center; padding:16px; border-left:4px solid #D4A843; margin-bottom:16px;">
        <div style="display:flex; justify-content:center; align-items:center; gap:12px;">
            <span style="font-size:36px;">{_score['level_emoji']}</span>
            <div style="text-align:left;">
                <div style="font-family:'DM Serif Display',Georgia,serif; font-size:28px; color:#2A2438;">
                    {_score['total']}<span style="font-size:14px; color:#9E96AB;">/100</span>
                </div>
                <div style="font-size:13px; color:#D4A843; font-weight:600;">{_score['level_name']}</div>
                <div style="font-size:11px; color:#9E96AB;">{_score['level_desc']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
except Exception:
    pass

col1, col2, col3 = st.columns(3)

with col1:
    streak_color = "#3A8F5C" if current_streak >= 7 else "#D4853A" if current_streak >= 3 else "#5B4FC4"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{streak_color};">{current_streak}</div>
        <div class="metric-label">Day Streak</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#5B4FC4;">{longest_streak}</div>
        <div class="metric-label">Best Streak</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    week_color = "#3A8F5C" if week_count >= 5 else "#D4853A" if week_count >= 3 else "#C44B5B"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{week_color};">{week_count}<span style="font-size:18px; color:#D0C8DB;">/6</span></div>
        <div class="metric-label">This Week</div>
    </div>
    """, unsafe_allow_html=True)

# ── 7-day activity sparkline ─────────────────────────────────
try:
    _spark_days = 7
    _spark_labels, _spark_prayer, _spark_chapters = [], [], []
    _spark_logged = []
    for _d in range(_spark_days - 1, -1, -1):
        _day = date.today() - timedelta(days=_d)
        _spark_labels.append(_day.strftime("%a"))
        _e = db.get_entry_by_date(_day.isoformat())
        _spark_prayer.append(_e.get("prayer_minutes", 0) if _e else 0)
        _spark_chapters.append(len(json.loads(_e["chapters_read"]) if _e and _e.get("chapters_read") and isinstance(_e["chapters_read"], str) else (_e.get("chapters_read") or [])) if _e else 0)
        _spark_logged.append(1 if _e else 0)

    _fig = go.Figure()
    _bar_colors = ["#5B4FC4" if v else "#EDE8F5" for v in _spark_logged]
    _fig.add_trace(go.Bar(
        x=_spark_labels, y=_spark_prayer,
        marker_color=_bar_colors,
        hovertemplate="%{x}<br>%{y} min prayer<extra></extra>",
        name="Prayer (min)",
    ))
    _fig.update_layout(
        height=90,
        margin=dict(l=0, r=0, t=4, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#9E96AB"), fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        bargap=0.3,
    )
    st.markdown('<div style="margin-top:8px; margin-bottom:2px; font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:1px;">Last 7 days — prayer minutes</div>', unsafe_allow_html=True)
    st.plotly_chart(_fig, use_container_width=True, config={"displayModeBar": False})
except Exception:
    pass

spacer()

# ==================== TODAY'S STATUS + Q1: QUICK LOG ====================
if today_entry:
    duration = format_prayer_duration(today_entry["prayer_minutes"])
    reading = today_entry.get("chapters_display", "N/A")
    sermon = today_entry.get("sermon_title", "")
    report_status = "Copied" if today_entry.get("report_copied") else "Not yet copied"
    report_color = "#3A8F5C" if today_entry.get("report_copied") else "#D4853A"

    details = f"Prayer: {duration} &nbsp;&bull;&nbsp; Reading: {reading}"
    if sermon:
        details += f" &nbsp;&bull;&nbsp; Sermon: {sermon}"

    st.markdown(f"""
    <div class="today-card today-done">
        <div class="today-title" style="color:#3A8F5C;">
            \u2705 Today\u2019s Entry Complete
        </div>
        <div class="today-detail">{details}</div>
        <div style="margin-top:8px;">
            <span style="font-size:12px; color:{report_color}; font-weight:500;">
                WhatsApp Report: {report_status}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Pending card with streak warning
    streak_msg = (
        f"You have a <b>{current_streak}-day streak</b> going \u2014 don\u2019t break it!"
        if current_streak > 0
        else "Start your spiritual journey today."
    )
    st.markdown(f"""
    <div class="today-card today-pending">
        <div class="today-title" style="color:#D4853A;">
            \u23f0 Today\u2019s Entry Pending
        </div>
        <div class="today-detail">{streak_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    # Q1: Quick Log Form
    with st.expander("\u26a1 Quick Log \u2014 Log in seconds", expanded=True):
        with st.form("quick_log_form"):
            ql_col1, ql_col2 = st.columns(2)
            with ql_col1:
                default_prayer = int(settings.get("default_prayer_minutes", "60"))
                prayer_options = list(range(15, 195, 15))
                ql_prayer = st.select_slider(
                    "Prayer (min)", options=prayer_options,
                    value=default_prayer if default_prayer in prayer_options else 60,
                )
            with ql_col2:
                book_names = get_book_names()
                ql_book = st.selectbox("Book", options=book_names,
                                       index=book_names.index("Psalms") if "Psalms" in book_names else 0)

            max_ch = get_chapter_count(ql_book)
            ql_chapters = st.multiselect("Chapters read", options=list(range(1, max_ch + 1)))

            ql_fasted = st.checkbox("I fasted today")

            ql_submit = st.form_submit_button("\u26a1 Save Quick Entry", type="primary", use_container_width=True)

        if ql_submit:
            if not ql_chapters:
                st.error("Please select at least one chapter.")
            else:
                chapters_display = format_chapters_display(ql_book, ql_chapters)
                db.upsert_daily_entry(
                    entry_date=today_str, prayer_minutes=ql_prayer,
                    bible_book=ql_book, chapters_read=sorted(ql_chapters),
                    chapters_display=chapters_display,
                    sermon_title="", sermon_speaker="", youtube_link="",
                )
                st.success("Entry logged!")
                st.rerun()

# ==================== Q5: YESTERDAY'S SUMMARY ====================
if yesterday_entry:
    y_duration = format_prayer_duration(yesterday_entry["prayer_minutes"])
    y_reading = yesterday_entry.get("chapters_display", "N/A")
    st.markdown(f"""
    <div class="entry-card" style="border-left:3px solid #5B4FC4;">
        <div style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">
            Yesterday
        </div>
        <div style="font-size:14px; color:#6B6580; margin-top:4px;">
            Prayer: {y_duration} &nbsp;&bull;&nbsp; Reading: {y_reading}
            {"&nbsp;&bull;&nbsp; Sermon: " + yesterday_entry['sermon_title'] if yesterday_entry.get('sermon_title') else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== READING PLAN CARD ====================
try:
    from modules.db import get_member_active_plan, get_plan_days
    _active_plan = get_member_active_plan(get_current_user_id())
    if _active_plan and not _active_plan.get("completed_at"):
        _rp = _active_plan.get("reading_plans") or {}
        _total = _rp.get("total_days", 0)
        _current = _active_plan.get("current_day", 1)
        _done = _current - 1
        _pct = int(_done / _total * 100) if _total > 0 else 0
        _pct_color = "#3A8F5C" if _pct >= 70 else "#D4853A" if _pct >= 30 else "#5B4FC4"
        _plan_days = get_plan_days(_active_plan["plan_id"])
        _today_day = next((d for d in _plan_days if d["day_number"] == _current), None)

        _ch_label = ""
        if _today_day:
            cs, ce = _today_day["chapter_start"], _today_day["chapter_end"]
            _ch_label = f"Ch {cs}" if cs == ce else f"Ch {cs}–{ce}"

        st.markdown(f"""
        <div class="entry-card" style="border-left:4px solid {_pct_color};">
            <div style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">
                Reading Plan
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:4px;">
                <div>
                    <span style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438;">
                        \U0001f4d6 {_rp.get('name', 'Reading Plan')}
                    </span>
                    {f'<div style="font-size:13px; color:#5B4FC4; margin-top:2px;">Today: {_today_day["book"]} {_ch_label}</div>' if _today_day else ''}
                </div>
                <span style="font-size:12px; color:{_pct_color}; font-weight:600; white-space:nowrap; margin-left:12px;">
                    Day {_done}/{_total}
                </span>
            </div>
            <div class="progress-bar-bg" style="height:5px; margin-top:8px;">
                <div class="progress-bar-fill" style="width:{_pct}%; background:{_pct_color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("\U0001f4d6 Open Reading Plan", key="dash_open_plan"):
            st.switch_page("views/Bible_Reading_Plan.py")
        spacer(4)
except Exception:
    pass

# ==================== Q4: CONTINUE READING BOOKMARK ====================
try:
    from modules.supabase_client import get_admin_client
    _admin = get_admin_client()
    _profile = _admin.table("user_profiles") \
        .select("last_read_book, last_read_chapter") \
        .eq("user_id", get_current_user_id()) \
        .execute()
    if _profile.data and _profile.data[0].get("last_read_book"):
        _book = _profile.data[0]["last_read_book"]
        _ch = _profile.data[0]["last_read_chapter"] or 1
        st.markdown(f"""
        <div class="entry-card" style="border-left:3px solid #9B5FA8;">
            <div style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">
                Continue Reading
            </div>
            <div style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438; margin-top:4px;">
                \U0001f4d6 {_book} Chapter {_ch}
            </div>
        </div>
        """, unsafe_allow_html=True)
except Exception:
    pass

# ==================== WEEKLY READING PROGRESS ====================
if assignment:
    breakdown = json.loads(assignment["daily_breakdown"]) if isinstance(
        assignment["daily_breakdown"], str
    ) else assignment["daily_breakdown"]

    all_assigned = []
    for chapters in breakdown.values():
        all_assigned.extend(chapters)
    total_assigned = len(all_assigned)

    chapters_done = set()
    for entry in week_entries:
        if entry.get("bible_book") == assignment["book"] and entry.get("chapters_read"):
            read = json.loads(entry["chapters_read"]) if isinstance(
                entry["chapters_read"], str
            ) else entry["chapters_read"]
            chapters_done.update(read)

    done_count = len(chapters_done.intersection(set(all_assigned)))
    progress_pct = int((done_count / total_assigned * 100)) if total_assigned > 0 else 0

    st.markdown(f"""
    <div class="progress-section">
        <div class="progress-title">\U0001f4d6 Weekly Reading \u2014 {assignment['book']} {assignment['start_chapter']}\u2013{assignment['end_chapter']}</div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{progress_pct}%;"></div>
        </div>
        <div class="progress-label">{done_count}/{total_assigned} chapters completed ({progress_pct}%)</div>
    </div>
    """, unsafe_allow_html=True)

spacer(8)

# ==================== TODAY'S CONFESSIONS CARD ====================
try:
    confession_plans = db.get_my_confession_plans(status="active")
    if confession_plans:
        confession_count_today = db.get_confession_count_today()
        total_active = len(confession_plans)
        pending = total_active - confession_count_today

        if pending > 0:
            st.markdown(f"""
            <div class="today-card today-pending" style="cursor:pointer;">
                <div class="today-header">
                    <span class="today-icon">\u2720\ufe0f</span>
                    <span class="today-title">Today's Confessions</span>
                </div>
                <div class="today-detail">{pending} confession{"s" if pending != 1 else ""} waiting &middot; {confession_count_today} completed today</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start Confessing", key="dash_confess", type="primary"):
                st.switch_page("views/8_Prayer_Engine.py")
        else:
            st.markdown(f"""
            <div class="today-card today-done">
                <div class="today-header">
                    <span class="today-icon">\u2720\ufe0f</span>
                    <span class="today-title">Confessions Complete</span>
                </div>
                <div class="today-detail">All {total_active} confession{"s" if total_active != 1 else ""} done for today!</div>
            </div>
            """, unsafe_allow_html=True)
        spacer(8)
except Exception:
    pass  # Graceful fallback if prayer engine tables not yet created

# ==================== CONFESSION OF THE WEEK ====================
try:
    cotw = db.get_confession_of_the_week()
    if cotw:
        tpl = cotw.get("confession_templates") or {}
        cat = tpl.get("confession_categories") or {}
        cat_color = cat.get("color", "#5B4FC4")
        cat_icon = cat.get("icon", "✝️")
        cat_name = cat.get("name", "")
        tpl_name = tpl.get("name", "Confession of the Week")
        sermon_theme = cotw.get("sermon_theme", "")
        sermon_ref = cotw.get("sermon_reference", "")
        date_range = f"{cotw.get('start_date', '')} – {cotw.get('end_date', '')}"

        theme_line = ""
        if sermon_theme:
            theme_line += f'<div style="font-size:13px; color:#6B6580; margin-top:6px;">Theme: <b>{sermon_theme}</b>'
            if sermon_ref:
                theme_line += f' &nbsp;&middot;&nbsp; <span style="color:{cat_color};">{sermon_ref}</span>'
            theme_line += "</div>"

        st.markdown(f"""
        <div class="entry-card" style="border-left:4px solid {cat_color}; background:linear-gradient(135deg,rgba(255,255,255,0.9),rgba(237,235,250,0.4));">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px; font-weight:600; margin-bottom:4px;">
                        Confession of the Week
                    </div>
                    <div style="font-family:'DM Serif Display',Georgia,serif; font-size:17px; color:#2A2438;">
                        {cat_icon} {tpl_name}
                    </div>
                    <div style="font-size:12px; color:{cat_color}; margin-top:2px;">{cat_name}</div>
                    {theme_line}
                </div>
                <div style="font-size:11px; color:#D0C8DB; white-space:nowrap; margin-left:16px; text-align:right;">
                    {date_range}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        spacer(4)
except Exception:
    pass

# ==================== 3 SECTION CARDS ====================
section_label("Your Spiritual Toolkit")

col1, col2, col3 = st.columns(3)

with col1:
    total_entries = len(all_dates)
    st.markdown(f"""
    <div class="section-card">
        <div class="section-icon">\u270f\ufe0f</div>
        <div class="section-title">Daily Assignment</div>
        <div class="section-desc">
            Track prayer, Bible reading & sermons.
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #EDE8F5;">
            <span style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#5B4FC4;">{total_entries}</span>
            <span style="font-size:12px; color:#9E96AB; margin-left:4px;">entries logged</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    notes_count = len(sermon_notes)
    st.markdown(f"""
    <div class="section-card">
        <div class="section-icon">\U0001f4dd</div>
        <div class="section-title">Sermon Notes</div>
        <div class="section-desc">
            Capture sermon insights with<br/>
            auto Bible scripture lookup.
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #EDE8F5;">
            <span style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#D4853A;">{notes_count}</span>
            <span style="font-size:12px; color:#9E96AB; margin-left:4px;">notes saved</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_prayers = sum(c["total"] for c in prayer_counts.values())
    answered = sum(c["answered"] for c in prayer_counts.values())
    st.markdown(f"""
    <div class="section-card">
        <div class="section-icon">\U0001f64f</div>
        <div class="section-title">Prayer Journal</div>
        <div class="section-desc">
            Confessions, declarations &<br/>
            scripture-backed prayers.
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #EDE8F5;">
            <span style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#3A8F5C;">{total_prayers}</span>
            <span style="font-size:12px; color:#9E96AB; margin-left:4px;">prayers</span>
            {"<span style='margin-left:12px; font-family:DM Serif Display,Georgia,serif; font-size:24px; color:#C44B5B;'>" + str(answered) + "</span><span style='font-size:12px; color:#9E96AB; margin-left:4px;'>answered</span>" if answered else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== PRAYER CATEGORIES PILLS ====================
if prayer_categories:
    spacer(8)

    def hex_to_rgba(hex_color, alpha):
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"

    pills_html = ""
    for cat in prayer_categories:
        count = prayer_counts.get(cat["id"], {})
        total = count.get("total", 0)
        ongoing = count.get("ongoing", 0)
        color = cat.get("color", "#5B4FC4")
        bg = hex_to_rgba(color, 0.08)
        border = hex_to_rgba(color, 0.2)
        pills_html += f"""
        <span class="prayer-pill" style="background:{bg}; color:{color}; border:1px solid {border};">
            {cat['icon']} {cat['name']}
            <span style="font-weight:700; margin-left:4px;">{total}</span>
            {"<span style='font-size:11px; opacity:0.7; margin-left:2px;'>(" + str(ongoing) + " active)</span>" if ongoing else ""}
        </span>
        """
    st.markdown(f"""
    <div class="progress-section">
        <div class="progress-title">\U0001f64f Prayer Categories</div>
        <div>{pills_html}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== RECENT SERMON NOTES ====================
if sermon_notes:
    section_label("Recent Sermon Notes")

    for note in sermon_notes[:3]:
        preview = (note.get("notes_text", "") or "")[:80]
        if len(note.get("notes_text", "") or "") > 80:
            preview += "..."
        st.markdown(f"""
        <div class="entry-card" style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-family:'DM Serif Display',Georgia,serif; font-weight:400; color:#2A2438; font-size:15px;">{note['title']}</div>
                <div style="font-size:13px; color:#5B4FC4;">{note['speaker']}</div>
                <div style="font-size:12px; color:#9E96AB; margin-top:2px;">{preview}</div>
            </div>
            <div style="font-size:12px; color:#D0C8DB; white-space:nowrap; margin-left:16px;">
                {note['sermon_date']}
            </div>
        </div>
        """, unsafe_allow_html=True)
