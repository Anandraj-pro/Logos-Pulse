import streamlit as st
from modules.styles import inject_styles, spacer
from modules.auth import require_login, get_current_user_id
from modules.supabase_client import get_admin_client

require_login()
inject_styles()

user_id = get_current_user_id()
admin = get_admin_client()

profile = admin.table("user_profiles") \
    .select("onboarding_completed") \
    .eq("user_id", user_id) \
    .execute()

if profile.data and profile.data[0].get("onboarding_completed"):
    st.rerun()

if "onboard_step" not in st.session_state:
    st.session_state["onboard_step"] = 1

step = st.session_state["onboard_step"]
TOTAL_STEPS = 4

# Progress dots
dots = ""
for i in range(1, TOTAL_STEPS + 1):
    if i < step:
        dots += '<span style="width:12px; height:12px; border-radius:50%; background:#5B4FC4; display:inline-block; margin:0 4px;"></span>'
    elif i == step:
        dots += '<span style="width:12px; height:12px; border-radius:50%; background:#5B4FC4; display:inline-block; margin:0 4px; box-shadow:0 0 0 3px rgba(91,79,196,0.2);"></span>'
    else:
        dots += '<span style="width:12px; height:12px; border-radius:50%; background:#EDE8F5; display:inline-block; margin:0 4px;"></span>'

st.markdown(f'<div style="text-align:center; margin:20px 0;">{dots}</div>', unsafe_allow_html=True)

# ── Step 1: Welcome ──────────────────────────────────────────
if step == 1:
    st.markdown("""
    <div style="text-align:center; padding:40px 20px;">
        <div style="font-size:64px; margin-bottom:16px;">\U0001f64f</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:28px; color:#2A2438; margin-bottom:8px;">
            Welcome to Logos Pulse
        </div>
        <div style="font-size:16px; color:#6B6580; max-width:400px; margin:0 auto; line-height:1.6;">
            Your spiritual growth companion. Track your prayer life, Bible reading,
            and grow alongside your church community.
        </div>
    </div>
    """, unsafe_allow_html=True)

    spacer()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Let's Get Started →", type="primary", use_container_width=True):
            st.session_state["onboard_step"] = 2
            st.rerun()

