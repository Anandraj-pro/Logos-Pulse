import streamlit as st
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_login, require_password_changed
from modules import db

require_login()
require_password_changed()
inject_styles()

page_header("\U0001f3af", "Personal Goals", "Set and track your spiritual growth goals")

tab_active, tab_create, tab_completed = st.tabs(["\U0001f3af Active", "➕ New Goal", "✅ Completed"])

# ==================== ACTIVE GOALS ====================
with tab_active:
    goals = db.get_personal_goals(status="active")

    if not goals:
        empty_state("\U0001f3af", "No active goals", "Create your first goal in the 'New Goal' tab!")
    else:
        for g in goals:
            target = g.get("target_value") or 0
            current = g.get("current_value", 0)
            pct = int(current / target * 100) if target > 0 else 0
            pct = min(pct, 100)
            pct_color = "#2B5A3E" if pct >= 80 else "#C48A1C" if pct >= 40 else "#B85A30"
            fill_class = "fill-terra" if pct < 40 else ("fill-gold" if pct < 80 else "fill-terra")

            type_icons = {"reading": "\U0001f4d6", "prayer": "\U0001f64f", "fasting": "\U0001f374", "custom": "\U0001f3af"}
            icon = type_icons.get(g.get("goal_type", "custom"), "\U0001f3af")

            tracking = g.get("tracking_mode", "manual")
            auto_badge_html = ""
            if tracking != "manual":
                auto_label = {
                    "auto_prayer": "&#9889; Auto: prayer",
                    "auto_reading": "&#9889; Auto: reading",
                    "auto_fasting": "&#9889; Auto: fasting"
                }.get(tracking, "")
                auto_badge_html = (
                    '<span style="background:#E8F3ED; color:#2B5A3E; padding:2px 8px;'
                    ' border-radius:8px; font-size:11px; font-weight:600; margin-left:8px;">'
                    + auto_label + '</span>'
                )
            unit = g.get("unit") or ""
            due_html = (' | Due: ' + g['target_date']) if g.get('target_date') else ''
            desc_html = (
                '<div style="font-size:13px; color:#5A4A32; margin:6px 0;">' + g['description'] + '</div>'
                if g.get('description') else ''
            )

            st.markdown(
                '<div class="entry-card">'
                + '<div style="display:flex; justify-content:space-between; align-items:center;">'
                + '<div>'
                + f'<span style="font-size:20px;">{icon}</span>'
                + f'<span style="font-family:\'Cormorant\',Georgia,serif; font-size:16px; color:#1A1208; margin-left:8px;">{g["title"]}</span>'
                + auto_badge_html
                + '</div>'
                + f'<span style="font-family:\'Cormorant\',Georgia,serif; font-size:20px; color:{pct_color};">{pct}%</span>'
                + '</div>'
                + desc_html
                + '<div style="margin-top:8px;">'
                + '<div class="db-prog-track">'
                + f'<div class="db-prog-fill {fill_class}" style="width:{pct}%;"></div>'
                + '</div>'
                + f'<div style="font-size:11px; color:#A09080; margin-top:4px;">{current}/{target} {unit}{due_html}</div>'
                + '</div>'
                + '</div>',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                new_val = st.number_input("Progress", min_value=0, max_value=target if target > 0 else 9999,
                                          value=current, key=f"prog_{g['id']}", label_visibility="collapsed",
                                          disabled=(tracking != "manual"))
            with col2:
                if st.button("Update", key=f"upd_{g['id']}", use_container_width=True):
                    new_status = "completed" if new_val >= target and target > 0 else "active"
                    db.update_goal_progress(g["id"], new_val, new_status)
                    if new_status == "completed":
                        st.balloons()
                    st.rerun()
            with col3:
                if st.button("Abandon", key=f"abn_{g['id']}", use_container_width=True):
                    db.update_goal_progress(g["id"], current, "abandoned")
                    st.rerun()

# ==================== NEW GOAL ====================
with tab_create:
    section_label("Create a New Goal")

    TRACKING_OPTIONS = {
        "manual": ("Manual (I update progress myself)", None),
        "auto_prayer": ("Auto — track prayer minutes from daily entries", "minutes"),
        "auto_reading": ("Auto — track chapters read from daily entries", "chapters"),
        "auto_fasting": ("Auto — track fasting days from daily entries", "days"),
    }

    with st.form("new_goal_form"):
        g_title = st.text_input("Goal Title", placeholder="e.g., Read the New Testament in 90 days")
        g_desc = st.text_area("Description (optional)", height=80,
                              placeholder="What specifically do you want to achieve?")
        g_type = st.selectbox("Goal Type", ["reading", "prayer", "fasting", "custom"],
                              format_func=lambda x: x.title())

        g_tracking = st.selectbox(
            "Progress Tracking",
            options=list(TRACKING_OPTIONS.keys()),
            format_func=lambda x: TRACKING_OPTIONS[x][0],
            help="Auto-tracking updates this goal automatically each time you save a daily entry.",
        )

        col1, col2 = st.columns(2)
        with col1:
            g_target = st.number_input("Target Value", min_value=1, value=30,
                                       help="e.g., 260 chapters, 30 hours, 12 days")
        with col2:
            g_date = st.date_input("Target Date (optional)")

        g_submit = st.form_submit_button("Create Goal", type="primary", use_container_width=True)

    if g_submit:
        if not g_title.strip():
            st.error("Please enter a goal title.")
        else:
            _, unit = TRACKING_OPTIONS[g_tracking]
            db.create_personal_goal(
                title=g_title.strip(),
                description=g_desc.strip(),
                goal_type=g_type,
                target_value=g_target,
                target_date=g_date.isoformat() if g_date else None,
                tracking_mode=g_tracking,
                unit=unit,
            )
            auto_msg = " Progress will update automatically from your daily entries." if g_tracking != "manual" else ""
            st.success("Goal created!" + auto_msg)
            st.rerun()

# ==================== COMPLETED ====================
with tab_completed:
    completed = db.get_personal_goals(status="completed")
    abandoned = db.get_personal_goals(status="abandoned")

    if not completed and not abandoned:
        empty_state("✅", "No completed goals yet", "Keep working on your active goals!")
    else:
        if completed:
            section_label(f"Completed ({len(completed)})")
            for g in completed:
                achieved = g.get('target_value', 0)
                st.markdown(
                    '<div class="entry-card" style="border-left:3px solid #2B5A3E;">'
                    + f'&#x2705; <strong>{g["title"]}</strong> &mdash; {achieved} achieved'
                    + '</div>',
                    unsafe_allow_html=True
                )

        if abandoned:
            section_label(f"Abandoned ({len(abandoned)})")
            for g in abandoned:
                cur = g.get('current_value', 0)
                tgt = g.get('target_value', 0)
                st.markdown(
                    '<div class="entry-card" style="border-left:3px solid #A09080; opacity:0.7;">'
                    + f'&#x26AA; {g["title"]} &mdash; {cur}/{tgt}'
                    + '</div>',
                    unsafe_allow_html=True
                )
