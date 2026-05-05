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

page_header("\U0001f4d6", "Reading Plan", "Your guided Bible reading journey")

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
        badge = ' <span style="background:#E8F5E9; color:#2E7D32; padding:2px 8px; border-radius:8px; font-size:11px; font-weight:600; margin-left:8px;">Already completed</span>' if already_done else ""

        st.markdown(f"""
        <div class="entry-card" style="border-left:4px solid #5B4FC4;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div style="font-family:'DM Serif Display',Georgia,serif; font-size:18px; color:#2A2438;">
                        {p['name']}{badge}
                    </div>
                    <div style="font-size:13px; color:#6B6580; margin-top:4px;">{p.get('description','')}</div>
                </div>
                <div style="font-size:12px; color:#9E96AB; white-space:nowrap; margin-left:16px;">
                    {p['total_days']} days
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
pct_color = "#3A8F5C" if pct >= 70 else "#D4853A" if pct >= 30 else "#5B4FC4"

# ── Plan header card ──
st.markdown(f"""
<div class="entry-card" style="border-left:4px solid #5B4FC4;">
    <div style="font-family:'DM Serif Display',Georgia,serif; font-size:20px; color:#2A2438;">{plan_name}</div>
    <div style="font-size:13px; color:#6B6580; margin-top:2px; margin-bottom:12px;">{plan_desc}</div>
    <div class="progress-bar-bg" style="height:10px;">
        <div class="progress-bar-fill" style="width:{pct}%; background:{pct_color};"></div>
    </div>
    <div style="display:flex; justify-content:space-between; margin-top:6px;">
        <span style="font-size:12px; color:#9E96AB;">Day {days_done} of {total_days} complete</span>
        <span style="font-size:12px; color:{pct_color}; font-weight:600;">{pct}%</span>
    </div>
</div>
""", unsafe_allow_html=True)

spacer()

# ── Today's assignment ──
if completed_plan:
    st.markdown("""
    <div class="today-card today-done" style="text-align:center; padding:24px;">
        <div style="font-size:32px; margin-bottom:8px;">\U0001f3c6</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:20px; color:#2E7D32;">Plan Complete!</div>
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
            st.markdown(f"""
            <div class="today-card today-done">
                <div style="font-family:'DM Serif Display',Georgia,serif; font-size:26px; color:#2A2438; margin-bottom:6px;">
                    \U0001f4d6 {today_reading['book']}
                </div>
                <div style="font-size:18px; color:#5B4FC4; font-weight:600;">{ch_label}</div>
                <div style="font-size:13px; color:#3A8F5C; margin-top:8px;">✅ Completed today — well done!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="today-card today-pending">
                <div style="font-family:'DM Serif Display',Georgia,serif; font-size:26px; color:#2A2438; margin-bottom:6px;">
                    \U0001f4d6 {today_reading['book']}
                </div>
                <div style="font-size:18px; color:#5B4FC4; font-weight:600;">{ch_label}</div>
                <div style="font-size:13px; color:#6B6580; margin-top:8px;">
                    {count} chapter{"s" if count != 1 else ""} to read today
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("✅ Mark Today Complete", type="primary", use_container_width=True):
                mark_plan_day_complete(progress_id, total_days)
                st.success("Day complete! Keep going.")
                st.rerun()

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
                icon, text_style = "\U0001f4d6", "color:#5B4FC4; font-weight:600;"
            else:
                icon, text_style = "○", "color:#9E96AB;"

            st.markdown(f"""
            <div style="display:flex; gap:12px; align-items:center; padding:5px 0;
                        border-bottom:1px solid #F5F3FA; {text_style}">
                <span style="min-width:18px; font-size:13px;">{icon}</span>
                <span style="min-width:55px; font-size:12px;">Day {dn}</span>
                <span style="font-size:13px;">{day['book']} &nbsp;<span style="opacity:0.7;">{ch_r}</span></span>
            </div>
            """, unsafe_allow_html=True)

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
