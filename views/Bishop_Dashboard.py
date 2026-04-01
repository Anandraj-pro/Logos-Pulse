import streamlit as st
from datetime import date
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id, get_current_role
from modules.rbac import get_pastors_for_bishop, get_pastors_list, get_members_for_pastor
from modules.supabase_client import get_admin_client

require_role(["admin", "bishop"])

inject_styles()

role = get_current_role()
my_id = get_current_user_id()

page_header("\u2696\ufe0f", "Bishop Dashboard", "Oversight of pastors and their groups")

# Get pastors
if role == "admin":
    pastors = get_pastors_list()
else:
    pastors = get_pastors_for_bishop(my_id)

if not pastors:
    empty_state("\u2696\ufe0f", "No pastors assigned yet", "Pastors will appear here once assigned to this bishop")
    st.stop()

# Get today's entries across all members
admin = get_admin_client()
today_str = date.today().isoformat()

# Aggregate stats
total_pastors = len(pastors)
total_members = 0
total_logged = 0

pastor_stats = []
for pastor in pastors:
    members = get_members_for_pastor(pastor["user_id"])
    member_count = len(members)
    total_members += member_count

    # Check who logged today
    if members:
        member_ids = [m["user_id"] for m in members]
        entries = admin.table("daily_entries") \
            .select("user_id", count="exact") \
            .eq("date", today_str) \
            .in_("user_id", member_ids) \
            .execute()
        logged = entries.count or 0
    else:
        logged = 0

    total_logged += logged

    pastor_stats.append({
        **pastor,
        "member_count": member_count,
        "logged_today": logged,
        "pct": int(logged / member_count * 100) if member_count > 0 else 0,
    })

# Summary metrics
overall_pct = int(total_logged / total_members * 100) if total_members > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#2196F3;">{total_pastors}</div>
        <div class="stat-label">Pastors</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#5B4FC4;">{total_members}</div>
        <div class="stat-label">Total Members</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    color = "#3A8F5C" if overall_pct >= 70 else "#D4853A" if overall_pct >= 40 else "#C44B5B"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:{color};">{total_logged}/{total_members}</div>
        <div class="stat-label">Logged Today</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:{color};">{overall_pct}%</div>
        <div class="stat-label">Engagement</div>
    </div>
    """, unsafe_allow_html=True)

spacer()

# Pastor breakdown
section_label("Pastors & Groups")

for ps in pastor_stats:
    pct = ps["pct"]
    pct_color = "#3A8F5C" if pct >= 70 else "#D4853A" if pct >= 40 else "#C44B5B"
    region_text = f" | {ps['region_or_group']}" if ps.get("region_or_group") else ""

    st.markdown(f"""
    <div class="entry-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438;">
                    {ps['display_name']}
                </span>
                <span style="font-size:12px; color:#9E96AB; margin-left:8px;">
                    {ps['email']}{region_text}
                </span>
            </div>
            <span style="background:{'#E8F5E9' if pct >= 70 else '#FFF3E0' if pct >= 40 else '#FFEBEE'};
                         color:{pct_color}; padding:3px 12px;
                         border-radius:10px; font-size:12px; font-weight:600;">
                {ps['logged_today']}/{ps['member_count']} logged ({pct}%)
            </span>
        </div>
        <div style="margin-top:8px;">
            <div class="progress-bar-bg" style="height:8px;">
                <div class="progress-bar-fill" style="width:{pct}%;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)