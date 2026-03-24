import streamlit as st
import json
from modules import db
from modules.scripture_lookup import parse_references, render_reference_with_text

db.init_db()

# ==================== SHARED CSS ====================
st.markdown("""
<style>
    .pj-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 28px 24px;
        margin-bottom: 20px;
        color: white;
    }
    .pj-header-title {
        font-size: 28px;
        font-weight: 700;
    }
    .pj-header-sub {
        font-size: 14px;
        color: rgba(255,255,255,0.7);
        margin-top: 4px;
    }
    .cat-card {
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.15s, box-shadow 0.15s;
        border: 2px solid transparent;
    }
    .cat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .cat-card-active {
        border: 2px solid currentColor;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .cat-icon { font-size: 28px; margin-bottom: 4px; }
    .cat-name { font-size: 13px; font-weight: 600; }
    .cat-count { font-size: 11px; opacity: 0.7; }
    .wizard-step {
        background: white;
        border: 1px solid #F0EBF8;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.03);
    }
    .wizard-step-num {
        display: inline-block;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-size: 14px;
        font-weight: 700;
        color: white;
        margin-right: 10px;
    }
    .wizard-step-title {
        font-size: 16px;
        font-weight: 600;
        color: #2C2C2C;
        display: inline;
    }
    .wizard-step-desc {
        font-size: 13px;
        color: #999;
        margin: 4px 0 12px 38px;
    }
    .prayer-card {
        background: white;
        border: 1px solid #F0EBF8;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 12px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.03);
    }
    .prayer-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .prayer-name {
        font-size: 16px;
        font-weight: 600;
        color: #2C2C2C;
    }
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }
    .scripture-block {
        background: #FFF9F0;
        border-left: 3px solid;
        padding: 10px 14px;
        margin: 6px 0;
        border-radius: 6px;
        font-family: Georgia, serif;
        font-size: 14px;
        line-height: 1.7;
        color: #3C2F1E;
    }
    .confession-block {
        background: #E8F5E9;
        border-radius: 10px;
        padding: 12px 16px;
        font-weight: 500;
        color: #2E7D32;
        line-height: 1.7;
    }
    .declaration-block {
        background: #FFF3E0;
        border-radius: 10px;
        padding: 12px 16px;
        font-weight: 600;
        color: #E65100;
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
categories = db.get_prayer_categories()
total_prayers = 0
for cat in categories:
    total_prayers += len(db.get_prayers_by_category(cat["id"]))

st.markdown(f"""
<div class="pj-header">
    <div class="pj-header-title">\U0001f64f Prayer Journal</div>
    <div class="pj-header-sub">{total_prayers} prayers across {len(categories)} categories</div>
</div>
""", unsafe_allow_html=True)

# ==================== CATEGORY SELECTOR ====================
# Build category cards
cat_counts = {}
for cat in categories:
    prayers = db.get_prayers_by_category(cat["id"])
    cat_counts[cat["id"]] = len(prayers)

cols = st.columns(len(categories) + 1)

# Initialize selected category
if "pj_category" not in st.session_state and categories:
    st.session_state["pj_category"] = categories[0]["id"]

for i, cat in enumerate(categories):
    with cols[i]:
        count = cat_counts.get(cat["id"], 0)
        is_active = st.session_state.get("pj_category") == cat["id"]
        color = cat.get("color", "#7B68EE")
        active_class = "cat-card-active" if is_active else ""

        st.markdown(f"""
        <div class="cat-card {active_class}" style="background:{color}10; color:{color};">
            <div class="cat-icon">{cat['icon']}</div>
            <div class="cat-name">{cat['name']}</div>
            <div class="cat-count">{count} prayer{"s" if count != 1 else ""}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(cat["name"], key=f"cat_{cat['id']}", use_container_width=True, type="secondary" if not is_active else "primary"):
            st.session_state["pj_category"] = cat["id"]
            st.session_state.pop("pj_wizard_step", None)
            st.rerun()

# New category button
with cols[-1]:
    st.markdown("""
    <div class="cat-card" style="background:#F5F5F5; color:#999;">
        <div class="cat-icon">+</div>
        <div class="cat-name">New</div>
        <div class="cat-count">Category</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Add New", key="new_cat_btn", use_container_width=True):
        st.session_state["pj_category"] = "new"
        st.rerun()

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ==================== NEW CATEGORY ====================
if st.session_state.get("pj_category") == "new":
    st.markdown("""
    <div class="wizard-step">
        <span class="wizard-step-num" style="background:#667eea;">+</span>
        <span class="wizard-step-title">Create New Category</span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("new_category_form"):
        cat_name = st.text_input("Category Name", placeholder="e.g., Family, Ministry, Health")
        col1, col2 = st.columns(2)
        with col1:
            cat_icon = st.text_input("Emoji Icon", value="\U0001f4d6", max_chars=2)
        with col2:
            cat_colors = {"Purple": "#7B68EE", "Green": "#4CAF50", "Pink": "#E91E63",
                          "Orange": "#FF9800", "Blue": "#2196F3", "Teal": "#009688"}
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
        cat_color = category.get("color", "#7B68EE")

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
                st.markdown(f"<div style='text-align:right; padding-top:8px; font-size:13px; color:#999;'>{len(prayers)} total</div>", unsafe_allow_html=True)

            if status_filter and status_filter != "All":
                status_key = status_filter.lower().replace(" ", "_")
                prayers = [p for p in prayers if p.get("status") == status_key]

            if not prayers:
                st.markdown(f"""
                <div style="text-align:center; padding:40px; color:#ccc;">
                    <div style="font-size:48px; margin-bottom:8px;">{category['icon']}</div>
                    <div style="font-size:16px; color:#999;">No prayers here yet</div>
                    <div style="font-size:13px; color:#bbb;">Add your first prayer in the "New Prayer" tab</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                for prayer in prayers:
                    status = prayer.get("status", "ongoing")
                    status_config = {
                        "ongoing": ("#FF9800", "#FFF3E0", "Ongoing"),
                        "answered": ("#4CAF50", "#E8F5E9", "Answered"),
                        "standing_in_faith": ("#7B68EE", "#F0EBF8", "Standing in Faith"),
                    }
                    s_color, s_bg, s_label = status_config.get(status, ("#888", "#F5F5F5", status))

                    # Count scriptures
                    ref_count = 0
                    if prayer.get("scriptures"):
                        refs = json.loads(prayer["scriptures"]) if isinstance(prayer["scriptures"], str) else prayer["scriptures"]
                        ref_count = len(refs) if isinstance(refs, list) else 0

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
                            <div style="background:#F5F0FF; border-radius:10px; padding:14px 18px;
                                        font-style:italic; color:#4A3728; line-height:1.8; font-size:15px;">
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
                                <div style="font-size:12px; color:{cat_color}; text-transform:uppercase;
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
                            <div style="font-size:12px; color:#2E7D32; text-transform:uppercase;
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
                            <div style="font-size:12px; color:#E65100; text-transform:uppercase;
                                        letter-spacing:1px; font-weight:600; margin:16px 0 8px 0;">
                                Declarations
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="declaration-block">
                                {prayer['declarations'].replace(chr(10), '<br/>')}
                            </div>
                            """, unsafe_allow_html=True)

                        # Actions row
                        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
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
                    dot_style = f"background:{cat_color}; color:white; box-shadow:0 0 0 4px {cat_color}30;"
                    label_style = f"color:{cat_color}; font-weight:700;"
                else:
                    dot_style = "background:#E0E0E0; color:#999;"
                    label_style = "color:#bbb;"
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
                st.markdown(f"""
                <div style="font-size:12px; color:#999; text-transform:uppercase;
                            letter-spacing:1.5px; font-weight:600; margin-bottom:8px;">
                    Review Your Prayer
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"**Title:** {data.get('title', '')}")
                if data.get("prayer_text"):
                    st.markdown(f"**Prayer:** {data['prayer_text'][:100]}...")
                if data.get("scriptures_text"):
                    st.markdown(f"**Scriptures:** {data['scriptures_text'][:80]}...")
                if data.get("confessions"):
                    st.markdown(f"**Confessions:** {data['confessions'][:80]}...")
                if declarations:
                    st.markdown(f"**Declarations:** {declarations[:80]}...")

                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

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
