import html as _html
import streamlit as st
import json
from datetime import date, timedelta
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


# ── Confession Plans helper (used in Tab 2) ───────────────────────────────────
def _render_plan_card(plan, completed_plan_ids):
    tpl = plan.get("confession_templates", {})
    cat = tpl.get("confession_categories", {}) if tpl else {}
    is_done_today = plan["id"] in completed_plan_ids
    progress_text = ""
    progress_pct = 0
    if plan.get("start_date") and plan.get("end_date"):
        start = date.fromisoformat(plan["start_date"])
        end = date.fromisoformat(plan["end_date"])
        total_days = (end - start).days + 1
        completions = db.get_completions_for_plan(plan["id"])
        days_done = len({c["completed_date"] for c in completions})
        progress_pct = min(days_done / total_days, 1.0) if total_days > 0 else 0
        progress_text = f"Day {days_done} of {total_days}"
    else:
        completions = db.get_completions_for_plan(plan["id"])
        progress_text = f"{len(completions)} days completed"
    badge_html = ""
    if plan.get("assigned_by"):
        badge_html = '<span class="plan-badge" style="background:#FDF0E8; color:#B85A30;">Prescribed by Pastor</span>'
    if plan.get("is_new_believer_track"):
        badge_html = '<span class="plan-badge" style="background:#E8F3ED; color:#2B5A3E;">New Believer Track</span>'
    if is_done_today:
        badge_html += ' <span class="plan-badge" style="background:#E8F3ED; color:#2B5A3E;">Done Today</span>'
    status_icon = "&#9989;" if is_done_today else "&#9203;"
    bar_color = cat.get("color") or "#B85A30"
    bar_pct = f"{progress_pct * 100:.0f}%"
    note_html = ""
    if plan.get("assignment_note"):
        note_html = '<div style="font-size:12px; color:#A09080; margin-top:4px; font-style:italic;">Note: ' + plan.get("assignment_note", "") + '</div>'
    st.markdown(
        '<div class="plan-card">'
        + '<div style="display:flex; justify-content:space-between; align-items:center;">'
        + '<div>'
        + f'<span style="font-size:20px;">{status_icon}</span>'
        + f'<span class="plan-title">{tpl.get("name", "Confession")}</span>'
        + '</div>'
        + '<div>' + badge_html + '</div>'
        + '</div>'
        + f'<div style="font-size:13px; color:#5A4A32; margin-top:6px;">{cat.get("icon", "")} {cat.get("name", "")} &middot; {progress_text}</div>'
        + note_html
        + '<div class="plan-progress-bar">'
        + f'<div class="plan-progress-fill" style="width:{bar_pct}; background:{bar_color};"></div>'
        + '</div>'
        + '</div>',
        unsafe_allow_html=True
    )
    col_a, col_b = st.columns(2)
    with col_a:
        if not is_done_today:
            if st.button("Confess Now", key=f"confess_{plan['id']}", type="primary", use_container_width=True):
                st.session_state["pe_confess_plan"] = plan["id"]
                st.session_state[f"confess_line_{plan['id']}"] = 0
                st.rerun()
        else:
            st.button("Completed", key=f"done_{plan['id']}", disabled=True, use_container_width=True)
    with col_b:
        if st.button("Remove", key=f"remove_{plan['id']}", use_container_width=True):
            db.update_plan_status(plan["id"], "removed")
            st.rerun()


# ── Shared CSS (plan cards + confession engine) ───────────────────────────────
st.markdown(
    '<style>'
    '.need-chip{display:inline-block;padding:10px 20px;border-radius:24px;font-family:"Jost",sans-serif;'
    'font-size:14px;font-weight:600;cursor:pointer;margin:4px;transition:all 0.2s;}'
    '.need-chip:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(26,18,8,0.10);}'
    '.cotw-banner{background:linear-gradient(135deg,#B85A30 0%,#C48A1C 100%);color:white;'
    'border-radius:16px;padding:20px 24px;margin-bottom:16px;}'
    '.cotw-banner .cotw-label{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;opacity:0.8;}'
    '.cotw-banner .cotw-title{font-family:"Cormorant",serif;font-size:22px;margin:6px 0;}'
    '.cotw-banner .cotw-theme{font-size:13px;opacity:0.85;}'
    '.cat-grid-card{background:#FFFFFF;border:1px solid rgba(26,18,8,0.09);border-radius:14px;'
    'padding:18px;text-align:center;transition:all 0.2s;min-height:140px;}'
    '.cat-grid-card:hover{border-color:#B85A30;box-shadow:0 4px 16px rgba(184,90,48,0.10);}'
    '.cat-grid-icon{font-size:32px;margin-bottom:8px;}'
    '.cat-grid-name{font-family:"Cormorant",serif;font-size:15px;color:#1A1208;margin-bottom:4px;}'
    '.cat-grid-count{font-size:12px;color:#A09080;}'
    '.template-card{background:#FFFFFF;border:1px solid rgba(26,18,8,0.09);border-radius:14px;padding:20px;margin-bottom:12px;}'
    '.template-name{font-family:"Cormorant",serif;font-size:18px;color:#1A1208;}'
    '.template-desc{font-size:13px;color:#5A4A32;margin:6px 0 12px;}'
    '.template-shortform{background:#FFF9F0;border-left:3px solid #C48A1C;padding:12px 16px;'
    'border-radius:0 8px 8px 0;font-size:14px;line-height:1.8;color:#1A1208;white-space:pre-line;}'
    '.plan-card{background:#FFFFFF;border:1px solid rgba(26,18,8,0.09);border-radius:14px;padding:18px;margin-bottom:12px;}'
    '.plan-card .plan-title{font-family:"Cormorant",serif;font-size:16px;color:#1A1208;}'
    '.plan-card .plan-badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:11px;font-weight:600;}'
    '.plan-progress-bar{height:6px;background:rgba(26,18,8,0.06);border-radius:3px;margin-top:10px;overflow:hidden;}'
    '.plan-progress-fill{height:100%;border-radius:3px;transition:width 0.3s;}'
    '.confess-line{font-family:"Cormorant",serif;font-size:22px;color:#1A1208;line-height:1.6;text-align:center;padding:30px 20px;}'
    '.confess-scripture{font-family:"Jost",sans-serif;font-size:14px;color:#B85A30;text-align:center;margin-top:8px;}'
    '.maturity-warning{background:#FDF0E8;border:1px solid #C48A1C;border-radius:12px;'
    'padding:16px;margin-bottom:16px;font-size:14px;color:#5A4A32;}'
    '</style>',
    unsafe_allow_html=True
)

