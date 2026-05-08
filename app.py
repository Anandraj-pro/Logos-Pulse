import streamlit as st

from modules.auth import is_authenticated, sign_out, get_current_role

# ── Auto-restore session from URL token after idle reconnect ──
if not st.session_state.get("authenticated"):
    _saved_rt = st.query_params.get("_s")
    if _saved_rt:
        try:
            from modules.supabase_client import get_supabase_client as _gsc, get_admin_client as _gac
            _sc = _gsc()
            _resp = _sc.auth.refresh_session(_saved_rt)
            if _resp and _resp.session:
                _u = _resp.user
                _sess = _resp.session
                _pd = _gac().table("user_profiles") \
                    .select("*").eq("user_id", _u.id).single().execute().data
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = _u.id
                st.session_state["user_email"] = _u.email
                st.session_state["access_token"] = _sess.access_token
                st.session_state["refresh_token"] = _sess.refresh_token
                st.session_state["role"] = _pd["role"]
                st.session_state["must_change_password"] = _pd.get("must_change_password", False)
                st.session_state["preferred_name"] = (
                    _u.user_metadata.get("preferred_name")
                    or _u.user_metadata.get("first_name")
                    or _u.email.split("@")[0]
                )
                st.query_params["_s"] = _sess.refresh_token
        except Exception:
            st.query_params.pop("_s", None)

# ── Logout via query param (used by top nav sign-out link) ──
if st.query_params.get("action") == "logout":
    if st.session_state.get("impersonating"):
        st.session_state.pop("impersonating", None)
    sign_out()
    st.query_params.clear()
    st.rerun()

# --- Auth-aware navigation ---
authenticated = is_authenticated()

if not authenticated:
    st.set_page_config(
        page_title="Logos Pulse",
        page_icon="\U0001f64f",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={},
    )
    st.markdown('<style>[data-testid="stSidebar"]{display:none!important;}[data-testid="stSidebarCollapsedControl"]{display:none!important;}[data-testid="stHeader"]{display:none!important;}[data-testid="stToolbar"]{display:none!important;}[data-testid="stDecoration"]{display:none!important;}[data-testid="stStatusWidget"]{display:none!important;}#MainMenu{display:none!important;visibility:hidden!important;}.stAppToolbar{display:none!important;}.stDeployButton{display:none!important;}button[kind="header"]{display:none!important;}[data-testid="stAppViewContainer"]{padding-top:0!important;margin-top:0!important;}[data-testid="stMain"],.stMain,.main{padding-top:0!important;}[data-testid="stMainBlockContainer"],.main .block-container,.block-container{padding-top:24px!important;padding-left:24px!important;padding-right:24px!important;max-width:720px!important;margin-left:auto!important;margin-right:auto!important;}</style>', unsafe_allow_html=True)
    pg = st.navigation([
        st.Page("views/Login.py", title="Login", icon="\U0001f511", default=True),
    ])
    pg.run()

elif st.session_state.get("must_change_password"):
    st.set_page_config(
        page_title="Logos Pulse",
        page_icon="\U0001f64f",
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items={},
    )
    st.markdown('<style>[data-testid="stSidebar"]{display:none!important;}[data-testid="stSidebarCollapsedControl"]{display:none!important;}[data-testid="stHeader"]{display:none!important;}[data-testid="stToolbar"]{display:none!important;}[data-testid="stDecoration"]{display:none!important;}[data-testid="stStatusWidget"]{display:none!important;}#MainMenu{display:none!important;visibility:hidden!important;}.stAppToolbar{display:none!important;}.stDeployButton{display:none!important;}button[kind="header"]{display:none!important;}[data-testid="stAppViewContainer"]{padding-top:0!important;margin-top:0!important;}[data-testid="stMain"],.stMain,.main{padding-top:0!important;}[data-testid="stMainBlockContainer"],.main .block-container,.block-container{padding-top:24px!important;padding-left:24px!important;padding-right:24px!important;max-width:720px!important;margin-left:auto!important;margin-right:auto!important;}</style>', unsafe_allow_html=True)
    pg = st.navigation([
        st.Page("views/Change_Password.py", title="Change Password", icon="\U0001f510", default=True),
    ])
    pg.run()

