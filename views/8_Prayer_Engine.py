import streamlit as st
import json
from datetime import date, timedelta
from modules import db
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_login, require_password_changed

require_login()
require_password_changed()
inject_styles()


# ==================== HELPER: Render Plan Card ====================
def _render_plan_card(plan, completed_plan_ids):
    tpl = plan.get("confession_templates", {})
    cat = tpl.get("confession_categories", {}) if tpl else {}
    is_done_today = plan["id"] in completed_plan_ids

    # Calculate progress for timed plans
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

    # Badge
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

    # Action buttons
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


# ==================== CUSTOM CSS ====================
st.markdown(
    '<style>'
    '.need-chip {'
    '    display: inline-block;'
    '    padding: 10px 20px;'
    '    border-radius: 24px;'
    '    font-family: "Jost", sans-serif;'
    '    font-size: 14px;'
    '    font-weight: 600;'
    '    cursor: pointer;'
    '    margin: 4px;'
    '    transition: all 0.2s;'
    '}'
    '.need-chip:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(26,18,8,0.10); }'
    '.cotw-banner {'
    '    background: linear-gradient(135deg, #B85A30 0%, #C48A1C 100%);'
    '    color: white;'
    '    border-radius: 16px;'
    '    padding: 20px 24px;'
    '    margin-bottom: 16px;'
    '}'
    '.cotw-banner .cotw-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8; }'
    '.cotw-banner .cotw-title { font-family: "Cormorant", serif; font-size: 22px; margin: 6px 0; }'
    '.cotw-banner .cotw-theme { font-size: 13px; opacity: 0.85; }'
    '.cat-grid-card {'
    '    background: #FFFFFF;'
    '    border: 1px solid rgba(26,18,8,0.09);'
    '    border-radius: 14px;'
    '    padding: 18px;'
    '    text-align: center;'
    '    transition: all 0.2s;'
    '    min-height: 140px;'
    '}'
    '.cat-grid-card:hover { border-color: #B85A30; box-shadow: 0 4px 16px rgba(184,90,48,0.10); }'
    '.cat-grid-icon { font-size: 32px; margin-bottom: 8px; }'
    '.cat-grid-name { font-family: "Cormorant", serif; font-size: 15px; color: #1A1208; margin-bottom: 4px; }'
    '.cat-grid-count { font-size: 12px; color: #A09080; }'
    '.template-card {'
    '    background: #FFFFFF;'
    '    border: 1px solid rgba(26,18,8,0.09);'
    '    border-radius: 14px;'
    '    padding: 20px;'
    '    margin-bottom: 12px;'
    '}'
    '.template-name { font-family: "Cormorant", serif; font-size: 18px; color: #1A1208; }'
    '.template-desc { font-size: 13px; color: #5A4A32; margin: 6px 0 12px; }'
    '.template-shortform {'
    '    background: #FFF9F0;'
    '    border-left: 3px solid #C48A1C;'
    '    padding: 12px 16px;'
    '    border-radius: 0 8px 8px 0;'
    '    font-size: 14px;'
    '    line-height: 1.8;'
    '    color: #1A1208;'
    '    white-space: pre-line;'
    '}'
    '.plan-card {'
    '    background: #FFFFFF;'
    '    border: 1px solid rgba(26,18,8,0.09);'
    '    border-radius: 14px;'
    '    padding: 18px;'
    '    margin-bottom: 12px;'
    '}'
    '.plan-card .plan-title { font-family: "Cormorant", serif; font-size: 16px; color: #1A1208; }'
    '.plan-card .plan-badge {'
    '    display: inline-block;'
    '    padding: 2px 10px;'
    '    border-radius: 12px;'
    '    font-size: 11px;'
    '    font-weight: 600;'
    '}'
    '.plan-progress-bar {'
    '    height: 6px;'
    '    background: rgba(26,18,8,0.06);'
    '    border-radius: 3px;'
    '    margin-top: 10px;'
    '    overflow: hidden;'
    '}'
    '.plan-progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }'
    '.confess-line {'
    '    font-family: "Cormorant", serif;'
    '    font-size: 22px;'
    '    color: #1A1208;'
    '    line-height: 1.6;'
    '    text-align: center;'
    '    padding: 30px 20px;'
    '}'
    '.confess-scripture {'
    '    font-family: "Jost", sans-serif;'
    '    font-size: 14px;'
    '    color: #B85A30;'
    '    text-align: center;'
    '    margin-top: 8px;'
    '}'
    '.maturity-warning {'
    '    background: #FDF0E8;'
    '    border: 1px solid #C48A1C;'
    '    border-radius: 12px;'
    '    padding: 16px;'
    '    margin-bottom: 16px;'
    '    font-size: 14px;'
    '    color: #5A4A32;'
    '}'
    '</style>',
    unsafe_allow_html=True
)


