import streamlit as st
from datetime import date, timedelta
import calendar
import json
import plotly.graph_objects as go
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id
from modules.utils import calculate_streaks, format_prayer_duration
from modules import db
from modules.supabase_client import get_admin_client

require_role(["admin", "bishop", "pastor"])

inject_styles()

# Get member_id from session state (set by Pastor Dashboard)
member_id = st.session_state.get("viewing_member_id")
if not member_id:
    st.warning("No member selected. Go to Pastor Dashboard and click a member.")
    st.stop()

# Fetch member info
admin = get_admin_client()
try:
    user_resp = admin.auth.admin.get_user_by_id(member_id)
    user_meta = user_resp.user.user_metadata or {}
    member_name = user_meta.get("preferred_name") or user_meta.get("first_name", "Member")
    member_email = user_resp.user.email
except Exception:
    member_name = "Member"
    member_email = ""

profile = admin.table("user_profiles") \
    .select("membership_card_id, prayer_benchmark_min") \
    .eq("user_id", member_id) \
    .execute()
profile_data = profile.data[0] if profile.data else {}

page_header("\U0001f464", f"{member_name}", f"{member_email}")

# Back button
if st.button("\u2190 Back to Dashboard"):
    st.session_state.pop("viewing_member_id", None)
    st.rerun()

# ==================== STATS ROW ====================
all_dates = db.get_member_entry_dates(member_id)
current_streak, longest_streak = calculate_streaks(all_dates)
total_entries = len(all_dates)

