import html as _html
import streamlit as st
import json
from modules import db
from modules.scripture_lookup import parse_references, render_reference_with_text
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_login, require_password_changed

require_login()
require_password_changed()
inject_styles()
def hex_to_rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"
# ==================== HEADER ====================
categories = db.get_prayer_categories()
total_prayers = 0
for cat in categories:
    total_prayers += len(db.get_prayers_by_category(cat["id"]))

page_header("\U0001f64f", "Prayer Journal", f"{total_prayers} prayers across {len(categories)} categories")

# ==================== CATEGORY SELECTOR ====================
cat_counts = {}
for cat in categories:
    prayers = db.get_prayers_by_category(cat["id"])
    cat_counts[cat["id"]] = len(prayers)

cols = st.columns(len(categories) + 3)

# Initialize selected category
if "pj_category" not in st.session_state and categories:
    st.session_state["pj_category"] = categories[0]["id"]

for i, cat in enumerate(categories):
    with cols[i]:
        count = cat_counts.get(cat["id"], 0)
        is_active = st.session_state.get("pj_category") == cat["id"]
        color = cat.get("color", "#5B4FC4")
        active_class = "cat-card-active" if is_active else ""

        st.markdown(f"""
        <div class="cat-card {active_class}" style="background:{hex_to_rgba(color, 0.06)}; color:{color};">
            <div class="cat-icon">{cat['icon']}</div>
            <div class="cat-name">{cat['name']}</div>
            <div class="cat-count">{count} prayer{"s" if count != 1 else ""}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(cat["name"], key=f"cat_{cat['id']}", use_container_width=True, type="secondary" if not is_active else "primary"):
            st.session_state["pj_category"] = cat["id"]
            st.session_state.pop("pj_wizard_step", None)
            st.rerun()

# Bible Notes button
with cols[-3]:
    is_bn = st.session_state.get("pj_category") == "bible_notes"
    st.markdown(f"""
    <div class="cat-card {'cat-card-active' if is_bn else ''}" style="background:{'rgba(33,150,243,0.08)' if is_bn else '#F0F4FF'}; color:#2196F3;">
        <div class="cat-icon">\U0001f4d6</div>
        <div class="cat-name">Bible</div>
        <div class="cat-count">Notes</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Bible Notes", key="bible_notes_btn", use_container_width=True,
                 type="primary" if is_bn else "secondary"):
        st.session_state["pj_category"] = "bible_notes"
        st.rerun()

