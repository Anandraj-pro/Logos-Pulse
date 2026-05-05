import streamlit as st

from modules.auth import is_authenticated, sign_out, get_current_role

# ── Auto-restore session from URL token after idle reconnect ──
# When Streamlit's WebSocket drops (idle timeout), session state is cleared.
# The URL still contains ?_s=<refresh_token>, so we can silently restore.
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
                # Rotate to new token
                st.query_params["_s"] = _sess.refresh_token
        except Exception:
            st.query_params.pop("_s", None)

# --- Auth-aware navigation ---
authenticated = is_authenticated()

if not authenticated:
    st.set_page_config(
        page_title="Logos Pulse",
        page_icon="\U0001f64f",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    # Hide sidebar completely on login
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
    </style>
    """, unsafe_allow_html=True)
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
    )
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarCollapsedControl"] { display: none; }
    </style>
    """, unsafe_allow_html=True)
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
        )
        st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
            [data-testid="stSidebarCollapsedControl"] { display: none; }
        </style>
        """, unsafe_allow_html=True)
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
        role = get_current_role()

        # Build page list
        all_pages = [
            st.Page("views/0_Dashboard.py", title="Dashboard", icon="\U0001f3e0", default=True),
            st.Page("views/1_Daily_Entry.py", title="Daily Entry", icon="\u270f\ufe0f"),
            st.Page("views/2_Daily_Log.py", title="Daily Log", icon="\U0001f4c5"),
            st.Page("views/3_Weekly_Assignment.py", title="Weekly Assignment", icon="\U0001f4d6"),
            st.Page("views/4_Streaks_and_Stats.py", title="Streaks & Stats", icon="\U0001f525"),
            st.Page("views/6_Sermon_Notes.py", title="Sermon Notes", icon="\U0001f4dd"),
            st.Page("views/7_Prayer_Journal.py", title="Prayer Journal", icon="\U0001f64f"),
            st.Page("views/8_Prayer_Engine.py", title="Prayer Engine", icon="\U0001f64f"),
            st.Page("views/Fasting_Tracker.py", title="Fasting Tracker", icon="\U0001f374"),
            st.Page("views/Personal_Goals.py", title="My Goals", icon="\U0001f3af"),
            st.Page("views/Testimonies.py", title="Testimonies", icon="\U0001f31f"),
            st.Page("views/Bible_Reading_Plan.py", title="Reading Plan", icon="\U0001f4d6"),
            st.Page("views/Notifications.py", title="Notifications", icon="\U0001f514"),
            st.Page("views/5_Settings.py", title="Settings", icon="\u2699\ufe0f"),
            st.Page("views/Profile.py", title="My Profile", icon="\U0001f464"),
        ]

        # Role-specific pages
        if role == "admin":
            all_pages.append(st.Page("views/Admin_Panel.py", title="Admin Panel", icon="\U0001f6e1\ufe0f"))
        if role in ("admin", "bishop"):
            all_pages.append(st.Page("views/Bishop_Dashboard.py", title="Bishop Dashboard", icon="\u2696\ufe0f"))
        if role in ("admin", "bishop", "pastor"):
            all_pages.append(st.Page("views/Pastor_Dashboard.py", title="Pastor Dashboard", icon="\U0001f465"))
            all_pages.append(st.Page("views/Wizard_Assignment.py", title="Custom Assignments", icon="\U0001f9d9"))
            all_pages.append(st.Page("views/Member_Detail.py", title="Member Detail", icon="\U0001f464"))

        pg = st.navigation(all_pages)

        # Sidebar branding + user info
        with st.sidebar:
            from modules.styles import sidebar_logo
            sidebar_logo()

            name = st.session_state.get("preferred_name", "User")
            role_display = role.replace("_", " ").title() if role else "User"
            role_colors = {
                "admin": "#B5383C",
                "bishop": "#1565C0",
                "pastor": "#2D6A4F",
                "prayer_warrior": "#3B2F8E",
            }
            badge_color = role_colors.get(role, "#3B2F8E")

            try:
                from modules.db import get_unread_notification_count as _notif_count
                _unread = _notif_count()
            except Exception:
                _unread = 0
            _bell = f' <span style="background:#B5383C; color:white; padding:1px 7px; border-radius:10px; font-size:10px; font-weight:800; vertical-align:middle;">{_unread}</span>' if _unread > 0 else ""
            st.markdown(f"""
            <div style="padding:12px 0 16px 0; border-bottom:1px solid rgba(59,47,142,0.08); margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <div style="font-family:'Playfair Display','DM Serif Display',Georgia,serif; font-size:18px; font-weight:700; color:#1A1628; letter-spacing:-0.2px;">
                        {name}
                    </div>
                    <span style="font-size:16px;">🔔{_bell}</span>
                </div>
                <span style="background:{badge_color}; color:white; padding:3px 11px;
                             border-radius:100px; font-size:10px; font-weight:800;
                             letter-spacing:0.5px; text-transform:uppercase;
                             font-family:'Nunito',sans-serif;">
                    {role_display}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # REQ-1: Admin Impersonation
            if role == "admin":
                st.markdown("<div style='border-top:1px solid rgba(59,47,142,0.08); margin:12px 0; padding-top:12px;'></div>", unsafe_allow_html=True)
                st.markdown("<span style='font-size:10px; color:#9E96AB; text-transform:uppercase; letter-spacing:2px; font-weight:800; font-family:Nunito,sans-serif;'>Impersonate</span>", unsafe_allow_html=True)

                if st.session_state.get("impersonating"):
                    imp = st.session_state["impersonating"]
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#FFF4E6,#FFFDF7); border:1px solid rgba(194,107,44,0.2); border-radius:10px; padding:10px 14px; margin:4px 0; font-size:12px; color:#C26B2C; font-weight:700; font-family:Nunito,sans-serif;">
                        👁️ Viewing as <b>{imp['name']}</b><br/>
                        <span style="font-weight:600; opacity:0.8;">{imp['role'].replace('_',' ').title()}</span>
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
                                # Override session state for impersonated user
                                st.session_state["_real_user_id"] = st.session_state["user_id"]
                                st.session_state["_real_role"] = st.session_state["role"]
                                st.session_state["_real_preferred_name"] = st.session_state["preferred_name"]
                                st.session_state["user_id"] = imp_data["user_id"]
                                st.session_state["role"] = imp_data["role"]
                                st.session_state["preferred_name"] = imp_data["name"]
                                st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("\U0001f6aa Logout", use_container_width=True):
                # Restore real user if impersonating
                if st.session_state.get("impersonating"):
                    st.session_state.pop("impersonating", None)
                sign_out()
                st.rerun()

        # Impersonation banner
        if st.session_state.get("impersonating"):
            imp = st.session_state["impersonating"]
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#FFF4E6,#FFFDF7); border:1px solid rgba(194,107,44,0.25);
                        border-radius:12px; padding:10px 18px; margin-bottom:16px; font-size:13px;
                        color:#C26B2C; font-weight:700; font-family:'Nunito',sans-serif;
                        box-shadow:0 2px 8px rgba(194,107,44,0.08);">
                👁️ <b>Admin View Active</b> — as {imp['name']} ({imp['role'].replace('_',' ').title()})
            </div>
            """, unsafe_allow_html=True)

        pg.run()