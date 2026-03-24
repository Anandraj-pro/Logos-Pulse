import streamlit as st
from datetime import date, timedelta, datetime
from modules import db
from modules.utils import calculate_streaks, format_prayer_duration
import json

db.init_db()

# --- Load Data ---
settings = db.get_all_settings()
greeting_name = settings.get("greeting_name", "Anna")
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

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 40px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-greeting {
        font-size: 15px;
        color: rgba(255,255,255,0.7);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 6px;
        font-weight: 500;
    }
    .hero-name {
        font-size: 36px;
        font-weight: 700;
        color: white;
        margin-bottom: 4px;
        line-height: 1.2;
    }
    .hero-date {
        font-size: 14px;
        color: rgba(255,255,255,0.6);
    }
    .hero-verse {
        margin-top: 20px;
        padding: 14px 18px;
        background: rgba(255,255,255,0.12);
        border-radius: 12px;
        font-family: Georgia, serif;
        font-style: italic;
        font-size: 15px;
        color: rgba(255,255,255,0.9);
        line-height: 1.6;
        backdrop-filter: blur(4px);
    }

    .metric-card {
        background: white;
        border: 1px solid #F0EBF8;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.06);
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 13px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 500;
    }

    .section-card {
        background: white;
        border: 1px solid #F0EBF8;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: box-shadow 0.2s, transform 0.2s;
    }
    .section-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    .section-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #2C2C2C;
        margin-bottom: 4px;
    }
    .section-desc {
        font-size: 13px;
        color: #888;
        line-height: 1.5;
    }

    .today-card {
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .today-done {
        background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
        border: 1px solid #C8E6C9;
    }
    .today-pending {
        background: linear-gradient(135deg, #FFF3E0, #FFF8E1);
        border: 1px solid #FFE0B2;
    }
    .today-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .today-detail {
        font-size: 14px;
        color: #555;
        line-height: 1.6;
    }

    .progress-section {
        background: white;
        border: 1px solid #F0EBF8;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .progress-title {
        font-size: 14px;
        font-weight: 600;
        color: #555;
        margin-bottom: 12px;
    }
    .progress-bar-bg {
        background: #F0EBF8;
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
    }
    .progress-label {
        font-size: 12px;
        color: #999;
        margin-top: 6px;
    }

    .prayer-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin: 3px 4px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
# Daily verse rotation
verses = [
    ("Proverbs 3:5-6", "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight."),
    ("Philippians 4:13", "I can do all things through Christ who strengthens me."),
    ("Jeremiah 29:11", "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future."),
    ("Isaiah 40:31", "But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary."),
    ("Psalm 23:1", "The Lord is my shepherd; I shall not want."),
    ("Romans 8:28", "And we know that in all things God works for the good of those who love him, who have been called according to his purpose."),
    ("Joshua 1:9", "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go."),
]
verse_ref, verse_text = verses[today.timetuple().tm_yday % len(verses)]

st.markdown(f"""
<div class="hero-section">
    <div class="hero-greeting">{greeting}</div>
    <div class="hero-name">{greeting_name}</div>
    <div class="hero-date">{formatted_date}</div>
    <div class="hero-verse">
        \u201c{verse_text}\u201d
        <br/><span style="font-style:normal; font-size:12px; color:rgba(255,255,255,0.5);">\u2014 {verse_ref}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== STREAK METRICS ====================
col1, col2, col3 = st.columns(3)

with col1:
    streak_color = "#4CAF50" if current_streak >= 7 else "#FF9800" if current_streak >= 3 else "#7B68EE"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{streak_color};">{current_streak}</div>
        <div class="metric-label">Day Streak</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#7B68EE;">{longest_streak}</div>
        <div class="metric-label">Best Streak</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    week_color = "#4CAF50" if week_count >= 5 else "#FF9800" if week_count >= 3 else "#E91E63"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:{week_color};">{week_count}<span style="font-size:18px; color:#ccc;">/6</span></div>
        <div class="metric-label">This Week</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ==================== TODAY'S STATUS ====================
if today_entry:
    duration = format_prayer_duration(today_entry["prayer_minutes"])
    reading = today_entry.get("chapters_display", "N/A")
    sermon = today_entry.get("sermon_title", "")
    report_status = "Copied" if today_entry.get("report_copied") else "Not yet copied"
    report_color = "#4CAF50" if today_entry.get("report_copied") else "#FF9800"

    details = f"Prayer: {duration} &nbsp;&bull;&nbsp; Reading: {reading}"
    if sermon:
        details += f" &nbsp;&bull;&nbsp; Sermon: {sermon}"

    st.markdown(f"""
    <div class="today-card today-done">
        <div class="today-title" style="color:#2E7D32;">
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
    st.markdown("""
    <div class="today-card today-pending">
        <div class="today-title" style="color:#E65100;">
            \u23f0 Today\u2019s Entry Pending
        </div>
        <div class="today-detail">You haven\u2019t logged today\u2019s spiritual activities yet.</div>
    </div>
    """, unsafe_allow_html=True)

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
            <div class="progress-bar-fill" style="width:{progress_pct}%; background:linear-gradient(90deg, #667eea, #764ba2);"></div>
        </div>
        <div class="progress-label">{done_count}/{total_assigned} chapters completed ({progress_pct}%)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ==================== 3 SECTION CARDS ====================
st.markdown("""
<div style="font-size:12px; color:#999; text-transform:uppercase; letter-spacing:1.5px;
            font-weight:600; margin-bottom:12px;">
    Your Spiritual Toolkit
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# --- Daily Assignment Card ---
with col1:
    total_entries = len(all_dates)
    st.markdown(f"""
    <div class="section-card">
        <div class="section-icon">\u270f\ufe0f</div>
        <div class="section-title">Daily Assignment</div>
        <div class="section-desc">
            Track prayer, Bible reading & sermons.<br/>
            Send daily report to Ps. Deepak.
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #F0EBF8;">
            <span style="font-size:24px; font-weight:700; color:#7B68EE;">{total_entries}</span>
            <span style="font-size:12px; color:#999; margin-left:4px;">entries logged</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Sermon Notes Card ---
with col2:
    notes_count = len(sermon_notes)
    latest_sermon = sermon_notes[0]["title"][:25] + "..." if sermon_notes else "None yet"
    st.markdown(f"""
    <div class="section-card">
        <div class="section-icon">\U0001f4dd</div>
        <div class="section-title">Sermon Notes</div>
        <div class="section-desc">
            Capture sermon insights with<br/>
            auto Bible scripture lookup.
        </div>
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #F0EBF8;">
            <span style="font-size:24px; font-weight:700; color:#FF9800;">{notes_count}</span>
            <span style="font-size:12px; color:#999; margin-left:4px;">notes saved</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Prayer Journal Card ---
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
        <div style="margin-top:14px; padding-top:12px; border-top:1px solid #F0EBF8;">
            <span style="font-size:24px; font-weight:700; color:#4CAF50;">{total_prayers}</span>
            <span style="font-size:12px; color:#999; margin-left:4px;">prayers</span>
            {"<span style='margin-left:12px; font-size:24px; font-weight:700; color:#E91E63;'>" + str(answered) + "</span><span style='font-size:12px; color:#999; margin-left:4px;'>answered</span>" if answered else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== PRAYER CATEGORIES PILLS ====================
if prayer_categories:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    pills_html = ""
    for cat in prayer_categories:
        count = prayer_counts.get(cat["id"], {})
        total = count.get("total", 0)
        ongoing = count.get("ongoing", 0)
        color = cat.get("color", "#7B68EE")
        pills_html += f"""
        <span class="prayer-pill" style="background:{color}15; color:{color}; border:1px solid {color}30;">
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
    st.markdown("""
    <div style="font-size:12px; color:#999; text-transform:uppercase; letter-spacing:1.5px;
                font-weight:600; margin:16px 0 12px 0;">
        Recent Sermon Notes
    </div>
    """, unsafe_allow_html=True)

    for note in sermon_notes[:3]:
        preview = (note.get("notes_text", "") or "")[:80]
        if len(note.get("notes_text", "") or "") > 80:
            preview += "..."
        st.markdown(f"""
        <div style="background:white; border:1px solid #F0EBF8; border-radius:12px;
                    padding:14px 18px; margin-bottom:8px; display:flex;
                    justify-content:space-between; align-items:center;
                    box-shadow:0 1px 4px rgba(0,0,0,0.02);">
            <div>
                <div style="font-weight:600; color:#4A3728; font-size:15px;">{note['title']}</div>
                <div style="font-size:13px; color:#7B68EE;">{note['speaker']}</div>
                <div style="font-size:12px; color:#aaa; margin-top:2px;">{preview}</div>
            </div>
            <div style="font-size:12px; color:#ccc; white-space:nowrap; margin-left:16px;">
                {note['sermon_date']}
            </div>
        </div>
        """, unsafe_allow_html=True)