# ==================== HEADER ====================
page_header("✝️", "Confession Plans", "Confessions, declarations & faith-building plans")

# ==================== TABS ====================
tab_discover, tab_plan, tab_confess = st.tabs(["Discover", "My Plan", "Confess"])


# ==================== TAB 1: DISCOVER ====================
with tab_discover:

    # --- Confession of the Week Banner ---
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
            unsafe_allow_html=True
        )
        if st.button("Add to My Plan", key="cotw_add", type="primary"):
            db.add_to_my_plan(tpl["id"], plan_type="7_days")
            st.success("Confession of the Week added to your plan!")
            st.rerun()
        spacer()

    # --- "What are you believing God for?" ---
    st.markdown(
        '<div style="text-align:center; padding: 10px 0 6px;">'
        '<div style="font-family:\'Cormorant\',serif; font-size:24px; color:#1A1208;">'
        'What are you believing God for?'
        '</div>'
        '<div style="font-size:14px; color:#5A4A32; margin-top:4px;">'
        'Select a need to find the right confessions'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Need chips mapped to categories
    NEED_CHIPS = [
        ("🏥 Healing", 1, "#2B5A3E"),
        ("💰 Finances", 2, "#C48A1C"),
        ("✨ Faith & Favor", 3, "#B85A30"),
        ("🦋 Identity", 4, "#B85A30"),
        ("🌍 Salvation", 5, "#2B5A3E"),
        ("🌅 Daily", 6, "#C48A1C"),
    ]

    chip_cols = st.columns(len(NEED_CHIPS))
    for i, (label, cat_id, color) in enumerate(NEED_CHIPS):
        with chip_cols[i]:
            if st.button(label, key=f"chip_{cat_id}", use_container_width=True):
                st.session_state["pe_selected_cat"] = cat_id

    spacer(8)

    # --- Category Grid (progressive disclosure) ---
    categories = db.get_confession_categories()
    tier1_cats = [c for c in categories if c["tier"] == 1]
    tier23_cats = [c for c in categories if c["tier"] > 1]

    selected_cat = st.session_state.get("pe_selected_cat", None)

    if not selected_cat:
        # Show Tier 1 category grid
        section_label("Core Categories")
        cols = st.columns(3)
        for i, cat in enumerate(tier1_cats):
            with cols[i % 3]:
                templates = db.get_confession_templates(category_id=cat["id"])
                tcount = len(templates)
                tplural = "s" if tcount != 1 else ""
                st.markdown(
                    '<div class="cat-grid-card">'
                    + f'<div class="cat-grid-icon">{cat["icon"]}</div>'
                    + f'<div class="cat-grid-name">{cat["name"]}</div>'
                    + f'<div class="cat-grid-count">{tcount} confession{tplural}</div>'
                    + '</div>',
                    unsafe_allow_html=True
                )
                if st.button("Browse", key=f"browse_{cat['id']}", use_container_width=True):
                    st.session_state["pe_selected_cat"] = cat["id"]
                    st.rerun()

        # Explore More
        if tier23_cats:
            spacer()
            with st.expander("Explore More Categories"):
                cols2 = st.columns(3)
                for i, cat in enumerate(tier23_cats):
                    with cols2[i % 3]:
                        templates = db.get_confession_templates(category_id=cat["id"])
                        tcount = len(templates)
                        tplural = "s" if tcount != 1 else ""
                        st.markdown(
                            '<div class="cat-grid-card">'
                            + f'<div class="cat-grid-icon">{cat["icon"]}</div>'
                            + f'<div class="cat-grid-name">{cat["name"]}</div>'
                            + f'<div class="cat-grid-count">{tcount} confession{tplural}</div>'
                            + '</div>',
                            unsafe_allow_html=True
                        )
                        if st.button("Browse", key=f"browse2_{cat['id']}", use_container_width=True):
                            st.session_state["pe_selected_cat"] = cat["id"]
                            st.rerun()

    else:
        # Show templates in selected category
        sel_cat = next((c for c in categories if c["id"] == selected_cat), None)
        if sel_cat:
            col_back, col_title = st.columns([1, 5])
            with col_back:
                if st.button("< Back", key="back_to_cats"):
                    del st.session_state["pe_selected_cat"]
                    st.rerun()
            with col_title:
                st.markdown(f"### {sel_cat['icon']} {sel_cat['name']}")

            # Maturity warning for Spiritual Warfare (id=13)
            if sel_cat.get("id") == 13 or sel_cat.get("name", "").startswith("Spiritual Warfare"):
                st.markdown(
                    '<div class="maturity-warning">'
                    '<strong>A note from your Bishop:</strong> These are powerful declarations of authority in Christ. '
                    'We recommend engaging with these under pastoral guidance, especially if you are new in your faith walk.'
                    '</div>',
                    unsafe_allow_html=True
                )

            templates = db.get_confession_templates(category_id=selected_cat)
            if not templates:
                empty_state("📖", "Coming Soon", "Confessions for this category are being prepared.")
            else:
                for tpl in templates:
                    # Skip new believer track templates from library browse
                    if tpl.get("sort_order", 0) >= 100:
                        continue

                    tpl_desc = tpl.get('description', '')
                    tpl_short = tpl.get('short_form_text', '')
                    st.markdown(
                        '<div class="template-card">'
                        + f'<div class="template-name">{tpl["name"]}</div>'
                        + f'<div class="template-desc">{tpl_desc}</div>'
                        + f'<div class="template-shortform">{tpl_short}</div>'
                        + '</div>',
                        unsafe_allow_html=True
                    )

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
                            key=f"dur_{tpl['id']}"
                        )
                    with col3:
                        if st.button("Add to My Plan", key=f"add_{tpl['id']}", type="primary", use_container_width=True):
                            db.add_to_my_plan(tpl["id"], plan_type=duration)
                            st.success(f"Added '{tpl['name']}' to your plan!")
                            st.rerun()
                    spacer(8)


