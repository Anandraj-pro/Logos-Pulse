import streamlit as st
import html as _html
from datetime import date, timedelta, datetime
from modules import db
from modules.utils import calculate_streaks, format_prayer_duration, format_chapters_display
from modules.styles import inject_styles, spacer
from modules.auth import require_login, require_password_changed, get_current_user_id
from modules.bible_data import get_book_names, get_chapter_count
import json

require_login()
require_password_changed()

# ── Data ─────────────────────────────────────────────────────────────────────
settings        = db.get_all_settings()
greeting_name   = st.session_state.get("preferred_name") or settings.get("greeting_name", "User")
today_str       = date.today().isoformat()
today_entry     = db.get_entry_by_date(today_str)
all_dates       = db.get_all_entry_dates()
current_streak, longest_streak = calculate_streaks(all_dates)
today           = date.today()
monday          = today - timedelta(days=today.weekday())
saturday        = monday + timedelta(days=5)
week_entries    = db.get_entries_in_range(monday.isoformat(), saturday.isoformat())
week_count      = len(week_entries)
assignment      = db.get_active_assignment()
sermon_notes    = db.get_all_sermon_notes()
prayer_categories = db.get_prayer_categories()
yesterday_str   = (today - timedelta(days=1)).isoformat()
yesterday_entry = db.get_entry_by_date(yesterday_str)

prayer_counts = {}
for cat in prayer_categories:
    prayers = db.get_prayers_by_category(cat["id"])
    prayer_counts[cat["id"]] = {
        "total":   len(prayers),
        "ongoing": sum(1 for p in prayers if p.get("status") == "ongoing"),
        "answered":sum(1 for p in prayers if p.get("status") == "answered"),
    }
total_prayers = sum(c["total"]   for c in prayer_counts.values())
answered      = sum(c["answered"] for c in prayer_counts.values())

hour = datetime.now().hour
if hour < 12:   greeting, greeting_emoji = "Good Morning",   "🌅"
elif hour < 17: greeting, greeting_emoji = "Good Afternoon",  "☀️"
else:           greeting, greeting_emoji = "Good Evening",    "🌙"
formatted_date = today.strftime("%A, %B %d, %Y")

try:
    from modules.growth_score import calculate_growth_score
    _score = calculate_growth_score(get_current_user_id())
except Exception:
    _score = {"total":0,"level_name":"Seed","level_emoji":"🌱","level_desc":"","consistency":0,"quantity":0,"diversity":0,"engagement":0}

VERSES = [
    ("Proverbs 3:5-6",   "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight."),
    ("Philippians 4:13", "I can do all things through Christ who strengthens me."),
    ("Jeremiah 29:11",   "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future."),
    ("Isaiah 40:31",     "But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary."),
    ("Psalm 23:1",       "The Lord is my shepherd; I shall not want."),
    ("Romans 8:28",      "And we know that in all things God works for the good of those who love him, who have been called according to his purpose."),
    ("Joshua 1:9",       "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go."),
    ("Psalm 46:10",      "Be still, and know that I am God."),
    ("Matthew 6:33",     "But seek first his kingdom and his righteousness, and all these things will be given to you as well."),
    ("Isaiah 41:10",     "So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you."),
    ("Psalm 119:105",    "Your word is a lamp for my feet, a light on my path."),
    ("Romans 12:2",      "Do not conform to the pattern of this world, but be transformed by the renewing of your mind."),
    ("Philippians 4:6-7","Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God."),
    ("2 Timothy 1:7",    "For the Spirit God gave us does not make us timid, but gives us power, love and self-discipline."),
    ("Psalm 27:1",       "The Lord is my light and my salvation — whom shall I fear?"),
    ("Hebrews 11:1",     "Now faith is confidence in what we hope for and assurance about what we do not see."),
    ("Colossians 3:23",  "Whatever you do, work at it with all your heart, as working for the Lord, not for human masters."),
    ("Psalm 37:4",       "Take delight in the Lord, and he will give you the desires of your heart."),
    ("1 Corinthians 10:13","No temptation has overtaken you except what is common to mankind. And God is faithful; he will not let you be tempted beyond what you can bear."),
    ("James 1:5",        "If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault, and it will be given to you."),
    ("Galatians 5:22-23","But the fruit of the Spirit is love, joy, peace, forbearance, kindness, goodness, faithfulness, gentleness and self-control."),
    ("Psalm 91:1-2",     "Whoever dwells in the shelter of the Most High will rest in the shadow of the Almighty. I will say of the Lord, He is my refuge and my fortress."),
    ("Matthew 11:28",    "Come to me, all you who are weary and burdened, and I will give you rest."),
    ("Ephesians 6:10",   "Finally, be strong in the Lord and in his mighty power."),
    ("Psalm 34:8",       "Taste and see that the Lord is good; blessed is the one who takes refuge in him."),
    ("1 John 4:4",       "You, dear children, are from God and have overcome them, because the one who is in you is greater than the one who is in the world."),
    ("Proverbs 18:10",   "The name of the Lord is a fortified tower; the righteous run to it and are safe."),
    ("Deuteronomy 31:6", "Be strong and courageous. Do not be afraid or terrified because of them, for the Lord your God goes with you; he will never leave you nor forsake you."),
    ("Psalm 139:14",     "I praise you because I am fearfully and wonderfully made; your works are wonderful, I know that full well."),
    ("Romans 15:13",     "May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit."),
    ("Isaiah 26:3",      "You will keep in perfect peace those whose minds are steadfast, because they trust in you."),
]
verse_ref, verse_text = VERSES[today.timetuple().tm_yday % len(VERSES)]

