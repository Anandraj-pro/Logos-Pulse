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
        badge_html = '<span class="plan-badge" style="background:#EDEBFA; color:#5B4FC4;">Prescribed by Pastor</span>'
    if plan.get("is_new_believer_track"):
        badge_html = '<span class="plan-badge" style="background:#E3F2FD; color:#1565C0;">New Believer Track</span>'
    if is_done_today:
        badge_html += ' <span class="plan-badge" style="background:#E8F5E9; color:#3A8F5C;">Done Today</span>'

    status_icon = "&#9989;" if is_done_today else "&#9203;"

    st.markdown(f"""
    <div class="plan-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:20px;">{status_icon}</span>
                <span class="plan-title">{tpl.get('name', 'Confession')}</span>
            </div>
            <div>{badge_html}</div>
        </div>
        <div style="font-size:13px; color:#6B6580; margin-top:6px;">
            {cat.get('icon', '')} {cat.get('name', '')} &middot; {progress_text}
        </div>
        {f'<div style="font-size:12px; color:#9E96AB; margin-top:4px; font-style:italic;">Note: {plan.get("assignment_note", "")}</div>' if plan.get("assignment_note") else ''}
        <div class="plan-progress-bar">
            <div class="plan-progress-fill" style="width:{progress_pct*100:.0f}%; background:{cat.get('color', '#5B4FC4')};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
st.markdown("""
<style>
.need-chip {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 24px;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    margin: 4px;
    transition: all 0.2s;
}
.need-chip:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }

