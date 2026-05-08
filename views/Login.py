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

/* Daybreak font classes */
.lp-brand-name {
    font-family: 'Cormorant', serif;
    font-size: 20px; font-weight: 600; color: #1A1208;
    letter-spacing: 0.04em; line-height: 1.2;
}
.lp-brand-tag {
    font-size: 9px; color: rgba(184,90,48,0.72);
    text-transform: uppercase; letter-spacing: 2.5px;
    font-weight: 700; font-family: 'Jost', sans-serif;
}
.lp-brand-headline {
    font-family: 'Cormorant', serif; font-size: 38px; font-weight: 600;
    color: #1A1208; line-height: 1.15; letter-spacing: -0.01em;
    margin-bottom: 14px;
}
.lp-brand-sub {
    font-size: 14px; color: #5A4A32;
    line-height: 1.72; font-family: 'Jost', sans-serif; margin-bottom: 36px;
}
.lp-verse-text {
    font-family: 'Cormorant', serif;
    font-style: italic; font-size: 15px;
    color: #1A1208; line-height: 1.82; margin-bottom: 10px;
}
.lp-verse-ref {
    font-size: 13px; color: #B85A30;
    font-family: 'Cormorant', serif; font-weight: 600; letter-spacing: 0.04em;
}
.lp-form-title {
    font-family: 'Cormorant', serif; font-size: 28px; font-weight: 600;
    color: #1A1208; letter-spacing: -0.01em; margin-bottom: 6px;
}
.lp-form-sub {
    font-size: 14px; color: #A09080;
    margin-bottom: 28px; font-family: 'Jost', sans-serif;
}
.lp-gold-rule {
    width: 48px; height: 2px;
    background: linear-gradient(90deg, #B85A30, #DFA830);
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
    brand_html = (
        '<div style="background:linear-gradient(148deg,rgba(253,250,245,0.97),rgba(247,242,234,0.94));'
        'border:1px solid rgba(184,90,48,0.18);border-radius:20px;padding:44px 40px 36px 40px;'
        'min-height:540px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(26,18,8,0.09);">'
        # Gold orb top-right
        '<div style="position:absolute;top:-60px;right:-60px;width:240px;height:240px;'
        'border-radius:50%;pointer-events:none;'
        'background:radial-gradient(circle,rgba(196,138,28,0.12) 0%,transparent 68%);"></div>'
        # Terra orb bottom-left
        '<div style="position:absolute;bottom:-40px;left:-40px;width:180px;height:180px;'
        'border-radius:50%;pointer-events:none;'
        'background:radial-gradient(circle,rgba(184,90,48,0.07) 0%,transparent 68%);"></div>'
        # Logo mark
        '<div style="display:flex;align-items:center;gap:12px;margin-bottom:44px;position:relative;z-index:1;">'
        '<div style="width:36px;height:36px;border-radius:9px;flex-shrink:0;background:#B85A30;'
        'display:flex;align-items:center;justify-content:center;'
        'font-family:Cormorant,serif;font-size:16px;font-weight:700;color:white;'
        'box-shadow:0 3px 10px rgba(184,90,48,0.32);">LP</div>'
        '<div><div class="lp-brand-name">Logos Pulse</div>'
        '<div class="lp-brand-tag">Sanctuary</div></div>'
        '</div>'
        # Headline
        '<div style="position:relative;z-index:1;">'
        '<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:3px;'
        'color:#B85A30;margin-bottom:14px;display:flex;align-items:center;gap:8px;'
        'font-family:Jost,sans-serif;">'
        '<span style="display:inline-block;width:20px;height:1.5px;background:#B85A30;"></span>'
        'Spiritual Growth</div>'
        '<div class="lp-brand-headline">Track your<br>walk with God</div>'
        '<div class="lp-brand-sub">A sanctuary for daily prayer, scripture reading, '
        'and spiritual reflection &#8212; designed for the whole church family.</div>'
        # Verse card
        '<div style="background:rgba(255,255,255,0.70);border:1px solid rgba(26,18,8,0.09);'
        'border-radius:16px;padding:20px 22px;box-shadow:0 2px 12px rgba(26,18,8,0.06);position:relative;">'
        '<div style="font-size:8.5px;text-transform:uppercase;letter-spacing:2.5px;color:#B85A30;'
        'font-weight:700;font-family:Jost,sans-serif;margin-bottom:12px;'
        'display:flex;align-items:center;gap:6px;">'
        '<span style="display:inline-block;width:14px;height:1px;background:#B85A30;opacity:.45;flex-shrink:0;"></span>'
        'Verse of the Day</div>'
        f'<div class="lp-verse-text">&#8220;{verse_text}&#8221;</div>'
        f'<div class="lp-verse-ref">&#8212; {verse_ref}</div>'
        '</div></div>'
        # Footer
        '<div style="font-size:10px;color:#A09080;text-transform:uppercase;letter-spacing:2.5px;'
        'font-family:Jost,sans-serif;margin-top:28px;position:relative;z-index:1;">'
        'Prayer &bull; Scripture &bull; Reflection</div>'
        '</div>'
    )
    st.markdown(brand_html, unsafe_allow_html=True)

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