# ── Styles ────────────────────────────────────────────────────────────────────
inject_styles()
st.markdown(
    '<style>'
    '@import url("https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,600&family=Jost:wght@300;400;500;600;700;800;900&display=swap");'
    ':root{'
    '--terra:#B85A30;--terra2:#D46A38;--terra-pale:#FDF0E8;--terra-mid:#F5D8C4;'
    '--gold:#C48A1C;--gold2:#DFA830;--gold-pale:#FDF6E3;'
    '--done:#2B5A3E;--done-pale:#E8F3ED;'
    '--bg:#F9F5EF;--bg2:#F3EFE7;--bg3:#EDE8DF;--white:#FFFFFF;'
    '--text:#1A1208;--text2:#5A4A32;--text3:#A09080;'
    '--border:rgba(26,18,8,0.09);--border2:rgba(26,18,8,0.05);'
    '--shadow-sm:0 2px 12px rgba(26,18,8,0.06);--shadow-md:0 8px 32px rgba(26,18,8,0.09);'
    '--r-sm:10px;--r-md:16px;--r-lg:24px;--tr:0.28s cubic-bezier(0.22,1,0.36,1);}'
    '@keyframes fadeUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}'
    '@keyframes shimmer{0%{background-position:-200% 0;}100%{background-position:200% 0;}}'
    '@keyframes fire{0%,100%{transform:scaleY(1) rotate(-2deg);}25%{transform:scaleY(1.08) rotate(1deg);}50%{transform:scaleY(0.95) rotate(-1deg);}75%{transform:scaleY(1.05) rotate(2deg);}}'
    '@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(184,90,48,0.4);}50%{box-shadow:0 0 0 5px rgba(184,90,48,0);}}'
    '.db-hero{margin-bottom:22px;animation:fadeUp 0.6s cubic-bezier(0.22,1,0.36,1) both;}'
    '.db-hero-inner{'
    'background:linear-gradient(148deg,rgba(255,253,250,0.97),rgba(249,245,238,0.95));'
    'border:1px solid rgba(184,90,48,0.12);border-radius:var(--r-lg);padding:36px 42px;'
    'display:flex;justify-content:space-between;align-items:flex-start;gap:30px;'
    'box-shadow:var(--shadow-md);position:relative;overflow:hidden;}'
    '.db-hero-inner::after{content:"";position:absolute;top:-60px;right:-60px;width:240px;height:240px;border-radius:50%;pointer-events:none;background:radial-gradient(circle,rgba(196,138,28,0.10) 0%,transparent 68%);}'
    '.db-hero-left{flex:1;position:relative;z-index:1;}'
    '.db-eyebrow{display:flex;align-items:center;gap:8px;font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:3px;color:var(--terra);margin-bottom:11px;font-family:Jost,sans-serif;}'
    '.db-eyebrow::before{content:"";width:20px;height:1.5px;background:var(--terra);flex-shrink:0;}'
    '.db-name{font-family:Cormorant,serif;font-size:50px;font-weight:600;color:var(--text);line-height:1.06;margin-bottom:5px;letter-spacing:-0.01em;}'
    '.db-date{font-size:12px;color:var(--text3);font-weight:500;margin-bottom:18px;font-family:Jost,sans-serif;}'
    '.db-tags{display:flex;gap:8px;flex-wrap:wrap;}'
    '.db-tag{padding:5px 14px;border-radius:100px;font-size:11px;font-weight:700;font-family:Jost,sans-serif;transition:transform 0.18s;cursor:default;}'
    '.db-tag:hover{transform:translateY(-1px);}'
    '.db-tag-terra{background:var(--terra-pale);color:var(--terra);border:1px solid rgba(184,90,48,0.20);}'
    '.db-tag-gold{background:var(--gold-pale);color:var(--gold);border:1px solid rgba(196,138,28,0.20);}'
    '.db-verse{max-width:255px;flex-shrink:0;background:rgba(255,255,255,0.70);border:1px solid var(--border);border-radius:var(--r-md);padding:17px 19px;box-shadow:var(--shadow-sm);position:relative;z-index:1;transition:all var(--tr);}'
    '.db-verse:hover{transform:translateY(-2px);box-shadow:var(--shadow-md);}'
    '.db-verse-eye{font-size:8px;text-transform:uppercase;letter-spacing:2.5px;color:var(--terra);font-weight:700;margin-bottom:9px;display:flex;align-items:center;gap:6px;font-family:Jost,sans-serif;}'
    '.db-verse-eye::before{content:"";width:12px;height:1px;background:var(--terra);opacity:0.45;flex-shrink:0;}'
    '.db-verse-text{font-family:Cormorant,serif;font-style:italic;font-size:14px;color:var(--text);line-height:1.78;margin-bottom:8px;}'
    '.db-verse-ref{font-family:Cormorant,serif;font-size:12.5px;color:var(--terra);font-weight:600;}'
    '.db-sec-label{font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:3px;color:var(--text3);margin:0 0 14px;display:flex;align-items:center;gap:12px;font-family:Jost,sans-serif;}'
    '.db-sec-label::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent);}'
    '.db-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:26px;}'
    '.db-stat{background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:19px 16px;text-align:center;position:relative;overflow:hidden;box-shadow:var(--shadow-sm);transition:transform 0.18s,box-shadow 0.22s;animation:fadeUp 0.55s cubic-bezier(0.22,1,0.36,1) both;}'
    '.db-stat::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;}'
    '.db-stat.c1::before{background:var(--terra);}'
    '.db-stat.c2::before{background:linear-gradient(90deg,var(--terra),var(--gold));}'
    '.db-stat.c3::before{background:var(--gold);}'
    '.db-stat.c4::before{background:linear-gradient(90deg,var(--gold),var(--terra));}'
    '.db-stat:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(26,18,8,0.11);}'
    '.db-stat-val{font-family:Jost,sans-serif;font-size:36px;font-weight:900;color:var(--text);line-height:1;margin-bottom:5px;font-variant-numeric:tabular-nums;}'
    '.db-stat-lbl{font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:2px;font-weight:700;font-family:Jost,sans-serif;}'
    '.db-stat-sub{font-size:11px;font-weight:600;margin-top:5px;color:var(--text3);font-family:Jost,sans-serif;}'
    '.db-grid{display:grid;grid-template-columns:1.48fr 1fr;gap:16px;}'
    '.db-card{background:var(--white);border:1px solid var(--border);border-radius:var(--r-md);padding:22px;box-shadow:var(--shadow-sm);transition:box-shadow 0.22s;}'
    '.db-card:hover{box-shadow:var(--shadow-md);}'
    '.db-card-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:13px;border-bottom:1px solid var(--border2);}'
    '.db-card-title{font-family:Cormorant,serif;font-size:18px;font-weight:600;color:var(--text);}'
    '.db-card-sub{font-size:9.5px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:1px;font-family:Jost,sans-serif;}'
    '.db-day{display:flex;align-items:center;gap:11px;padding:8px 9px;border-radius:9px;margin-bottom:2px;transition:background 0.16s;}'
    '.db-day:hover{background:var(--bg);}'
    '.db-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}'
    '.db-day.done .db-dot{background:var(--done);box-shadow:0 0 0 2.5px rgba(43,90,62,0.14);}'
    '.db-day.pend .db-dot{background:transparent;border:1.5px solid var(--text3);}'
    '.db-day-name{font-weight:700;font-size:13px;width:76px;color:var(--text);font-family:Jost,sans-serif;}'
    '.db-day-ch{flex:1;font-size:13px;color:var(--text2);font-family:Jost,sans-serif;}'
    '.db-day-st{font-size:14px;font-weight:700;font-family:Jost,sans-serif;}'
    '.db-day.done .db-day-st{color:var(--done);}'
    '.db-day.pend .db-day-st{color:var(--text3);}'
    '.db-prog-item{margin-bottom:14px;}'
    '.db-prog-item:last-child{margin-bottom:0;}'
    '.db-prog-row{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;}'
    '.db-prog-name{font-size:13px;font-weight:600;color:var(--text);font-family:Jost,sans-serif;}'
    '.db-prog-pct{font-family:Jost,sans-serif;font-size:15px;font-weight:800;}'
    '.db-prog-track{height:5px;background:var(--bg3);border-radius:100px;overflow:hidden;}'
    '.db-prog-fill{height:100%;border-radius:100px;transition:width 1.2s cubic-bezier(0.22,1,0.36,1);}'
    '.fill-terra{background-image:linear-gradient(90deg,#B85A30 0%,#D46A38 50%,#B85A30 100%);background-size:200% 100%;animation:shimmer 2.8s linear infinite;box-shadow:0 0 8px rgba(184,90,48,0.22);}'
    '.fill-gold{background:var(--gold);}'
    '.fill-ts{background:var(--terra);}'
    '.fill-tw{background:var(--terra2);opacity:0.75;}'
    '.db-streak{background:linear-gradient(148deg,#FFF5EE 0%,#FDEADE 60%,#F8E0D0 100%);border:1.5px solid rgba(184,90,48,0.22);border-radius:var(--r-md);padding:24px 20px;text-align:center;margin-bottom:14px;box-shadow:0 8px 32px rgba(184,90,48,0.14);position:relative;overflow:hidden;transition:transform var(--tr),box-shadow var(--tr);}'
    '.db-streak::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:repeating-linear-gradient(-42deg,rgba(184,90,48,0.025) 0px,rgba(184,90,48,0.025) 1px,transparent 1px,transparent 14px);}'
    '.db-streak:hover{transform:translateY(-3px);box-shadow:0 14px 44px rgba(184,90,48,0.22);}'
    '.db-fire{font-size:30px;display:block;margin-bottom:2px;animation:fire 0.85s ease-in-out infinite;transform-origin:bottom center;filter:drop-shadow(0 0 8px rgba(255,140,0,0.5));}'
    '.db-snum{font-family:Jost,sans-serif;font-size:64px;font-weight:900;color:var(--terra);line-height:1;font-variant-numeric:tabular-nums;margin-bottom:3px;}'
    '.db-slbl{font-size:8.5px;text-transform:uppercase;letter-spacing:3px;font-weight:800;color:var(--text3);font-family:Jost,sans-serif;}'
    '.db-sdiv{width:32px;height:1px;background:rgba(184,90,48,0.22);margin:11px auto;}'
    '.db-sbadge{padding:3px 10px;border-radius:100px;font-size:10.5px;font-weight:700;background:rgba(184,90,48,0.08);color:var(--terra);border:1px solid rgba(184,90,48,0.20);font-family:Jost,sans-serif;}'
    '.db-pi{display:flex;align-items:center;gap:10px;padding:9px 7px;border-radius:9px;margin-bottom:2px;transition:background 0.16s;cursor:default;}'
    '.db-pi:hover{background:var(--bg);}'
    '.db-pcat{width:31px;height:31px;border-radius:8px;background:var(--bg2);display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;transition:transform 0.22s;}'
    '.db-pi:hover .db-pcat{transform:scale(1.1);}'
    '.db-pname{font-size:13.5px;font-weight:600;color:var(--text);line-height:1.3;font-family:Jost,sans-serif;}'
    '.db-pmeta{font-size:10.5px;color:var(--text3);margin-top:1px;font-family:Jost,sans-serif;}'
    '.db-pbadge{padding:3px 10px;border-radius:100px;font-size:10px;font-weight:800;flex-shrink:0;font-family:Jost,sans-serif;}'
    '.db-ongoing{background:var(--terra-pale);color:var(--terra);border:1px solid rgba(184,90,48,0.20);}'
    '.db-answered{background:var(--done-pale);color:var(--done);border:1px solid rgba(43,90,62,0.22);}'
    '.db-actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;}'
    '.db-abtn{background:var(--bg);border:1.5px solid var(--border);border-radius:10px;padding:14px 10px;text-align:center;text-decoration:none;display:block;transition:all 0.22s;}'
    '.db-abtn:hover{border-color:var(--terra);transform:translateY(-3px);box-shadow:0 6px 18px rgba(184,90,48,0.12);background:var(--terra-pale);}'
    '.db-aicon{font-size:20px;margin-bottom:6px;display:block;}'
    '.db-albl{font-size:10px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:1px;font-family:Jost,sans-serif;}'
    '</style>',
    unsafe_allow_html=True
)

