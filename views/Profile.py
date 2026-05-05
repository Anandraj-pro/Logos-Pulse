import html as _html
import streamlit as st
from modules.styles import inject_styles, page_header, section_label, spacer
from modules.auth import require_login, require_password_changed, change_password, get_current_user_id
from modules.supabase_client import get_admin_client

require_login()
require_password_changed()

inject_styles()

user_id = get_current_user_id()
admin = get_admin_client()

# Fetch profile and auth user data
profile = admin.table("user_profiles") \
    .select("*") \
    .eq("user_id", user_id) \
    .single() \
    .execute()
profile_data = profile.data

user_resp = admin.auth.admin.get_user_by_id(user_id)
user_meta = user_resp.user.user_metadata or {}

role = profile_data["role"]
role_display = role.replace("_", " ").title()
role_colors = {
    "admin": "#C44B5B",
    "bishop": "#2196F3",
    "pastor": "#3A8F5C",
    "prayer_warrior": "#5B4FC4",
}

page_header("\U0001f464", "My Profile", f"{role_display} Account")

# ==================== PROFILE INFO ====================
st.markdown(f"""
<div class="entry-card" style="text-align:center; padding:28px;">
    <div style="font-size:48px; margin-bottom:8px;">\U0001f464</div>
    <div style="font-family:'DM Serif Display',Georgia,serif; font-size:24px; color:#2A2438;">
        {user_meta.get('preferred_name') or user_meta.get('first_name', '')} {user_meta.get('last_name', '')}
    </div>
    <span style="background:{role_colors.get(role, '#5B4FC4')}; color:white; padding:3px 14px;
                 border-radius:12px; font-size:12px; font-weight:600;">
        {role_display}
    </span>
    <div style="font-size:13px; color:#9E96AB; margin-top:8px;">
        {user_resp.user.email}
    </div>
    {"<div style='font-size:12px; color:#9E96AB; margin-top:4px;'>Card: " + profile_data['membership_card_id'] + "</div>" if profile_data.get('membership_card_id') else ""}
</div>
""", unsafe_allow_html=True)

spacer()

