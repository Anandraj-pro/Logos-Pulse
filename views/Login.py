import streamlit as st
from modules.styles import inject_styles
from modules.auth import sign_in, sign_up, is_authenticated, DEFAULT_PASSWORDS
from modules.rbac import get_pastors_list
from modules.seed import seed_user_data

inject_styles()

# If already logged in, redirect to dashboard
if is_authenticated():
    if st.session_state.get("must_change_password"):
        st.switch_page("views/Change_Password.py")
    else:
        st.switch_page("views/0_Dashboard.py")

# ==================== HEADER ====================
st.markdown("""
<div style="text-align:center; padding:40px 0 20px 0;">
    <div style="font-size:48px; margin-bottom:8px;">\U0001f64f</div>
    <div style="font-family:'DM Serif Display',Georgia,serif; font-size:32px; color:#2A2438;">
        Logos Pulse
    </div>
    <div style="font-size:14px; color:#9E96AB; margin-top:4px;">
        Spiritual Growth Tracker
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== TABS ====================
tab_login, tab_register, tab_forgot = st.tabs(["\U0001f511 Login", "\u270f\ufe0f Register", "\U0001f504 Forgot Password"])

# ==================== LOGIN ====================
with tab_login:
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)

    if submitted:
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            with st.spinner("Signing in..."):
                result = sign_in(email.strip().lower(), password)
            if result["success"]:
                st.success(f"Welcome, {st.session_state.get('preferred_name', 'User')}!")
                if st.session_state.get("must_change_password"):
                    st.info("You must change your default password before continuing.")
                    st.switch_page("views/Change_Password.py")
                else:
                    st.rerun()
            else:
                st.error(result["error"])

# ==================== REGISTER ====================
with tab_register:
    st.markdown("""
    <div style="font-size:13px; color:#9E96AB; margin-bottom:12px;">
        Create a Prayer Warrior account to start tracking your spiritual growth.
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form"):
        reg_email = st.text_input("Email", placeholder="your@email.com", key="reg_email")

        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="John")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Doe")

        preferred_name = st.text_input("Preferred Name", placeholder="What should we call you?")

        # Pastor dropdown
        pastors = get_pastors_list()
        if pastors:
            pastor_options = {p["display_name"] + f" ({p['email']})": p["user_id"] for p in pastors}
            selected_pastor = st.selectbox("Select Your Pastor", options=list(pastor_options.keys()))
            pastor_id = pastor_options[selected_pastor] if selected_pastor else None
        else:
            st.warning("No pastors available yet. Contact your admin to set up pastor accounts first.")
            pastor_id = None
            selected_pastor = None

        membership_card = st.text_input("Church Membership Card ID (optional)", placeholder="e.g. TKT1694")

        prayer_benchmark = st.number_input("Daily Prayer Goal (minutes)", min_value=15, max_value=480, value=60, step=15)

        reg_submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)

    if reg_submitted:
        if not reg_email or not first_name or not last_name:
            st.error("Please fill in all required fields.")
        elif not pastor_id:
            st.error("Please select your pastor.")
        else:
            with st.spinner("Creating your account..."):
                result = sign_up(
                    email=reg_email.strip().lower(),
                    password=DEFAULT_PASSWORDS["prayer_warrior"],
                    first_name=first_name.strip(),
                    last_name=last_name.strip(),
                    preferred_name=(preferred_name.strip() or first_name.strip()),
                    pastor_id=pastor_id,
                    prayer_benchmark=prayer_benchmark,
                    membership_card_id=membership_card.strip() if membership_card else None,
                )

            if result["success"]:
                # Seed default data
                with st.spinner("Setting up your account..."):
                    seed_user_data(
                        user_id=result["user_id"],
                        preferred_name=(preferred_name.strip() or first_name.strip()),
                        prayer_benchmark=prayer_benchmark,
                    )
                st.success("Account created! You can now sign in.")
                st.info(f"Your temporary password is: **{DEFAULT_PASSWORDS['prayer_warrior']}** \u2014 you'll be asked to change it on first login.")
            else:
                st.error(result["error"])

# ==================== FORGOT PASSWORD ====================
with tab_forgot:
    st.markdown("""
    <div style="font-size:13px; color:#9E96AB; margin-bottom:12px;">
        Enter your email to receive a password reset link.
    </div>
    """, unsafe_allow_html=True)

    with st.form("forgot_form"):
        forgot_email = st.text_input("Email", placeholder="your@email.com", key="forgot_email")
        forgot_submitted = st.form_submit_button("Send Reset Link", type="primary", use_container_width=True)

    if forgot_submitted:
        if not forgot_email:
            st.error("Please enter your email.")
        else:
            from modules.auth import request_password_reset
            with st.spinner("Sending..."):
                result = request_password_reset(forgot_email.strip().lower())
            if result["success"]:
                st.success("If an account exists with that email, you'll receive a password reset link.")
            else:
                st.success("If an account exists with that email, you'll receive a password reset link.")