# ── Announcements ─────────────────────────────────────────────────────────────
from modules.auth import get_current_role
_announcements = db.get_active_announcements(role=get_current_role())
for _ann in _announcements[:3]:
    _at = _html.escape(_ann.get('title','') or '')
    _am = _html.escape(_ann.get('message','') or '')
    col_ann, col_dis = st.columns([10, 1])
    with col_ann:
        st.markdown(
            '<div class="announcement-card">'
            f'<div class="announcement-title">&#128226; {_at}</div>'
            f'<div class="announcement-body">{_am}</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col_dis:
        if st.button("✖", key=f"dis_{_ann['id']}", help="Dismiss", use_container_width=True):
            db.dismiss_announcement(_ann["id"])
            st.rerun()

# ── Milestone ─────────────────────────────────────────────────────────────────
_milestones = {3:"🌱 3 days! A new habit is forming.",7:"🔥 7-day streak!",14:"⭐ 2 weeks strong!",21:"💪 21 days! You did it!",30:"🏆 30-day streak!",50:"👑 50 days!",100:"🌟 100 days!",365:"🎉 ONE YEAR!"}
if current_streak in _milestones:
    st.balloons()
    st.markdown('<div class="goal-banner" style="text-align:center;">' + _milestones[current_streak] + '</div>', unsafe_allow_html=True)

# ── Compute progress data ─────────────────────────────────────────────────────
prayer_days = sum(1 for e in week_entries if e.get("prayer_minutes", 0) > 0)
sermon_days = sum(1 for e in week_entries if e.get("sermon_title", ""))
prayer_pct  = int(prayer_days / 6 * 100)
sermon_pct  = int(sermon_days / 6 * 100)

bible_pct = 0
if assignment:
    try:
        _bd = json.loads(assignment["daily_breakdown"]) if isinstance(assignment["daily_breakdown"], str) else (assignment["daily_breakdown"] or {})
        _all = [ch for v in _bd.values() for ch in v]
        _done_ch = set()
        for _e in week_entries:
            if _e.get("bible_book") == assignment.get("book") and _e.get("chapters_read"):
                _cr = _e["chapters_read"]
                if isinstance(_cr, str):
                    try: _cr = json.loads(_cr)
                    except: _cr = []
                _done_ch.update(_cr)
        bible_pct = int(len(_done_ch.intersection(set(_all))) / len(_all) * 100) if _all else 0
    except Exception:
        bible_pct = 0

conf_pct = 0
try:
    _ct = db.get_confession_count_today()
    _ap = db.get_my_confession_plans(status="active")
    _ta = len(_ap) if _ap else 0
    conf_pct = min(int(_ct / _ta * 100), 100) if _ta > 0 else 0
except Exception:
    pass

# ── Build Hero HTML ───────────────────────────────────────────────────────────
streak_tag = f'<span class="db-tag db-tag-terra">&#128293; {current_streak}-Day Streak</span>' if current_streak > 0 else ''
level_tag  = f'<span class="db-tag db-tag-gold">&#127795; {_score["level_name"]}</span>'
score_tag  = f'<span class="db-tag db-tag-gold">&#10024; {_score["total"]} Growth Score</span>'

hero_html = (
    '<div class="db-hero">'
    '<div class="db-hero-inner">'
    '<div class="db-hero-left">'
    f'<div class="db-eyebrow">{greeting_emoji} {greeting.upper()}</div>'
    f'<div class="db-name">{_html.escape(greeting_name)}</div>'
    f'<div class="db-date">{formatted_date}</div>'
    '<div class="db-tags">' + streak_tag + level_tag + score_tag + '</div>'
    '</div>'
    '<div class="db-verse">'
    '<div class="db-verse-eye">Verse of the Day</div>'
    f'<div class="db-verse-text">&#8220;{_html.escape(verse_text)}&#8221;</div>'
    f'<div class="db-verse-ref">&#8212; {_html.escape(verse_ref)}</div>'
    '</div>'
    '</div>'
    '</div>'
)

# ── Build Stats HTML ──────────────────────────────────────────────────────────
remaining = max(0, 6 - week_count)
stats_html = (
    '<div class="db-sec-label">This Week</div>'
    '<div class="db-stats">'
    f'<div class="db-stat c1"><div class="db-stat-val" style="color:var(--terra);">{current_streak}</div><div class="db-stat-lbl">Day Streak</div><div class="db-stat-sub" style="color:var(--terra);">Best: {longest_streak} days</div></div>'
    f'<div class="db-stat c2"><div class="db-stat-val" style="color:var(--terra);">{_score["total"]}</div><div class="db-stat-lbl">Growth Score</div><div class="db-stat-sub" style="color:var(--gold);">&#127795; {_score["level_name"]}</div></div>'
    f'<div class="db-stat c3"><div class="db-stat-val" style="color:var(--terra);">{week_count}/6</div><div class="db-stat-lbl">Week Entries</div><div class="db-stat-sub">{remaining} days remaining</div></div>'
    f'<div class="db-stat c4"><div class="db-stat-val" style="color:var(--terra);">{total_prayers}</div><div class="db-stat-lbl">Prayer Items</div><div class="db-stat-sub" style="color:var(--done);">{answered} answered &#10003;</div></div>'
    '</div>'
)

# ── Build Weekly Assignment HTML ──────────────────────────────────────────────
def _day_row(day_name, ch_str, is_done):
    cls  = 'db-day done' if is_done else 'db-day pend'
    st_c = '&#10003;' if is_done else '&#9675;'
    return (
        f'<div class="{cls}">'
        '<div class="db-dot"></div>'
        f'<div class="db-day-name">{day_name[:3]}</div>'
        f'<div class="db-day-ch">{ch_str}</div>'
        f'<div class="db-day-st">{st_c}</div>'
        '</div>'
    )

assign_html = '<div class="db-card-hdr"><div class="db-card-title">Weekly Assignment</div><div class="db-card-sub">No assignment</div></div>'
if assignment:
    try:
        _bd = json.loads(assignment["daily_breakdown"]) if isinstance(assignment["daily_breakdown"], str) else (assignment["daily_breakdown"] or {})
        book = assignment.get("book", "")
        try:
            _as = date.fromisoformat(assignment.get("start_date", today_str))
            _wn = _as.isocalendar()[1]
        except Exception:
            _wn = today.isocalendar()[1]
        _dcs = set()
        for _e in week_entries:
            if _e.get("bible_book") == book and _e.get("chapters_read"):
                _cr = _e["chapters_read"]
                if isinstance(_cr, str):
                    try: _cr = json.loads(_cr)
                    except: _cr = []
                _dcs.update(_cr)
        _day_map = {"Monday":"mon","Tuesday":"tue","Wednesday":"wed","Thursday":"thu","Friday":"fri","Saturday":"sat"}
        rows_html = ''
        for dn in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]:
            key = _day_map[dn]
            chs = _bd.get(key, _bd.get(dn, _bd.get(dn.lower(), [])))
            if chs:
                ch_str = f"{book} {chs[0]}" if chs[0] == chs[-1] else f"{book} {chs[0]}–{chs[-1]}"
                is_done = all(c in _dcs for c in chs)
            else:
                ch_str = "—"
                is_done = False
            rows_html += _day_row(dn, ch_str, is_done)
        assign_html = (
            f'<div class="db-card-hdr"><div class="db-card-title">Weekly Assignment</div><div class="db-card-sub">{book.upper()} &middot; W{_wn}</div></div>'
            + rows_html
        )
    except Exception:
        pass

