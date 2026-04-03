import streamlit as st
from datetime import date, timedelta
import plotly.graph_objects as go
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

admin = get_admin_client()
today_str = date.today().isoformat()

# Aggregate today's stats
total_pastors = len(pastors)
total_members = 0
total_logged = 0

pastor_stats = []
for pastor in pastors:
    members = get_members_for_pastor(pastor["user_id"])
    member_count = len(members)
    total_members += member_count

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
        "member_ids": [m["user_id"] for m in members],
    })

overall_pct = int(total_logged / total_members * 100) if total_members > 0 else 0

# ==================== METRICS ====================
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

# ==================== TABS ====================
tab_pastors, tab_trends = st.tabs(["\U0001f465 Pastors & Groups", "\U0001f4c8 Engagement Trends"])

# ==================== PASTORS TAB ====================
with tab_pastors:
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

        with st.expander(f"View {ps['display_name']}'s members"):
            p_members = get_members_for_pastor(ps["user_id"])
            if not p_members:
                st.caption("No members assigned")
            else:
                for m in p_members:
                    m_entry = admin.table("daily_entries") \
                        .select("prayer_minutes, chapters_display") \
                        .eq("user_id", m["user_id"]) \
                        .eq("date", today_str) \
                        .execute()
                    m_logged = bool(m_entry.data)
                    m_icon = "\u2705" if m_logged else "\u274c"
                    m_detail = ""
                    if m_entry.data:
                        me = m_entry.data[0]
                        m_detail = f" \u2014 {me.get('prayer_minutes', 0)} min, {me.get('chapters_display', '')}"
                    st.markdown(f"{m_icon} **{m['display_name']}**{m_detail}")

# ==================== M5: ENGAGEMENT TRENDS TAB ====================
with tab_trends:
    section_label("Weekly Engagement \u2014 Last 12 Weeks")

    # Build weekly engagement data per pastor
    colors = ["#5B4FC4", "#3A8F5C", "#D4853A", "#C44B5B", "#2196F3", "#9B5FA8", "#E85D3A", "#009688"]

    fig = go.Figure()

    for idx, ps in enumerate(pastor_stats):
        if not ps["member_ids"]:
            continue

        week_labels = []
        week_pcts = []

        for w in range(12):
            w_end = date.today() - timedelta(days=w * 7)
            w_start = w_end - timedelta(days=6)
            week_labels.append(w_start.strftime("%b %d"))

            # Count entries for this pastor's members in this week
            total_possible = ps["member_count"] * 6  # Mon-Sat
            if total_possible == 0:
                week_pcts.append(0)
                continue

            entries = admin.table("daily_entries") \
                .select("user_id", count="exact") \
                .in_("user_id", ps["member_ids"]) \
                .gte("date", w_start.isoformat()) \
                .lte("date", w_end.isoformat()) \
                .execute()
            logged = entries.count or 0
            week_pcts.append(int(logged / total_possible * 100))

        week_labels.reverse()
        week_pcts.reverse()

        fig.add_trace(go.Scatter(
            x=week_labels, y=week_pcts,
            mode="lines+markers",
            name=ps["display_name"],
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=6),
            hovertemplate="%{x}<br>%{y}% engagement<extra>" + ps["display_name"] + "</extra>",
        ))

    # Goal line
    fig.add_hline(y=70, line_dash="dot", line_color="#3A8F5C",
                  annotation_text="Target: 70%", annotation_position="top right",
                  annotation_font_color="#3A8F5C")

    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#9E96AB")),
        yaxis=dict(showgrid=True, gridcolor="#EDE8F5", tickfont=dict(size=10, color="#9E96AB"),
                   title="Engagement %", range=[0, 105]),
        legend=dict(orientation="h", y=-0.15, font=dict(size=11)),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary table
    spacer()
    section_label("Pastor Comparison")
    for ps in pastor_stats:
        trend = "\u2191" if ps["pct"] >= 50 else "\u2193" if ps["pct"] < 30 else "\u2192"
        st.markdown(f"**{ps['display_name']}** \u2014 {ps['member_count']} members, {ps['pct']}% today {trend}")
