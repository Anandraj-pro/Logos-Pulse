import streamlit as st
import json
from modules import db
from modules.styles import inject_styles, page_header, section_label, spacer
from modules.auth import require_login, require_password_changed, get_current_user_id
from modules.supabase_client import get_admin_client

require_login()
require_password_changed()
inject_styles()

page_header("\u2699\ufe0f", "Settings", "Report preferences and data management")

settings = db.get_all_settings()
user_id = get_current_user_id()
_admin = get_admin_client()

# --- Link to Profile ---
st.markdown("""
<div class="goal-banner">
    \U0001f464 To edit your name, prayer goal, or password, go to <b>My Profile</b> in the sidebar.
</div>
""", unsafe_allow_html=True)

# --- Report Preferences ---
section_label("\U0001f4cb Report Preferences")

with st.form("settings_form"):
    omit_sermon = st.checkbox(
        "Omit 'Listening to the Word' line when sermon is empty",
        value=settings.get("omit_empty_sermon", "false") == "true",
    )

    if st.form_submit_button("Save Preferences", type="primary", use_container_width=True):
        db.save_settings({
            "omit_empty_sermon": "true" if omit_sermon else "false",
        })
        st.toast("Preferences saved!", icon="✅")
        st.rerun()

spacer(8)

# --- Reminder Preferences ---
section_label("\U0001f514 Reminder Preferences")

_profile = _admin.table("user_profiles").select("reminder_enabled").eq("user_id", user_id).single().execute()
_reminder_on = _profile.data.get("reminder_enabled", True) if _profile.data else True

_new_reminder = st.toggle(
    "Receive daily reminder emails when I haven't logged my disciplines",
    value=_reminder_on,
    help="A reminder is sent at 7:00 PM if you haven't logged today. You can turn this off at any time.",
)
if _new_reminder != _reminder_on:
    _admin.table("user_profiles") \
        .update({"reminder_enabled": _new_reminder}) \
        .eq("user_id", user_id) \
        .execute()
    st.toast("Reminder preference saved!", icon="✅")
    st.rerun()

spacer()

# --- Data Management ---
section_label("\U0001f4be Data Management")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background:#E8F5E9; border-radius:12px; padding:16px; text-align:center;">
        <div style="font-size:24px; margin-bottom:4px;">\U0001f4e4</div>
        <div style="font-size:14px; font-weight:600; color:#3A8F5C;">Export Backup</div>
        <div style="font-size:12px; color:#66BB6A;">Download all your data</div>
    </div>
    """, unsafe_allow_html=True)
    export_data = db.export_all_data()
    st.download_button(
        "Download JSON",
        data=json.dumps(export_data, indent=2, default=str),
        file_name="logos_pulse_backup.json",
        mime="application/json",
        use_container_width=True,
    )

with col2:
    st.markdown("""
    <div style="background:#FFF3E0; border-radius:12px; padding:16px; text-align:center;">
        <div style="font-size:24px; margin-bottom:4px;">\U0001f4e5</div>
        <div style="font-size:14px; font-weight:600; color:#D4853A;">Import Data</div>
        <div style="font-size:12px; color:#FF9800;">Restore from backup</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload JSON", type=["json"], label_visibility="collapsed",
                                help="Upload a JSON backup file previously exported from Logos Pulse")
    if uploaded:
        try:
            data = json.loads(uploaded.read())
            if st.button("Confirm Import", type="primary", use_container_width=True):
                db.import_all_data(data)
                st.toast("Data imported!", icon="✅")
                st.rerun()
        except json.JSONDecodeError:
            st.error("Invalid JSON file.")