# ── Page header & top-level tabs ──────────────────────────────────────────────
categories = db.get_prayer_categories()
total_prayers = sum(len(db.get_prayers_by_category(c["id"])) for c in categories)

page_header("\U0001f64f", "Prayer", "My Prayers & Confession Plans")

tab_prayers, tab_confession = st.tabs(["\U0001f64f My Prayers", "✝️ Confession Plans"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MY PRAYERS (Prayer Journal)
# ══════════════════════════════════════════════════════════════════════════════
with tab_prayers:
    cat_counts = {cat["id"]: len(db.get_prayers_by_category(cat["id"])) for cat in categories}

    cols = st.columns(len(categories) + 3)

    if "pj_category" not in st.session_state and categories:
        st.session_state["pj_category"] = categories[0]["id"]

    for i, cat in enumerate(categories):
        with cols[i]:
            count = cat_counts.get(cat["id"], 0)
            is_active = st.session_state.get("pj_category") == cat["id"]
            color = cat.get("color", "#B85A30")
            active_class = "cat-card-active" if is_active else ""
            st.markdown(f"""
            <div class="cat-card {active_class}" style="background:{hex_to_rgba(color, 0.06)}; color:{color};">
                <div class="cat-icon">{cat['icon']}</div>
                <div class="cat-name">{cat['name']}</div>
                <div class="cat-count">{count} prayer{"s" if count != 1 else ""}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(cat["name"], key=f"cat_{cat['id']}", use_container_width=True,
                         type="secondary" if not is_active else "primary"):
                st.session_state["pj_category"] = cat["id"]
                st.session_state.pop("pj_wizard_step", None)
                st.rerun()

    with cols[-3]:
        is_bn = st.session_state.get("pj_category") == "bible_notes"
        st.markdown(f"""
        <div class="cat-card {'cat-card-active' if is_bn else ''}" style="background:{'rgba(184,90,48,0.08)' if is_bn else '#F9F5EF'}; color:#B85A30;">
            <div class="cat-icon">\U0001f4d6</div>
            <div class="cat-name">Bible</div>
            <div class="cat-count">Notes</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Bible Notes", key="bible_notes_btn", use_container_width=True,
                     type="primary" if is_bn else "secondary"):
            st.session_state["pj_category"] = "bible_notes"
            st.rerun()

    with cols[-2]:
        is_pw = st.session_state.get("pj_category") == "prayer_wall"
        st.markdown(f"""
        <div class="cat-card {'cat-card-active' if is_pw else ''}" style="background:{'rgba(43,90,62,0.08)' if is_pw else '#EEF5F1'}; color:#2B5A3E;">
            <div class="cat-icon">\U0001f64c</div>
            <div class="cat-name">Prayer</div>
            <div class="cat-count">Wall</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Prayer Wall", key="prayer_wall_btn", use_container_width=True,
                     type="primary" if is_pw else "secondary"):
            st.session_state["pj_category"] = "prayer_wall"
            st.rerun()

    with cols[-1]:
        st.markdown("""
        <div class="cat-card" style="background:#F5F5F5; color:#A09080;">
            <div class="cat-icon">+</div>
            <div class="cat-name">New</div>
            <div class="cat-count">Category</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Add New", key="new_cat_btn", use_container_width=True):
            st.session_state["pj_category"] = "new"
            st.rerun()

    spacer(12)

    # ── Bible Notes ──────────────────────────────────────────────────────────
    if st.session_state.get("pj_category") == "bible_notes":
        from modules.db import get_all_bookmarks, get_highlight_count, update_bookmark_note, delete_bookmark
        section_label("\U0001f516 My Bookmarks")
        all_bm = get_all_bookmarks()
        hl_count = get_highlight_count()
        if not all_bm and hl_count == 0:
            st.markdown("""
            <div style="text-align:center; padding:32px 16px; color:#A09080;">
                <div style="font-size:32px; margin-bottom:8px;">\U0001f4d6</div>
                <div style="font-size:14px;">No bookmarks yet.</div>
                <div style="font-size:12px; margin-top:4px;">Open Daily Entry, switch on 🔖 Annotate, and tap ☆ on any verse.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if hl_count > 0:
                st.markdown(f"""
                <div class="entry-card" style="border-left:4px solid #C48A1C;">
                    <span style="font-size:13px; color:#5A4A32;">
                        \U0001f7e1 <b>{hl_count}</b> verse{"s" if hl_count != 1 else ""} highlighted.
                        Open Daily Entry → Annotate mode to manage highlights.
                    </span>
                </div>
                """, unsafe_allow_html=True)
                spacer(4)
            if all_bm:
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
                                <div style="font-family:'Cormorant',Georgia,serif;font-size:14px;color:#1A1208;margin-bottom:2px;">
                                    <span style="color:#B85A30;font-weight:700;font-size:11px;vertical-align:super;margin-right:4px;">v{bm['verse_number']}</span>
                                    {book} {chapter}:{bm['verse_number']}
                                </div>
                                """, unsafe_allow_html=True)
                                new_note = st.text_input("Note", value=bm.get("note") or "",
                                                         key=f"bm_note_{bm['id']}", placeholder="Add a note…",
                                                         label_visibility="collapsed")
                                if new_note != (bm.get("note") or ""):
                                    update_bookmark_note(book, chapter, bm["verse_number"], new_note)
                                    st.rerun()
                            with col_del:
                                if st.button("🗑", key=f"del_bm_{bm['id']}", help="Remove bookmark"):
                                    delete_bookmark(bm["id"])
                                    st.rerun()

    # ── Prayer Wall ──────────────────────────────────────────────────────────
    elif st.session_state.get("pj_category") == "prayer_wall":
        from modules.db import get_prayer_requests, create_prayer_request, toggle_pray_for, mark_prayer_answered
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
            <div style="text-align:center; padding:32px 16px; color:#A09080;">
                <div style="font-size:32px; margin-bottom:8px;">\U0001f64c</div>
                <div style="font-size:14px;">No prayer requests yet.</div>
                <div style="font-size:12px; margin-top:4px;">Be the first to share a request — the community will pray with you.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            from modules.db import create_testimony
            for req in requests:
                is_mine = req["user_id"] == my_uid
                author = "Anonymous" if req.get("is_anonymous") else req.get("display_name", "Member")
                pray_count = req.get("pray_count", 0)
                has_prayed = req.get("has_prayed", False)
                pray_color = "#2B5A3E" if has_prayed else "#A09080"
                pray_label = f"\U0001f64f Praying ({pray_count})" if has_prayed else f"\U0001f64f Pray ({pray_count})"
                _title_e = _html.escape(req['title'])
                _body_e = _html.escape(req['body']) if req.get('body') else ""
                _author_e = _html.escape(author)
                _body_html = ('<div style="font-size:13px;color:#5A4A32;margin-top:6px;">' + _body_e + '</div>') if _body_e else ''
                st.markdown(
                    '<div class="entry-card">'
                    '<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
                    f'<div style="font-family:\'Cormorant\',Georgia,serif;font-size:15px;color:#1A1208;flex:1;">{_title_e}</div>'
                    f'<span style="font-size:11px;color:#A09080;white-space:nowrap;margin-left:12px;">{_author_e}</span>'
                    '</div>' + _body_html + '</div>',
                    unsafe_allow_html=True)
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
        if st.session_state.get("pj_share_testimony_for"):
            from modules.db import create_testimony
            _req_title = st.session_state["pj_share_testimony_title"]
            st.success(f"🙌 Prayer answered: \"{_req_title}\"")
            st.markdown("**Would you like to share this as a testimony on the Testimony Wall?**")
            c1, c2 = st.columns(2)
            with c1:
                _anon = st.checkbox("Share anonymously", key="pj_testimony_anon")
            _testimony_text = st.text_area("Add details (optional)",
                                           placeholder="Share how God answered your prayer…",
                                           height=80, key="pj_testimony_text")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✨ Share as Testimony", type="primary", use_container_width=True):
                    from modules.db import create_testimony as _ct
                    _ct(title=f"Answered prayer: {_req_title}",
                        testimony=_testimony_text.strip() if _testimony_text else f"God answered my prayer: {_req_title}",
                        is_anonymous=_anon)
                    st.session_state.pop("pj_share_testimony_for", None)
                    st.session_state.pop("pj_share_testimony_title", None)
                    st.success("Testimony shared! 🎉")
                    st.rerun()
            with col_no:
                if st.button("No thanks", use_container_width=True):
                    st.session_state.pop("pj_share_testimony_for", None)
                    st.session_state.pop("pj_share_testimony_title", None)
                    st.rerun()

    # ── New Category ─────────────────────────────────────────────────────────
    elif st.session_state.get("pj_category") == "new":
        st.markdown("""
        <div class="wizard-step">
            <span class="wizard-step-num" style="background:#B85A30;">+</span>
            <span class="wizard-step-title">Create New Category</span>
        </div>
        """, unsafe_allow_html=True)
        with st.form("new_category_form"):
            cat_name = st.text_input("Category Name", placeholder="e.g., Family, Ministry, Health")
            col1, col2 = st.columns(2)
            with col1:
                cat_icon = st.text_input("Emoji Icon", value="\U0001f4d6", max_chars=2)
            with col2:
                cat_colors = {"Purple": "#B85A30", "Green": "#3A8F5C", "Pink": "#C44B5B",
                              "Orange": "#C48A1C", "Blue": "#2196F3", "Teal": "#009688"}
                cat_color = st.selectbox("Color", options=list(cat_colors.keys()))
            if st.form_submit_button("Create Category", type="primary", use_container_width=True):
                if cat_name.strip():
                    new_cat = db.create_prayer_category(cat_name.strip(), cat_icon, cat_colors[cat_color])
                    st.session_state["pj_category"] = new_cat["id"]
                    st.success(f"Category '{cat_name}' created!")
                    st.rerun()
                else:
                    st.error("Please enter a category name.")

    # ── Category View ─────────────────────────────────────────────────────────
    elif st.session_state.get("pj_category"):
        cat_id = st.session_state["pj_category"]
        category = next((c for c in categories if c["id"] == cat_id), None)
        if not category:
            st.session_state["pj_category"] = categories[0]["id"] if categories else None
            st.rerun()
        else:
            cat_color = category.get("color", "#B85A30")
            tab_list, tab_new = st.tabs(["\U0001f4cb My Prayers", "➕ New Prayer"])

            with tab_list:
                prayers = db.get_prayers_by_category(cat_id)
                col_filter, col_count = st.columns([3, 1])
                with col_filter:
                    status_filter = st.segmented_control(
                        "Filter", ["All", "Ongoing", "Answered", "Standing in Faith"],
                        default="All", label_visibility="collapsed")
                with col_count:
                    st.markdown(f"<div style='text-align:right;padding-top:8px;font-size:13px;color:#A09080;'>{len(prayers)} total</div>", unsafe_allow_html=True)
                if status_filter and status_filter != "All":
                    status_key = status_filter.lower().replace(" ", "_")
                    prayers = [p for p in prayers if p.get("status") == status_key]
                if not prayers:
                    empty_state(category['icon'], "No prayers here yet", 'Add your first prayer in the "New Prayer" tab')
                else:
                    for prayer in prayers:
                        status = prayer.get("status", "ongoing")
                        status_config = {
                            "ongoing": ("#C48A1C", "#FDF6EC", "Ongoing"),
                            "answered": ("#2B5A3E", "#EEF5F1", "Answered"),
                            "standing_in_faith": ("#B85A30", "rgba(184,90,48,0.08)", "Standing in Faith"),
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
                            if prayer.get("prayer_text"):
                                st.markdown(f"""
                                <div style="background:#FDF6EC;border-radius:10px;padding:14px 18px;
                                            font-style:italic;color:#1A1208;line-height:1.8;font-size:15px;">
                                    {prayer['prayer_text'].replace(chr(10), '<br/>')}
                                </div>
                                """, unsafe_allow_html=True)
                            if prayer.get("scriptures"):
                                refs = json.loads(prayer["scriptures"]) if isinstance(prayer["scriptures"], str) else prayer["scriptures"]
                                if refs:
                                    st.markdown(f'<div style="font-size:11px;color:{cat_color};text-transform:uppercase;letter-spacing:1px;font-weight:600;margin:16px 0 8px 0;">Scriptures ({len(refs)})</div>', unsafe_allow_html=True)
                                    for ref in refs:
                                        if isinstance(ref, dict):
                                            enriched = render_reference_with_text(ref)
                                            if enriched.get("scripture_text"):
                                                st.markdown(f'<div class="scripture-block" style="border-color:{cat_color};"><b style="color:{cat_color};font-size:13px;">{ref.get("reference","")}</b><br/><i>{enriched["scripture_text"]}</i></div>', unsafe_allow_html=True)
                            if prayer.get("confessions"):
                                st.markdown('<div style="font-size:11px;color:#2B5A3E;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin:16px 0 8px 0;">Confessions</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="confession-block">{prayer["confessions"].replace(chr(10), "<br/>")}</div>', unsafe_allow_html=True)
                            if prayer.get("declarations"):
                                st.markdown('<div style="font-size:11px;color:#B85A30;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin:16px 0 8px 0;">Declarations</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="declaration-block">{prayer["declarations"].replace(chr(10), "<br/>")}</div>', unsafe_allow_html=True)
                            spacer(8)
                            is_shared = prayer.get("shared_with_pastor", False)
                            if is_shared:
                                st.markdown('<div style="background:rgba(184,90,48,0.08);border-radius:8px;padding:6px 12px;font-size:12px;color:#B85A30;">\U0001f91d Shared with your pastor</div>', unsafe_allow_html=True)
                                if st.button("Stop Sharing", key=f"unshare_{prayer['id']}"):
                                    db.unshare_prayer(prayer["id"])
                                    st.rerun()
                            else:
                                if st.button("\U0001f91d Share with Pastor", key=f"share_{prayer['id']}", use_container_width=True):
                                    db.share_prayer_with_pastor(prayer["id"])
                                    st.success("Shared! Your pastor can now see this prayer request.")
                                    st.rerun()
                            spacer(12)
                            col_s, col_d = st.columns([3, 1])
                            with col_s:
                                new_status = st.selectbox(
                                    "Update Status",
                                    ["ongoing", "answered", "standing_in_faith"],
                                    index=["ongoing", "answered", "standing_in_faith"].index(status),
                                    key=f"status_{prayer['id']}",
                                    format_func=lambda x: x.replace("_", " ").title())
                                if new_status != status:
                                    db.update_prayer_entry(
                                        prayer["id"], title=prayer["title"],
                                        prayer_text=prayer.get("prayer_text", ""),
                                        scriptures=json.loads(prayer["scriptures"]) if isinstance(prayer.get("scriptures"), str) else prayer.get("scriptures", []),
                                        confessions=prayer.get("confessions", ""),
                                        declarations=prayer.get("declarations", ""),
                                        status=new_status)
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

            with tab_new:
                if "pj_wizard_step" not in st.session_state:
                    st.session_state["pj_wizard_step"] = 1
                if "pj_wizard_data" not in st.session_state:
                    st.session_state["pj_wizard_data"] = {}
                step = st.session_state["pj_wizard_step"]
                data = st.session_state["pj_wizard_data"]
                steps_labels = ["Purpose", "Prayer", "Scripture", "Confessions", "Declarations"]
                progress_html = ""
                for i, s_name in enumerate(steps_labels):
                    s_num = i + 1
                    if s_num < step:
                        dot_style = f"background:{cat_color}; color:white;"
                        label_style = f"color:{cat_color}; font-weight:600;"
                    elif s_num == step:
                        dot_style = f"background:{cat_color}; color:white; box-shadow:0 0 0 4px {hex_to_rgba(cat_color, 0.2)};"
                        label_style = f"color:{cat_color}; font-weight:700;"
                    else:
                        dot_style = "background:#E0E0E0; color:#A09080;"
                        label_style = "color:#A09080;"
                    progress_html += (
                        '<div style="text-align:center;flex:1;">'
                        f'<div style="width:32px;height:32px;border-radius:50%;{dot_style}display:inline-flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;">{s_num}</div>'
                        f'<div style="font-size:11px;margin-top:4px;{label_style}">{s_name}</div>'
                        '</div>'
                    )
                st.markdown('<div style="display:flex;justify-content:space-between;margin:8px 0 24px 0;">' + progress_html + '</div>', unsafe_allow_html=True)

                if step == 1:
                    st.markdown(f'<div class="wizard-step"><span class="wizard-step-num" style="background:{cat_color};">1</span><span class="wizard-step-title">What are you praying for?</span><div class="wizard-step-desc">Give your prayer a clear purpose or title.</div></div>', unsafe_allow_html=True)
                    prayer_title = st.text_input("Prayer Title", value=data.get("title", ""),
                                                 placeholder="e.g., Wisdom for career decision, Healing",
                                                 label_visibility="collapsed")
                    templates = db.get_prayer_templates()
                    if templates:
                        template_options = {"-- No template (start blank) --": None}
                        for t in templates:
                            badge = "\U0001f4cb" if t["template_type"] == "standard" else "✏️"
                            template_options[f"{badge} {t['name']}"] = t
                        selected_tpl = st.selectbox("Use a template (optional)", options=list(template_options.keys()), label_visibility="collapsed")
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
                        if st.button("Next →", type="primary", use_container_width=True):
                            if not prayer_title.strip():
                                st.error("Please enter a prayer title.")
                            else:
                                data["title"] = prayer_title.strip()
                                st.session_state["pj_wizard_step"] = 2
                                st.rerun()

                elif step == 2:
                    st.markdown(f'<div class="wizard-step"><span class="wizard-step-num" style="background:{cat_color};">2</span><span class="wizard-step-title">Write your prayer</span><div class="wizard-step-desc">Pour your heart out.</div></div>', unsafe_allow_html=True)
                    prayer_text = st.text_area("Prayer", value=data.get("prayer_text", ""), height=200,
                                               placeholder="Dear Lord, I come before you today...", label_visibility="collapsed")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("← Back", use_container_width=True):
                            data["prayer_text"] = prayer_text
                            st.session_state["pj_wizard_step"] = 1
                            st.rerun()
                    with col2:
                        if st.button("Skip", use_container_width=True):
                            st.session_state["pj_wizard_step"] = 3
                            st.rerun()
                    with col3:
                        if st.button("Next →", type="primary", use_container_width=True):
                            data["prayer_text"] = prayer_text
                            st.session_state["pj_wizard_step"] = 3
                            st.rerun()

                elif step == 3:
                    st.markdown(f'<div class="wizard-step"><span class="wizard-step-num" style="background:{cat_color};">3</span><span class="wizard-step-title">Bible Scriptures</span><div class="wizard-step-desc">Anchor your prayer in God\'s Word.</div></div>', unsafe_allow_html=True)
                    scriptures_text = st.text_area("Scriptures", value=data.get("scriptures_text", ""), height=120,
                                                   placeholder="Philippians 4:19\nJeremiah 29:11", label_visibility="collapsed")
                    if scriptures_text.strip():
                        parsed = parse_references(scriptures_text)
                        for ref in parsed:
                            enriched = render_reference_with_text(ref)
                            if enriched.get("scripture_text"):
                                st.markdown(f'<div class="scripture-block" style="border-color:{cat_color};"><b style="color:{cat_color};font-size:13px;">{enriched["reference"]}</b><br/><i>{enriched["scripture_text"]}</i></div>', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("← Back", use_container_width=True, key="s3_back"):
                            data["scriptures_text"] = scriptures_text
                            st.session_state["pj_wizard_step"] = 2
                            st.rerun()
                    with col2:
                        if st.button("Skip", use_container_width=True, key="s3_skip"):
                            st.session_state["pj_wizard_step"] = 4
                            st.rerun()
                    with col3:
                        if st.button("Next →", type="primary", use_container_width=True, key="s3_next"):
                            data["scriptures_text"] = scriptures_text
                            st.session_state["pj_wizard_step"] = 4
                            st.rerun()

                elif step == 4:
                    st.markdown(f'<div class="wizard-step"><span class="wizard-step-num" style="background:{cat_color};">4</span><span class="wizard-step-title">Confessions</span><div class="wizard-step-desc">Declare what you believe based on God\'s promises.</div></div>', unsafe_allow_html=True)
                    confessions = st.text_area("Confessions", value=data.get("confessions", ""), height=150,
                                               placeholder="I confess that God is my provider...", label_visibility="collapsed")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("← Back", use_container_width=True, key="s4_back"):
                            data["confessions"] = confessions
                            st.session_state["pj_wizard_step"] = 3
                            st.rerun()
                    with col2:
                        if st.button("Skip", use_container_width=True, key="s4_skip"):
                            st.session_state["pj_wizard_step"] = 5
                            st.rerun()
                    with col3:
                        if st.button("Next →", type="primary", use_container_width=True, key="s4_next"):
                            data["confessions"] = confessions
                            st.session_state["pj_wizard_step"] = 5
                            st.rerun()

                elif step == 5:
                    st.markdown(f'<div class="wizard-step"><span class="wizard-step-num" style="background:{cat_color};">5</span><span class="wizard-step-title">Declarations</span><div class="wizard-step-desc">Speak faith statements over your life.</div></div>', unsafe_allow_html=True)
                    declarations = st.text_area("Declarations", value=data.get("declarations", ""), height=150,
                                                placeholder="I declare that this is my year of abundance...", label_visibility="collapsed")
                    st.divider()
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
                        if st.button("← Back", use_container_width=True, key="s5_back"):
                            data["declarations"] = declarations
                            st.session_state["pj_wizard_step"] = 4
                            st.rerun()
                    with col2:
                        if st.button("\U0001f64f Save Prayer", type="primary", use_container_width=True, key="s5_save"):
                            data["declarations"] = declarations
                            refs_list = []
                            if data.get("scriptures_text", "").strip():
                                parsed = parse_references(data["scriptures_text"])
                                refs_list = [{"reference": r["reference"], "book": r["book"],
                                              "chapter": r["chapter"], "start_verse": r.get("start_verse"),
                                              "end_verse": r.get("end_verse")} for r in parsed]
                            db.create_prayer_entry(
                                category_id=cat_id, title=data.get("title", ""),
                                prayer_text=data.get("prayer_text", ""), scriptures=refs_list,
                                confessions=data.get("confessions", ""), declarations=data.get("declarations", ""))
                            st.session_state["pj_wizard_step"] = 1
                            st.session_state["pj_wizard_data"] = {}
                            st.success("Prayer saved!")
                            st.balloons()
                            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CONFESSION PLANS (Prayer Engine)
# ══════════════════════════════════════════════════════════════════════════════
with tab_confession:
    sub_discover, sub_plan, sub_confess = st.tabs(["Discover", "My Plan", "Confess Aloud"])

    # ── Sub-tab: Discover ────────────────────────────────────────────────────
    with sub_discover:
        cotw = db.get_confession_of_the_week()
        if cotw:
            tpl = cotw.get("confession_templates", {})
            tpl_name = tpl.get('name', '')
            sermon_theme = cotw.get('sermon_theme', '') or ''
            sermon_ref = cotw.get('sermon_reference', '') or ''
            ref_part = (' &mdash; ' + sermon_ref) if sermon_ref else ''
            st.markdown(
                '<div class="cotw-banner">'
                + '<div class="cotw-label">Confession of the Week</div>'
                + f'<div class="cotw-title">{tpl_name}</div>'
                + f'<div class="cotw-theme">{sermon_theme}{ref_part}</div>'
                + '</div>',
                unsafe_allow_html=True)
            if st.button("Add to My Plan", key="cotw_add", type="primary"):
                db.add_to_my_plan(tpl["id"], plan_type="7_days")
                st.success("Confession of the Week added to your plan!")
                st.rerun()
            spacer()

        st.markdown(
            '<div style="text-align:center;padding:10px 0 6px;">'
            '<div style="font-family:\'Cormorant\',serif;font-size:24px;color:#1A1208;">What are you believing God for?</div>'
            '<div style="font-size:14px;color:#5A4A32;margin-top:4px;">Select a need to find the right confessions</div>'
            '</div>',
            unsafe_allow_html=True)

        NEED_CHIPS = [
            ("🏥 Healing", 1, "#2B5A3E"), ("💰 Finances", 2, "#C48A1C"),
            ("✨ Faith & Favor", 3, "#B85A30"), ("🦋 Identity", 4, "#B85A30"),
            ("🌍 Salvation", 5, "#2B5A3E"), ("🌅 Daily", 6, "#C48A1C"),
        ]
        chip_cols = st.columns(len(NEED_CHIPS))
        for i, (label, cat_id_chip, color) in enumerate(NEED_CHIPS):
            with chip_cols[i]:
                if st.button(label, key=f"chip_{cat_id_chip}", use_container_width=True):
                    st.session_state["pe_selected_cat"] = cat_id_chip
        spacer(8)

        conf_categories = db.get_confession_categories()
        tier1_cats = [c for c in conf_categories if c["tier"] == 1]
        tier23_cats = [c for c in conf_categories if c["tier"] > 1]
        selected_cat = st.session_state.get("pe_selected_cat", None)

        if not selected_cat:
            section_label("Core Categories")
            cols = st.columns(3)
            for i, cat in enumerate(tier1_cats):
                with cols[i % 3]:
                    templates = db.get_confession_templates(category_id=cat["id"])
                    tcount = len(templates)
                    st.markdown(
                        '<div class="cat-grid-card">'
                        + f'<div class="cat-grid-icon">{cat["icon"]}</div>'
                        + f'<div class="cat-grid-name">{cat["name"]}</div>'
                        + f'<div class="cat-grid-count">{tcount} confession{"s" if tcount != 1 else ""}</div>'
                        + '</div>', unsafe_allow_html=True)
                    if st.button("Browse", key=f"browse_{cat['id']}", use_container_width=True):
                        st.session_state["pe_selected_cat"] = cat["id"]
                        st.rerun()
            if tier23_cats:
                spacer()
                with st.expander("Explore More Categories"):
                    cols2 = st.columns(3)
                    for i, cat in enumerate(tier23_cats):
                        with cols2[i % 3]:
                            templates = db.get_confession_templates(category_id=cat["id"])
                            tcount = len(templates)
                            st.markdown(
                                '<div class="cat-grid-card">'
                                + f'<div class="cat-grid-icon">{cat["icon"]}</div>'
                                + f'<div class="cat-grid-name">{cat["name"]}</div>'
                                + f'<div class="cat-grid-count">{tcount} confession{"s" if tcount != 1 else ""}</div>'
                                + '</div>', unsafe_allow_html=True)
                            if st.button("Browse", key=f"browse2_{cat['id']}", use_container_width=True):
                                st.session_state["pe_selected_cat"] = cat["id"]
                                st.rerun()
        else:
            sel_cat = next((c for c in conf_categories if c["id"] == selected_cat), None)
            if sel_cat:
                col_back, col_title = st.columns([1, 5])
                with col_back:
                    if st.button("< Back", key="back_to_cats"):
                        del st.session_state["pe_selected_cat"]
                        st.rerun()
                with col_title:
                    st.markdown(f"### {sel_cat['icon']} {sel_cat['name']}")
                if sel_cat.get("id") == 13 or sel_cat.get("name", "").startswith("Spiritual Warfare"):
                    st.markdown('<div class="maturity-warning"><strong>A note from your Bishop:</strong> These are powerful declarations of authority in Christ. We recommend engaging with these under pastoral guidance.</div>', unsafe_allow_html=True)
                templates = db.get_confession_templates(category_id=selected_cat)
                if not templates:
                    empty_state("📖", "Coming Soon", "Confessions for this category are being prepared.")
                else:
                    for tpl in templates:
                        if tpl.get("sort_order", 0) >= 100:
                            continue
                        st.markdown(
                            '<div class="template-card">'
                            + f'<div class="template-name">{tpl["name"]}</div>'
                            + f'<div class="template-desc">{tpl.get("description", "")}</div>'
                            + f'<div class="template-shortform">{tpl.get("short_form_text", "")}</div>'
                            + '</div>', unsafe_allow_html=True)
                        col1, col2, col3 = st.columns([2, 2, 2])
                        with col1:
                            with st.expander("Read Full Confession"):
                                confessions = tpl.get("confessions", [])
                                if isinstance(confessions, str):
                                    confessions = json.loads(confessions)
                                for c in confessions:
                                    st.markdown(f"**{c['text']}**")
                                    if c.get("scripture_ref"):
                                        st.caption(f"*{c['scripture_ref']}*")
                                declarations = tpl.get("declarations", [])
                                if isinstance(declarations, str):
                                    declarations = json.loads(declarations)
                                if declarations:
                                    st.markdown("---")
                                    st.markdown("**Declarations:**")
                                    for d in declarations:
                                        st.markdown(f"**{d['text']}**")
                                        if d.get("scripture_ref"):
                                            st.caption(f"*{d['scripture_ref']}*")
                                prayers = tpl.get("prayers", [])
                                if isinstance(prayers, str):
                                    prayers = json.loads(prayers)
                                if prayers:
                                    st.markdown("---")
                                    st.markdown("**Prayer:**")
                                    for p in prayers:
                                        st.markdown(f"*{p['text']}*")
                        with col2:
                            duration = st.selectbox(
                                "Duration", ["ongoing", "7_days", "21_days"],
                                format_func=lambda x: {"ongoing": "Ongoing", "7_days": "7 Days", "21_days": "21 Days"}[x],
                                key=f"dur_{tpl['id']}")
                        with col3:
                            if st.button("Add to My Plan", key=f"add_{tpl['id']}", type="primary", use_container_width=True):
                                db.add_to_my_plan(tpl["id"], plan_type=duration)
                                st.success(f"Added '{tpl['name']}' to your plan!")
                                st.rerun()
                        spacer(8)

    # ── Sub-tab: My Plan ─────────────────────────────────────────────────────
    with sub_plan:
        plans = db.get_my_confession_plans(status="active")
        today_completions = db.get_today_completions()
        completed_plan_ids = {c["plan_id"] for c in today_completions}
        if not plans:
            empty_state("📋", "No Active Confessions", "Visit the Discover tab to find confessions for your situation.")
        else:
            assigned = [p for p in plans if p.get("assigned_by")]
            self_selected = [p for p in plans if not p.get("assigned_by")]
            if assigned:
                section_label("Prescribed by Pastor")
                for plan in assigned:
                    _render_plan_card(plan, completed_plan_ids)
            if self_selected:
                section_label("My Confessions")
                for plan in self_selected:
                    _render_plan_card(plan, completed_plan_ids)

    # ── Sub-tab: Confess Aloud ───────────────────────────────────────────────
    with sub_confess:
        plans = db.get_my_confession_plans(status="active")
        today_completions = db.get_today_completions()
        completed_plan_ids = {c["plan_id"] for c in today_completions}
        pending_plans = [p for p in plans if p["id"] not in completed_plan_ids]

        if not pending_plans:
            if plans:
                st.markdown(
                    '<div style="text-align:center;padding:40px 20px;">'
                    '<div style="font-size:48px;">&#x1F389;</div>'
                    '<div style="font-family:\'Cormorant\',serif;font-size:22px;color:#1A1208;margin:12px 0;">All confessions complete for today!</div>'
                    '<div style="font-size:14px;color:#5A4A32;">Great job speaking God\'s Word over your life today.</div>'
                    '</div>',
                    unsafe_allow_html=True)
            else:
                empty_state("🎤", "No Confessions to Speak", "Add confessions from the Discover tab to start your daily confession practice.")
        else:
            if "pe_confess_plan" not in st.session_state:
                st.session_state["pe_confess_plan"] = pending_plans[0]["id"]
            plan_names = {p["id"]: p.get("confession_templates", {}).get("name", "Confession") for p in pending_plans}
            selected_plan_id = st.selectbox(
                "Choose confession to speak:",
                options=[p["id"] for p in pending_plans],
                format_func=lambda pid: plan_names.get(pid, "Confession"),
                key="pe_confess_select")
            current_plan = next((p for p in pending_plans if p["id"] == selected_plan_id), None)
            if current_plan:
                tpl = current_plan.get("confession_templates", {})
                tpl_name = tpl.get('name', '')
                st.markdown(
                    '<div style="text-align:center;padding:10px 0;">'
                    '<div style="font-size:12px;color:#A09080;text-transform:uppercase;letter-spacing:1.5px;">Confess Aloud</div>'
                    f'<div style="font-family:\'Cormorant\',serif;font-size:20px;color:#1A1208;margin:6px 0;">{tpl_name}</div>'
                    '</div>',
                    unsafe_allow_html=True)
                all_lines = []
                for field, label in [("confessions", "confession"), ("declarations", "declaration"), ("prayers", "prayer")]:
                    items = tpl.get(field, [])
                    if isinstance(items, str):
                        items = json.loads(items)
                    for item in items:
                        all_lines.append((label, item))
                if all_lines:
                    line_key = f"confess_line_{selected_plan_id}"
                    if line_key not in st.session_state:
                        st.session_state[line_key] = 0
                    idx = st.session_state[line_key]
                    total = len(all_lines)
                    line_type, line_data = all_lines[min(idx, total - 1)]
                    st.progress((idx + 1) / total)
                    st.caption(f"Line {idx + 1} of {total}")
                    text = line_data.get("text", "")
                    ref = line_data.get("scripture_ref", "")
                    type_label = {"confession": "Confess", "declaration": "Declare", "prayer": "Pray"}.get(line_type, "")
                    type_color = {"confession": "#2B5A3E", "declaration": "#C48A1C", "prayer": "#B85A30"}.get(line_type, "#B85A30")
                    st.markdown(
                        f'<div style="text-align:center;padding:8px 0;"><span style="background:{type_color}20;color:{type_color};padding:3px 12px;border-radius:12px;font-size:11px;font-weight:600;text-transform:uppercase;">{type_label}</span></div>'
                        f'<div class="confess-line">{text}</div>',
                        unsafe_allow_html=True)
                    if ref:
                        st.markdown(f'<div class="confess-scripture">&mdash; {ref}</div>', unsafe_allow_html=True)
                    spacer()
                    nav_cols = st.columns([1, 1, 1])
                    with nav_cols[0]:
                        if idx > 0:
                            if st.button("< Previous", key="confess_prev", use_container_width=True):
                                st.session_state[line_key] = idx - 1
                                st.rerun()
                    with nav_cols[2]:
                        if idx < total - 1:
                            if st.button("Next >", key="confess_next", type="primary", use_container_width=True):
                                st.session_state[line_key] = idx + 1
                                st.rerun()
                    if idx >= total - 1:
                        spacer()
                        st.markdown("---")
                        reflection = st.text_area("What spoke to you today? (optional)",
                                                  placeholder="Share your thoughts privately...",
                                                  key=f"reflect_{selected_plan_id}")
                        if st.button("Mark as Confessed Today", key="mark_done", type="primary", use_container_width=True):
                            db.mark_confession_complete(selected_plan_id, reflection_note=reflection if reflection else None)
                            st.session_state[line_key] = 0
                            st.success("Confession complete! Well done.")
                            st.balloons()
                            st.rerun()