else:
    # Check if onboarding needed
    _needs_onboarding = False
    try:
        from modules.supabase_client import get_admin_client as _get_admin
        from modules.auth import get_current_user_id as _get_uid
        _prof = _get_admin().table("user_profiles") \
            .select("onboarding_completed") \
            .eq("user_id", _get_uid()) \
            .execute()
        if _prof.data and not _prof.data[0].get("onboarding_completed"):
            _needs_onboarding = True
    except Exception:
        pass

    if _needs_onboarding:
        st.set_page_config(
            page_title="Logos Pulse",
            page_icon="\U0001f64f",
            layout="centered",
            initial_sidebar_state="collapsed",
            menu_items={},
        )
        st.markdown('<style>[data-testid="stSidebar"]{display:none!important;}[data-testid="stSidebarCollapsedControl"]{display:none!important;}[data-testid="stHeader"]{display:none!important;}[data-testid="stToolbar"]{display:none!important;}[data-testid="stDecoration"]{display:none!important;}[data-testid="stStatusWidget"]{display:none!important;}#MainMenu{display:none!important;visibility:hidden!important;}.stAppToolbar{display:none!important;}.stDeployButton{display:none!important;}button[kind="header"]{display:none!important;}[data-testid="stAppViewContainer"]{padding-top:0!important;margin-top:0!important;}[data-testid="stMain"],.stMain,.main{padding-top:0!important;}[data-testid="stMainBlockContainer"],.main .block-container,.block-container{padding-top:24px!important;padding-left:24px!important;padding-right:24px!important;max-width:720px!important;margin-left:auto!important;margin-right:auto!important;}</style>', unsafe_allow_html=True)
        pg = st.navigation([
            st.Page("views/Onboarding.py", title="Welcome", icon="\U0001f31f", default=True),
        ])
        pg.run()

    else:
        st.set_page_config(
            page_title="Logos Pulse",
            page_icon="\U0001f64f",
            layout="wide",
            initial_sidebar_state="collapsed",
            menu_items={},
        )

        # Inject sidebar-kill CSS before st.navigation() to prevent any flash
        st.markdown(
            '<style>'
            '[data-testid="stSidebar"],'
            '[data-testid="stSidebarCollapsedControl"],'
            '[data-testid="stSidebarNavItems"],'
            'section[data-testid="stSidebar"],'
            'div[data-testid="stSidebarCollapsedControl"],'
            'button[data-testid="collapsedControl"],'
            '.stSidebar,.css-1d391kg,.css-hxt7ib'
            '{'
            'display:none!important;'
            'visibility:hidden!important;'
            'pointer-events:none!important;'
            'width:0!important;'
            'min-width:0!important;'
            'max-width:0!important;'
            'overflow:hidden!important;'
            '}'
            '</style>',
            unsafe_allow_html=True,
        )

        role = get_current_role()

        # Build page list with explicit url_paths
        all_pages = [
            st.Page("views/0_Dashboard.py",        title="Dashboard",         icon="\U0001f3e0", default=True, url_path="dashboard"),
            st.Page("views/1_Daily_Entry.py",       title="Daily Entry",       icon="✏️",            url_path="daily-entry"),
            st.Page("views/2_Daily_Log.py",         title="Daily Log",         icon="\U0001f4c5",              url_path="daily-log"),
            st.Page("views/3_Weekly_Assignment.py", title="My Bible Plan",     icon="\U0001f4d6",              url_path="bible-plan"),
            st.Page("views/4_Streaks_and_Stats.py", title="Streaks & Stats",   icon="\U0001f525",              url_path="streaks"),
            st.Page("views/6_Sermon_Notes.py",      title="Sermon Notes",      icon="\U0001f4dd",              url_path="sermon-notes"),
            st.Page("views/7_Prayer_Journal.py",    title="Prayer Journal",    icon="\U0001f64f",              url_path="prayer-journal"),
            st.Page("views/8_Prayer_Engine.py",     title="Confession Plans",  icon="\U0001f64f",              url_path="confession-plans"),
            st.Page("views/Fasting_Tracker.py",     title="Fasting Tracker",   icon="\U0001f374",              url_path="fasting"),
            st.Page("views/Personal_Goals.py",      title="My Goals",          icon="\U0001f3af",              url_path="goals"),
            st.Page("views/Testimonies.py",         title="Testimonies",       icon="\U0001f31f",              url_path="testimonies"),
            st.Page("views/Bible_Reading_Plan.py",  title="Bible Library",     icon="\U0001f4d6",              url_path="reading-plan"),
            st.Page("views/Notifications.py",       title="Notifications",     icon="\U0001f514",              url_path="notifications"),
            st.Page("views/5_Settings.py",          title="Settings",          icon="⚙️",            url_path="settings"),
            st.Page("views/Profile.py",             title="My Profile",        icon="\U0001f464",              url_path="profile"),
        ]

        if role == "admin":
            all_pages.append(st.Page("views/Admin_Panel.py",      title="Admin Panel",       icon="\U0001f6e1️", url_path="admin"))
        if role in ("admin", "bishop"):
            all_pages.append(st.Page("views/Bishop_Dashboard.py", title="Bishop Dashboard",  icon="⚖️",     url_path="bishop"))
        if role in ("admin", "bishop", "pastor"):
            all_pages.append(st.Page("views/Pastor_Dashboard.py", title="Pastor Dashboard",  icon="\U0001f465",       url_path="pastor"))
            all_pages.append(st.Page("views/Wizard_Assignment.py", title="Custom Assignments", icon="\U0001f9d9",       url_path="assignments"))
            all_pages.append(st.Page("views/Member_Detail.py",    title="Member Detail",     icon="\U0001f464",       url_path="member"))

        pg = st.navigation(all_pages)

        # Detect current page url_path for active nav highlight
        try:
            _cur = pg.url_path or ""
        except AttributeError:
            _cur = ""

        def _lnk(path, label):
            cls = "db-lnk db-active" if _cur == path else "db-lnk"
            return f'<a class="{cls}" href="/{path}{_q}"{_t}>{label}</a>'

        def _dlnk(path, label, icon=""):
            cls = "lp-dlnk lp-dlnk-active" if _cur == path else "lp-dlnk"
            pfx = f"{icon} " if icon else ""
            return f'<label for="lp-drawer-toggle"><a class="{cls}" href="/{path}{_q}"{_t}>{pfx}{label}</a></label>'

        # ── Inject Daybreak top nav ────────────────────────────────────────────
        name          = st.session_state.get("preferred_name", "User")
        role_display  = role.replace("_", " ").title() if role else "User"
        avatar_letter = (name[0].upper() if name else "U")
        try:
            from modules.db import get_unread_notification_count as _notif_count
            _unread = _notif_count()
        except Exception:
            _unread = 0

        imp = st.session_state.get("impersonating")
        # Include refresh token in all nav hrefs so full-page reloads restore session
        _rt = st.session_state.get("refresh_token", "")
        _q  = f"?_s={_rt}" if _rt else ""

        # ── 1. CSS: hide remaining Streamlit chrome, layout reset ────────────
        st.markdown(
            '<style>'
            '[data-testid="stHeader"],[data-testid="stToolbar"],'
            '[data-testid="stDecoration"],[data-testid="stStatusWidget"],'
            '#MainMenu,.stAppToolbar,.stDeployButton,button[kind="header"],header'
            '{display:none!important;} #MainMenu{visibility:hidden!important;}'
            '[data-testid="stAppViewContainer"]{padding-top:0!important;margin-top:0!important;}'
            '[data-testid="stMain"],.stMain,.main{padding-top:0!important;overflow-x:hidden!important;}'
            '[data-testid="stMainBlockContainer"],.main .block-container,.block-container'
            '{padding-top:72px!important;padding-left:24px!important;padding-right:24px!important;'
            'padding-bottom:80px!important;max-width:1180px!important;'
            'margin-left:auto!important;margin-right:auto!important;}'
            '.db-nav{position:fixed;top:0;left:0;right:0;z-index:9999;height:56px;'
            'background:rgba(249,245,239,0.94);border-bottom:1px solid rgba(26,18,8,0.07);'
            'backdrop-filter:blur(20px) saturate(160%);-webkit-backdrop-filter:blur(20px) saturate(160%);'
            'display:flex;align-items:center;padding:0 20px;'
            'box-shadow:0 1px 0 rgba(26,18,8,0.05),0 4px 20px rgba(26,18,8,0.03);'
            'font-family:Jost,sans-serif;}'
            '.db-logo{display:flex;align-items:center;gap:9px;margin-right:20px;'
            'flex-shrink:0;text-decoration:none;}'
            '.db-lm{width:28px;height:28px;border-radius:7px;background:#B85A30;'
            'display:flex;align-items:center;justify-content:center;'
            'font-family:Cormorant,serif;font-size:13px;font-weight:700;color:white;'
            'box-shadow:0 2px 8px rgba(184,90,48,0.32);flex-shrink:0;}'
            '.db-lt{font-family:Cormorant,serif;font-size:17px;font-weight:600;'
            'color:#1A1208;letter-spacing:0.03em;white-space:nowrap;}'
            '.db-links{display:flex;align-items:center;gap:1px;flex:1;overflow:hidden;}'
            '.db-lnk{padding:6px 10px;border-radius:8px;font-size:13px;font-weight:500;'
            'color:#5A4A32;text-decoration:none;white-space:nowrap;transition:all 0.18s;}'
            '.db-lnk:hover{background:rgba(184,90,48,0.06);color:#1A1208;}'
            '.db-more{position:relative;}'
            '.db-mbtn{padding:6px 10px;border-radius:8px;font-size:13px;font-weight:500;'
            'color:#5A4A32;cursor:pointer;background:transparent;border:none;'
            'white-space:nowrap;font-family:Jost,sans-serif;transition:all 0.18s;}'
            '.db-mbtn:hover{background:rgba(184,90,48,0.06);color:#1A1208;}'
            '.db-drop{display:none;position:absolute;top:calc(100% + 6px);left:0;'
            'background:#FFFFFF;border:1px solid rgba(26,18,8,0.09);border-radius:12px;'
            'box-shadow:0 8px 32px rgba(26,18,8,0.12);min-width:190px;'
            'z-index:10000;flex-direction:column;padding:6px;}'
            '.db-more:focus-within .db-drop{display:flex;}'
            '.db-di{padding:8px 12px;border-radius:8px;font-size:13px;font-weight:500;'
            'color:#5A4A32;text-decoration:none;white-space:nowrap;'
            'transition:background 0.16s;display:block;font-family:Jost,sans-serif;}'
            '.db-di:hover{background:rgba(184,90,48,0.06);color:#1A1208;}'
            '.db-active{color:#B85A30!important;border-bottom:2px solid #B85A30;'
            'border-radius:8px 8px 0 0;padding-bottom:4px!important;}'
            '.db-divider{font-size:9px;font-weight:800;text-transform:uppercase;'
            'letter-spacing:2px;color:#A09080;padding:8px 12px 4px;'
            'font-family:Jost,sans-serif;pointer-events:none;}'
            '.db-divider-line{height:1px;background:rgba(26,18,8,0.07);margin:4px 6px;}'
            '.db-right{display:flex;align-items:center;gap:6px;margin-left:auto;flex-shrink:0;}'
            '.db-ava-wrap{position:relative;}'
            '.db-ava-btn{width:30px;height:30px;border-radius:50%;'
            'background:linear-gradient(135deg,#B85A30,#C48A1C);'
            'display:flex;align-items:center;justify-content:center;'
            'font-size:12px;font-weight:800;color:white;'
            'border:2px solid rgba(184,90,48,0.22);cursor:pointer;'
            'transition:transform 0.2s;flex-shrink:0;}'
            '.db-ava-btn:hover{transform:scale(1.1);box-shadow:0 3px 12px rgba(184,90,48,0.28);}'
            '.db-ava-drop{right:0!important;left:auto!important;min-width:160px;}'
            '.db-ibtn{width:32px;height:32px;border-radius:8px;'
            'background:rgba(26,18,8,0.04);border:1px solid rgba(26,18,8,0.07);'
            'display:flex;align-items:center;justify-content:center;font-size:14px;'
            'text-decoration:none;position:relative;transition:all 0.18s;}'
            '.db-ibtn:hover{background:rgba(26,18,8,0.08);}'
            '.db-ndot{position:absolute;top:5px;right:5px;width:6px;height:6px;'
            'border-radius:50%;background:#B85A30;border:1.5px solid #F9F5EF;}'
            '#lp-drawer-toggle{display:none;}'
            '.lp-ham{width:32px;height:32px;border-radius:8px;background:rgba(26,18,8,0.04);'
            'border:1px solid rgba(26,18,8,0.07);display:flex;align-items:center;'
            'justify-content:center;font-size:16px;cursor:pointer;transition:all 0.18s;'
            'flex-shrink:0;margin-right:8px;color:#5A4A32;user-select:none;line-height:1;}'
            '.lp-ham:hover{background:rgba(26,18,8,0.08);}'
            '.lp-drawer{position:fixed;top:56px;left:0;bottom:0;width:280px;z-index:9998;'
            'background:#F9F5EF;border-right:1px solid rgba(26,18,8,0.08);'
            'transform:translateX(-100%);transition:transform 0.22s cubic-bezier(0.22,1,0.36,1);'
            'overflow-y:auto;padding:16px 0;box-shadow:4px 0 24px rgba(26,18,8,0.10);}'
            '.lp-drawer-overlay{display:none;position:fixed;inset:56px 0 0 0;z-index:9997;'
            'background:rgba(26,18,8,0.18);cursor:pointer;}'
            '#lp-drawer-toggle:checked~.lp-drawer{transform:translateX(0);}'
            '#lp-drawer-toggle:checked~.lp-drawer-overlay{display:block;}'
            '.lp-dlnk{display:block;padding:9px 20px;font-size:13px;font-weight:500;'
            'color:#5A4A32;text-decoration:none;font-family:Jost,sans-serif;transition:background 0.16s;}'
            '.lp-dlnk:hover{background:rgba(184,90,48,0.06);color:#1A1208;}'
            '.lp-dlnk-active{color:#B85A30!important;font-weight:600;}'
            '.lp-dsec{font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:2px;'
            'color:#A09080;padding:12px 20px 4px;font-family:Jost,sans-serif;'
            'pointer-events:none;display:block;}'
            '.lp-dline{height:1px;background:rgba(26,18,8,0.07);margin:8px 12px;}'
            '</style>',
            unsafe_allow_html=True
        )

        # ── 2. Build nav HTML ─────────────────────────────────────────────────
        ndot = '<span class="db-ndot"></span>' if _unread > 0 else ""
        _t = ' target="_self"'

        # Drawer: role-gated Leadership section
        _ld = ""
        if role == "admin":
            _ld += _dlnk("admin",       "Admin Panel",        "&#128737;")
        if role in ("admin", "bishop"):
            _ld += _dlnk("bishop",      "Bishop Dashboard",   "&#9878;")
        if role in ("admin", "bishop", "pastor"):
            _ld += (
                _dlnk("pastor",       "Pastor Dashboard",   "&#128101;")
                + _dlnk("assignments", "Custom Assignments", "&#129497;")
                + _dlnk("member",      "Member Detail",      "&#128100;")
            )
        drawer_lead = (
            '<div class="lp-dline"></div><div class="lp-dsec">Leadership</div>' + _ld
        ) if _ld else ""

        drawer_html = (
            '<input type="checkbox" id="lp-drawer-toggle">'
            '<nav class="lp-drawer">'
            + _dlnk("dashboard",      "Dashboard",      "&#127968;")
            + _dlnk("daily-entry",    "Daily Entry",    "&#9999;&#65039;")
            + _dlnk("prayer-journal", "Prayer",         "&#128591;")
            + _dlnk("sermon-notes",   "Sermon Notes",   "&#128221;")
            + _dlnk("bible-plan",     "My Bible Plan",  "&#128214;")
            + _dlnk("streaks",        "Streaks & Stats","&#128293;")
            + '<div class="lp-dline"></div>'
            + '<div class="lp-dsec">Personal</div>'
            + _dlnk("fasting",        "Fasting Tracker","&#127860;")
            + _dlnk("goals",          "My Goals",       "&#127919;")
            + _dlnk("testimonies",    "Testimonies",    "&#127775;")
            + _dlnk("reading-plan",   "Bible Library",  "&#128214;")
            + _dlnk("notifications",  "Notifications",  "&#128276;")
            + '<div class="lp-dline"></div>'
            + '<div class="lp-dsec">Account</div>'
            + _dlnk("profile",        "My Profile",     "&#128100;")
            + _dlnk("settings",       "Settings",       "&#9881;&#65039;")
            + drawer_lead
            + '<div class="lp-dline"></div>'
            + f'<a class="lp-dlnk" href="/?action=logout"{_t}>&#8618; Sign Out</a>'
            + '</nav>'
            + '<label class="lp-drawer-overlay" for="lp-drawer-toggle"></label>'
        )

        imp_bar = ""
        if imp:
            _in = imp.get("name", "")
            _ir = imp.get("role", "").replace("_", " ").title()
            imp_bar = (
                '<div style="position:fixed;top:56px;left:0;right:0;z-index:9998;'
                'background:#FDF0E8;border-bottom:1px solid rgba(184,90,48,0.2);'
                'padding:6px 24px;font-size:12px;color:#B85A30;font-weight:700;'
                'font-family:Jost,sans-serif;">'
                f'&#128065; Viewing as <b>{_in}</b> ({_ir})'
                ' &nbsp;&middot;&nbsp;'
                '<a href="/?action=stop_impersonate" style="color:#B85A30;text-decoration:underline;">Stop</a>'
                '</div>'
            )

        # Admin: "Users" pinned; others: "My Bible Plan" + "Streaks"
        _extra_top = (
            _lnk("admin", "Users")
            if role == "admin"
            else _lnk("bible-plan", "My Bible Plan") + _lnk("streaks", "Streaks")
        )

        nav_html = (
            drawer_html
            + '<div class="db-nav">'
            f'<label for="lp-drawer-toggle" class="lp-ham">&#9776;</label>'
            f'<a class="db-logo" href="/dashboard{_q}"{_t}>'
            '<div class="db-lm">LP</div>'
            '<span class="db-lt">Logos Pulse</span>'
            '</a>'
            '<div class="db-links">'
            + _lnk("dashboard",      "Dashboard")
            + _lnk("daily-entry",    "Daily Entry")
            + _lnk("prayer-journal", "Prayer")
            + _lnk("sermon-notes",   "Sermon Notes")
            + _extra_top
            + '</div>'
            '<div class="db-right">'
            f'<a class="db-ibtn" href="/notifications{_q}"{_t}>&#128276;{ndot}</a>'
            '<div class="db-more db-ava-wrap">'
            f'<button class="db-ava-btn" title="{name}">{avatar_letter}</button>'
            '<div class="db-drop db-ava-drop">'
            f'<a class="db-di" href="/profile{_q}"{_t}>&#128100; My Profile</a>'
            f'<a class="db-di" href="/settings{_q}"{_t}>&#9881;&#65039; Settings</a>'
            '<div class="db-divider-line"></div>'
            f'<a class="db-di" href="/?action=logout"{_t}>&#8618; Sign out</a>'
            '</div>'
            '</div>'
            '</div>'
            '</div>'
            + imp_bar
        )
        st.markdown(nav_html, unsafe_allow_html=True)

        # ── Admin impersonation stop ───────────────────────────────────────────
        if st.query_params.get("action") == "stop_impersonate":
            if st.session_state.get("_real_user_id"):
                st.session_state["user_id"] = st.session_state.pop("_real_user_id")
                st.session_state["role"] = st.session_state.pop("_real_role")
                st.session_state["preferred_name"] = st.session_state.pop("_real_preferred_name")
            st.session_state.pop("impersonating", None)
            st.query_params.clear()
            st.rerun()

        # (Admin impersonation controls are in Admin_Panel.py)

        pg.run()
