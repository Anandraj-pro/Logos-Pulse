import streamlit as st
from modules.styles import inject_styles, page_header
from modules.auth import is_authenticated, change_password, require_login

inject_styles()

require_login()

page_header("\U0001f510", "Change Password", "You must set a new password before continuing")

st.markdown("""
<div style="background:#FFF3E0; border-left:4px solid #D4853A;
            padding:14px 18px; border-radius:6px; margin-bottom:20px;">
    <b style="color:#E65100;">Action Required:</b> You are using a default password.
    Please set a new password to secure your account.
</div>
""", unsafe_allow_html=True)

with st.form("change_password_form"):
    new_password = st.text_input("New Password", type="password", placeholder="Minimum 8 characters")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter new password")
    submitted = st.form_submit_button("Update Password", type="primary", use_container_width=True)

if submitted:
    if not new_password or not confirm_password:
        st.error("Please fill in both fields.")
    elif new_password != confirm_password:
        st.error("Passwords do not match.")
    elif len(new_password) < 8:
        st.error("Password must be at least 8 characters.")
    elif new_password in ("Raju@002", "Bishop@123", "Pastor@123", "Open@123"):
        st.error("Please choose a password that is different from the default passwords.")
    else:
        with st.spinner("Updating password..."):
            result = change_password(new_password)
        if result["success"]:
            st.success("Password updated! Redirecting...")
            st.rerun()
        else:
            st.error(f"Failed to update password: {result['error']}")