# ── Build Weekly Progress HTML ────────────────────────────────────────────────
def _bar(label, pct, fill_cls, color):
    return (
        '<div class="db-prog-item">'
        '<div class="db-prog-row">'
        f'<span class="db-prog-name">{label}</span>'
        f'<span class="db-prog-pct" style="color:{color};">{pct}%</span>'
        '</div>'
        '<div class="db-prog-track">'
        f'<div class="db-prog-fill {fill_cls}" style="width:{pct}%;"></div>'
        '</div>'
        '</div>'
    )

prog_html = (
    '<div class="db-card-hdr"><div class="db-card-title">Weekly Progress</div><div class="db-card-sub">This Week</div></div>'
    + _bar('&#128214; Bible Chapters', bible_pct, 'fill-terra', '#B85A30')
    + _bar('&#128591; Prayer Minutes', prayer_pct, 'fill-gold',  '#C48A1C')
    + _bar('&#127897; Sermons',        sermon_pct, 'fill-ts',    '#B85A30')
    + _bar('&#9889; Confessions',      conf_pct,   'fill-tw',    '#C48A1C')
)

# ── Build Streak HTML ─────────────────────────────────────────────────────────
_sb = 'class="db-sbadge"'
streak_html = (
    '<div class="db-streak">'
    '<span class="db-fire">&#128293;</span>'
    f'<div class="db-snum">{current_streak}</div>'
    '<div class="db-slbl">Day Streak</div>'
    '<div class="db-sdiv"></div>'
    '<div style="display:flex;gap:6px;justify-content:center;flex-wrap:wrap;">'
    f'<span {_sb}>{_score["level_name"]} {_score["level_emoji"]}</span>'
    f'<span {_sb}>{_score["total"]} pts</span>'
    f'<span {_sb}>Best: {longest_streak}</span>'
    '</div>'
    '</div>'
)

