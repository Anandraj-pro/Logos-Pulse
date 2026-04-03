import streamlit as st
from modules.styles import inject_styles, spacer
from modules.auth import require_login, get_current_user_id
from modules.supabase_client import get_admin_client

require_login()
inject_styles()

user_id = get_current_user_id()
admin = get_admin_client()

# Check if onboarding already completed
profile = admin.table("user_profiles") \
    .select("onboarding_completed") \
    .eq("user_id", user_id) \
    .execute()

if profile.data and profile.data[0].get("onboarding_completed"):
    st.rerun()

# Onboarding wizard
if "onboard_step" not in st.session_state:
    st.session_state["onboard_step"] = 1

step = st.session_state["onboard_step"]

# Progress dots
dots = ""
for i in range(1, 5):
    if i < step:
        dots += '<span style="width:12px; height:12px; border-radius:50%; background:#5B4FC4; display:inline-block; margin:0 4px;"></span>'
    elif i == step:
        dots += '<span style="width:12px; height:12px; border-radius:50%; background:#5B4FC4; display:inline-block; margin:0 4px; box-shadow:0 0 0 3px rgba(91,79,196,0.2);"></span>'
    else:
        dots += '<span style="width:12px; height:12px; border-radius:50%; background:#EDE8F5; display:inline-block; margin:0 4px;"></span>'

st.markdown(f'<div style="text-align:center; margin:20px 0;">{dots}</div>', unsafe_allow_html=True)

# --- Step 1: Welcome ---
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
        if st.button("Let's Get Started \u2192", type="primary", use_container_width=True):
            st.session_state["onboard_step"] = 2
            st.rerun()

# --- Step 2: Set Your Prayer Goal ---
elif step == 2:
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:48px; margin-bottom:12px;">\u23f0</div>
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
        if st.button("\u2190 Back", use_container_width=True):
            st.session_state["onboard_step"] = 1
            st.rerun()
    with col3:
        if st.button("Next \u2192", type="primary", use_container_width=True):
            # Save goal
            admin.table("user_profiles") \
                .update({"prayer_benchmark_min": goal}) \
                .eq("user_id", user_id) \
                .execute()
            from modules.db import save_setting
            save_setting("default_prayer_minutes", str(goal))
            st.session_state["onboard_step"] = 3
            st.rerun()

# --- Step 3: Quick Tour ---
elif step == 3:
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:48px; margin-bottom:12px;">\U0001f4d6</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#2A2438; margin-bottom:16px;">
            Here's What You Can Do
        </div>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("\u270f\ufe0f", "Daily Entry", "Log prayer time, Bible reading, and sermons"),
        ("\U0001f4d6", "Bible Reader", "Read scripture right in the app"),
        ("\U0001f4cb", "WhatsApp Report", "Generate and send your daily report to your pastor"),
        ("\U0001f64f", "Prayer Journal", "Confessions, declarations, and scripture-backed prayers"),
        ("\U0001f4dd", "Sermon Notes", "Capture insights with Bible reference lookup"),
        ("\U0001f525", "Streaks & Stats", "Track your consistency with charts and heatmaps"),
    ]

    for icon, title, desc in features:
        st.markdown(f"""
        <div class="entry-card" style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:24px;">{icon}</span>
            <div>
                <div style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">{title}</div>
                <div style="font-size:13px; color:#9E96AB;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    spacer()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("\u2190 Back", use_container_width=True, key="s3b"):
            st.session_state["onboard_step"] = 2
            st.rerun()
    with col3:
        if st.button("Next \u2192", type="primary", use_container_width=True, key="s3n"):
            st.session_state["onboard_step"] = 4
            st.rerun()

# --- Step 4: Make Your First Entry ---
elif step == 4:
    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:48px; margin-bottom:12px;">\U0001f31f</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#2A2438; margin-bottom:8px;">
            You're All Set!
        </div>
        <div style="font-size:14px; color:#6B6580; max-width:400px; margin:0 auto; line-height:1.6;">
            Your journey starts now. Head to the Dashboard and log your first entry.
            Every day counts \u2014 let's build that streak!
        </div>
    </div>
    """, unsafe_allow_html=True)

    spacer()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("\U0001f680 Go to Dashboard", type="primary", use_container_width=True):
            # Mark onboarding complete
            admin.table("user_profiles") \
                .update({"onboarding_completed": True}) \
                .eq("user_id", user_id) \
                .execute()
            st.session_state.pop("onboard_step", None)
            st.rerun()
