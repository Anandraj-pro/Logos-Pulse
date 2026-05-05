import streamlit as st
from datetime import date, timedelta
import plotly.graph_objects as go
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id, get_current_role
from modules.rbac import get_pastors_for_bishop, get_pastors_list, get_members_for_pastor
from modules.supabase_client import get_admin_client
from modules.db import get_bishop_care_overview

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

    # \u2500\u2500 Care Overview \u2500\u2500
    spacer()
    section_label("\U0001f6a8 Care Overview")
    try:
        bishop_id_for_care = my_id if role == "bishop" else None
        if bishop_id_for_care:
            care = get_bishop_care_overview(bishop_id_for_care)
        else:
            # Admin view \u2014 aggregate across all pastors
            all_pastors = get_pastors_list()
            open_total, inactive_total = 0, 0
            admin_c = get_admin_client()
            for p in all_pastors:
                c = get_bishop_care_overview(p["user_id"])
                open_total += c["open_tasks"]
                inactive_total += c["inactive_7d"]
            care = {"open_tasks": open_total, "inactive_7d": inactive_total}

        col_a, col_b = st.columns(2)
        ot_color = "#C44B5B" if care["open_tasks"] > 0 else "#3A8F5C"
        i7_color = "#C44B5B" if care["inactive_7d"] > 0 else "#3A8F5C"
        with col_a:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color:{ot_color};">{care['open_tasks']}</div>
                <div class="stat-label">Open Care Tasks</div>
                <div style="font-size:11px; color:#C0B8CC; margin-top:2px;">across all pastors</div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value" style="color:{i7_color};">{care['inactive_7d']}</div>
                <div class="stat-label">Inactive 7+ Days</div>
                <div style="font-size:11px; color:#C0B8CC; margin-top:2px;">members needing attention</div>
            </div>
            """, unsafe_allow_html=True)
        if care["open_tasks"] > 0 or care["inactive_7d"] > 0:
            st.caption("Open Pastor Dashboard \u2192 Care Alerts to manage follow-up tasks.")
    except Exception:
        st.caption("Care overview will appear once care tasks are in use.")

    # \u2500\u2500 Church Health This Week \u2500\u2500
    spacer()
    section_label("\u26ea Church Health \u2014 This Week")
    try:
        from datetime import timedelta
        _week_start = date.today() - timedelta(days=date.today().weekday())
        _week_end = _week_start + timedelta(days=5)
        _all_member_ids = []
        for ps in pastor_stats:
            _all_member_ids.extend(ps.get("member_ids", []))

        if _all_member_ids:
            _week_entries = admin.table("daily_entries") \
                .select("user_id, prayer_minutes, chapters_read") \
                .in_("user_id", _all_member_ids) \
                .gte("date", _week_start.isoformat()) \
                .lte("date", _week_end.isoformat()) \
                .execute()
            _entries = _week_entries.data or []

            import json as _json
            _total_prayer = sum(e.get("prayer_minutes", 0) for e in _entries)
            _total_chapters = 0
            for e in _entries:
                if e.get("chapters_read"):
                    chs = _json.loads(e["chapters_read"]) if isinstance(e["chapters_read"], str) else e["chapters_read"]
                    _total_chapters += len(chs)
            _active_uids = len({e["user_id"] for e in _entries})
            _prayer_hrs = round(_total_prayer / 60, 1)

            _ch_col, _pr_col, _act_col = st.columns(3)
            with _ch_col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color:#9B5FA8;">{_total_chapters}</div>
                    <div class="stat-label">Chapters This Week</div>
                    <div style="font-size:11px; color:#C0B8CC; margin-top:2px;">across all groups</div>
                </div>
                """, unsafe_allow_html=True)
            with _pr_col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color:#5B4FC4;">{_prayer_hrs}h</div>
                    <div class="stat-label">Prayer Hours</div>
                    <div style="font-size:11px; color:#C0B8CC; margin-top:2px;">this week</div>
                </div>
                """, unsafe_allow_html=True)
            with _act_col:
                _act_pct = int(_active_uids / total_members * 100) if total_members > 0 else 0
                _act_color = "#3A8F5C" if _act_pct >= 70 else "#D4853A" if _act_pct >= 40 else "#C44B5B"
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value" style="color:{_act_color};">{_active_uids}/{total_members}</div>
                    <div class="stat-label">Active Members</div>
                    <div style="font-size:11px; color:#C0B8CC; margin-top:2px;">{_act_pct}% engaged</div>
                </div>
                """, unsafe_allow_html=True)
    except Exception:
        st.caption("Church health stats will appear once members start logging entries.")