# ── Build Prayer Journal HTML ─────────────────────────────────────────────────
prayer_items_html = '<div class="db-card-hdr"><div class="db-card-title">&#128591; Prayer Journal</div><div class="db-card-sub" style="font-size:8.5px;">This week</div></div>'
for cat in prayer_categories[:4]:
    _icon  = cat.get("icon", "🙏")
    _cname = _html.escape(cat.get("name", ""))
    _ctype = _html.escape(cat.get("type", "Personal"))
    _cnt   = prayer_counts.get(cat["id"], {})
    _ans   = _cnt.get("answered", 0) > 0 and _cnt.get("ongoing", 0) == 0
    _bcls  = 'db-pbadge db-answered' if _ans else 'db-pbadge db-ongoing'
    _btxt  = 'Answered &#10003;' if _ans else 'Ongoing'
    prayer_items_html += (
        '<div class="db-pi">'
        f'<div class="db-pcat">{_icon}</div>'
        '<div style="flex:1;min-width:0;">'
        f'<div class="db-pname">{_cname}</div>'
        f'<div class="db-pmeta">{_ctype}</div>'
        '</div>'
        f'<span class="{_bcls}">{_btxt}</span>'
        '</div>'
    )

# ── Build Quick Actions HTML ──────────────────────────────────────────────────
_ab = 'class="db-abtn"'
actions_html = (
    '<div class="db-card-hdr" style="margin-bottom:13px;padding-bottom:11px;">'
    '<div class="db-card-title">Quick Actions</div>'
    '</div>'
    '<div class="db-actions">'
    f'<a {_ab} href="/daily-entry"><span class="db-aicon">&#128214;</span><div class="db-albl">Log Entry</div></a>'
    f'<a {_ab} href="/prayer-journal"><span class="db-aicon">&#128591;</span><div class="db-albl">Prayer List</div></a>'
    f'<a {_ab} href="/sermon-notes"><span class="db-aicon">&#128221;</span><div class="db-albl">Sermon Note</div></a>'
    f'<a {_ab} href="/streaks"><span class="db-aicon">&#128202;</span><div class="db-albl">My Stats</div></a>'
    '</div>'
)

