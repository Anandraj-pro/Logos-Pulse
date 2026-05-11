import streamlit as st
import random
from modules.styles import inject_styles
from modules.auth import sign_in, sign_up, is_authenticated, DEFAULT_PASSWORDS
from modules.seed import seed_user_data

inject_styles()

if is_authenticated():
    st.rerun()

if "lp_forgot" not in st.session_state:
    st.session_state["lp_forgot"] = False

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

st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

[data-testid="stMainBlockContainer"],
.main .block-container, .block-container {
    padding: 0 !important; max-width: 100% !important; margin: 0 !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 0 !important; min-height: 100vh !important; align-items: stretch !important;
}
[data-testid="column"] { padding: 0 !important; }

[data-testid="column"]:nth-child(2) {
    background: #F5F1E9 !important;
    border-left: 1px solid rgba(42,29,126,0.10) !important;
}
[data-testid="column"]:nth-child(2) > div:first-child {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    min-height: 100vh !important;
    padding: 48px 56px !important;
    box-sizing: border-box !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(42,29,126,0.07) !important;
    border: 1px solid rgba(42,29,126,0.09) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 0 !important;
    margin-bottom: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 9px !important;
    padding: 10px 0 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    color: #8A85A0 !important;
    border: none !important;
    flex: 1 !important;
    justify-content: center !important;
    font-family: 'Jost', sans-serif !important;
    transition: all 0.25s !important;
    min-height: 44px !important;
}
.stTabs [aria-selected="true"][data-baseweb="tab"] {
    background: linear-gradient(135deg, #2A1D7E 0%, #3D2DA0 100%) !important;
    color: white !important;
    box-shadow: 0 2px 10px rgba(42,29,126,0.30) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-family: 'Jost', sans-serif !important;
    font-size: 11px !important; font-weight: 700 !important;
    color: #8A85A0 !important; letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
}
.stTextInput, .stNumberInput, .stSelectbox { margin-bottom: 4px !important; }

[data-testid="stFormSubmitButton"] > button {
    min-height: 50px !important; font-size: 15px !important;
    letter-spacing: 0.5px !important; margin-top: 8px !important;
    background: linear-gradient(135deg, #2A1D7E 0%, #4B3DC0 100%) !important;
    border: none !important;
}

.lp-forgot-wrap button {
    background: transparent !important; border: none !important;
    color: #2A1D7E !important; font-weight: 600 !important;
    font-size: 12.5px !important; box-shadow: none !important;
    padding: 2px 0 !important; text-align: right !important;
    justify-content: flex-end !important;
}
.lp-forgot-wrap button:hover {
    text-decoration: underline !important;
    background: transparent !important; box-shadow: none !important;
}
.lp-back-wrap button {
    background: transparent !important; border: none !important;
    color: #8A85A0 !important; font-weight: 600 !important;
    font-size: 13px !important; box-shadow: none !important; padding: 0 !important;
}
.lp-back-wrap button:hover {
    color: #2A1D7E !important; background: transparent !important;
    box-shadow: none !important;
}

.lp-form-title {
    font-family: 'Cinzel', 'Cormorant', serif; font-size: 28px; font-weight: 400;
    color: #1A1A2E; letter-spacing: 0.01em; margin-bottom: 5px; line-height: 1.3;
}
.lp-form-sub { font-size: 14px; color: #8A85A0; font-family: 'Jost', sans-serif; margin-bottom: 20px; }
.lp-gold-rule {
    width: 48px; height: 2px;
    background: linear-gradient(90deg, #2A1D7E, #C4902A);
    border-radius: 2px; margin-bottom: 24px;
}
.lp-copyright {
    font-size: 11px; color: #C8C4D0; font-family: 'Jost', sans-serif;
    margin-top: 32px; letter-spacing: 0.3px; text-align: center;
}

.lp-headline {
    font-family: 'Cinzel', 'Cormorant', serif; font-size: 38px; font-weight: 300;
    color: #FFFFFF; line-height: 1.15; letter-spacing: 0.01em; margin-bottom: 16px;
}
.lp-headline span { color: #E8C050; }
.lp-body {
    font-size: 14px; color: rgba(255,255,255,0.38); line-height: 1.85;
    font-family: 'Jost', sans-serif; margin-bottom: 36px; max-width: 280px;
}
.lp-verse-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(201,152,42,0.16);
    border-radius: 16px; padding: 22px 24px; backdrop-filter: blur(16px);
}
.lp-vlabel {
    font-size: 9px; text-transform: uppercase; letter-spacing: 3px; color: rgba(201,152,42,0.6);
    font-weight: 700; font-family: 'Jost', sans-serif;
    display: flex; align-items: center; gap: 8px; margin-bottom: 12px;
}
.lp-vlabel::before {
    content: ''; display: inline-block; width: 14px; height: 1.5px; background: rgba(201,152,42,0.65);
}
.lp-vtext {
    font-family: 'Cinzel', 'Cormorant', serif; font-style: italic;
    font-size: 16px; color: rgba(255,255,255,0.68); line-height: 1.85; margin-bottom: 10px;
}
.lp-vref { font-size: 11.5px; color: #c9982a; font-family: 'Cinzel', serif; font-weight: 500; letter-spacing: 0.04em; }
.lp-tagline {
    font-size: 9px; color: rgba(255,255,255,0.18); text-transform: uppercase; letter-spacing: 3.5px;
    font-family: 'Jost', sans-serif; margin-top: 32px;
    display: flex; align-items: center; gap: 14px;
}
.lp-mobile-hdr { display: none; }

@media (max-width: 639px) {
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    [data-testid="column"]:nth-child(1) {
        display: none !important; max-width: 0 !important;
        min-width: 0 !important; overflow: hidden !important;
    }
    [data-testid="column"]:nth-child(2) {
        width: 100% !important; max-width: 100% !important;
        min-width: 100% !important; flex: 1 1 100% !important;
        border-left: none !important;
    }
    [data-testid="column"]:nth-child(2) > div:first-child {
        justify-content: flex-start !important;
        padding: 0 24px 48px !important;
    }
    .lp-mobile-hdr { display: block !important; margin: 0 -24px 32px -24px !important; }
    .lp-headline { font-size: 30px !important; }
}

@keyframes lp-rise {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
.lp-a1 { animation: lp-rise 0.65s 0.04s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a2 { animation: lp-rise 0.65s 0.12s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a3 { animation: lp-rise 0.65s 0.22s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a4 { animation: lp-rise 0.65s 0.32s cubic-bezier(0.22,1,0.36,1) both; }
.lp-a5 { animation: lp-rise 0.65s 0.10s cubic-bezier(0.22,1,0.36,1) both; }
</style>
""", unsafe_allow_html=True)

col_brand, col_form = st.columns([9, 11], gap="small")

with col_brand:
    brand_html = (
        '<div style="background:linear-gradient(148deg,#0F0930 0%,#1A1060 30%,#221574 60%,#2E1E88 100%);'
        'min-height:100vh;padding:52px 48px 44px;'
        'display:flex;flex-direction:column;justify-content:space-between;'
        'position:relative;overflow:hidden;">'

        '<div style="position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);'
        'width:320px;height:320px;border-radius:50%;pointer-events:none;'
        'background:radial-gradient(circle,rgba(196,144,42,0.10) 0%,transparent 68%);"></div>'

        '<svg style="position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);" '
        'width="110" height="150" viewBox="0 0 110 150" fill="none">'
        '<defs><linearGradient id="cg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#C4902A" stop-opacity="0.2"/>'
        '<stop offset="50%" stop-color="#E8C050" stop-opacity="0.55"/>'
        '<stop offset="100%" stop-color="#C4902A" stop-opacity="0.15"/>'
        '</linearGradient></defs>'
        '<rect x="48" y="0" width="14" height="150" rx="7" fill="url(#cg)"/>'
        '<rect x="0" y="48" width="110" height="14" rx="7" fill="url(#cg)"/>'
        '</svg>'

        '<div style="position:absolute;inset:0;pointer-events:none;'
        'background-image:radial-gradient(circle,rgba(255,255,255,0.08) 1px,transparent 1px);'
        'background-size:36px 36px;opacity:0.5;"></div>'

        '<div style="position:absolute;top:0;left:32px;right:32px;height:1px;'
        'background:linear-gradient(90deg,transparent,rgba(201,152,42,0.35),transparent);"></div>'

        '<div class="lp-a1" style="display:flex;align-items:center;gap:12px;'
        'margin-bottom:60px;position:relative;z-index:1;">'
        '<div style="width:40px;height:40px;border-radius:50%;flex-shrink:0;'
        'background:rgba(201,152,42,0.1);border:1px solid rgba(201,152,42,0.3);'
        'display:flex;align-items:center;justify-content:center;">'
        '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#c9982a" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
        '</svg></div>'
        '<div>'
        '<div style="font-family:Cinzel,Cormorant,serif;font-size:15px;font-weight:400;'
        'color:#FFFFFF;letter-spacing:0.05em;line-height:1.2;">Logos Pulse</div>'
        '<div style="font-size:9px;color:rgba(201,152,42,0.5);text-transform:uppercase;'
        'letter-spacing:3.5px;font-weight:700;font-family:Jost,sans-serif;">Sanctuary</div>'
        '</div></div>'

        '<div class="lp-headline lp-a2" style="position:relative;z-index:1;">'
        'Track your<br><span>walk with God</span></div>'

        '<div class="lp-body lp-a3" style="position:relative;z-index:1;">'
        'A sanctuary for daily prayer, scripture reading, and spiritual '
        'reflection &#8212; built for the whole church family.</div>'

        '<div class="lp-verse-card lp-a4" style="position:relative;z-index:1;">'
        '<div class="lp-vlabel">Verse of the Day</div>'
        f'<div class="lp-vtext">&#8220;{verse_text}&#8221;</div>'
        f'<div class="lp-vref">&#8212; {verse_ref}</div>'
        '</div>'

        '<div class="lp-tagline lp-a4" style="position:relative;z-index:1;">'
        'Prayer <span style="opacity:0.3;margin:0 2px;">|</span> '
        'Scripture <span style="opacity:0.3;margin:0 2px;">|</span> Reflection'
        '</div>'
        '</div>'
    )
    st.markdown(brand_html, unsafe_allow_html=True)

with col_form:
    mobile_hdr = (
        '<div class="lp-mobile-hdr" style="'
        'background:linear-gradient(148deg,#0F0930 0%,#1A1060 60%,#221574 100%);'
        'padding:24px 24px 20px;border-bottom:1px solid rgba(201,152,42,0.18);'
        'position:relative;overflow:hidden;">'
        '<div style="display:flex;align-items:center;gap:12px;position:relative;">'
        '<div style="width:36px;height:36px;border-radius:50%;flex-shrink:0;'
        'background:rgba(201,152,42,0.1);border:1px solid rgba(201,152,42,0.3);'
        'display:flex;align-items:center;justify-content:center;">'
        '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#c9982a" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
        '</svg></div>'
        '<div>'
        '<div style="font-family:Cinzel,Cormorant,serif;font-size:17px;font-weight:400;'
        'color:#FFFFFF;letter-spacing:0.04em;line-height:1.2;">Logos Pulse</div>'
        '<div style="font-size:9px;color:rgba(201,152,42,0.5);text-transform:uppercase;'
        'letter-spacing:2.5px;font-weight:700;font-family:Jost,sans-serif;">Sanctuary</div>'
        '</div></div>'
        f'<div style="font-family:Cinzel,Cormorant,serif;font-style:italic;font-size:13px;'
        f'color:rgba(255,255,255,0.55);line-height:1.65;margin-top:14px;">'
        f'&#8220;{verse_text}&#8221;'
        f' <span style="color:#c9982a;font-weight:600;font-style:normal;">&#8212; {verse_ref}</span>'
        f'</div>'
        '</div>'
    )
    st.markdown(mobile_hdr, unsafe_allow_html=True)

    if st.session_state["lp_forgot"]:
        st.markdown(
            '<div class="lp-form-title lp-a5">Reset Password</div>'
            '<div class="lp-form-sub">Enter your email and we\'ll send a reset link.</div>'
            '<div class="lp-gold-rule"></div>',
            unsafe_allow_html=True
        )
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

        st.markdown('<div class="lp-back-wrap">', unsafe_allow_html=True)
        if st.button("← Back to Sign In", key="btn_back"):
            st.session_state["lp_forgot"] = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        tab_login, tab_register = st.tabs(["Sign In", "Register"])

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

            _, fp_col = st.columns([3, 2])
            with fp_col:
                st.markdown('<div class="lp-forgot-wrap">', unsafe_allow_html=True)
                if st.button("Forgot password?", key="btn_forgot", use_container_width=True):
                    st.session_state["lp_forgot"] = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

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
                    st.warning("No pastors available. Contact your administrator.")
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

    st.markdown(
        '<div class="lp-copyright">&#169; Logos Pulse &bull; Your daily spiritual companion</div>',
        unsafe_allow_html=True
    )