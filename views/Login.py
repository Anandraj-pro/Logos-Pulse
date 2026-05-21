import streamlit as st
from modules.auth import sign_in, sign_up, is_authenticated, DEFAULT_PASSWORDS
from modules.seed import seed_user_data
from modules.styles import inject_styles

if is_authenticated():
    st.rerun()

inject_styles()

# ── Codex login header ─────────────────────────────────────────────────────
st.markdown("""
<style>
/* Centre the entire page content */
[data-testid="stMainBlockContainer"] .block-container {
    max-width: 480px !important;
    margin: 0 auto !important;
    padding-top: 40px !important;
}

/* Hide native Streamlit title styling */
[data-testid="stHeading"] { display: none !important; }

/* Tab bar — Cinzel */
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
}

/* Ornament rule */
.codex-rule {
    display: flex; align-items: center; gap: 10px;
    margin: 12px 0;
}
.codex-rule::before, .codex-rule::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,138,28,0.35), transparent);
}
.codex-rule-diamond {
    width: 6px; height: 6px;
    border: 1px solid rgba(196,138,28,0.45);
    transform: rotate(45deg); flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:20px 0 8px 0;">
    <div style="
        display:inline-flex; align-items:center; justify-content:center;
        width:56px; height:56px; border-radius:50%;
        border:1px solid rgba(196,138,28,0.30);
        background:radial-gradient(circle, rgba(196,138,28,0.14) 0%, transparent 70%);
        font-size:26px; margin-bottom:14px;
        box-shadow:0 0 24px rgba(196,138,28,0.18);
    ">✟</div>
    <div style="
        font-family:'IM Fell English','Cormorant',Georgia,serif;
        font-size:32px; font-weight:400; font-style:italic;
        color:#F5E8C0; letter-spacing:0.04em; line-height:1.15;
    ">Logos Pulse</div>
    <div style="
        font-family:'Cinzel',serif; font-size:8.5px; letter-spacing:3.5px;
        color:rgba(196,138,28,0.50); text-transform:uppercase;
        font-weight:400; margin-top:6px;
    ">Spiritual Chronicle</div>
    <div class="codex-rule"><div class="codex-rule-diamond"></div></div>
</div>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────────────────────────────────
if "lp_forgot" not in st.session_state:
    st.session_state["lp_forgot"] = False

# ── Forgot Password ────────────────────────────────────────────────────────
if st.session_state["lp_forgot"]:
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="font-family:'IM Fell English',serif; font-size:20px; font-style:italic; color:#F5E8C0; margin-bottom:4px;">
            Reset thy Passage
        </div>
        <div style="font-family:'Cinzel',serif; font-size:9px; letter-spacing:2px; color:rgba(196,138,28,0.45); text-transform:uppercase;">
            Enter the email upon thy account
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("forgot_form"):
        forgot_email = st.text_input("Email address", placeholder="you@church.org")
        forgot_submitted = st.form_submit_button("Send Reset Link", type="primary", use_container_width=True)

    if forgot_submitted:
        if not forgot_email:
            st.error("Please enter your email address.")
        else:
            try:
                from modules.auth import request_password_reset
                with st.spinner("Sending..."):
                    request_password_reset(forgot_email.strip().lower())
            except Exception:
                pass
            st.success("If an account exists with that address, a reset link has been dispatched.")

    if st.button("← Return to Sign In", use_container_width=True):
        st.session_state["lp_forgot"] = False
        st.rerun()

# ── Main Login / Register ──────────────────────────────────────────────────
else:
    tab_login, tab_register = st.tabs(["Enter the Chronicle", "Register"])

    with tab_login:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        with st.form("login_form"):
            email    = st.text_input("Email address",  placeholder="you@church.org")
            password = st.text_input("Password", type="password", placeholder="Your secret passage")
            submitted = st.form_submit_button("Open the Chronicle", type="primary", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("Please enter both your email and password.")
            else:
                with st.spinner("Opening the chronicle..."):
                    result = sign_in(email.strip().lower(), password)
                if result["success"]:
                    st.rerun()
                else:
                    st.error(result["error"])

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("Forgot thy password?", use_container_width=True):
            st.session_state["lp_forgot"] = True
            st.rerun()

        st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <div style="font-family:'Cinzel',serif; font-size:8px; letter-spacing:2px;
                        color:rgba(196,138,28,0.25); text-transform:uppercase;">
                ✦ &nbsp; ✦ &nbsp; ✦
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_register:
        st.markdown("""
        <div style="margin-bottom:16px;">
            <div style="font-family:'IM Fell English',serif; font-size:18px; font-style:italic; color:#F5E8C0; margin-bottom:3px;">
                Enter the Congregation
            </div>
            <div style="font-family:'Cinzel',serif; font-size:8.5px; letter-spacing:2px;
                        color:rgba(196,138,28,0.45); text-transform:uppercase;">
                Create a Prayer Warrior account
            </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            from modules.rbac import get_pastors_list
            pastors = get_pastors_list()
        except Exception:
            pastors = []

        with st.form("register_form"):
            reg_email = st.text_input("Email address", placeholder="you@church.org", key="reg_email")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", placeholder="John")
            with col2:
                last_name = st.text_input("Last Name", placeholder="Doe")
            preferred_name = st.text_input("Preferred Name", placeholder="What shall we call you?")

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
            reg_submitted    = st.form_submit_button("Join the Chronicle", type="primary", use_container_width=True)

        if reg_submitted:
            if not reg_email or not first_name or not last_name:
                st.error("Please fill in all required fields.")
            elif not pastor_id:
                st.error("Please select your pastor.")
            else:
                with st.spinner("Opening your chronicle..."):
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
                    with st.spinner("Illuminating your pages..."):
                        seed_user_data(
                            user_id=result["user_id"],
                            preferred_name=(preferred_name.strip() or first_name.strip()),
                            prayer_benchmark=prayer_benchmark,
                        )
                    st.success("Your chronicle has been prepared. You may now sign in.")
                    st.info(f"Your temporary password is: **{DEFAULT_PASSWORDS['prayer_warrior']}** — you will be asked to change it upon first entry.")
                else:
                    st.error(result["error"])