# ── Step 2: Daily Prayer Goal ────────────────────────────────
elif step == 2:
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:48px; margin-bottom:12px;">⏰</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#2A2438; margin-bottom:8px;">
            Set Your Daily Prayer Goal
        </div>
        <div style="font-size:14px; color:#6B6580;">
            How many minutes do you want to pray each day?
        </div>
    </div>
    """, unsafe_allow_html=True)

    prayer_options = list(range(15, 195, 15))
    goal = st.select_slider("Prayer goal (minutes)", options=prayer_options, value=60)

    spacer()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state["onboard_step"] = 1
            st.rerun()
    with col3:
        if st.button("Next →", type="primary", use_container_width=True):
            admin.table("user_profiles") \
                .update({"prayer_benchmark_min": goal}) \
                .eq("user_id", user_id) \
                .execute()
            from modules.db import save_setting
            save_setting("default_prayer_minutes", str(goal))
            st.session_state["onboard_step"] = 3
            st.rerun()

# ── Step 3: Pick a Reading Plan ──────────────────────────────
elif step == 3:
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:48px; margin-bottom:12px;">\U0001f4d6</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#2A2438; margin-bottom:8px;">
            Start a Reading Plan
        </div>
        <div style="font-size:14px; color:#6B6580;">
            Choose a guided plan to work through — or skip for now.
        </div>
    </div>
    """, unsafe_allow_html=True)

    spacer(8)

    from modules.db import get_reading_plans, enroll_in_plan
    plans = get_reading_plans()

    if not plans:
        st.info("No reading plans seeded yet — your admin can add them from the Admin Panel.")
    else:
        selected_plan = st.session_state.get("onboard_plan_id")
        for p in plans:
            is_sel = selected_plan == p["id"]
            border = "border-left:4px solid #5B4FC4;" if is_sel else "border-left:4px solid #EDE8F5;"
            bg = "background:#F5F3FF;" if is_sel else ""
            st.markdown(f"""
            <div class="entry-card" style="{border}{bg}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438;">
                            {p['name']}
                        </div>
                        <div style="font-size:12px; color:#6B6580; margin-top:2px;">{p.get('description','')}</div>
                    </div>
                    <span style="font-size:12px; color:#9E96AB; white-space:nowrap; margin-left:12px;">{p['total_days']} days</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            btn_label = "Selected ✓" if is_sel else "Select"
            btn_type = "primary" if is_sel else "secondary"
            if st.button(btn_label, key=f"ob_plan_{p['id']}", type=btn_type, use_container_width=True):
                st.session_state["onboard_plan_id"] = p["id"]
                st.rerun()

    spacer()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", use_container_width=True, key="s3b"):
            st.session_state["onboard_step"] = 2
            st.rerun()
    with col2:
        if st.button("Skip", use_container_width=True, key="s3skip"):
            st.session_state["onboard_step"] = 4
            st.rerun()
    with col3:
        selected = st.session_state.get("onboard_plan_id")
        if st.button("Next →", type="primary", use_container_width=True, key="s3n",
                     disabled=(selected is None)):
            if selected:
                enroll_in_plan(user_id=user_id, plan_id=selected)
            st.session_state["onboard_step"] = 4
            st.rerun()

# ── Step 4: Set First Goal + Done ────────────────────────────
elif step == 4:
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:48px; margin-bottom:12px;">\U0001f3af</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#2A2438; margin-bottom:8px;">
            Set a Personal Goal
        </div>
        <div style="font-size:14px; color:#6B6580; max-width:360px; margin:0 auto;">
            Give yourself something to work towards — you can add more goals later.
        </div>
    </div>
    """, unsafe_allow_html=True)

    spacer(8)

    from modules.db import create_personal_goal
    GOAL_PRESETS = [
        ("Pray 30 hours this month", "prayer", "auto_prayer", 30 * 60, "minutes"),
        ("Read 60 chapters this month", "reading", "auto_reading", 60, "chapters"),
        ("Fast 4 days this month", "fasting", "auto_fasting", 4, "days"),
    ]

    preset_sel = st.session_state.get("onboard_goal_preset")
    for idx, (label, gtype, tracking, target, unit) in enumerate(GOAL_PRESETS):
        is_sel = preset_sel == idx
        border = "border-left:4px solid #5B4FC4;" if is_sel else "border-left:4px solid #EDE8F5;"
        bg = "background:#F5F3FF;" if is_sel else ""
        icon = {"reading": "\U0001f4d6", "prayer": "\U0001f64f", "fasting": "\U0001f374"}[gtype]
        st.markdown(f"""
        <div class="entry-card" style="{border}{bg}">
            <span style="font-size:18px;">{icon}</span>
            <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438; margin-left:8px;">
                {label}
            </span>
        </div>
        """, unsafe_allow_html=True)
        btn_label = "Selected ✓" if is_sel else "Select"
        if st.button(btn_label, key=f"ob_goal_{idx}",
                     type="primary" if is_sel else "secondary",
                     use_container_width=True):
            st.session_state["onboard_goal_preset"] = idx
            st.rerun()

    spacer()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", use_container_width=True, key="s4b"):
            st.session_state["onboard_step"] = 3
            st.rerun()
    with col2:
        if st.button("Skip & Finish", use_container_width=True, key="s4skip"):
            admin.table("user_profiles") \
                .update({"onboarding_completed": True}) \
                .eq("user_id", user_id) \
                .execute()
            for k in ("onboard_step", "onboard_plan_id", "onboard_goal_preset"):
                st.session_state.pop(k, None)
            st.rerun()
    with col3:
        preset_idx = st.session_state.get("onboard_goal_preset")
        if st.button("\U0001f680 Finish", type="primary", use_container_width=True, key="s4n",
                     disabled=(preset_idx is None)):
            if preset_idx is not None:
                label, gtype, tracking, target, unit = GOAL_PRESETS[preset_idx]
                create_personal_goal(
                    title=label,
                    description="",
                    goal_type=gtype,
                    target_value=target,
                    target_date=None,
                    tracking_mode=tracking,
                    unit=unit,
                )
            admin.table("user_profiles") \
                .update({"onboarding_completed": True}) \
                .eq("user_id", user_id) \
                .execute()
            for k in ("onboard_step", "onboard_plan_id", "onboard_goal_preset"):
                st.session_state.pop(k, None)
            st.rerun()