# Prayer Wall button
with cols[-2]:
    is_pw = st.session_state.get("pj_category") == "prayer_wall"
    st.markdown(f"""
    <div class="cat-card {'cat-card-active' if is_pw else ''}" style="background:{'rgba(58,143,92,0.08)' if is_pw else '#F0FFF4'}; color:#3A8F5C;">
        <div class="cat-icon">\U0001f64c</div>
        <div class="cat-name">Prayer</div>
        <div class="cat-count">Wall</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Prayer Wall", key="prayer_wall_btn", use_container_width=True,
                 type="primary" if is_pw else "secondary"):
        st.session_state["pj_category"] = "prayer_wall"
        st.rerun()

# New category button
with cols[-1]:
    st.markdown("""
    <div class="cat-card" style="background:#F5F5F5; color:#9E96AB;">
        <div class="cat-icon">+</div>
        <div class="cat-name">New</div>
        <div class="cat-count">Category</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Add New", key="new_cat_btn", use_container_width=True):
        st.session_state["pj_category"] = "new"
        st.rerun()

spacer(12)

# ==================== BIBLE NOTES ====================
if st.session_state.get("pj_category") == "bible_notes":
    from modules.db import get_all_bookmarks, get_highlight_count, update_bookmark_note, delete_bookmark
    from modules.auth import get_current_user_id

    section_label("\U0001f516 My Bookmarks")

    all_bm = get_all_bookmarks()
    hl_count = get_highlight_count()

    if not all_bm and hl_count == 0:
        st.markdown("""
        <div style="text-align:center; padding:32px 16px; color:#9E96AB;">
            <div style="font-size:32px; margin-bottom:8px;">\U0001f4d6</div>
            <div style="font-size:14px;">No bookmarks yet.</div>
            <div style="font-size:12px; margin-top:4px;">Open Daily Entry, switch on 🔖 Annotate, and tap ☆ on any verse.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Highlight summary
        if hl_count > 0:
            st.markdown(f"""
            <div class="entry-card" style="border-left:4px solid #F4C430;">
                <span style="font-size:13px; color:#6B6580;">
                    🟡 <b>{hl_count}</b> verse{"s" if hl_count != 1 else ""} highlighted.
                    Open Daily Entry → Annotate mode to manage highlights.
                </span>
            </div>
            """, unsafe_allow_html=True)
            spacer(4)

        if all_bm:
            # Group by book + chapter
            from collections import defaultdict
            grouped: dict = defaultdict(list)
            for bm in all_bm:
                grouped[(bm["book"], bm["chapter"])].append(bm)

            for (book, chapter), verses in sorted(grouped.items()):
                with st.expander(f"\U0001f4d6 {book} {chapter} — {len(verses)} bookmark{'s' if len(verses) != 1 else ''}"):
                    for bm in sorted(verses, key=lambda x: x["verse_number"]):
                        col_v, col_del = st.columns([10, 1])
                        with col_v:
                            st.markdown(f"""
                            <div style="font-family:'DM Serif Display',Georgia,serif;
                                        font-size:14px; color:#2A2438; margin-bottom:2px;">
                                <span style="color:#5B4FC4; font-weight:700; font-size:11px;
                                             vertical-align:super; margin-right:4px;">v{bm['verse_number']}</span>
                                {book} {chapter}:{bm['verse_number']}
                            </div>
                            """, unsafe_allow_html=True)

                            note_key = f"bm_note_{bm['id']}"
                            new_note = st.text_input(
                                "Note", value=bm.get("note") or "",
                                key=note_key, placeholder="Add a note…",
                                label_visibility="collapsed",
                            )
                            if new_note != (bm.get("note") or ""):
                                update_bookmark_note(book, chapter, bm["verse_number"], new_note)
                                st.rerun()
                        with col_del:
                            if st.button("🗑", key=f"del_bm_{bm['id']}", help="Remove bookmark"):
                                delete_bookmark(bm["id"])
                                st.rerun()

# ==================== PRAYER WALL ====================
elif st.session_state.get("pj_category") == "prayer_wall":
    from modules.db import (
        get_prayer_requests, create_prayer_request, toggle_pray_for, mark_prayer_answered,
    )
    from modules.auth import get_current_user_id as _get_uid_pj

    my_uid = _get_uid_pj()
    requests = get_prayer_requests()

    col_wall, col_new = st.columns([3, 1])
    with col_wall:
        section_label("\U0001f64c Community Prayer Wall")
    with col_new:
        if st.button("+ New Request", use_container_width=True, type="primary"):
            st.session_state["pj_show_new_request"] = not st.session_state.get("pj_show_new_request", False)

    if st.session_state.get("pj_show_new_request"):
        with st.form("new_prayer_request_form"):
            pr_title = st.text_input("Prayer Request", placeholder="What do you need prayer for?")
            pr_body = st.text_area("Details (optional)", height=80, placeholder="Share more context if you'd like…")
            pr_anon = st.checkbox("Post anonymously")
            pr_submit = st.form_submit_button("Submit Request", type="primary", use_container_width=True)
        if pr_submit:
            if not pr_title.strip():
                st.error("Please enter a title for your request.")
            else:
                create_prayer_request(pr_title.strip(), pr_body.strip(), pr_anon)
                st.session_state.pop("pj_show_new_request", None)
                st.success("Your prayer request has been shared with the community.")
                st.rerun()

    spacer(8)

    if not requests:
        st.markdown("""
        <div style="text-align:center; padding:32px 16px; color:#9E96AB;">
            <div style="font-size:32px; margin-bottom:8px;">\U0001f64c</div>
            <div style="font-size:14px;">No prayer requests yet.</div>
            <div style="font-size:12px; margin-top:4px;">Be the first to share a request — the community will pray with you.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for req in requests:
            is_mine = req["user_id"] == my_uid
            author = "Anonymous" if req.get("is_anonymous") else req.get("display_name", "Member")
            pray_count = req.get("pray_count", 0)
            has_prayed = req.get("has_prayed", False)
            pray_color = "#3A8F5C" if has_prayed else "#9E96AB"
            pray_label = f"\U0001f64f Praying ({pray_count})" if has_prayed else f"\U0001f64f Pray ({pray_count})"

            _title_e = _html.escape(req['title'])
            _body_e = _html.escape(req['body']) if req.get('body') else ""
            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div style="font-family:'DM Serif Display',Georgia,serif; font-size:15px; color:#2A2438; flex:1;">
                        {_title_e}
                    </div>
                    <span style="font-size:11px; color:#9E96AB; white-space:nowrap; margin-left:12px;">
                        {_html.escape(author)}
                    </span>
                </div>
                {"<div style='font-size:13px; color:#6B6580; margin-top:6px;'>" + _body_e + "</div>" if _body_e else ""}
            </div>
            """, unsafe_allow_html=True)

            btn_cols = st.columns([2, 2, 6]) if is_mine else st.columns([2, 8])
            with btn_cols[0]:
                if st.button(pray_label, key=f"pray_{req['id']}", use_container_width=True):
                    toggle_pray_for(req["id"])
                    st.rerun()
            if is_mine:
                with btn_cols[1]:
                    if st.button("Mark Answered", key=f"ans_{req['id']}", use_container_width=True):
                        mark_prayer_answered(req["id"])
                        st.session_state["pj_share_testimony_for"] = req["id"]
                        st.session_state["pj_share_testimony_title"] = req["title"]
                        st.rerun()

    # Offer to share as testimony after marking answered
    if st.session_state.get("pj_share_testimony_for"):
        from modules.db import create_testimony
        _req_title = st.session_state["pj_share_testimony_title"]
        st.success(f"🙌 Prayer answered: \"{_req_title}\"")
        st.markdown("**Would you like to share this as a testimony on the Testimony Wall?**")
        c1, c2 = st.columns(2)
        with c1:
            _anon = st.checkbox("Share anonymously", key="pj_testimony_anon")
        _testimony_text = st.text_area(
            "Add details (optional)",
            placeholder="Share how God answered your prayer…",
            height=80,
            key="pj_testimony_text",
        )
        col_yes, col_no = st.columns(2)
        with col_yes:
            if st.button("✨ Share as Testimony", type="primary", use_container_width=True):
                create_testimony(
                    title=f"Answered prayer: {_req_title}",
                    testimony=_testimony_text.strip() if _testimony_text else f"God answered my prayer: {_req_title}",
                    is_anonymous=_anon,
                )
                st.session_state.pop("pj_share_testimony_for", None)
                st.session_state.pop("pj_share_testimony_title", None)
                st.success("Testimony shared! 🎉")
                st.rerun()
        with col_no:
            if st.button("No thanks", use_container_width=True):
                st.session_state.pop("pj_share_testimony_for", None)
                st.session_state.pop("pj_share_testimony_title", None)
                st.rerun()

# ==================== NEW CATEGORY ====================
elif st.session_state.get("pj_category") == "new":
    st.markdown(f"""
    <div class="wizard-step">
        <span class="wizard-step-num" style="background:#5B4FC4;">+</span>
        <span class="wizard-step-title">Create New Category</span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("new_category_form"):
        cat_name = st.text_input("Category Name", placeholder="e.g., Family, Ministry, Health")
        col1, col2 = st.columns(2)
        with col1:
            cat_icon = st.text_input("Emoji Icon", value="\U0001f4d6", max_chars=2)
        with col2:
            cat_colors = {"Purple": "#5B4FC4", "Green": "#3A8F5C", "Pink": "#C44B5B",
                          "Orange": "#D4853A", "Blue": "#2196F3", "Teal": "#009688"}
            cat_color = st.selectbox("Color", options=list(cat_colors.keys()))

        if st.form_submit_button("Create Category", type="primary", use_container_width=True):
            if cat_name.strip():
                new_cat = db.create_prayer_category(cat_name.strip(), cat_icon, cat_colors[cat_color])
                st.session_state["pj_category"] = new_cat["id"]
                st.success(f"Category '{cat_name}' created!")
                st.rerun()
            else:
                st.error("Please enter a category name.")

# ==================== CATEGORY VIEW ====================
elif st.session_state.get("pj_category"):
    cat_id = st.session_state["pj_category"]
    category = next((c for c in categories if c["id"] == cat_id), None)

    if not category:
        st.session_state["pj_category"] = categories[0]["id"] if categories else None
        st.rerun()
    else:
        cat_color = category.get("color", "#5B4FC4")

        tab_list, tab_new = st.tabs(["\U0001f4cb My Prayers", "\u2795 New Prayer"])

        # ==================== PRAYERS LIST ====================
        with tab_list:
            prayers = db.get_prayers_by_category(cat_id)

            # Status filter row
            col_filter, col_count = st.columns([3, 1])
            with col_filter:
                status_filter = st.segmented_control(
                    "Filter",
                    ["All", "Ongoing", "Answered", "Standing in Faith"],
                    default="All",
                    label_visibility="collapsed",
                )
            with col_count:
                st.markdown(f"<div style='text-align:right; padding-top:8px; font-size:13px; color:#9E96AB;'>{len(prayers)} total</div>", unsafe_allow_html=True)

            if status_filter and status_filter != "All":
                status_key = status_filter.lower().replace(" ", "_")
                prayers = [p for p in prayers if p.get("status") == status_key]

            if not prayers:
                empty_state(category['icon'], "No prayers here yet", 'Add your first prayer in the "New Prayer" tab')
            else:
                for prayer in prayers:
                    status = prayer.get("status", "ongoing")
                    status_config = {
                        "ongoing": ("#D4853A", "#FFF3E0", "Ongoing"),
                        "answered": ("#3A8F5C", "#E8F5E9", "Answered"),
                        "standing_in_faith": ("#5B4FC4", "#EDEBFA", "Standing in Faith"),
                    }
                    s_color, s_bg, s_label = status_config.get(status, ("#888", "#F5F5F5", status))

                    st.markdown(f"""
                    <div class="prayer-card">
                        <div class="prayer-title-row">
                            <span class="prayer-name">{prayer['title']}</span>
                            <span class="status-badge" style="background:{s_bg}; color:{s_color};">{s_label}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("View Details", expanded=False):
                        # Prayer text
                        if prayer.get("prayer_text"):
                            st.markdown(f"""
                            <div style="background:#EDEBFA; border-radius:10px; padding:14px 18px;
                                        font-style:italic; color:#2A2438; line-height:1.8; font-size:15px;">
                                {prayer['prayer_text'].replace(chr(10), '<br/>')}
                            </div>
                            """, unsafe_allow_html=True)

                        # Scriptures
                        if prayer.get("scriptures"):
                            refs = json.loads(prayer["scriptures"]) if isinstance(
                                prayer["scriptures"], str
                            ) else prayer["scriptures"]
                            if refs:
                                st.markdown(f"""
                                <div style="font-size:11px; color:{cat_color}; text-transform:uppercase;
                                            letter-spacing:1px; font-weight:600; margin:16px 0 8px 0;">
                                    Scriptures ({len(refs)})
                                </div>
                                """, unsafe_allow_html=True)
                                for ref in refs:
                                    if isinstance(ref, dict):
                                        enriched = render_reference_with_text(ref)
                                        if enriched.get("scripture_text"):
                                            st.markdown(f"""
                                            <div class="scripture-block" style="border-color:{cat_color};">
                                                <b style="color:{cat_color}; font-size:13px;">{ref.get('reference', '')}</b><br/>
                                                <i>{enriched['scripture_text']}</i>
                                            </div>
                                            """, unsafe_allow_html=True)

                        # Confessions
                        if prayer.get("confessions"):
                            st.markdown("""
                            <div style="font-size:11px; color:#2E7D32; text-transform:uppercase;
                                        letter-spacing:1px; font-weight:600; margin:16px 0 8px 0;">
                                Confessions
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="confession-block">
                                {prayer['confessions'].replace(chr(10), '<br/>')}
                            </div>
                            """, unsafe_allow_html=True)

                        # Declarations
                        if prayer.get("declarations"):
                            st.markdown("""
                            <div style="font-size:11px; color:#E65100; text-transform:uppercase;
                                        letter-spacing:1px; font-weight:600; margin:16px 0 8px 0;">
                                Declarations
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="declaration-block">
                                {prayer['declarations'].replace(chr(10), '<br/>')}
                            </div>
                            """, unsafe_allow_html=True)

                        # M4: Share with Pastor toggle
                        spacer(8)
                        is_shared = prayer.get("shared_with_pastor", False)
                        if is_shared:
                            st.markdown("""
                            <div style="background:#EDEBFA; border-radius:8px; padding:6px 12px; font-size:12px; color:#5B4FC4;">
                                \U0001f91d Shared with your pastor
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("Stop Sharing", key=f"unshare_{prayer['id']}"):
                                db.unshare_prayer(prayer["id"])
                                st.rerun()
                        else:
                            if st.button("\U0001f91d Share with Pastor", key=f"share_{prayer['id']}", use_container_width=True):
                                db.share_prayer_with_pastor(prayer["id"])
                                st.success("Shared! Your pastor can now see this prayer request.")
                                st.rerun()

                        # Actions row
                        spacer(12)
                        col_s, col_d = st.columns([3, 1])
                        with col_s:
                            new_status = st.selectbox(
                                "Update Status",
                                ["ongoing", "answered", "standing_in_faith"],
                                index=["ongoing", "answered", "standing_in_faith"].index(status),
                                key=f"status_{prayer['id']}",
                                format_func=lambda x: x.replace("_", " ").title(),
                            )
                            if new_status != status:
                                db.update_prayer_entry(
                                    prayer["id"],
                                    title=prayer["title"],
                                    prayer_text=prayer.get("prayer_text", ""),
                                    scriptures=json.loads(prayer["scriptures"]) if isinstance(
                                        prayer.get("scriptures"), str
                                    ) else prayer.get("scriptures", []),
                                    confessions=prayer.get("confessions", ""),
                                    declarations=prayer.get("declarations", ""),
                                    status=new_status,
                                )
                                if new_status == "answered":
                                    st.balloons()
                                st.rerun()
                        with col_d:
                            if st.button("Delete", key=f"del_{prayer['id']}"):
                                st.session_state[f"confirm_del_{prayer['id']}"] = True
                            if st.session_state.get(f"confirm_del_{prayer['id']}"):
                                st.warning("Sure?")
                                c1, c2 = st.columns(2)
                                with c1:
                                    if st.button("Yes", key=f"yes_del_{prayer['id']}", type="primary"):
                                        db.delete_prayer_entry(prayer["id"])
                                        st.session_state.pop(f"confirm_del_{prayer['id']}", None)
                                        st.rerun()
                                with c2:
                                    if st.button("No", key=f"no_del_{prayer['id']}"):
                                        st.session_state.pop(f"confirm_del_{prayer['id']}", None)
                                        st.rerun()

        # ==================== NEW PRAYER WIZARD ====================
        with tab_new:
            if "pj_wizard_step" not in st.session_state:
                st.session_state["pj_wizard_step"] = 1
            if "pj_wizard_data" not in st.session_state:
                st.session_state["pj_wizard_data"] = {}

            step = st.session_state["pj_wizard_step"]
            data = st.session_state["pj_wizard_data"]

            # Progress indicator
            steps = ["Purpose", "Prayer", "Scripture", "Confessions", "Declarations"]
            progress_html = ""
            for i, s_name in enumerate(steps):
                s_num = i + 1
                if s_num < step:
                    dot_style = f"background:{cat_color}; color:white;"
                    label_style = f"color:{cat_color}; font-weight:600;"
                elif s_num == step:
                    dot_style = f"background:{cat_color}; color:white; box-shadow:0 0 0 4px {hex_to_rgba(cat_color, 0.2)};"
                    label_style = f"color:{cat_color}; font-weight:700;"
                else:
                    dot_style = "background:#E0E0E0; color:#9E96AB;"
                    label_style = "color:#C0B8CC;"
                progress_html += f"""
                <div style="text-align:center; flex:1;">
                    <div style="width:32px; height:32px; border-radius:50%; {dot_style}
                                display:inline-flex; align-items:center; justify-content:center;
                                font-size:14px; font-weight:700;">{s_num}</div>
                    <div style="font-size:11px; margin-top:4px; {label_style}">{s_name}</div>
                </div>
                """

            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; margin:8px 0 24px 0;">
                {progress_html}
            </div>
            """, unsafe_allow_html=True)

            # --- Step 1: Purpose ---
            if step == 1:
                st.markdown(f"""
                <div class="wizard-step">
                    <span class="wizard-step-num" style="background:{cat_color};">1</span>
                    <span class="wizard-step-title">What are you praying for?</span>
                    <div class="wizard-step-desc">Give your prayer a clear purpose or title.</div>
                </div>
                """, unsafe_allow_html=True)

                prayer_title = st.text_input(
                    "Prayer Title",
                    value=data.get("title", ""),
                    placeholder="e.g., Wisdom for career decision, Financial breakthrough, Healing",
                    label_visibility="collapsed",
                )

                # REQ-4: Template selector
                templates = db.get_prayer_templates()
                if templates:
                    template_options = {"-- No template (start blank) --": None}
                    for t in templates:
                        badge = "\U0001f4cb" if t["template_type"] == "standard" else "\u270f\ufe0f"
                        template_options[f"{badge} {t['name']}"] = t
                    selected_tpl = st.selectbox(
                        "Use a template (optional)",
                        options=list(template_options.keys()),
                        label_visibility="collapsed",
                    )
                    tpl = template_options[selected_tpl]
                    if tpl:
                        st.caption(f"{tpl.get('description', '')}")
                        if st.button("Apply Template", use_container_width=True):
                            data["prayer_text"] = tpl.get("prayers", "")
                            data["confessions"] = tpl.get("confessions", "")
                            data["declarations"] = tpl.get("declarations", "")
                            if not prayer_title.strip():
                                data["title"] = tpl["name"]
                            st.rerun()

                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("Next \u2192", type="primary", use_container_width=True):
                        if not prayer_title.strip():
                            st.error("Please enter a prayer title.")
                        else:
                            data["title"] = prayer_title.strip()
                            st.session_state["pj_wizard_step"] = 2
                            st.rerun()

            # --- Step 2: Prayer ---
            elif step == 2:
                st.markdown(f"""
                <div class="wizard-step">
                    <span class="wizard-step-num" style="background:{cat_color};">2</span>
                    <span class="wizard-step-title">Write your prayer</span>
                    <div class="wizard-step-desc">Pour your heart out. This is your conversation with God.</div>
                </div>
                """, unsafe_allow_html=True)

                prayer_text = st.text_area(
                    "Prayer",
                    value=data.get("prayer_text", ""),
                    height=200,
                    placeholder="Dear Lord, I come before you today...",
                    label_visibility="collapsed",
                )

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("\u2190 Back", use_container_width=True):
                        data["prayer_text"] = prayer_text
                        st.session_state["pj_wizard_step"] = 1
                        st.rerun()
                with col2:
                    if st.button("Skip", use_container_width=True):
                        st.session_state["pj_wizard_step"] = 3
                        st.rerun()
                with col3:
                    if st.button("Next \u2192", type="primary", use_container_width=True):
                        data["prayer_text"] = prayer_text
                        st.session_state["pj_wizard_step"] = 3
                        st.rerun()

            # --- Step 3: Scripture ---
            elif step == 3:
                st.markdown(f"""
                <div class="wizard-step">
                    <span class="wizard-step-num" style="background:{cat_color};">3</span>
                    <span class="wizard-step-title">Bible Scriptures</span>
                    <div class="wizard-step-desc">Type references to anchor your prayer in God's Word.</div>
                </div>
                """, unsafe_allow_html=True)

                scriptures_text = st.text_area(
                    "Scriptures",
                    value=data.get("scriptures_text", ""),
                    height=120,
                    placeholder="Philippians 4:19\nJeremiah 29:11\nPsalms 23:1",
                    label_visibility="collapsed",
                )

                if scriptures_text.strip():
                    parsed = parse_references(scriptures_text)
                    for ref in parsed:
                        enriched = render_reference_with_text(ref)
                        if enriched.get("scripture_text"):
                            st.markdown(f"""
                            <div class="scripture-block" style="border-color:{cat_color};">
                                <b style="color:{cat_color}; font-size:13px;">{enriched['reference']}</b><br/>
                                <i>{enriched['scripture_text']}</i>
                            </div>
                            """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("\u2190 Back", use_container_width=True, key="s3_back"):
                        data["scriptures_text"] = scriptures_text
                        st.session_state["pj_wizard_step"] = 2
                        st.rerun()
                with col2:
                    if st.button("Skip", use_container_width=True, key="s3_skip"):
                        st.session_state["pj_wizard_step"] = 4
                        st.rerun()
                with col3:
                    if st.button("Next \u2192", type="primary", use_container_width=True, key="s3_next"):
                        data["scriptures_text"] = scriptures_text
                        st.session_state["pj_wizard_step"] = 4
                        st.rerun()

            # --- Step 4: Confessions ---
            elif step == 4:
                st.markdown(f"""
                <div class="wizard-step">
                    <span class="wizard-step-num" style="background:{cat_color};">4</span>
                    <span class="wizard-step-title">Confessions</span>
                    <div class="wizard-step-desc">Declare what you believe based on God's promises.</div>
                </div>
                """, unsafe_allow_html=True)

                confessions = st.text_area(
                    "Confessions",
                    value=data.get("confessions", ""),
                    height=150,
                    placeholder="I confess that God is my provider...\nI confess that no weapon formed against me shall prosper...",
                    label_visibility="collapsed",
                )

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("\u2190 Back", use_container_width=True, key="s4_back"):
                        data["confessions"] = confessions
                        st.session_state["pj_wizard_step"] = 3
                        st.rerun()
                with col2:
                    if st.button("Skip", use_container_width=True, key="s4_skip"):
                        st.session_state["pj_wizard_step"] = 5
                        st.rerun()
                with col3:
                    if st.button("Next \u2192", type="primary", use_container_width=True, key="s4_next"):
                        data["confessions"] = confessions
                        st.session_state["pj_wizard_step"] = 5
                        st.rerun()

            # --- Step 5: Declarations + Review ---
            elif step == 5:
                st.markdown(f"""
                <div class="wizard-step">
                    <span class="wizard-step-num" style="background:{cat_color};">5</span>
                    <span class="wizard-step-title">Declarations</span>
                    <div class="wizard-step-desc">Speak faith statements over your life.</div>
                </div>
                """, unsafe_allow_html=True)

                declarations = st.text_area(
                    "Declarations",
                    value=data.get("declarations", ""),
                    height=150,
                    placeholder="I declare that this is my year of abundance...\nI declare divine favor over my life...",
                    label_visibility="collapsed",
                )

                st.divider()

                # Review summary
                section_label("Review Your Prayer")

                st.markdown(f"**Title:** {data.get('title', '')}")
                if data.get("prayer_text"):
                    st.markdown(f"**Prayer:** {data['prayer_text'][:100]}...")
                if data.get("scriptures_text"):
                    st.markdown(f"**Scriptures:** {data['scriptures_text'][:80]}...")
                if data.get("confessions"):
                    st.markdown(f"**Confessions:** {data['confessions'][:80]}...")
                if declarations:
                    st.markdown(f"**Declarations:** {declarations[:80]}...")

                spacer(12)

                col1, col2 = st.columns([1, 2])
                with col1:
                    if st.button("\u2190 Back", use_container_width=True, key="s5_back"):
                        data["declarations"] = declarations
                        st.session_state["pj_wizard_step"] = 4
                        st.rerun()
                with col2:
                    if st.button("\U0001f64f Save Prayer", type="primary", use_container_width=True, key="s5_save"):
                        data["declarations"] = declarations

                        # Parse scriptures
                        refs_list = []
                        if data.get("scriptures_text", "").strip():
                            parsed = parse_references(data["scriptures_text"])
                            refs_list = [{"reference": r["reference"], "book": r["book"],
                                          "chapter": r["chapter"],
                                          "start_verse": r.get("start_verse"),
                                          "end_verse": r.get("end_verse")} for r in parsed]

                        db.create_prayer_entry(
                            category_id=cat_id,
                            title=data.get("title", ""),
                            prayer_text=data.get("prayer_text", ""),
                            scriptures=refs_list,
                            confessions=data.get("confessions", ""),
                            declarations=data.get("declarations", ""),
                        )

                        # Reset wizard
                        st.session_state["pj_wizard_step"] = 1
                        st.session_state["pj_wizard_data"] = {}
                        st.success("Prayer saved!")
                        st.balloons()
                        st.rerun()