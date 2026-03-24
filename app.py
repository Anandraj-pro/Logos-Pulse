import streamlit as st
from modules import db

db.init_db()

st.set_page_config(
    page_title="Spiritual Growth Tracker",
    page_icon="\U0001f64f",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Navigation with sections ---
pages = {
    "Daily Assignment": [
        st.Page("pages/0_Dashboard.py", title="Dashboard", icon="\U0001f3e0", default=True),
        st.Page("pages/1_Daily_Entry.py", title="Daily Entry", icon="\u270f\ufe0f"),
        st.Page("pages/2_Daily_Log.py", title="Daily Log", icon="\U0001f4c5"),
        st.Page("pages/3_Weekly_Assignment.py", title="Weekly Assignment", icon="\U0001f4d6"),
        st.Page("pages/4_Streaks_and_Stats.py", title="Streaks & Stats", icon="\U0001f525"),
    ],
    "Sermon Notes": [
        st.Page("pages/6_Sermon_Notes.py", title="Sermon Notes", icon="\U0001f4dd"),
    ],
    "Prayer Journal": [
        st.Page("pages/7_Prayer_Journal.py", title="Prayer Journal", icon="\U0001f64f"),
    ],
    "Settings": [
        st.Page("pages/5_Settings.py", title="Settings", icon="\u2699\ufe0f"),
    ],
}

pg = st.navigation(pages)
pg.run()
