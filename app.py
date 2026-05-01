import streamlit as st

from modules.auth import is_authenticated, sign_out, get_current_role

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
                "admin": "#C44B5B",
                "bishop": "#2196F3",
                "pastor": "#3A8F5C",
                "prayer_warrior": "#5B4FC4",
            }
            badge_color = role_colors.get(role, "#5B4FC4")

            st.markdown(f"""
            <div style="padding:12px 0 16px 0; border-bottom:1px solid #EDE8F5; margin-bottom:12px;">
                <div style="font-family:'DM Serif Display',Georgia,serif; font-size:18px; color:#2A2438;">
                    {name}
                </div>
                <span style="background:{badge_color}; color:white; padding:2px 10px;
                             border-radius:10px; font-size:11px; font-weight:600;">
                    {role_display}
                </span>
            </div>
            """, unsafe_allow_html=True)

            # REQ-1: Admin Impersonation
            if role == "admin":
                st.markdown("<div style='border-top:1px solid #EDE8F5; margin:12px 0; padding-top:12px;'></div>", unsafe_allow_html=True)
                st.markdown("<span style='font-size:10px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px;'>Impersonate</span>", unsafe_allow_html=True)

                if st.session_state.get("impersonating"):
                    imp = st.session_state["impersonating"]
                    st.markdown(f"""
                    <div style="background:#FFF3E0; border-radius:8px; padding:8px 12px; margin:4px 0; font-size:12px;">
                        Viewing as <b>{imp['name']}</b> ({imp['role'].replace('_',' ').title()})
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
            <div style="background:#FFF3E0; border:1px solid #FFE0B2; border-radius:8px;
                        padding:8px 16px; margin-bottom:16px; font-size:13px; color:#E65100;">
                \U0001f50d <b>Admin Impersonation Active</b> — Viewing as {imp['name']} ({imp['role'].replace('_',' ').title()})
            </div>
            """, unsafe_allow_html=True)

        pg.run()