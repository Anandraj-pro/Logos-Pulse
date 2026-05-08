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
    "prayer_request":   "#2B5A3E",
    "checkin_request":  "#C48A1C",
    "general":          "#B85A30",
}

spacer(4)

if not notifications:
    st.markdown(
        '<div class="empty-state">'
        '<span class="empty-state-icon">\U0001f514</span>'
        '<div class="empty-state-title">All caught up!</div>'
        '<div class="empty-state-sub">No notifications yet.</div>'
        '</div>',
        unsafe_allow_html=True
    )
else:
    for n in notifications:
        is_unread = not n.get("is_read", False)
        ntype = n.get("type", "general")
        icon = TYPE_ICONS.get(ntype, "\U0001f514")
        color = TYPE_COLORS.get(ntype, "#B85A30")
        border = "3px solid " + color if is_unread else "1px solid #F3EFE7"
        bg = "#FFFFFF" if is_unread else "#FAFAFA"
        created = n.get("created_at", "")[:10]

        _n_title = _html.escape(n["title"])
        _n_body = _html.escape(n["body"]) if n.get("body") else ""
        _fw = "font-weight:700;" if is_unread else ""
        _body_html = ("<div style='font-size:13px; color:#5A4A32; margin-top:3px;'>" + _n_body + "</div>") if _n_body else ""
        _dot_html = ("<span style='width:8px; height:8px; border-radius:50%; background:" + color + "; display:inline-block; flex-shrink:0; margin-top:6px;'></span>") if is_unread else ""

        st.markdown(
            '<div class="entry-card" style="border-left:' + border + '; background:' + bg + '; margin-bottom:8px;">'
            '<div style="display:flex; align-items:flex-start; gap:12px;">'
            '<span style="font-size:20px; margin-top:2px;">' + icon + '</span>'
            '<div style="flex:1;">'
            '<div style="display:flex; justify-content:space-between; align-items:center;">'
            '<span style="font-family:\'Cormorant\',Georgia,serif; font-size:15px; color:#1A1208; ' + _fw + '">'
            + _n_title +
            '</span>'
            '<span style="font-size:11px; color:#A09080; white-space:nowrap; margin-left:12px;">' + created + '</span>'
            '</div>'
            + _body_html +
            '</div>'
            + _dot_html +
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )
