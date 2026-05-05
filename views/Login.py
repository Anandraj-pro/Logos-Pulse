import streamlit as st
import random
from modules.styles import inject_styles
from modules.auth import sign_in, sign_up, is_authenticated, DEFAULT_PASSWORDS
from modules.seed import seed_user_data

inject_styles()

if is_authenticated():
    st.rerun()

# ── Page-level CSS ────────────────────────────────────────────────────────────
# The vine SVG is embedded here as a CSS background-image data URI so that
# Streamlit's HTML sanitizer (which strips <svg> tags) cannot remove it.
_VINE_SVG = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 380 700'%3E"
    "%3Cpath d='M190 700 C190 700 155 560 148 410 C140 255 175 120 190 0'"
    " stroke='%23c9982a' stroke-width='1.1' fill='none' opacity='0.30'/%3E"
    "%3Cpath d='M174 510 C138 478 102 488 68 455'"
    " stroke='%23c9982a' stroke-width='0.7' fill='none' opacity='0.22'/%3E"
    "%3Cpath d='M166 358 C120 328 90 348 52 316'"
    " stroke='%23c9982a' stroke-width='0.7' fill='none' opacity='0.18'/%3E"
    "%3Cpath d='M202 460 C242 428 288 444 328 412'"
    " stroke='%23c9982a' stroke-width='0.7' fill='none' opacity='0.22'/%3E"
    "%3Cpath d='M198 285 C248 254 300 268 348 238'"
    " stroke='%23c9982a' stroke-width='0.7' fill='none' opacity='0.18'/%3E"
    "%3Cellipse cx='68' cy='455' rx='13' ry='8' fill='%23c9982a' opacity='0.14'"
    " transform='rotate(-28 68 455)'/%3E"
    "%3Cellipse cx='328' cy='412' rx='13' ry='8' fill='%23c9982a' opacity='0.14'"
    " transform='rotate(22 328 412)'/%3E"
    "%3Cg opacity='0.22' transform='translate(22,26)'%3E"
    "%3Crect x='15' y='6' width='4' height='22' rx='2' fill='%23c9982a'/%3E"
    "%3Crect x='8' y='13' width='18' height='4' rx='2' fill='%23c9982a'/%3E"
    "%3C/g%3E"
    "%3Cg opacity='0.14' transform='translate(336,636)'%3E"
    "%3Crect x='7' y='0' width='3' height='17' rx='1.5' fill='%23c9982a'/%3E"
    "%3Crect x='2' y='6' width='13' height='3' rx='1.5' fill='%23c9982a'/%3E"
    "%3C/g%3E"
    "%3C/svg%3E"
)

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] > div:first-child > div:first-child {{
    padding-top: 0 !important;
}}
[data-testid="block-container"] {{
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
}}
section[data-testid="stSidebar"] {{ display: none !important; }}

