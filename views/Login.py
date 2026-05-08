import streamlit as st
import random
from modules.styles import inject_styles
from modules.auth import sign_in, sign_up, is_authenticated, DEFAULT_PASSWORDS
from modules.seed import seed_user_data

inject_styles()

if is_authenticated():
    st.rerun()

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

# ── Layout + typography overrides ─────────────────────────────────────────────
# inject_styles() adds padding-top:72px for the authenticated nav bar.
# Login has no nav bar, so we reset the block-container and go edge-to-edge.
st.markdown("""
<style>
section[data-testid="stSidebar"] { display: none !important; }

[data-testid="stMainBlockContainer"],
.main .block-container,
.block-container {
    padding-top:    0 !important;
    padding-left:   0 !important;
    padding-right:  0 !important;
    padding-bottom: 0 !important;
    max-width:      100% !important;
    margin:         0 !important;
}

[data-testid="stHorizontalBlock"] { gap: 0 !important; }
[data-testid="column"] {
    padding-left:  0 !important;
    padding-right: 0 !important;
}

/* Right column: white form panel with terra accent bar */
[data-testid="column"]:nth-child(2) {
    background: #FFFFFF !important;
    border-left: 1px solid rgba(26,18,8,0.07) !important;
    padding: 52px 56px 52px 52px !important;
    position: relative !important;
}
[data-testid="column"]:nth-child(2)::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #B85A30, #DFA830 48%, #B85A30);
    pointer-events: none;
}

/* Left panel overline label */
.lp-overline {
    font-size: 10px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: #B85A30;
    font-family: 'Jost', sans-serif;
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 16px;
}
.lp-overline::before {
    content: ''; display: inline-block;
    width: 24px; height: 1.5px; background: #B85A30;
}

.lp-headline {
    font-family: 'Cormorant', serif;
    font-size: 44px; font-weight: 600;
    color: #1A1208; line-height: 1.08;
    letter-spacing: -0.01em; margin-bottom: 18px;
}

.lp-body {
    font-size: 15px; color: #5A4A32;
    line-height: 1.78; font-family: 'Jost', sans-serif;
    margin-bottom: 38px; max-width: 320px;
}

/* Verse card */
.lp-verse-card {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(196,144,42,0.22);
    border-radius: 18px; padding: 22px 24px;
    box-shadow: 0 4px 20px rgba(26,18,8,0.07),
                inset 0 1px 0 rgba(255,255,255,0.90);
    backdrop-filter: blur(8px);
}
.lp-vlabel {
    font-size: 8.5px; text-transform: uppercase;
    letter-spacing: 2.5px; color: #B85A30;
    font-weight: 700; font-family: 'Jost', sans-serif;
    display: flex; align-items: center; gap: 7px;
    margin-bottom: 12px;
}
.lp-vlabel::before {
    content: ''; display: inline-block;
    width: 14px; height: 1px; background: rgba(184,90,48,0.45);
}
.lp-vtext {
    font-family: 'Cormorant', serif; font-style: italic;
    font-size: 16px; color: #1A1208; line-height: 1.85; margin-bottom: 10px;
}
.lp-vref {
    font-size: 13px; color: #B85A30;
    font-family: 'Cormorant', serif; font-weight: 600; letter-spacing: 0.04em;
}

.lp-tagline {
    font-size: 10px; color: #A09080;
    text-transform: uppercase; letter-spacing: 2.5px;
    font-family: 'Jost', sans-serif; margin-top: 32px;
    display: flex; align-items: center; gap: 10px;
}
.lp-tagline::before {
    content: ''; width: 24px; height: 1px;
    background: rgba(160,144,128,0.40); flex-shrink: 0;
}

/* Form panel typography */
.lp-form-title {
    font-family: 'Cormorant', serif; font-size: 32px; font-weight: 600;
    color: #1A1208; letter-spacing: -0.01em; margin-bottom: 5px;
}
.lp-form-sub {
    font-size: 14px; color: #A09080;
    font-family: 'Jost', sans-serif; margin-bottom: 14px;
}
.lp-gold-rule {
    width: 48px; height: 2px;
    background: linear-gradient(90deg, #B85A30, #DFA830);
    border-radius: 2px; margin-bottom: 28px;
}
.lp-copyright {
    font-size: 11px; color: #C0B5A5;
    font-family: 'Jost', sans-serif;
    margin-top: 40px; letter-spacing: 0.3px; text-align: center;
}

/* Entrance animations */
@keyframes lp-rise {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.lp-a1 { animation: lp-rise 0.65s 0.04s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a2 { animation: lp-rise 0.65s 0.12s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a3 { animation: lp-rise 0.65s 0.22s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a4 { animation: lp-rise 0.65s 0.32s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a5 { animation: lp-rise 0.65s 0.10s cubic-bezier(0.22,1,0.36,1) both; }

@media (max-width: 768px) {
    .lp-headline { font-size: 30px; }
    .lp-body     { font-size: 14px; margin-bottom: 28px; }
    [data-testid="column"]:nth-child(2) {
        padding: 36px 28px !important;
        border-left: none !important;
        border-top: 3px solid #B85A30 !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
col_brand, col_form = st.columns([9, 11], gap="small")

# ── LEFT: Brand panel ─────────────────────────────────────────────────────────
with col_brand:
    brand_html = (
        '<div style="background:linear-gradient(150deg,#F9F5EF 0%,#F2E8D9 55%,#EBE0CC 100%);'
        'min-height:100vh;padding:48px 44px 44px;'
        'display:flex;flex-direction:column;position:relative;overflow:hidden;">'

        '<div style="position:absolute;top:-80px;right:-80px;width:360px;height:360px;'
        'border-radius:50%;pointer-events:none;'
        'background:radial-gradient(circle,rgba(196,144,42,0.13) 0%,transparent 65%);"></div>'

        '<div style="position:absolute;bottom:-60px;left:-60px;width:280px;height:280px;'
        'border-radius:50%;pointer-events:none;'
        'background:radial-gradient(circle,rgba(184,90,48,0.07) 0%,transparent 65%);"></div>'

        '<div style="position:absolute;inset:0;pointer-events:none;'
        'background:repeating-linear-gradient(-45deg,'
        'rgba(196,144,42,0.018) 0px,rgba(196,144,42,0.018) 1px,'
        'transparent 1px,transparent 18px);"></div>'

        '<div class="lp-a1" style="display:flex;align-items:center;gap:14px;'
        'margin-bottom:60px;position:relative;z-index:1;">'
        '<div style="width:42px;height:42px;border-radius:11px;background:#B85A30;'
        'display:flex;align-items:center;justify-content:center;'
        'font-family:Cormorant,serif;font-size:18px;font-weight:700;color:white;'
        'box-shadow:0 4px 14px rgba(184,90,48,0.36);flex-shrink:0;">LP</div>'
        '<div>'
        '<div style="font-family:Cormorant,serif;font-size:21px;font-weight:600;'
        'color:#1A1208;letter-spacing:0.04em;line-height:1.2;">Logos Pulse</div>'
        '<div style="font-size:9px;color:rgba(184,90,48,0.72);text-transform:uppercase;'
        'letter-spacing:2.5px;font-weight:700;font-family:Jost,sans-serif;">Sanctuary</div>'
        '</div></div>'

        '<div class="lp-overline lp-a2" style="position:relative;z-index:1;">Spiritual Growth</div>'

        '<div class="lp-headline lp-a2" style="position:relative;z-index:1;">'
        'Track your<br>walk with God</div>'

        '<div class="lp-body lp-a3" style="position:relative;z-index:1;">'
        'A sanctuary for daily prayer, scripture reading, and spiritual reflection '
        '&#8212; designed for the whole church family.</div>'

        '<div class="lp-verse-card lp-a4" style="position:relative;z-index:1;">'
        '<div class="lp-vlabel">Verse of the Day</div>'
        f'<div class="lp-vtext">&#8220;{verse_text}&#8221;</div>'
        f'<div class="lp-vref">&#8212; {verse_ref}</div>'
        '</div>'

        '<div class="lp-tagline" style="position:relative;z-index:1;">'
        'Prayer &bull; Scripture &bull; Reflection</div>'

        '</div>'
    )
    st.markdown(brand_html, unsafe_allow_html=True)

# ── RIGHT: Form panel ─────────────────────────────────────────────────────────
with col_form:
    tab_login, tab_register, tab_forgot = st.tabs(["🔑 Sign In", "✏️ Register", "🔄 Forgot Password"])

    # ── SIGN IN ───────────────────────────────────────────────────────────────
    with tab_login:
        st.markdown(
            '<div class="lp-form-title lp-a5">Welcome back</div>'
            '<div class="lp-form-sub">Sign in to continue your spiritual journey</div>'
            '<div class="lp-gold-rule"></div>',
            unsafe_allow_html=True
        )
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
        st.markdown(
            '<div class="lp-form-title">Join the sanctuary</div>'
            '<div class="lp-form-sub">Create a Prayer Warrior account to begin your journey.</div>'
            '<div class="lp-gold-rule"></div>',
            unsafe_allow_html=True
        )

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

            membership_card  = st.text_input("Membership Card ID (optional)", placeholder="e.g. TKT1694")
            prayer_benchmark = st.number_input("Daily Prayer Goal (minutes)", min_value=15, max_value=480, value=60, step=15)
            reg_submitted    = st.form_submit_button("Create Account →", type="primary", use_container_width=True)

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
        st.markdown(
            '<div class="lp-form-title">Reset Password</div>'
            '<div class="lp-form-sub">Enter your email to receive a password reset link.</div>'
            '<div class="lp-gold-rule"></div>',
            unsafe_allow_html=True
        )
        with st.form("forgot_form"):
            forgot_email     = st.text_input("Email", placeholder="you@church.org", key="forgot_email")
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

    st.markdown(
        '<div class="lp-copyright">&#169; Logos Pulse &bull; Your daily spiritual companion</div>',
        unsafe_allow_html=True
    )
