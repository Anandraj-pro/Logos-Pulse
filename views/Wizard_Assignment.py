import streamlit as st
from datetime import date, timedelta
from modules.styles import inject_styles, page_header, section_label, empty_state, spacer
from modules.auth import require_role, get_current_user_id, get_current_role
from modules.rbac import get_members_for_pastor
from modules import db

require_role(["admin", "bishop", "pastor"])

inject_styles()

role = get_current_role()
my_id = get_current_user_id()

page_header("\U0001f9d9", "Custom Assignment Wizard", "Create composite spiritual growth assignments")

tab_create, tab_my_assignments = st.tabs(["\u2795 Create New", "\U0001f4cb My Assignments"])

# ==================== CREATE TAB ====================
with tab_create:
    if "wiz_step" not in st.session_state:
        st.session_state["wiz_step"] = 1
    if "wiz_data" not in st.session_state:
        st.session_state["wiz_data"] = {}

    step = st.session_state["wiz_step"]
    data = st.session_state["wiz_data"]

    # Progress indicator
    steps = ["Basics", "Components", "Configure", "Review"]
    progress_html = ""
    for i, s_name in enumerate(steps):
        s_num = i + 1
        if s_num < step:
            dot_style = "background:#5B4FC4; color:white;"
            label_style = "color:#5B4FC4; font-weight:600;"
        elif s_num == step:
            dot_style = "background:#5B4FC4; color:white; box-shadow:0 0 0 4px rgba(91,79,196,0.2);"
            label_style = "color:#5B4FC4; font-weight:700;"
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
    st.markdown(f'<div style="display:flex; justify-content:space-between; margin:8px 0 24px 0;">{progress_html}</div>', unsafe_allow_html=True)

    # --- Step 1: Basics ---
    if step == 1:
        section_label("Assignment Details")

        title = st.text_input("Title", value=data.get("title", ""),
                              placeholder="e.g., Week of Spiritual Warfare")
        description = st.text_area("Description (optional)", value=data.get("description", ""),
                                   height=80, placeholder="What is this assignment about?")

        col1, col2 = st.columns(2)
        with col1:
            start_dt = st.date_input("Start Date", value=date.today())
        with col2:
            end_dt = st.date_input("End Date", value=date.today() + timedelta(days=6))

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Next \u2192", type="primary", use_container_width=True):
                if not title.strip():
                    st.error("Please enter a title.")
                elif end_dt <= start_dt:
                    st.error("End date must be after start date.")
                else:
                    data["title"] = title.strip()
                    data["description"] = description.strip()
                    data["start_date"] = start_dt.isoformat()
                    data["end_date"] = end_dt.isoformat()
                    st.session_state["wiz_step"] = 2
                    st.rerun()

    # --- Step 2: Select Components ---
    elif step == 2:
        section_label("Select Components")
        st.caption("Choose what to include in this assignment.")

        comp_prayer = st.checkbox("\U0001f64f Prayer Template", value=data.get("comp_prayer", False))
        comp_bible = st.checkbox("\U0001f4d6 Bible Reading", value=data.get("comp_bible", False))
        comp_sermon = st.checkbox("\U0001f3a7 Sermon Series", value=data.get("comp_sermon", False))
        comp_time = st.checkbox("\u23f0 Prayer Time Commitment", value=data.get("comp_time", False))

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("\u2190 Back", use_container_width=True):
                st.session_state["wiz_step"] = 1
                st.rerun()
        with col3:
            if st.button("Next \u2192", type="primary", use_container_width=True):
                if not any([comp_prayer, comp_bible, comp_sermon, comp_time]):
                    st.error("Select at least one component.")
                else:
                    data["comp_prayer"] = comp_prayer
                    data["comp_bible"] = comp_bible
                    data["comp_sermon"] = comp_sermon
                    data["comp_time"] = comp_time
                    st.session_state["wiz_step"] = 3
                    st.rerun()

    # --- Step 3: Configure Components ---
    elif step == 3:
        section_label("Configure Components")

        components = []

        if data.get("comp_prayer"):
            st.markdown("**\U0001f64f Prayer Template**")
            templates = db.get_prayer_templates()
            if templates:
                tpl_options = {t["name"]: t["id"] for t in templates}
                selected_tpls = st.multiselect("Select templates", options=list(tpl_options.keys()),
                                               default=data.get("selected_templates", []))
                data["selected_templates"] = selected_tpls
                components.append({
                    "type": "prayer_template",
                    "config": {"template_ids": [tpl_options[t] for t in selected_tpls]},
                })
            else:
                st.info("No prayer templates available.")
            spacer(8)

        if data.get("comp_bible"):
            st.markdown("**\U0001f4d6 Bible Reading**")
            from modules.bible_data import get_book_names, get_chapter_count
            bible_book = st.selectbox("Book", options=get_book_names(), key="wiz_bible_book")
            max_ch = get_chapter_count(bible_book)
            col1, col2 = st.columns(2)
            with col1:
                bible_start = st.number_input("From Chapter", min_value=1, max_value=max_ch, value=data.get("bible_start", 1), key="wiz_bs")
            with col2:
                bible_end = st.number_input("To Chapter", min_value=1, max_value=max_ch, value=data.get("bible_end", min(max_ch, 8)), key="wiz_be")
            data["bible_book"] = bible_book
            data["bible_start"] = bible_start
            data["bible_end"] = bible_end
            components.append({
                "type": "bible_reading",
                "config": {"books": [{"name": bible_book, "start": bible_start, "end": bible_end}]},
            })
            spacer(8)

        if data.get("comp_sermon"):
            st.markdown("**\U0001f3a7 Sermon Series**")
            series_list = db.get_sermon_series_list()
            if series_list:
                series_options = {f"{s['title']} ({s['speaker']}, {s['episode_count']} episodes)": s["id"] for s in series_list}
                selected_series = st.selectbox("Select Series", options=list(series_options.keys()),
                                               key="wiz_sermon_series")
                data["selected_series"] = selected_series
                s_id = series_options[selected_series]
                s_info = next(s for s in series_list if s["id"] == s_id)
                components.append({
                    "type": "sermon_series",
                    "config": {"series_id": s_id, "title": s_info["title"], "episode_count": s_info["episode_count"]},
                })
            else:
                st.info("No sermon series available. Ask Admin to add sermon series.")
            spacer(8)

        if data.get("comp_time"):
            st.markdown("**\u23f0 Prayer Time Commitment**")
            col1, col2 = st.columns(2)
            with col1:
                prayer_mins = st.number_input("Minutes", min_value=15, max_value=480,
                                              value=data.get("prayer_mins", 60), step=15, key="wiz_pm")
            with col2:
                prayer_freq = st.selectbox("Frequency", ["daily", "weekly", "total"],
                                           index=["daily", "weekly", "total"].index(data.get("prayer_freq", "daily")),
                                           key="wiz_pf")
            data["prayer_mins"] = prayer_mins
            data["prayer_freq"] = prayer_freq
            components.append({
                "type": "prayer_time",
                "config": {"duration_minutes": prayer_mins, "frequency": prayer_freq},
            })

        data["components"] = components

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("\u2190 Back", use_container_width=True, key="s3b"):
                st.session_state["wiz_step"] = 2
                st.rerun()
        with col3:
            if st.button("Next \u2192", type="primary", use_container_width=True, key="s3n"):
                st.session_state["wiz_step"] = 4
                st.rerun()

    # --- Step 4: Review & Publish ---
    elif step == 4:
        section_label("Review & Publish")

        st.markdown(f"**Title:** {data.get('title', '')}")
        st.markdown(f"**Dates:** {data.get('start_date', '')} to {data.get('end_date', '')}")
        if data.get("description"):
            st.markdown(f"**Description:** {data['description']}")

        st.markdown("**Components:**")
        for comp in data.get("components", []):
            ctype = comp["type"].replace("_", " ").title()
            if comp["type"] == "prayer_template":
                st.markdown(f"- \U0001f64f {ctype}: {len(comp['config'].get('template_ids', []))} template(s)")
            elif comp["type"] == "bible_reading":
                books = comp["config"].get("books", [])
                for b in books:
                    st.markdown(f"- \U0001f4d6 {b['name']} {b['start']}\u2013{b['end']}")
            elif comp["type"] == "sermon_series":
                st.markdown(f"- \U0001f3a7 {comp['config'].get('title', '')} ({comp['config'].get('episode_count', 0)} episodes)")
            elif comp["type"] == "prayer_time":
                st.markdown(f"- \u23f0 {comp['config']['duration_minutes']} min {comp['config']['frequency']}")

        spacer()

        # Select targets
        section_label("Assign To")
        members = get_members_for_pastor(my_id) if role == "pastor" else []
        if role in ("admin", "bishop"):
            from modules.rbac import get_pastors_list
            # For admin/bishop, show all prayer warriors across pastors
            all_pastors = get_pastors_list()
            for p in all_pastors:
                members.extend(get_members_for_pastor(p["user_id"]))

        if members:
            assign_all = st.checkbox("Assign to all members", value=True)
            if assign_all:
                target_ids = [m["user_id"] for m in members]
                st.caption(f"{len(target_ids)} member(s) will receive this assignment")
            else:
                member_options = {m["display_name"]: m["user_id"] for m in members}
                selected_members = st.multiselect("Select members", options=list(member_options.keys()))
                target_ids = [member_options[m] for m in selected_members]
        else:
            st.warning("No members found to assign to.")
            target_ids = []

        spacer()

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("\u2190 Back", use_container_width=True, key="s4b"):
                st.session_state["wiz_step"] = 3
                st.rerun()
        with col2:
            if st.button("\U0001f680 Publish Assignment", type="primary", use_container_width=True, key="s4p"):
                if not target_ids:
                    st.error("Please select at least one member.")
                elif not data.get("components"):
                    st.error("No components configured.")
                else:
                    with st.spinner("Publishing..."):
                        result = db.create_wizard_assignment(
                            title=data["title"],
                            description=data.get("description", ""),
                            created_by=my_id,
                            target_user_ids=target_ids,
                            start_date=data["start_date"],
                            end_date=data["end_date"],
                            components=data["components"],
                        )
                    if result.get("success"):
                        st.session_state["wiz_step"] = 1
                        st.session_state["wiz_data"] = {}
                        st.success(f"Assignment published to {len(target_ids)} member(s)!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(result.get("error", "Failed to publish"))

# ==================== MY ASSIGNMENTS TAB ====================
with tab_my_assignments:
    assignments = db.get_wizard_assignments_by_creator(my_id)

    if not assignments:
        empty_state("\U0001f9d9", "No wizard assignments yet", "Create one in the 'Create New' tab")
    else:
        for a in assignments:
            # Get components
            components = db.get_wizard_components(a["id"])
            comp_labels = []
            for c in components:
                if c["component_type"] == "prayer_template":
                    comp_labels.append("\U0001f64f Prayer")
                elif c["component_type"] == "bible_reading":
                    comp_labels.append("\U0001f4d6 Reading")
                elif c["component_type"] == "sermon_series":
                    comp_labels.append("\U0001f3a7 Sermon")
                elif c["component_type"] == "prayer_time":
                    comp_labels.append("\u23f0 Prayer Time")

            # Count targets
            from modules.supabase_client import get_admin_client
            _adm = get_admin_client()
            targets = _adm.table("wizard_assignment_targets") \
                .select("user_id", count="exact") \
                .eq("wizard_assignment_id", a["id"]) \
                .execute()
            target_count = targets.count or 0

            st.markdown(f"""
            <div class="entry-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-family:'DM Serif Display',Georgia,serif; font-size:16px; color:#2A2438;">
                            {a['title']}
                        </span>
                        <div style="font-size:12px; color:#9E96AB; margin-top:2px;">
                            {a['start_date']} to {a['end_date']} | {target_count} member(s)
                        </div>
                    </div>
                    <span style="background:#EDEBFA; color:#5B4FC4; padding:3px 10px;
                                 border-radius:10px; font-size:11px; font-weight:600;">
                        {len(components)} components
                    </span>
                </div>
                <div style="margin-top:8px; font-size:13px; color:#6B6580;">
                    {' | '.join(comp_labels)}
                </div>
            </div>
            """, unsafe_allow_html=True)