col1, col2, col3, col4 = st.columns(4)
with col1:
    streak_color = "#3A8F5C" if current_streak >= 7 else "#D4853A" if current_streak >= 3 else "#5B4FC4"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:{streak_color};">{current_streak}</div>
        <div class="stat-label">Streak</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#5B4FC4;">{longest_streak}</div>
        <div class="stat-label">Best Streak</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#9B5FA8;">{total_entries}</div>
        <div class="stat-label">Total Entries</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    benchmark = profile_data.get("prayer_benchmark_min", 60)
    card_id = profile_data.get("membership_card_id", "")
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value" style="color:#D4853A;">{benchmark}</div>
        <div class="stat-label">Prayer Goal (min)</div>
    </div>
    """, unsafe_allow_html=True)

if card_id:
    st.caption(f"Membership Card: {card_id}")

spacer()

# ==================== TABS ====================
tab_history, tab_charts, tab_notes = st.tabs(["\U0001f4c5 History", "\U0001f4ca Trends", "\U0001f4dd Pastor Notes"])

# ==================== HISTORY TAB ====================
with tab_history:
    entries = db.get_member_entries(member_id, limit=30)

    if not entries:
        empty_state("\U0001f4c5", "No entries yet")
    else:
        # 30-day heatmap
        section_label("Last 30 Days")
        entry_dates_set = set(e["date"] for e in entries)

        heatmap_html = "<div style='display:flex; flex-wrap:wrap; gap:4px; margin-bottom:16px;'>"
        for i in range(30):
            d = date.today() - timedelta(days=29 - i)
            d_str = d.isoformat()
            if d_str in entry_dates_set:
                color = "#5B4FC4"
                text_color = "white"
            elif d <= date.today():
                color = "#FFEBEE"
                text_color = "#FFAB91"
            else:
                color = "#F5F5F5"
                text_color = "#D0C8DB"
            heatmap_html += f'<div style="width:28px; height:28px; border-radius:6px; background:{color}; color:{text_color}; font-size:10px; display:flex; align-items:center; justify-content:center; font-weight:600;">{d.day}</div>'
        heatmap_html += "</div>"
        st.markdown(heatmap_html, unsafe_allow_html=True)

        # Entry list
        section_label("Recent Entries")
        for entry in entries[:15]:
            duration = format_prayer_duration(entry["prayer_minutes"])
            reading = entry.get("chapters_display", "N/A")
            fasted = "\U0001f374 Fasted" if entry.get("fasted") else ""

            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-family:'DM Serif Display',Georgia,serif; color:#2A2438;">{entry['date']}</span>
                    <span style="font-size:12px; color:#9E96AB;">
                        {"Report sent" if entry.get("report_copied") else ""}
                    </span>
                </div>
                <div style="font-size:13px; color:#6B6580; margin-top:4px;">
                    Prayer: {duration} &bull; Reading: {reading}
                    {"&bull; " + entry['sermon_title'] if entry.get('sermon_title') else ""}
                    {" &bull; " + fasted if fasted else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== CHARTS TAB ====================
with tab_charts:
    entries = db.get_member_entries(member_id, limit=30)

    if not entries:
        empty_state("\U0001f4ca", "No data for charts yet")
    else:
        entry_by_date = {e["date"]: e for e in entries}

        # Prayer time trend
        section_label("Prayer Time \u2014 Last 30 Days")
        dates_30 = []
        prayer_mins = []
        for i in range(30):
            d = date.today() - timedelta(days=29 - i)
            d_str = d.isoformat()
            dates_30.append(d.strftime("%b %d"))
            e = entry_by_date.get(d_str)
            prayer_mins.append(e["prayer_minutes"] if e else 0)

        fig_prayer = go.Figure()
        fig_prayer.add_trace(go.Bar(
            x=dates_30, y=prayer_mins,
            marker_color=["#5B4FC4" if m > 0 else "#EDE8F5" for m in prayer_mins],
            hovertemplate="%{x}<br>%{y} min<extra></extra>",
        ))
        fig_prayer.add_hline(
            y=profile_data.get("prayer_benchmark_min", 60),
            line_dash="dot", line_color="#D4853A",
            annotation_text=f"Goal: {profile_data.get('prayer_benchmark_min', 60)} min",
            annotation_position="top right", annotation_font_color="#D4853A",
        )
        fig_prayer.update_layout(
            height=220, margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickfont=dict(size=9, color="#9E96AB"), dtick=5),
            yaxis=dict(showgrid=True, gridcolor="#EDE8F5", tickfont=dict(size=10, color="#9E96AB")),
            bargap=0.3,
        )
        st.plotly_chart(fig_prayer, use_container_width=True)

        # Chapters per week
        section_label("Chapters Read \u2014 Weekly")
        week_labels = []
        week_chapters = []
        for w in range(4):
            w_end = date.today() - timedelta(days=w * 7)
            w_start = w_end - timedelta(days=6)
            week_labels.append(w_start.strftime("%b %d"))
            ch_count = 0
            for i in range(7):
                d = w_start + timedelta(days=i)
                e = entry_by_date.get(d.isoformat())
                if e and e.get("chapters_read"):
                    chs = json.loads(e["chapters_read"]) if isinstance(e["chapters_read"], str) else e["chapters_read"]
                    ch_count += len(chs)
            week_chapters.append(ch_count)

        week_labels.reverse()
        week_chapters.reverse()

        fig_ch = go.Figure()
        fig_ch.add_trace(go.Bar(
            x=week_labels, y=week_chapters,
            marker_color="#9B5FA8", text=week_chapters, textposition="outside",
            textfont=dict(size=12, color="#9B5FA8"),
            hovertemplate="%{x}<br>%{y} chapters<extra></extra>",
        ))
        fig_ch.update_layout(
            height=200, margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, tickfont=dict(size=10, color="#9E96AB")),
            yaxis=dict(showgrid=True, gridcolor="#EDE8F5", tickfont=dict(size=10, color="#9E96AB")),
            bargap=0.4,
        )
        st.plotly_chart(fig_ch, use_container_width=True)

# ==================== PASTOR NOTES TAB ====================
with tab_notes:
    pastor_id = get_current_user_id()

    section_label("Private Notes")
    st.caption("Only you can see these notes. They are not visible to the member.")

    # Add new note
    with st.form("add_note_form"):
        new_note = st.text_area("Add a note", placeholder="e.g., Spoke with them about prayer life. Needs encouragement this week.",
                                height=100, label_visibility="collapsed")
        note_submitted = st.form_submit_button("Save Note", type="primary", use_container_width=True)

    if note_submitted:
        if new_note.strip():
            db.add_pastor_note(pastor_id, member_id, new_note.strip())
            st.success("Note saved!")
            st.rerun()
        else:
            st.error("Please enter a note.")

    spacer()

    # Existing notes
    notes = db.get_pastor_notes(pastor_id, member_id)
    if not notes:
        empty_state("\U0001f4dd", "No notes yet", "Add your first note about this member above")
    else:
        for note in notes:
            created = note.get("created_at", "")[:10]
            st.markdown(f"""
            <div class="entry-card" style="border-left:3px solid #5B4FC4;">
                <div style="font-size:14px; color:#2A2438; line-height:1.6;">
                    {note['note_text']}
                </div>
                <div style="font-size:11px; color:#9E96AB; margin-top:6px;">{created}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Delete", key=f"del_note_{note['id']}"):
                db.delete_pastor_note(note["id"])
                st.rerun()