# ==================== TAB 2: MY PLAN ====================
with tab_plan:
    plans = db.get_my_confession_plans(status="active")
    today_completions = db.get_today_completions()
    completed_plan_ids = {c["plan_id"] for c in today_completions}

    if not plans:
        empty_state("📋", "No Active Confessions",
                    "Visit the Discover tab to find confessions for your situation.")
    else:
        # Separate pastor-assigned from self-selected
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


# ==================== TAB 3: CONFESS ALOUD ====================
with tab_confess:
    plans = db.get_my_confession_plans(status="active")
    today_completions = db.get_today_completions()
    completed_plan_ids = {c["plan_id"] for c in today_completions}

    # Filter to plans not yet completed today
    pending_plans = [p for p in plans if p["id"] not in completed_plan_ids]

    if not pending_plans:
        if plans:
            st.markdown(
                '<div style="text-align:center; padding:40px 20px;">'
                '<div style="font-size:48px;">&#x1F389;</div>'
                '<div style="font-family:\'Cormorant\',serif; font-size:22px; color:#1A1208; margin:12px 0;">'
                'All confessions complete for today!'
                '</div>'
                '<div style="font-size:14px; color:#5A4A32;">'
                'Great job speaking God\'s Word over your life today.'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            empty_state("🎤", "No Confessions to Speak",
                        "Add confessions from the Discover tab to start your daily confession practice.")
    else:
        # Select which plan to confess
        if "pe_confess_plan" not in st.session_state:
            st.session_state["pe_confess_plan"] = pending_plans[0]["id"]

        plan_names = {p["id"]: p.get("confession_templates", {}).get("name", "Confession") for p in pending_plans}
        selected_plan_id = st.selectbox(
            "Choose confession to speak:",
            options=[p["id"] for p in pending_plans],
            format_func=lambda pid: plan_names.get(pid, "Confession"),
            key="pe_confess_select"
        )

        current_plan = next((p for p in pending_plans if p["id"] == selected_plan_id), None)
        if current_plan:
            tpl = current_plan.get("confession_templates", {})
            tpl_name = tpl.get('name', '')
            st.markdown(
                '<div style="text-align:center; padding:10px 0;">'
                '<div style="font-size:12px; color:#A09080; text-transform:uppercase; letter-spacing:1.5px;">'
                'Confess Aloud'
                '</div>'
                f'<div style="font-family:\'Cormorant\',serif; font-size:20px; color:#1A1208; margin:6px 0;">{tpl_name}</div>'
                '</div>',
                unsafe_allow_html=True
            )

            # Gather all lines
            all_lines = []
            confessions = tpl.get("confessions", [])
            if isinstance(confessions, str):
                confessions = json.loads(confessions)
            for c in confessions:
                all_lines.append(("confession", c))

            declarations = tpl.get("declarations", [])
            if isinstance(declarations, str):
                declarations = json.loads(declarations)
            for d in declarations:
                all_lines.append(("declaration", d))

            prayers = tpl.get("prayers", [])
            if isinstance(prayers, str):
                prayers = json.loads(prayers)
            for p in prayers:
                all_lines.append(("prayer", p))

            if all_lines:
                # Line-by-line navigation
                line_key = f"confess_line_{selected_plan_id}"
                if line_key not in st.session_state:
                    st.session_state[line_key] = 0

                idx = st.session_state[line_key]
                total = len(all_lines)
                line_type, line_data = all_lines[min(idx, total - 1)]

                # Progress indicator
                st.progress((idx + 1) / total)
                st.caption(f"Line {idx + 1} of {total}")

                # Display the line
                text = line_data.get("text", "")
                ref = line_data.get("scripture_ref", "")

                type_label = {"confession": "Confess", "declaration": "Declare", "prayer": "Pray"}.get(line_type, "")
                type_color = {"confession": "#2B5A3E", "declaration": "#C48A1C", "prayer": "#B85A30"}.get(line_type, "#B85A30")

                st.markdown(
                    '<div style="text-align:center; padding:8px 0;">'
                    f'<span style="background:{type_color}20; color:{type_color}; padding:3px 12px; border-radius:12px;'
                    ' font-size:11px; font-weight:600; text-transform:uppercase;">'
                    f'{type_label}'
                    '</span>'
                    '</div>'
                    f'<div class="confess-line">{text}</div>',
                    unsafe_allow_html=True
                )
                if ref:
                    st.markdown(f'<div class="confess-scripture">&mdash; {ref}</div>', unsafe_allow_html=True)

                spacer()

                # Navigation
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

                # Mark complete (only on last line)
                if idx >= total - 1:
                    spacer()
                    st.markdown("---")
                    reflection = st.text_area(
                        "What spoke to you today? (optional)",
                        placeholder="Share your thoughts privately...",
                        key=f"reflect_{selected_plan_id}"
                    )
                    if st.button("Mark as Confessed Today", key="mark_done", type="primary", use_container_width=True):
                        db.mark_confession_complete(
                            selected_plan_id,
                            reflection_note=reflection if reflection else None
                        )
                        # Reset line counter
                        st.session_state[line_key] = 0
                        st.success("Confession complete! Well done.")
                        st.balloons()
                        st.rerun()