# Show hierarchy info
if role == "prayer_warrior" and profile_data.get("pastor_id"):
    try:
        pastor_user = admin.auth.admin.get_user_by_id(profile_data["pastor_id"]).user
        pastor_meta = pastor_user.user_metadata or {}
        pastor_name = pastor_meta.get("preferred_name") or pastor_meta.get("first_name", "")
        st.markdown(f"""
        <div class="entry-card">
            <div style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">
                My Pastor
            </div>
            <div style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438; margin-top:4px;">
                {pastor_name}
            </div>
            <div style="font-size:12px; color:#6B6580;">{pastor_user.email}</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

elif role == "pastor" and profile_data.get("bishop_id"):
    try:
        bishop_user = admin.auth.admin.get_user_by_id(profile_data["bishop_id"]).user
        bishop_meta = bishop_user.user_metadata or {}
        bishop_name = bishop_meta.get("preferred_name") or bishop_meta.get("first_name", "")
        st.markdown(f"""
        <div class="entry-card">
            <div style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px; font-weight:600;">
                My Bishop
            </div>
            <div style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438; margin-top:4px;">
                {bishop_name}
            </div>
            <div style="font-size:12px; color:#6B6580;">{bishop_user.email}</div>
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

spacer()

# ==================== EDIT PROFILE ====================
tab_edit, tab_password, tab_care = st.tabs(["\u270f\ufe0f Edit Profile", "\U0001f510 Change Password", "\U0001f4cb My Care"])

with tab_edit:
    section_label("Personal Information")

    with st.form("edit_profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", value=user_meta.get("first_name", ""))
        with col2:
            last_name = st.text_input("Last Name", value=user_meta.get("last_name", ""))

        preferred_name = st.text_input(
            "Preferred Name",
            value=user_meta.get("preferred_name", ""),
            help="This is what we'll call you in the app",
        )

        membership_card = st.text_input(
            "Church Membership Card ID",
            value=profile_data.get("membership_card_id") or "",
            placeholder="e.g. TKT1694",
        )

        prayer_benchmark = st.number_input(
            "Daily Prayer Goal (minutes)",
            min_value=15,
            max_value=480,
            value=profile_data.get("prayer_benchmark_min", 60),
            step=15,
        )

        submitted = st.form_submit_button("Save Changes", type="primary", use_container_width=True)

    if submitted:
        if not first_name or not last_name:
            st.error("First name and last name are required.")
        else:
            try:
                # Update auth user metadata
                admin.auth.admin.update_user_by_id(user_id, {
                    "user_metadata": {
                        "first_name": first_name.strip(),
                        "last_name": last_name.strip(),
                        "preferred_name": (preferred_name.strip() or first_name.strip()),
                    },
                })

                # Update profile
                admin.table("user_profiles") \
                    .update({
                        "membership_card_id": membership_card.strip() or None,
                        "prayer_benchmark_min": prayer_benchmark,
                    }) \
                    .eq("user_id", user_id) \
                    .execute()

                # Update greeting name in settings
                from modules.db import save_setting
                save_setting("greeting_name", preferred_name.strip() or first_name.strip())
                save_setting("default_prayer_minutes", str(prayer_benchmark))

                # Update session state
                st.session_state["preferred_name"] = preferred_name.strip() or first_name.strip()

                st.success("Profile updated!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to update profile: {e}")

with tab_password:
    section_label("Change Your Password")

    with st.form("change_pw_form"):
        new_pw = st.text_input("New Password", type="password", placeholder="Minimum 8 characters")
        confirm_pw = st.text_input("Confirm Password", type="password", placeholder="Re-enter new password")
        pw_submitted = st.form_submit_button("Update Password", type="primary", use_container_width=True)

    if pw_submitted:
        if not new_pw or not confirm_pw:
            st.error("Please fill in both fields.")
        elif new_pw != confirm_pw:
            st.error("Passwords do not match.")
        elif len(new_pw) < 8:
            st.error("Password must be at least 8 characters.")
        elif new_pw in ("Raju@002", "Bishop@123", "Pastor@123", "Open@123"):
            st.error("Please choose a password different from the defaults.")
        else:
            result = change_password(new_pw)
            if result["success"]:
                st.success("Password updated successfully!")
            else:
                st.error(f"Failed: {result['error']}")

with tab_care:
    from modules.db import create_checkin_request, get_my_checkin_requests

    section_label("Request a Pastoral Check-in")
    st.caption("Send a request to your pastor for a personal follow-up.")

    with st.form("checkin_form"):
        checkin_msg = st.text_area(
            "Message (optional)",
            height=80,
            placeholder="Let your pastor know what you'd like to discuss…",
        )
        checkin_submit = st.form_submit_button("Send Check-in Request", type="primary", use_container_width=True)

    if checkin_submit:
        if not profile_data.get("pastor_id"):
            st.warning("You haven't been assigned a pastor yet. Contact your admin.")
        else:
            create_checkin_request(checkin_msg.strip() if checkin_msg else None)
            st.success("Request sent! Your pastor will reach out to you.")

    spacer()
    section_label("My Check-in History")
    my_reqs = get_my_checkin_requests()
    if not my_reqs:
        st.caption("No check-in requests yet.")
    else:
        for cr in my_reqs:
            sc = "#3A8F5C" if cr.get("status") == "acknowledged" else "#D4853A"
            _cr_msg = _html.escape(cr['message']) if cr.get('message') else ""
            st.markdown(f"""
            <div class="entry-card" style="border-left:3px solid {sc};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:13px; color:#2A2438; font-weight:600;">
                            {"Acknowledged ✔" if cr['status'] == 'acknowledged' else "Pending"}
                        </span>
                        {"<div style='font-size:12px; color:#6B6580; margin-top:2px;'>" + _cr_msg + "</div>" if _cr_msg else ""}
                    </div>
                    <span style="font-size:11px; color:#9E96AB; white-space:nowrap; margin-left:8px;">{cr['created_at'][:10]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)