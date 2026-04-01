import streamlit as st
from datetime import date
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id, get_current_role
from modules.rbac import get_members_for_pastor
from modules.supabase_client import get_admin_client

require_role(["admin", "bishop", "pastor"])

inject_styles()

role = get_current_role()
my_id = get_current_user_id()

# If admin or bishop, let them pick which pastor to view
if role in ("admin", "bishop"):
    from modules.rbac import get_pastors_list, get_pastors_for_bishop

    if role == "admin":
        pastors = get_pastors_list()
    else:
        pastors = get_pastors_for_bishop(my_id)

    if not pastors:
        page_header("\U0001f9d1\u200d\U0001f91d\u200d\U0001f9d1", "Pastor Dashboard", "No pastors found")
        st.stop()

    pastor_options = {p["display_name"] + f" ({p['email']})": p["user_id"] for p in pastors}
    selected = st.selectbox("Select Pastor", options=list(pastor_options.keys()))
    viewing_pastor_id = pastor_options[selected]
    pastor_name = selected.split(" (")[0]
else:
    viewing_pastor_id = my_id
    pastor_name = st.session_state.get("preferred_name", "Pastor")

page_header("\U0001f9d1\u200d\U0001f91d\u200d\U0001f9d1", f"{pastor_name}'s Group", "Member progress and streak tracking")

# Get members
members = get_members_for_pastor(viewing_pastor_id)

if not members:
    empty_state("\U0001f465", "No members assigned yet", "Prayer Warriors will appear here once assigned to this pastor")
    st.stop()

# Get today's entries for all members
admin = get_admin_client()
today_str = date.today().isoformat()
member_ids = [m["user_id"] for m in members]

today_entries = admin.table("daily_entries") \
    .select("user_id, prayer_minutes, chapters_display, report_copied") \
    .eq("date", today_str) \
    .in_("user_id", member_ids) \
    .execute()

logged_user_ids = {e["user_id"] for e in (today_entries.data or [])}
entry_map = {e["user_id"]: e for e in (today_entries.data or [])}

# Summary metrics
logged_count = len(logged_user_ids)
total_count = len(members)
pct = int(logged_count / total_count * 100) if total_count > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#5B4FC4;">{total_count}</div>
        <div class="stat-label">Total Members</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    color = "#3A8F5C" if pct >= 70 else "#D4853A" if pct >= 40 else "#C44B5B"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:{color};">{logged_count}/{total_count}</div>
        <div class="stat-label">Logged Today</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    reports_copied = sum(1 for e in (today_entries.data or []) if e.get("report_copied"))
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#D4853A;">{reports_copied}</div>
        <div class="stat-label">Reports Sent</div>
    </div>
    """, unsafe_allow_html=True)

spacer()

# Member list
section_label("Members")

view_mode = st.segmented_control("Filter", ["All", "Logged Today", "Not Logged"], default="All", label_visibility="collapsed")

for member in members:
    uid = member["user_id"]
    logged = uid in logged_user_ids
    entry = entry_map.get(uid)

    if view_mode == "Logged Today" and not logged:
        continue
    if view_mode == "Not Logged" and logged:
        continue

    status_icon = "\u2705" if logged else "\u274c"
    status_color = "#3A8F5C" if logged else "#C44B5B"
    status_bg = "#E8F5E9" if logged else "#FFEBEE"

    details = ""
    if entry:
        details = f"Prayer: {entry.get('prayer_minutes', 0)} min | Reading: {entry.get('chapters_display', 'N/A')}"
        if entry.get("report_copied"):
            details += " | Report sent"

    card_id_text = f" | Card: {member['membership_card_id']}" if member.get("membership_card_id") else ""

    st.markdown(f"""
    <div class="entry-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;">
                    {status_icon} {member['display_name']}
                </span>
                <span style="font-size:12px; color:#9E96AB; margin-left:8px;">
                    {member['email']}{card_id_text}
                </span>
            </div>
            <span style="background:{status_bg}; color:{status_color}; padding:2px 10px;
                         border-radius:10px; font-size:11px; font-weight:600;">
                {"Logged" if logged else "Pending"}
            </span>
        </div>
        {"<div style='font-size:13px; color:#6B6580; margin-top:6px;'>" + details + "</div>" if details else ""}
    </div>
    """, unsafe_allow_html=True)