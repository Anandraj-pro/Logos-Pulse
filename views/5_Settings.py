import streamlit as st
import json
from modules import db
from modules.styles import inject_styles, page_header, section_label
from modules.auth import require_login, require_password_changed

require_login()
require_password_changed()

db.init_db()

inject_styles()

page_header("\u2699\ufe0f", "Settings", "Configure your app preferences")

settings = db.get_all_settings()

# --- Profile Settings ---
section_label("\U0001f464 Profile")

with st.form("settings_form"):
    col1, col2 = st.columns(2)
    with col1:
        greeting_name = st.text_input(
            "Greeting Name (used in WhatsApp message)",
            value=settings.get("greeting_name", "Anna"),
        )
    with col2:
        pastor_name = st.text_input(
            "Pastor's Name",
            value=settings.get("pastor_name", "Ps. Deepak"),
        )

    prayer_options = list(range(15, 195, 15))
    current_default = int(settings.get("default_prayer_minutes", "60"))
    default_idx = prayer_options.index(current_default) if current_default in prayer_options else 3
    default_prayer = st.select_slider(
        "Default Prayer Duration (minutes)",
        options=prayer_options,
        value=prayer_options[default_idx],
    )

    omit_sermon = st.checkbox(
        "Omit 'Listening to the Word' line when empty",
        value=settings.get("omit_empty_sermon", "false") == "true",
    )

    if st.form_submit_button("Save Settings", type="primary", use_container_width=True):
        db.save_settings({
            "greeting_name": greeting_name,
            "pastor_name": pastor_name,
            "default_prayer_minutes": str(default_prayer),
            "omit_empty_sermon": "true" if omit_sermon else "false",
        })
        st.success("Settings saved!")
        st.rerun()

# --- Data Management ---
section_label("\U0001f4be Data Management")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background:#E8F5E9; border-radius:12px; padding:16px; text-align:center;">
        <div style="font-size:24px; margin-bottom:4px;">\U0001f4e4</div>
        <div style="font-size:14px; font-weight:600; color:#2E7D32;">Export Backup</div>
        <div style="font-size:12px; color:#66BB6A;">Download all your data</div>
    </div>
    """, unsafe_allow_html=True)
    export_data = db.export_all_data()
    st.download_button(
        "Download JSON",
        data=json.dumps(export_data, indent=2),
        file_name="spiritual_growth_backup.json",
        mime="application/json",
        use_container_width=True,
    )

with col2:
    st.markdown("""
    <div style="background:#FFF3E0; border-radius:12px; padding:16px; text-align:center;">
        <div style="font-size:24px; margin-bottom:4px;">\U0001f4e5</div>
        <div style="font-size:14px; font-weight:600; color:#E65100;">Import Data</div>
        <div style="font-size:12px; color:#FF9800;">Restore from backup</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload JSON", type=["json"], label_visibility="collapsed")
    if uploaded:
        try:
            data = json.loads(uploaded.read())
            if st.button("Confirm Import", type="primary", use_container_width=True):
                db.import_all_data(data)
                st.success("Data imported!")
                st.rerun()
        except json.JSONDecodeError:
            st.error("Invalid JSON file.")