# ── Render all HTML in ONE call ───────────────────────────────────────────────
st.markdown(
    hero_html
    + stats_html
    + '<div class="db-grid">'
    + '<div>'                              # left col
    + '<div class="db-card">' + assign_html + '</div>'
    + '<div class="db-card" style="margin-top:14px;">' + prog_html + '</div>'
    + '</div>'
    + '<div>'                              # right col
    + streak_html
    + '<div class="db-card">' + prayer_items_html + '</div>'
    + '<div class="db-card" style="margin-top:14px;">' + actions_html + '</div>'
    + '</div>'
    + '</div>',
    unsafe_allow_html=True
)

spacer(24)

# ── Today's Status + Quick Log (interactive Streamlit components) ─────────────
from modules.auth import get_current_role as _gcr
_role = _gcr()

if today_entry:
    dur     = format_prayer_duration(today_entry["prayer_minutes"])
    reading = today_entry.get("chapters_display", "N/A")
    sermon  = today_entry.get("sermon_title", "")
    details = f"Prayer: {dur} &nbsp;&bull;&nbsp; Reading: {reading}"
    if sermon:
        details += f" &nbsp;&bull;&nbsp; Sermon: {sermon}"
    st.markdown(
        '<div class="today-card today-done">'
        '<div class="today-title" style="color:#2B5A3E;">&#9989; Today\'s Entry Complete</div>'
        f'<div class="today-detail">{details}</div>'
        '</div>',
        unsafe_allow_html=True
    )
