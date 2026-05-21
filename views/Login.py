import streamlit as st
from modules.auth import sign_in, sign_up, is_authenticated, DEFAULT_PASSWORDS
from modules.seed import seed_user_data

if is_authenticated():
    st.rerun()

if "lp_forgot" not in st.session_state:
    st.session_state["lp_forgot"] = False

st.title("Logos Pulse")

if st.session_state["lp_forgot"]:
    st.subheader("Reset Password")
    with st.form("forgot_form"):
        forgot_email = st.text_input("Email", placeholder="you@church.org")
        forgot_submitted = st.form_submit_button("Send Reset Link", use_container_width=True)

    if forgot_submitted:
        if not forgot_email:
            st.error("Please enter your email.")
        else:
            try:
                from modules.auth import request_password_reset
                with st.spinner("Sending..."):
                    request_password_reset(forgot_email.strip().lower())
            except Exception:
                pass
            st.success("If an account exists with that email, you'll receive a password reset link.")

    if st.button("← Back to Sign In"):
        st.session_state["lp_forgot"] = False
        st.rerun()

else:
    tab_login, tab_register = st.tabs(["Sign In", "Register"])

    with tab_login:
        with st.form("login_form"):
            email    = st.text_input("Email",    placeholder="you@church.org")
            password = st.text_input("Password", type="password", placeholder="Your password")
            submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Signing in..."):
                    result = sign_in(email.strip().lower(), password)
                if result["success"]:
                    st.rerun()
                else:
                    st.error(result["error"])

        if st.button("Forgot password?"):
            st.session_state["lp_forgot"] = True
            st.rerun()

    with tab_register:
        st.subheader("Create a Prayer Warrior Account")

        try:
            from modules.rbac import get_pastors_list
            pastors = get_pastors_list()
        except Exception:
            pastors = []

        with st.form("register_form"):
            reg_email = st.text_input("Email", placeholder="you@church.org", key="reg_email")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", placeholder="John")
            with col2:
                last_name = st.text_input("Last Name", placeholder="Doe")
            preferred_name = st.text_input("Preferred Name", placeholder="What should we call you?")

            if pastors:
                pastor_options = {p["display_name"] + f" ({p['email']})": p["user_id"] for p in pastors}
                selected_pastor = st.selectbox("Your Pastor", options=list(pastor_options.keys()))
                pastor_id = pastor_options[selected_pastor] if selected_pastor else None
            else:
                st.warning("No pastors available. Contact your administrator.")
                pastor_id = None
                selected_pastor = None

            membership_card  = st.text_input("Membership Card ID (optional)", placeholder="e.g. TKT1694")
            prayer_benchmark = st.number_input("Daily Prayer Goal (minutes)", min_value=15, max_value=480, value=60, step=15)
            reg_submitted    = st.form_submit_button("Create Account", type="primary", use_container_width=True)

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
                    with st.spinner("Setting up your account..."):
                        seed_user_data(
                            user_id=result["user_id"],
                            preferred_name=(preferred_name.strip() or first_name.strip()),
                            prayer_benchmark=prayer_benchmark,
                        )
                    st.success("Account created! You can now sign in.")
                    st.info(f"Your temporary password is: **{DEFAULT_PASSWORDS['prayer_warrior']}** — you'll be asked to change it on first login.")
                else:
                    st.error(result["error"])