/* ── Brand panel ── */
.lp-brand-panel {{
    background:
        radial-gradient(ellipse at 20% 15%, rgba(196,144,42,0.20) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(107,63,168,0.18) 0%, transparent 48%),
        linear-gradient(152deg, #170F4A 0%, #2A1D7E 40%, #3C2D90 70%, #4A2A88 100%);
    border-radius: 20px;
    padding: 52px 44px 40px 44px;
    min-height: 82vh;
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

/* Diagonal hatching + vine SVG — both as background-image layers */
.lp-brand-panel::before {{
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        url("{_VINE_SVG}"),
        repeating-linear-gradient(
            -52deg,
            rgba(255,255,255,0.012) 0px,
            rgba(255,255,255,0.012) 1px,
            transparent 1px,
            transparent 14px
        );
    background-size: cover, auto;
    background-repeat: no-repeat, repeat;
    pointer-events: none;
    border-radius: inherit;
}}

/* Gold orb top-right */
.lp-brand-panel::after {{
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(196,144,42,0.16) 0%, transparent 66%);
    border-radius: 50%;
    pointer-events: none;
}}

.lp-brand-logo {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 48px;
    position: relative;
    z-index: 1;
}}

.lp-brand-logo-icon {{
    width: 44px; height: 44px;
    border-radius: 12px;
    background: rgba(196,144,42,0.15);
    border: 1px solid rgba(196,144,42,0.40);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}}

.lp-brand-name {{
    font-family: 'Cinzel', serif;
    font-size: 20px;
    font-weight: 600;
    color: white;
    letter-spacing: 0.06em;
    line-height: 1.2;
}}

.lp-brand-tag {{
    font-size: 9px;
    color: rgba(196,144,42,0.7);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
}}

.lp-brand-headline {{
    font-family: 'Cinzel', serif;
    font-size: 36px;
    font-weight: 600;
    color: white;
    line-height: 1.22;
    letter-spacing: 0.02em;
    text-shadow: 0 3px 22px rgba(0,0,0,0.30);
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
}}

.lp-brand-headline em {{
    font-style: italic;
    color: #E8C050;
}}

.lp-brand-sub {{
    font-size: 14px;
    color: rgba(255,255,255,0.46);
    line-height: 1.72;
    font-family: 'Nunito', sans-serif;
    position: relative;
    z-index: 1;
    margin-bottom: 40px;
}}

.lp-verse-card {{
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(196,144,42,0.24);
    border-radius: 16px;
    padding: 22px 24px;
    backdrop-filter: blur(8px);
    position: relative;
    z-index: 1;
}}

.lp-verse-label {{
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: rgba(196,144,42,0.75);
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.lp-verse-label::before {{
    content: '';
    width: 24px; height: 1px;
    background: rgba(196,144,42,0.5);
    flex-shrink: 0;
}}

.lp-verse-text {{
    font-family: 'Spectral', 'EB Garamond', Georgia, serif;
    font-style: italic;
    font-size: 16px;
    color: rgba(255,255,255,0.82);
    line-height: 1.82;
    margin-bottom: 10px;
}}

.lp-verse-ref {{
    font-size: 13px;
    color: #C4902A;
    font-family: 'Cinzel', serif;
    font-weight: 500;
    letter-spacing: 0.04em;
}}

.lp-brand-footer {{
    font-size: 10px;
    color: rgba(255,255,255,0.20);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-family: 'Nunito', sans-serif;
    position: relative;
    z-index: 1;
    margin-top: 32px;
}}

/* ── Form panel ── */
.lp-form-panel {{
    padding: 52px 12px 40px 32px;
}}

.lp-form-title {{
    font-family: 'Cinzel', serif;
    font-size: 30px;
    font-weight: 600;
    color: #140F1A;
    letter-spacing: 0.02em;
    margin-bottom: 6px;
}}

.lp-form-sub {{
    font-size: 14px;
    color: #8A85A0;
    margin-bottom: 28px;
    font-family: 'Nunito', sans-serif;
}}

.lp-gold-rule {{
    width: 48px;
    height: 2px;
    background: linear-gradient(90deg, #C4902A, #E8C050);
    border-radius: 2px;
    margin-bottom: 28px;
}}
</style>
""", unsafe_allow_html=True)

# ── Daily verses ──────────────────────────────────────────────────────────────
VERSES = [
    ("Your word is a lamp to my feet and a light to my path.",  "Psalm 119:105"),
    ("The Lord is my shepherd; I shall not want.",               "Psalm 23:1"),
    ("Be still, and know that I am God.",                        "Psalm 46:10"),
    ("I can do all things through Christ who strengthens me.",   "Philippians 4:13"),
    ("Trust in the Lord with all your heart.",                   "Proverbs 3:5"),
    ("Those who hope in the Lord will renew their strength.",    "Isaiah 40:31"),
    ("Seek first his kingdom and his righteousness.",            "Matthew 6:33"),
]
verse_text, verse_ref = random.choice(VERSES)

# ── Two-column layout ─────────────────────────────────────────────────────────
col_brand, col_form = st.columns([9, 11], gap="large")

# ── LEFT: Brand panel ─────────────────────────────────────────────────────────
with col_brand:
    st.markdown(f"""
    <div class="lp-brand-panel">
        <div class="lp-brand-logo">
            <div class="lp-brand-logo-icon">&#128214;</div>
            <div>
                <div class="lp-brand-name">Logos Pulse</div>
                <div class="lp-brand-tag">Sanctuary</div>
            </div>
        </div>

        <div style="position:relative; z-index:1;">
            <div class="lp-brand-headline">
                Track your<br><em>walk with God</em>
            </div>
            <div class="lp-brand-sub">
                A sanctuary for daily prayer, scripture reading,
                and spiritual reflection &#8212; designed for the whole
                church family.
            </div>

            <div class="lp-verse-card">
                <div class="lp-verse-label">Verse of the Day</div>
                <div class="lp-verse-text">&#8220;{verse_text}&#8221;</div>
                <div class="lp-verse-ref">&#8212; {verse_ref}</div>
            </div>
        </div>

        <div class="lp-brand-footer">Prayer &bull; Scripture &bull; Reflection</div>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT: Form panel ─────────────────────────────────────────────────────────
with col_form:
    st.markdown('<div class="lp-form-panel">', unsafe_allow_html=True)

    tab_login, tab_register, tab_forgot = st.tabs(["🔑 Sign In", "✏️ Register", "🔄 Forgot Password"])

    # ── LOGIN ─────────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown("""
        <div class="lp-form-title">Welcome back</div>
        <div class="lp-gold-rule"></div>
        <div class="lp-form-sub">Sign in to continue your spiritual journey</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@church.org")
            password = st.text_input("Password", type="password", placeholder="Your password")
            submitted = st.form_submit_button("Sign In →", type="primary", use_container_width=True)

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

    # ── REGISTER ──────────────────────────────────────────────────────────────
    with tab_register:
        st.markdown("""
        <div class="lp-form-title">Join the sanctuary</div>
        <div class="lp-gold-rule"></div>
        <div class="lp-form-sub">Create a Prayer Warrior account to begin your journey.</div>
        """, unsafe_allow_html=True)

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
                st.warning("No pastors available. Ensure Supabase secrets are configured and pastor accounts exist.")
                pastor_id = None
                selected_pastor = None

            membership_card = st.text_input("Membership Card ID (optional)", placeholder="e.g. TKT1694")
            prayer_benchmark = st.number_input("Daily Prayer Goal (minutes)", min_value=15, max_value=480, value=60, step=15)
            reg_submitted = st.form_submit_button("Create Account →", type="primary", use_container_width=True)

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

    # ── FORGOT PASSWORD ───────────────────────────────────────────────────────
    with tab_forgot:
        st.markdown("""
        <div class="lp-form-title">Reset Password</div>
        <div class="lp-gold-rule"></div>
        <div class="lp-form-sub">Enter your email to receive a password reset link.</div>
        """, unsafe_allow_html=True)

        with st.form("forgot_form"):
            forgot_email = st.text_input("Email", placeholder="you@church.org", key="forgot_email")
            forgot_submitted = st.form_submit_button("Send Reset Link →", type="primary", use_container_width=True)

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

    st.markdown('</div>', unsafe_allow_html=True)