else:
    smsg = (f"You have a <b>{current_streak}-day streak</b> going — don’t break it!" if current_streak > 0 else "Start your spiritual journey today.")
    st.markdown(
        '<div class="today-card today-pending">'
        '<div class="today-title" style="color:#B85A30;">&#9200; Today\'s Entry Pending</div>'
        f'<div class="today-detail">{smsg}</div>'
        '</div>',
        unsafe_allow_html=True
    )
    with st.expander("&#9889; Quick Log — Log in seconds", expanded=True):
        with st.form("quick_log_form"):
            ql1, ql2 = st.columns(2)
            with ql1:
                _dp = int(settings.get("default_prayer_minutes", "60"))
                _po = list(range(15, 195, 15))
                ql_prayer = st.select_slider("Prayer (min)", options=_po, value=_dp if _dp in _po else 60)
            with ql2:
                book_names = get_book_names()
                ql_book = st.selectbox("Book", options=book_names, index=book_names.index("Psalms") if "Psalms" in book_names else 0)
            max_ch     = get_chapter_count(ql_book)
            ql_chapters= st.multiselect("Chapters read", options=list(range(1, max_ch + 1)))
            ql_fasted  = st.checkbox("I fasted today")
            ql_submit  = st.form_submit_button("&#9889; Save Quick Entry", type="primary", use_container_width=True)
        if ql_submit:
            if not ql_chapters:
                st.error("Please select at least one chapter.")
            else:
                db.upsert_daily_entry(
                    entry_date=today_str, prayer_minutes=ql_prayer,
                    bible_book=ql_book, chapters_read=sorted(ql_chapters),
                    chapters_display=format_chapters_display(ql_book, ql_chapters),
                    sermon_title="", sermon_speaker="", youtube_link="",
                )
                st.success("Entry logged!")
                st.rerun()

