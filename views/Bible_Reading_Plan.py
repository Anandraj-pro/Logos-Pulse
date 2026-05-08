import streamlit as st
from datetime import date
from modules.auth import require_login, require_password_changed, get_current_user_id
from modules.styles import inject_styles, page_header, section_label, spacer
from modules.db import (
    get_member_active_plan, get_plan_days, mark_plan_day_complete,
    get_reading_plans, enroll_in_plan, abandon_active_plan,
    get_member_completed_plan_ids,
)

require_login()
require_password_changed()
inject_styles()

page_header("\U0001f4d6", "Bible Library", "Your guided Bible reading journey")

user_id = get_current_user_id()
active = get_member_active_plan(user_id)

# ── No active plan: show plan browser ──
if not active:
    section_label("\U0001f4da Choose a Reading Plan")
    plans = get_reading_plans()
    completed_ids = get_member_completed_plan_ids(user_id)

    if not plans:
        st.info("No reading plans available yet. Ask your admin to seed the built-in plans from Admin Panel → Reminders.")
        st.stop()

    for p in plans:
        already_done = p["id"] in completed_ids
        badge = ' <span style="background:#E4F2EB; color:#2B5A3E; padding:2px 8px; border-radius:8px; font-size:11px; font-weight:600; margin-left:8px;">Already completed</span>' if already_done else ""
        st.markdown(
            '<div class="entry-card" style="border-left:4px solid #B85A30;">'
            '<div style="display:flex; justify-content:space-between; align-items:flex-start;">'
            '<div>'
            '<div style="font-family:\'Cormorant\',Georgia,serif; font-size:18px; color:#1A1208;">'
            + p['name'] + badge + '</div>'
            '<div style="font-size:13px; color:#5A4A32; margin-top:4px;">' + p.get('description', '') + '</div>'
            '</div>'
            '<div style="font-size:12px; color:#A09080; white-space:nowrap; margin-left:16px;">'
            + str(p['total_days']) + ' days</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(f"Start \"{p['name']}\"", key=f"enroll_{p['id']}", type="primary"):
            enroll_in_plan(user_id=user_id, plan_id=p["id"])
            st.success(f"Enrolled in {p['name']}! Day 1 starts now.")
            st.rerun()

    st.stop()

# ── Active plan view ──
plan = active.get("reading_plans") or {}
plan_name = plan.get("name", "Reading Plan")
plan_desc = plan.get("description", "")
total_days = plan.get("total_days", 0)
current_day = active.get("current_day", 1)
progress_id = active["id"]
last_completed = active.get("last_completed_date")
today_str = date.today().isoformat()

already_done_today = last_completed == today_str
completed_plan = bool(active.get("completed_at"))

days_done = current_day - 1
pct = int(days_done / total_days * 100) if total_days > 0 else 0
pct_color = "#3A8F5C" if pct >= 70 else "#C48A1C" if pct >= 30 else "#B85A30"

# ── Plan header card ──
st.markdown(
    '<div class="entry-card" style="border-left:4px solid #B85A30;">'
    f'<div style="font-family:\'Cormorant\',Georgia,serif; font-size:20px; color:#1A1208;">{plan_name}</div>'
    f'<div style="font-size:13px; color:#5A4A32; margin-top:2px; margin-bottom:12px;">{plan_desc}</div>'
    f'<div class="progress-bar-bg" style="height:10px;">'
    f'<div class="progress-bar-fill" style="width:{pct}%; background:{pct_color};"></div>'
    f'</div>'
    f'<div style="display:flex; justify-content:space-between; margin-top:6px;">'
    f'<span style="font-size:12px; color:#A09080;">Day {days_done} of {total_days} complete</span>'
    f'<span style="font-size:12px; color:{pct_color}; font-weight:600;">{pct}%</span>'
    f'</div>'
    '</div>',
    unsafe_allow_html=True
)

spacer()

# ── Today's assignment ──
if completed_plan:
    st.markdown("""
    <div class="today-card today-done" style="text-align:center; padding:24px;">
        <div style="font-size:32px; margin-bottom:8px;">\U0001f3c6</div>
        <div style="font-family:'Cormorant',Georgia,serif; font-size:20px; color:#2B5A3E;">Plan Complete!</div>
        <div style="font-size:13px; color:#3A8F5C; margin-top:4px;">
            Amazing work! Choose another plan below or let your pastor assign a new one.
        </div>
    </div>
    """, unsafe_allow_html=True)
    spacer()
    # After completion, show browse button
    if st.button("\U0001f4da Browse Plans", type="primary"):
        abandon_active_plan(user_id)
        st.rerun()
else:
    all_days = get_plan_days(active["plan_id"])
    today_reading = next((d for d in all_days if d["day_number"] == current_day), None)

    if today_reading:
        ch_start = today_reading["chapter_start"]
        ch_end = today_reading["chapter_end"]
        ch_label = (
            f"Chapter {ch_start}"
            if ch_start == ch_end
            else f"Chapters {ch_start}–{ch_end}"
        )
        count = ch_end - ch_start + 1

        section_label(f"\U0001f4c5 Day {current_day} — Today's Reading")

        if already_done_today:
            st.markdown(
                '<div class="today-card today-done">'
                f'<div style="font-family:\'Cormorant\',Georgia,serif; font-size:26px; color:#1A1208; margin-bottom:6px;">\U0001f4d6 {today_reading["book"]}</div>'
                f'<div style="font-size:18px; color:#B85A30; font-weight:600;">{ch_label}</div>'
                '<div style="font-size:13px; color:#2B5A3E; margin-top:8px;">Completed today — well done!</div>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            ch_plural = "s" if count != 1 else ""
            st.markdown(
                '<div class="today-card today-pending">'
                f'<div style="font-family:\'Cormorant\',Georgia,serif; font-size:26px; color:#1A1208; margin-bottom:6px;">\U0001f4d6 {today_reading["book"]}</div>'
                f'<div style="font-size:18px; color:#B85A30; font-weight:600;">{ch_label}</div>'
                f'<div style="font-size:13px; color:#5A4A32; margin-top:8px;">{count} chapter{ch_plural} to read today</div>'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button("✅ Mark Today Complete", type="primary", use_container_width=True):
                mark_plan_day_complete(progress_id, total_days)
                st.success("Day complete! Keep going.")
                st.rerun()

        # ── Bible Flip Book Reader ──────────────────────────────────────────
        spacer(8)
        section_label("📖 Read Today's Chapters")

        from modules.bible_reader import fetch_chapter

        # Fetch all chapters for today's reading
        book_name = today_reading["book"]
        chapters_data = []
        for ch_num in range(ch_start, ch_end + 1):
            try:
                data = fetch_chapter(book_name, ch_num)
                if data and data.get("verses"):
                    chapters_data.append({"chapter": ch_num, "verses": data["verses"]})
            except Exception:
                pass

        if chapters_data:
            # Build pages JSON for the flip book
            import json as _json

            pages_json = _json.dumps([
                {
                    "chapter": c["chapter"],
                    "book": book_name,
                    "verses": [
                        {"n": v.get("verse", i+1), "t": v.get("text", "").strip()}
                        for i, v in enumerate(c["verses"])
                    ]
                }
                for c in chapters_data
            ])

            flip_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/page-flip@2.0.7/dist/js/page-flip.browser.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:#F3EFE7;display:flex;flex-direction:column;align-items:center;padding:20px 10px 16px;font-family:'Jost',sans-serif;overflow-x:hidden;}}
#book-container{{position:relative;}}
.page{{background:#FEFCF8;overflow:hidden;}}
.page-inner{{height:100%;display:flex;flex-direction:column;padding:22px 20px 16px;position:relative;}}
.cover-page{{background:linear-gradient(160deg,#1A1208 0%,#2A1A08 45%,#3A2A10 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;}}
.cover-cross-v{{width:2px;height:50px;background:linear-gradient(180deg,#C48A1C,#DFA830);margin:0 auto;}}
.cover-cross-h{{width:30px;height:2px;background:#C48A1C;margin:-34px auto 0;}}
.cover-title{{font-family:'Cormorant',serif;font-size:28px;color:#fff;text-align:center;letter-spacing:0.08em;margin-top:14px;font-weight:400;}}
.cover-sub{{font-size:9px;color:rgba(196,138,28,0.55);letter-spacing:0.3em;text-transform:uppercase;margin-top:8px;text-align:center;}}
.cover-rule{{width:50px;height:1px;background:linear-gradient(90deg,transparent,#C48A1C,transparent);margin:10px auto;}}
.cover-ref{{font-family:'Cormorant',serif;font-style:italic;font-size:12px;color:rgba(240,228,210,0.5);text-align:center;padding:0 20px;line-height:1.6;}}
.page-lines div{{position:absolute;left:18px;right:18px;height:1px;background:rgba(26,18,8,0.04);}}
.page-top-bar{{height:2px;background:linear-gradient(90deg,transparent,#C48A1C,transparent);opacity:0.5;margin-bottom:14px;border-radius:2px;}}
.ch-header{{display:flex;align-items:baseline;justify-content:space-between;padding-bottom:10px;border-bottom:1px solid rgba(26,18,8,0.06);margin-bottom:10px;}}
.ch-book{{font-family:'Cormorant',serif;font-size:17px;font-weight:600;color:#1A1208;}}
.ch-badge{{width:26px;height:26px;border-radius:50%;background:rgba(184,90,48,0.1);border:1px solid rgba(184,90,48,0.25);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#B85A30;flex-shrink:0;}}
.ch-label{{font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:0.2em;color:#A09080;margin-bottom:8px;}}
.verses{{flex:1;overflow:hidden;}}
.verse{{display:flex;gap:6px;margin-bottom:5px;}}
.vnum{{font-size:8px;font-weight:700;color:#B85A30;width:14px;flex-shrink:0;margin-top:3px;opacity:0.8;}}
.vtext{{font-family:'Cormorant',serif;font-size:12.5px;line-height:1.72;color:#1A1208;flex:1;}}
.page-footer{{margin-top:auto;padding-top:8px;border-top:1px solid rgba(26,18,8,0.05);display:flex;justify-content:space-between;align-items:center;}}
.page-ref{{font-size:8px;text-transform:uppercase;letter-spacing:0.18em;color:#A09080;}}
.page-dots span{{width:4px;height:4px;border-radius:50%;background:#B85A30;opacity:0.25;display:inline-block;margin-left:3px;}}
.controls{{display:flex;align-items:center;gap:14px;margin-top:16px;}}
.ctrl-btn{{width:36px;height:36px;border-radius:50%;border:1px solid rgba(184,90,48,0.25);background:rgba(184,90,48,0.06);color:#B85A30;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:18px;transition:all 0.18s;}}
.ctrl-btn:hover{{background:#B85A30;color:#fff;}}
.ctrl-btn:disabled{{opacity:0.28;pointer-events:none;}}
.page-label{{font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:#A09080;min-width:120px;text-align:center;}}
.dots{{display:flex;gap:5px;align-items:center;}}
.dot{{width:5px;height:5px;border-radius:50%;background:rgba(26,18,8,0.15);transition:all 0.25s;}}
.dot.active{{background:#B85A30;width:16px;border-radius:3px;}}
</style>
</head>
<body>
<div id="book-container">
  <div id="book"></div>
</div>
<div class="controls">
  <button class="ctrl-btn" id="btn-prev" onclick="pf.flipPrev()" disabled>&#8249;</button>
  <div>
    <div class="dots" id="dots"></div>
    <div class="page-label" id="page-label">Cover</div>
  </div>
  <button class="ctrl-btn" id="btn-next" onclick="pf.flipNext()">&#8250;</button>
</div>
<script>
const PAGES_DATA = {pages_json};
const BOOK = "{book_name}";

// Build page HTML strings
function buildPageHTML(chapObj, isLeft) {{
  const shadow = isLeft
    ? 'linear-gradient(to left,rgba(26,18,8,0.04),transparent)'
    : 'linear-gradient(to right,rgba(26,18,8,0.04),transparent)';
  const shadowSide = isLeft ? 'right:0' : 'left:0';

  // Limit verses to fit the page (approx 14 short verses or 10 long ones)
  const maxVerses = 13;
  const verses = chapObj.verses.slice(0, maxVerses);
  const verseHTML = verses.map(v =>
    `<div class="verse"><span class="vnum">${{v.n}}</span><span class="vtext">${{v.t}}</span></div>`
  ).join('');
  const overflow = chapObj.verses.length > maxVerses
    ? `<div style="font-size:10px;color:#A09080;font-style:italic;margin-top:4px;">+${{chapObj.verses.length - maxVerses}} more verses...</div>` : '';

  return `<div class="page-inner">
    <div class="page-top-bar"></div>
    <div class="ch-header">
      <div>
        <div class="ch-book">${{chapObj.book}}</div>
      </div>
      <div class="ch-badge">${{chapObj.chapter}}</div>
    </div>
    <div class="ch-label">Chapter ${{chapObj.chapter}}</div>
    <div class="verses">${{verseHTML}}${{overflow}}</div>
    <div class="page-footer">
      <span class="page-ref">${{chapObj.book}} ${{chapObj.chapter}}</span>
      <div class="page-dots"><span></span><span></span><span></span></div>
    </div>
    <div style="position:absolute;inset-y:0;${{shadowSide}};width:18px;background:${{shadow}};pointer-events:none;"></div>
  </div>`;
}}

// Create DOM pages
const bookEl = document.getElementById('book');

// Cover
const cover = document.createElement('div');
cover.className = 'page';
cover.innerHTML = `<div class="cover-page">
  <div class="cover-cross-v"></div>
  <div class="cover-cross-h"></div>
  <div class="cover-title">${{BOOK}}</div>
  <div class="cover-rule"></div>
  <div class="cover-sub">Holy Bible &middot; NIV</div>
</div>`;
bookEl.appendChild(cover);

// Content pages
PAGES_DATA.forEach((ch, i) => {{
  const p = document.createElement('div');
  p.className = 'page';
  p.innerHTML = buildPageHTML(ch, i % 2 === 0);
  bookEl.appendChild(p);
}});

// Back cover
const back = document.createElement('div');
back.className = 'page';
back.innerHTML = `<div class="cover-page">
  <div style="text-align:center;padding:0 24px;">
    <div style="font-family:'Cormorant',serif;font-size:13px;font-style:italic;color:rgba(240,228,210,0.55);line-height:1.8;margin-bottom:10px;">
      &ldquo;Your word is a lamp to my feet and a light to my path.&rdquo;
    </div>
    <div style="font-size:10px;letter-spacing:0.2em;text-transform:uppercase;color:rgba(196,138,28,0.55);">Psalm 119:105</div>
  </div>
</div>`;
bookEl.appendChild(back);

const totalPages = PAGES_DATA.length + 2;

// Build dots
const dotsEl = document.getElementById('dots');
for (let i = 0; i < totalPages; i++) {{
  const d = document.createElement('div');
  d.className = 'dot' + (i === 0 ? ' active' : '');
  dotsEl.appendChild(d);
}}

// Init PageFlip
const pf = new St.PageFlip(bookEl, {{
  width: 300, height: 420, minWidth: 260, maxWidth: 300,
  minHeight: 360, maxHeight: 420, size: 'fixed',
  drawShadow: true, maxShadowOpacity: 0.35,
  showCover: true, flippingTime: 650,
  usePortrait: false, autoSize: false,
  useMouseEvents: true, showPageCorners: true,
  clickEventForward: true, swipeDistance: 30,
  mobileScrollSupport: true, startZIndex: 0,
}});

pf.loadFromHTML(bookEl.querySelectorAll('.page'));

pf.on('flip', (e) => {{
  const p = e.data;
  document.getElementById('btn-prev').disabled = p === 0;
  document.getElementById('btn-next').disabled = p >= totalPages - 1;
  const dots = document.querySelectorAll('.dot');
  dots.forEach((d, i) => d.classList.toggle('active', i === p));
  const label = p === 0 ? 'Cover'
    : p > PAGES_DATA.length ? 'End'
    : `${{BOOK}} Ch ${{PAGES_DATA[p-1]?.chapter}}`;
  document.getElementById('page-label').textContent = label;
}});
</script>
</body>
</html>
"""
            import streamlit.components.v1 as _components
            _components.html(flip_html, height=560, scrolling=False)
        else:
            st.info("Bible text not available right now — check your internet connection.")

    spacer()

    # ── Full schedule ──
    section_label("\U0001f4cb Full Schedule")
    with st.expander("View all days", expanded=False):
        for day in all_days:
            dn = day["day_number"]
            cs, ce = day["chapter_start"], day["chapter_end"]
            ch_r = f"Ch {cs}" if cs == ce else f"Ch {cs}–{ce}"

            if dn < current_day:
                icon, text_style = "✅", "color:#3A8F5C;"
            elif dn == current_day:
                icon, text_style = "\U0001f4d6", "color:#B85A30; font-weight:600;"
            else:
                icon, text_style = "○", "color:#A09080;"

            st.markdown(
                f'<div style="display:flex; gap:12px; align-items:center; padding:5px 0;'
                f' border-bottom:1px solid #F3EFE7; {text_style}">'
                f'<span style="min-width:18px; font-size:13px;">{icon}</span>'
                f'<span style="min-width:55px; font-size:12px;">Day {dn}</span>'
                f'<span style="font-size:13px;">{day["book"]} &nbsp;<span style="opacity:0.7;">{ch_r}</span></span>'
                f'</div>',
                unsafe_allow_html=True
            )

    spacer()

    # ── Switch plan ──
    with st.expander("🔄 Switch to a different plan"):
        st.caption("Switching will abandon your current progress. This cannot be undone.")
        other_plans = [p for p in get_reading_plans() if p["id"] != active["plan_id"]]
        if not other_plans:
            st.info("No other plans available.")
        else:
            completed_ids = get_member_completed_plan_ids(user_id)
            for p in other_plans:
                badge = " ✅" if p["id"] in completed_ids else ""
                col_info, col_btn = st.columns([3, 1])
                with col_info:
                    st.markdown(f"**{p['name']}{badge}** — {p['total_days']} days")
                    st.caption(p.get("description", ""))
                with col_btn:
                    if st.button("Switch", key=f"switch_{p['id']}"):
                        enroll_in_plan(user_id=user_id, plan_id=p["id"])
                        st.success(f"Switched to {p['name']}!")
                        st.rerun()
