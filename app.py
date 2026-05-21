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
            initial_sidebar_state="expanded",
        )
        # Ensure sidebar expand arrow is always visible so users can open a collapsed sidebar
        st.markdown(
            '<style>'
            '[data-testid="stSidebarCollapsedControl"]{display:flex!important;visibility:visible!important;}'
            '</style>',
            unsafe_allow_html=True,
        )
        role = get_current_role()

        # Core pages — visible to all authenticated users
        core_pages = [
            st.Page("views/0_Dashboard.py",        title="Dashboard",        icon="\U0001f3e0", default=True, url_path="dashboard"),
            st.Page("views/1_Daily_Entry.py",       title="Daily Entry",      icon="✏️",                       url_path="daily-entry"),
            st.Page("views/2_Daily_Log.py",         title="Daily Log",        icon="\U0001f4c5",               url_path="daily-log"),
            st.Page("views/3_Weekly_Assignment.py", title="My Bible Plan",    icon="\U0001f4d6",               url_path="bible-plan"),
            st.Page("views/4_Streaks_and_Stats.py", title="Streaks & Stats",  icon="\U0001f525",               url_path="streaks"),
            st.Page("views/6_Sermon_Notes.py",      title="Sermon Notes",     icon="\U0001f4dd",               url_path="sermon-notes"),
            st.Page("views/7_Prayer_Journal.py",    title="Prayer Journal",   icon="\U0001f64f",               url_path="prayer-journal"),
            st.Page("views/8_Prayer_Engine.py",     title="Confession Plans", icon="\U0001f64f",               url_path="confession-plans"),
            st.Page("views/Fasting_Tracker.py",     title="Fasting Tracker",  icon="\U0001f374",               url_path="fasting"),
            st.Page("views/Personal_Goals.py",      title="My Goals",         icon="\U0001f3af",               url_path="goals"),
            st.Page("views/Testimonies.py",         title="Testimonies",      icon="\U0001f31f",               url_path="testimonies"),
            st.Page("views/Bible_Reading_Plan.py",  title="Bible Library",    icon="\U0001f4d6",               url_path="reading-plan"),
            st.Page("views/Notifications.py",       title="Notifications",    icon="\U0001f514",               url_path="notifications"),
            st.Page("views/5_Settings.py",          title="Settings",         icon="⚙️",                       url_path="settings"),
            st.Page("views/Profile.py",             title="My Profile",       icon="\U0001f464",               url_path="profile"),
        ]

        # Scriptorium — clergy tools, role-gated
        scriptorium_pages = []
        if role == "admin":
            scriptorium_pages.append(st.Page("views/Admin_Panel.py",       title="Admin Panel",        icon="\U0001f6e1️", url_path="admin"))
        if role in ("admin", "bishop"):
            scriptorium_pages.append(st.Page("views/Bishop_Dashboard.py",  title="Bishop Dashboard",   icon="⚖️",     url_path="bishop"))
        if role in ("admin", "bishop", "pastor"):
            scriptorium_pages.append(st.Page("views/Pastor_Dashboard.py",  title="Pastor Dashboard",   icon="\U0001f465",       url_path="pastor"))
            scriptorium_pages.append(st.Page("views/Wizard_Assignment.py", title="Custom Assignments", icon="\U0001f9d9",       url_path="assignments"))
            scriptorium_pages.append(st.Page("views/Member_Detail.py",     title="Member Detail",      icon="\U0001f464",       url_path="member"))

        if scriptorium_pages:
            nav_sections = {
                "Chronicle": core_pages,
                "⚙ Scriptorium": scriptorium_pages,
            }
        else:
            nav_sections = {"Chronicle": core_pages}

        pg = st.navigation(nav_sections)

        # Sidebar branding + user info
        with st.sidebar:
            from modules.styles import sidebar_logo
            sidebar_logo()

            name = st.session_state.get("preferred_name", "User")
            role_display = role.replace("_", " ").title() if role else "User"
            role_colors = {
                "admin":          "rgba(196,138,28,0.60)",
                "bishop":         "rgba(100,160,220,0.50)",
                "pastor":         "rgba(74,168,112,0.50)",
                "prayer_warrior": "rgba(196,138,28,0.35)",
            }
            badge_color = role_colors.get(role, "rgba(196,138,28,0.35)")

            try:
                from modules.db import get_unread_notification_count as _notif_count
                _unread = _notif_count()
            except Exception:
                _unread = 0
            _bell = (
                f' <span style="background:rgba(196,138,28,0.55);color:#1a1108;padding:1px 7px;border-radius:10px;font-size:9px;font-weight:700;font-family:\'Cinzel\',serif;letter-spacing:1px;vertical-align:middle;">{_unread}</span>'
                if _unread > 0 else ""
            )
            st.markdown(f"""
            <div style="padding:12px 0 16px 0; border-bottom:1px solid rgba(196,138,28,0.12); margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="font-family:'IM Fell English','Cormorant',Georgia,serif; font-size:17px; font-weight:400; font-style:italic; color:#F5E8C0; letter-spacing:0.02em;">
                        {name}
                    </div>
                    <span style="font-size:14px; opacity:0.6;">\U0001f514{_bell}</span>
                </div>
                <span style="background:{badge_color}; color:#F5E8C0; padding:3px 11px;
                             border-radius:100px; font-size:9px; font-weight:400;
                             letter-spacing:2px; text-transform:uppercase;
                             font-family:'Cinzel',serif;
                             border:1px solid rgba(196,138,28,0.30);">
                    {role_display}
                </span>
            </div>
            """, unsafe_allow_html=True)

            if role == "admin":
                st.markdown("<div style='border-top:1px solid rgba(196,138,28,0.10); margin:12px 0; padding-top:12px;'></div>", unsafe_allow_html=True)
                st.markdown("<span style='font-size:9px; color:rgba(196,138,28,0.40); text-transform:uppercase; letter-spacing:2.5px; font-weight:400; font-family:Cinzel,serif;'>Impersonate</span>", unsafe_allow_html=True)

                if st.session_state.get("impersonating"):
                    imp = st.session_state["impersonating"]
                    st.markdown(f"""
                    <div style="background:rgba(196,138,28,0.08); border:1px solid rgba(196,138,28,0.22); border-radius:8px; padding:10px 14px; margin:4px 0; font-size:12px; color:#C4A870; font-family:'Cardo',Georgia,serif;">
                        \U0001f441️ <em>Viewing as <b style="color:#F5E8C0;">{imp['name']}</b></em><br/>
                        <span style="font-family:'Cinzel',serif; font-size:9px; letter-spacing:1.5px; text-transform:uppercase; color:rgba(196,138,28,0.55);">{imp['role'].replace('_',' ').title()}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Stop Impersonating", use_container_width=True):
                        st.session_state.pop("impersonating", None)
                        st.rerun()
                else:
                    from modules.supabase_client import get_admin_client
                    _adm = get_admin_client()
                    _test_profiles = _adm.table("user_profiles") \
                        .select("user_id, role") \
                        .neq("role", "admin") \
                        .limit(6) \
                        .execute()
                    if _test_profiles.data:
                        _options = {"-- Select --": None}
                        for _p in _test_profiles.data:
                            try:
                                _u = _adm.auth.admin.get_user_by_id(_p["user_id"]).user
                                _meta = _u.user_metadata or {}
                                _label = f"{_meta.get('preferred_name', _u.email)} ({_p['role'].replace('_',' ').title()})"
                                _options[_label] = {"user_id": _p["user_id"], "role": _p["role"],
                                                    "name": _meta.get("preferred_name", _u.email)}
                            except Exception:
                                pass
                        _selected = st.selectbox("View as", options=list(_options.keys()), label_visibility="collapsed")
                        if _selected != "-- Select --" and _options[_selected]:
                            if st.button("Impersonate", type="primary", use_container_width=True):
                                imp_data = _options[_selected]
                                st.session_state["impersonating"] = imp_data
                                st.session_state["_real_user_id"] = st.session_state["user_id"]
                                st.session_state["_real_role"] = st.session_state["role"]
                                st.session_state["_real_preferred_name"] = st.session_state["preferred_name"]
                                st.session_state["user_id"] = imp_data["user_id"]
                                st.session_state["role"] = imp_data["role"]
                                st.session_state["preferred_name"] = imp_data["name"]
                                st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("⬡  Exit Chronicle", use_container_width=True):
                if st.session_state.get("impersonating"):
                    st.session_state.pop("impersonating", None)
                sign_out()
                st.rerun()

        # Impersonation banner
        if st.session_state.get("impersonating"):
            imp = st.session_state["impersonating"]
            st.markdown(f"""
            <div style="background:rgba(196,138,28,0.07); border:1px solid rgba(196,138,28,0.22);
                        border-radius:10px; padding:10px 18px; margin-bottom:16px; font-size:13px;
                        color:#C4A870; font-family:'Cardo',Georgia,serif;
                        box-shadow:0 2px 8px rgba(0,0,0,0.2);">
                \U0001f441️ <em><b style="color:#F5E8C0;">Scribe Mode</b> — viewing as {imp['name']}</em>
                <span style="display:block;font-family:'Cinzel',serif;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(196,138,28,0.45);margin-top:3px;">{imp['role'].replace('_',' ').title()}</span>
            </div>
            """, unsafe_allow_html=True)

        pg.run()