# ── Yesterday ─────────────────────────────────────────────────────────────────
if yesterday_entry:
    _yd = format_prayer_duration(yesterday_entry["prayer_minutes"])
    _yr = yesterday_entry.get("chapters_display", "N/A")
    st.markdown(
        '<div class="entry-card" style="border-left:3px solid #C48A1C;">'
        '<div style="font-size:11px;color:#A09080;text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">Yesterday</div>'
        f'<div style="font-size:14px;color:#5A4A32;margin-top:4px;">Prayer: {_yd} &nbsp;&bull;&nbsp; Reading: {_yr}'
        + (f' &nbsp;&bull;&nbsp; Sermon: {yesterday_entry["sermon_title"]}' if yesterday_entry.get("sermon_title") else '')
        + '</div></div>',
        unsafe_allow_html=True
    )

# ── Confessions ───────────────────────────────────────────────────────────────
try:
    _cps = db.get_my_confession_plans(status="active")
    if _cps:
        _ct = db.get_confession_count_today()
        _ta = len(_cps)
        _pend = _ta - _ct
        if _pend > 0:
            st.markdown(
                '<div class="today-card today-pending">'
                '<div class="today-title" style="color:#B85A30;">&#10013; Today\'s Confessions</div>'
                f'<div class="today-detail">{_pend} confession{"s" if _pend != 1 else ""} waiting &middot; {_ct} completed today</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if st.button("Start Confessing", type="primary"):
                st.switch_page("views/8_Prayer_Engine.py")
        else:
            st.markdown(
                '<div class="today-card today-done">'
                '<div class="today-title" style="color:#2B5A3E;">&#10013; Confessions Complete</div>'
                f'<div class="today-detail">All {_ta} confession{"s" if _ta != 1 else ""} done for today!</div>'
                '</div>',
                unsafe_allow_html=True
            )
except Exception:
    pass
