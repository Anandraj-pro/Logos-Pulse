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

    pg = st.navigation(all_pages)

    # Sidebar user info
    with st.sidebar:
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

        if st.button("\U0001f6aa Logout", use_container_width=True):
            sign_out()
            st.rerun()

    pg.run()