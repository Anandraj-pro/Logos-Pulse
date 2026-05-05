import html as _html
import streamlit as st
from modules.styles import inject_styles, page_header, section_label, spacer
from modules.auth import require_login, require_password_changed
from modules.db import get_notifications, mark_all_notifications_read

require_login()
require_password_changed()
inject_styles()

page_header("\U0001f514", "Notifications", "Stay updated on your community")

notifications = get_notifications()

if notifications:
    unread_count = sum(1 for n in notifications if not n.get("is_read"))
    if unread_count > 0:
        col_hdr, col_btn = st.columns([3, 1])
        with col_hdr:
            st.caption(f"{unread_count} unread notification{'s' if unread_count != 1 else ''}")
        with col_btn:
            if st.button("Mark All Read", use_container_width=True):
                mark_all_notifications_read()
                st.rerun()

TYPE_ICONS = {
    "care_alert":       "\U0001f6a8",
    "prayer_request":   "\U0001f64f",
    "checkin_request":  "\U0001f4cb",
    "general":          "\U0001f514",
}
TYPE_COLORS = {
    "care_alert":       "#C44B5B",
    "prayer_request":   "#3A8F5C",
    "checkin_request":  "#D4853A",
    "general":          "#5B4FC4",
}

spacer(4)

if not notifications:
    st.markdown("""
    <div style="text-align:center; padding:48px 16px; color:#9E96AB;">
        <div style="font-size:40px; margin-bottom:12px;">\U0001f514</div>
        <div style="font-size:15px; font-family:'DM Serif Display',Georgia,serif; color:#2A2438;">All caught up!</div>
        <div style="font-size:13px; margin-top:4px;">No notifications yet.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for n in notifications:
        is_unread = not n.get("is_read", False)
        ntype = n.get("type", "general")
        icon = TYPE_ICONS.get(ntype, "\U0001f514")
        color = TYPE_COLORS.get(ntype, "#5B4FC4")
        border = "3px solid " + color if is_unread else "1px solid #EDE8F5"
        bg = "#FAFAFA" if not is_unread else "white"
        created = n.get("created_at", "")[:10]

        _n_title = _html.escape(n['title'])
        _n_body = _html.escape(n['body']) if n.get('body') else ""
        st.markdown(f"""
        <div class="entry-card" style="border-left:{border}; background:{bg}; margin-bottom:8px;">
            <div style="display:flex; align-items:flex-start; gap:12px;">
                <span style="font-size:20px; margin-top:2px;">{icon}</span>
                <div style="flex:1;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438;
                                     {'font-weight:700;' if is_unread else ''}">
                            {_n_title}
                        </span>
                        <span style="font-size:11px; color:#9E96AB; white-space:nowrap; margin-left:12px;">{created}</span>
                    </div>
                    {"<div style='font-size:13px; color:#6B6580; margin-top:3px;'>" + _n_body + "</div>" if _n_body else ""}
                </div>
                {"<span style='width:8px; height:8px; border-radius:50%; background:" + color + "; display:inline-block; flex-shrink:0; margin-top:6px;'></span>" if is_unread else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)