.cotw-banner {
    background: linear-gradient(135deg, #5B4FC4 0%, #7B6FD4 100%);
    color: white;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.cotw-banner .cotw-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.8; }
.cotw-banner .cotw-title { font-family: 'DM Serif Display', serif; font-size: 22px; margin: 6px 0; }
.cotw-banner .cotw-theme { font-size: 13px; opacity: 0.85; }

.cat-grid-card {
    background: white;
    border: 1px solid #EDE8F5;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    transition: all 0.2s;
    min-height: 140px;
}
.cat-grid-card:hover { border-color: #5B4FC4; box-shadow: 0 4px 16px rgba(91,79,196,0.1); }
.cat-grid-icon { font-size: 32px; margin-bottom: 8px; }
.cat-grid-name { font-family: 'DM Serif Display', serif; font-size: 15px; color: #2A2438; margin-bottom: 4px; }
.cat-grid-count { font-size: 12px; color: #9E96AB; }

.template-card {
    background: white;
    border: 1px solid #EDE8F5;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}
.template-name { font-family: 'DM Serif Display', serif; font-size: 18px; color: #2A2438; }
.template-desc { font-size: 13px; color: #6B6580; margin: 6px 0 12px; }
.template-shortform {
    background: #FFF9F0;
    border-left: 3px solid #D4A843;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    font-size: 14px;
    line-height: 1.8;
    color: #2A2438;
    white-space: pre-line;
}

.plan-card {
    background: white;
    border: 1px solid #EDE8F5;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
.plan-card .plan-title { font-family: 'DM Serif Display', serif; font-size: 16px; color: #2A2438; }
.plan-card .plan-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}
.plan-progress-bar {
    height: 6px;
    background: #EDE8F5;
    border-radius: 3px;
    margin-top: 10px;
    overflow: hidden;
}
.plan-progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }

.confess-line {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #2A2438;
    line-height: 1.6;
    text-align: center;
    padding: 30px 20px;
}
.confess-scripture {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    color: #5B4FC4;
    text-align: center;
    margin-top: 8px;
}

.maturity-warning {
    background: #FFF3E0;
    border: 1px solid #D4853A;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    font-size: 14px;
    color: #6B6580;
}
</style>
""", unsafe_allow_html=True)


# ==================== HEADER ====================
page_header("✝️", "Prayer Engine", "Confessions, declarations & faith-building plans")

# ==================== TABS ====================
tab_discover, tab_plan, tab_confess = st.tabs(["Discover", "My Plan", "Confess"])


# ==================== TAB 1: DISCOVER ====================
with tab_discover:

    # --- Confession of the Week Banner ---
    cotw = db.get_confession_of_the_week()
    if cotw:
        tpl = cotw.get("confession_templates", {})
        st.markdown(f"""
        <div class="cotw-banner">
            <div class="cotw-label">Confession of the Week</div>
            <div class="cotw-title">{tpl.get('name', '')}</div>
            <div class="cotw-theme">{cotw.get('sermon_theme', '') or ''} {('— ' + cotw.get('sermon_reference', '')) if cotw.get('sermon_reference') else ''}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Add to My Plan", key="cotw_add", type="primary"):
            db.add_to_my_plan(tpl["id"], plan_type="7_days")
            st.success("Confession of the Week added to your plan!")
            st.rerun()
        spacer()

    # --- "What are you believing God for?" ---
    st.markdown("""
    <div style="text-align:center; padding: 10px 0 6px;">
        <div style="font-family:'DM Serif Display',serif; font-size:24px; color:#2A2438;">
            What are you believing God for?
        </div>
        <div style="font-size:14px; color:#6B6580; margin-top:4px;">
            Select a need to find the right confessions
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Need chips mapped to categories
    NEED_CHIPS = [
        ("🏥 Healing", 1, "#3A8F5C"),
        ("💰 Finances", 2, "#D4853A"),
        ("✨ Faith & Favor", 3, "#5B4FC4"),
        ("🦋 Identity", 4, "#C44B5B"),
        ("🌍 Salvation", 5, "#2E7D32"),
        ("🌅 Daily", 6, "#FF8F00"),
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
                st.markdown(f"""
                <div class="cat-grid-card">
                    <div class="cat-grid-icon">{cat['icon']}</div>
                    <div class="cat-grid-name">{cat['name']}</div>
                    <div class="cat-grid-count">{len(templates)} confession{"s" if len(templates) != 1 else ""}</div>
                </div>
                """, unsafe_allow_html=True)
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
                        st.markdown(f"""
                        <div class="cat-grid-card">
                            <div class="cat-grid-icon">{cat['icon']}</div>
                            <div class="cat-grid-name">{cat['name']}</div>
                            <div class="cat-grid-count">{len(templates)} confession{"s" if len(templates) != 1 else ""}</div>
                        </div>
                        """, unsafe_allow_html=True)
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
                st.markdown("""
                <div class="maturity-warning">
                    <strong>A note from your Bishop:</strong> These are powerful declarations of authority in Christ.
                    We recommend engaging with these under pastoral guidance, especially if you are new in your faith walk.
                </div>
                """, unsafe_allow_html=True)

            templates = db.get_confession_templates(category_id=selected_cat)
            if not templates:
                empty_state("📖", "Coming Soon", "Confessions for this category are being prepared.")
            else:
                for tpl in templates:
                    # Skip new believer track templates from library browse
                    if tpl.get("sort_order", 0) >= 100:
                        continue

                    st.markdown(f"""
                    <div class="template-card">
                        <div class="template-name">{tpl['name']}</div>
                        <div class="template-desc">{tpl.get('description', '')}</div>
                        <div class="template-shortform">{tpl.get('short_form_text', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

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
            st.markdown("""
            <div style="text-align:center; padding:40px 20px;">
                <div style="font-size:48px;">🎉</div>
                <div style="font-family:'DM Serif Display',serif; font-size:22px; color:#2A2438; margin:12px 0;">
                    All confessions complete for today!
                </div>
                <div style="font-size:14px; color:#6B6580;">
                    Great job speaking God's Word over your life today.
                </div>
            </div>
            """, unsafe_allow_html=True)
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
            st.markdown(f"""
            <div style="text-align:center; padding:10px 0;">
                <div style="font-size:12px; color:#9E96AB; text-transform:uppercase; letter-spacing:1.5px;">
                    Confess Aloud
                </div>
                <div style="font-family:'DM Serif Display',serif; font-size:20px; color:#2A2438; margin:6px 0;">
                    {tpl.get('name', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

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
                type_color = {"confession": "#3A8F5C", "declaration": "#D4853A", "prayer": "#5B4FC4"}.get(line_type, "#5B4FC4")

                st.markdown(f"""
                <div style="text-align:center; padding:8px 0;">
                    <span style="background:{type_color}15; color:{type_color}; padding:3px 12px; border-radius:12px;
                                 font-size:11px; font-weight:600; text-transform:uppercase;">
                        {type_label}
                    </span>
                </div>
                <div class="confess-line">{text}</div>
                """, unsafe_allow_html=True)
                if ref:
                    st.markdown(f'<div class="confess-scripture">— {ref}</div>', unsafe_allow_html=True)

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

