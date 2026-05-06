import streamlit as st
import random
from modules.styles import inject_styles
from modules.auth import sign_in, sign_up, is_authenticated, DEFAULT_PASSWORDS
from modules.seed import seed_user_data

inject_styles()

if is_authenticated():
    st.rerun()

# ── Login-page typography & form classes only (no layout-critical styles here)
st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none !important; }

.lp-brand-name {
    font-family: 'Cinzel', serif;
    font-size: 20px; font-weight: 600; color: white;
    letter-spacing: 0.06em; line-height: 1.2;
}
.lp-brand-tag {
    font-size: 9px; color: rgba(196,144,42,0.72);
    text-transform: uppercase; letter-spacing: 2.5px;
    font-weight: 700; font-family: 'Nunito', sans-serif;
}
.lp-brand-headline {
    font-family: 'Cinzel', serif; font-size: 34px; font-weight: 600;
    color: white; line-height: 1.22; letter-spacing: 0.02em;
    text-shadow: 0 3px 22px rgba(0,0,0,0.30); margin-bottom: 14px;
}
.lp-brand-headline em { font-style: italic; color: #E8C050; }
.lp-brand-sub {
    font-size: 14px; color: rgba(255,255,255,0.46);
    line-height: 1.72; font-family: 'Nunito', sans-serif; margin-bottom: 36px;
}
.lp-verse-text {
    font-family: 'Spectral', 'EB Garamond', Georgia, serif;
    font-style: italic; font-size: 15px;
    color: rgba(255,255,255,0.82); line-height: 1.82; margin-bottom: 10px;
}
.lp-verse-ref {
    font-size: 13px; color: #C4902A;
    font-family: 'Cinzel', serif; font-weight: 500; letter-spacing: 0.04em;
}
.lp-form-title {
    font-family: 'Cinzel', serif; font-size: 28px; font-weight: 600;
    color: #140F1A; letter-spacing: 0.02em; margin-bottom: 6px;
}
.lp-form-sub {
    font-size: 14px; color: #8A85A0;
    margin-bottom: 28px; font-family: 'Nunito', sans-serif;
}
.lp-gold-rule {
    width: 48px; height: 2px;
    background: linear-gradient(90deg, #C4902A, #E8C050);
    border-radius: 2px; margin-bottom: 28px;
}
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

# ── LEFT: Brand panel — all critical styles are INLINE so the gradient always renders
with col_brand:
    st.markdown(f"""
    <div style="
        background:
            radial-gradient(ellipse at 18% 14%, rgba(196,144,42,0.22) 0%, transparent 50%),
            radial-gradient(ellipse at 82% 82%, rgba(107,63,168,0.20) 0%, transparent 48%),
            linear-gradient(152deg, #170F4A 0%, #2A1D7E 40%, #3C2D90 68%, #4A2A88 100%);
        border-radius: 20px;
        padding: 44px 40px 36px 40px;
        min-height: 540px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 24px 64px rgba(42,29,126,0.36), 0 4px 16px rgba(42,29,126,0.20);
    ">

        <!-- Diagonal hatching overlay -->
        <div style="
            position:absolute; inset:0; border-radius:20px; pointer-events:none;
            background: repeating-linear-gradient(
                -52deg,
                rgba(255,255,255,0.013) 0px, rgba(255,255,255,0.013) 1px,
                transparent 1px, transparent 14px
            );
        "></div>

        <!-- Gold orb top-right -->
        <div style="
            position:absolute; top:-70px; right:-70px;
            width:300px; height:300px; border-radius:50%; pointer-events:none;
            background: radial-gradient(circle, rgba(196,144,42,0.18) 0%, transparent 66%);
        "></div>

        <!-- Logo -->
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:44px; position:relative; z-index:1;">
            <div style="
                width:42px; height:42px; border-radius:11px; flex-shrink:0;
                background:rgba(196,144,42,0.14); border:1px solid rgba(196,144,42,0.40);
                display:flex; align-items:center; justify-content:center; font-size:20px;
            ">&#128214;</div>
            <div>
                <div class="lp-brand-name">Logos Pulse</div>
                <div class="lp-brand-tag">Sanctuary</div>
            </div>
        </div>

        <!-- Headline + sub -->
        <div style="position:relative; z-index:1;">
            <div class="lp-brand-headline">
                Track your<br><em>walk with God</em>
            </div>
            <div class="lp-brand-sub">
                A sanctuary for daily prayer, scripture reading,
                and spiritual reflection &#8212; designed for the whole
                church family.
            </div>

            <!-- Verse card -->
            <div style="
                background:rgba(255,255,255,0.07);
                border:1px solid rgba(196,144,42,0.26);
                border-radius:16px; padding:20px 22px;
                backdrop-filter:blur(8px); position:relative;
            ">
                <div style="
                    font-size:9px; text-transform:uppercase; letter-spacing:2.5px;
                    color:rgba(196,144,42,0.78); font-weight:700;
                    font-family:'Nunito',sans-serif; margin-bottom:12px;
                    display:flex; align-items:center; gap:8px;
                ">
                    <span style="display:inline-block;width:22px;height:1px;
                        background:rgba(196,144,42,0.5);flex-shrink:0;"></span>
                    Verse of the Day
                </div>
                <div class="lp-verse-text">&#8220;{verse_text}&#8221;</div>
                <div class="lp-verse-ref">&#8212; {verse_ref}</div>
            </div>
        </div>

        <!-- Footer -->
        <div style="
            font-size:10px; color:rgba(255,255,255,0.20);
            text-transform:uppercase; letter-spacing:2.5px;
            font-family:'Nunito',sans-serif; margin-top:28px;
            position:relative; z-index:1;
        ">Prayer &bull; Scripture &bull; Reflection</div>

    </div>
    """, unsafe_allow_html=True)

# ── RIGHT: Form panel ─────────────────────────────────────────────────────────
with col_form:
    st.markdown('<div style="padding: 44px 8px 36px 28px;">', unsafe_allow_html=True)

    tab_login, tab_register, tab_forgot = st.tabs(["🔑 Sign In", "✏️ Register", "🔄 Forgot Password"])

    # ── LOGIN ─────────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown("""
        <div class="lp-form-title">Welcome back</div>
        <div class="lp-gold-rule"></div>
        <div class="lp-form-sub">Sign in to continue your spiritual journey</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email    = st.text_input("Email",    placeholder="you@church.org")
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
                st.warning("No pastors available. Ensure Supabase secrets are configured.")
                pastor_id = None
                selected_pastor = None

            membership_card    = st.text_input("Membership Card ID (optional)", placeholder="e.g. TKT1694")
            prayer_benchmark   = st.number_input("Daily Prayer Goal (minutes)", min_value=15, max_value=480, value=60, step=15)
            reg_submitted      = st.form_submit_button("Create Account →", type="primary", use_container_width=True)

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
            forgot_email   = st.text_input("Email", placeholder="you@church.org", key="forgot_email")
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
