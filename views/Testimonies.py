import streamlit as st
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_login, require_password_changed, get_current_role
from modules import db

require_login()
require_password_changed()
inject_styles()

role = get_current_role()

page_header("\U0001f31f", "Testimony Wall", "Celebrate what God has done")

tab_wall, tab_share = st.tabs(["\U0001f31f Praise Wall", "\u270f\ufe0f Share Testimony"])

# ==================== PRAISE WALL ====================
with tab_wall:
    testimonies = db.get_testimonies(approved_only=True)

    if not testimonies:
        empty_state("\U0001f31f", "No testimonies yet", "Be the first to share what God has done in your life!")
    else:
        for t in testimonies:
            reactions = t.get("reactions") or {"pray": 0, "amen": 0, "hallelujah": 0}
            created = (t.get("created_at") or "")[:10]

            st.markdown(f"""
            <div class="entry-card" style="border-left:3px solid #D4A843;">
                <div style="font-family:'DM Serif Display',Georgia,serif; font-size:18px; color:#2A2438; margin-bottom:4px;">
                    {t['title']}
                </div>
                <div style="font-size:14px; color:#6B6580; line-height:1.7; margin-bottom:8px;">
                    {t['testimony'][:300].replace(chr(10), '<br/>')}{'...' if len(t.get('testimony','')) > 300 else ''}
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:12px; color:#9E96AB;">
                        {t.get('author_name', 'Member')} &bull; {created}
                    </span>
                    <span style="font-size:13px;">
                        \U0001f64f {reactions.get('pray', 0)} &nbsp;
                        \U0001f64c {reactions.get('amen', 0)} &nbsp;
                        \U0001f389 {reactions.get('hallelujah', 0)}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("\U0001f64f Pray", key=f"pray_{t['id']}", use_container_width=True):
                    db.react_to_testimony(t["id"], "pray")
                    st.rerun()
            with col2:
                if st.button("\U0001f64c Amen", key=f"amen_{t['id']}", use_container_width=True):
                    db.react_to_testimony(t["id"], "amen")
                    st.rerun()
            with col3:
                if st.button("\U0001f389 Hallelujah", key=f"hal_{t['id']}", use_container_width=True):
                    db.react_to_testimony(t["id"], "hallelujah")
                    st.rerun()

    # Pastor/Admin: Pending approvals
    if role in ("admin", "bishop", "pastor"):
        spacer()
        pending = db.get_testimonies(approved_only=False)
        pending = [t for t in pending if not t.get("is_approved")]
        if pending:
            section_label(f"Pending Approval ({len(pending)})")
            for t in pending:
                st.markdown(f"""
                <div class="entry-card" style="border-left:3px solid #D4853A;">
                    <div style="font-size:15px; font-weight:600; color:#2A2438;">{t['title']}</div>
                    <div style="font-size:13px; color:#6B6580; margin-top:4px;">{t['testimony'][:150]}...</div>
                    <div style="font-size:12px; color:#9E96AB; margin-top:4px;">by {t.get('author_name', 'Member')}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Approve", key=f"approve_{t['id']}", type="primary", use_container_width=True):
                    db.approve_testimony(t["id"])
                    st.success("Testimony approved!")
                    st.rerun()

# ==================== SHARE TESTIMONY ====================
with tab_share:
    section_label("Share Your Testimony")
    st.caption("Your testimony will be reviewed by your pastor before appearing on the wall.")

    with st.form("testimony_form"):
        t_title = st.text_input("Title", placeholder="e.g., God healed my mother!")
        t_text = st.text_area("Your testimony", height=200,
                              placeholder="Share what God has done in your life...")
        t_anon = st.checkbox("Share anonymously")
        t_submit = st.form_submit_button("Submit Testimony", type="primary", use_container_width=True)

    if t_submit:
        if not t_title.strip() or not t_text.strip():
            st.error("Please fill in both title and testimony.")
        else:
            db.create_testimony(t_title.strip(), t_text.strip(), t_anon)
            st.success("Testimony submitted! It will appear on the wall after pastor approval.")
