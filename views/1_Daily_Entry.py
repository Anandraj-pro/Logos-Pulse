import streamlit as st
import json
from datetime import date
from modules import db
from modules.utils import format_chapters_display, is_valid_youtube_url, format_prayer_duration
from modules.message import format_whatsapp_message
from modules.chapter_splitter import get_today_suggestion
from modules.bible_data import get_book_names, get_chapter_count
from modules.clipboard import copy_button
from modules.bible_reader import fetch_chapter, render_chapter_with_annotations
from modules.styles import inject_styles, page_header, section_label, spacer
from modules.auth import require_login, require_password_changed

require_login()
require_password_changed()
inject_styles()

settings = db.get_all_settings()
default_prayer = int(settings.get("default_prayer_minutes", "60"))
omit_sermon = settings.get("omit_empty_sermon", "false") == "true"

# Get pastor name dynamically from profile hierarchy
greeting_name = settings.get("greeting_name", "Pastor")
try:
    from modules.supabase_client import get_admin_client
    from modules.auth import get_current_user_id
    _admin = get_admin_client()
    _profile = _admin.table("user_profiles").select("pastor_id").eq("user_id", get_current_user_id()).execute()
    if _profile.data and _profile.data[0].get("pastor_id"):
        _pastor_user = _admin.auth.admin.get_user_by_id(_profile.data[0]["pastor_id"]).user
        _pastor_meta = _pastor_user.user_metadata or {}
        greeting_name = _pastor_meta.get("preferred_name") or _pastor_meta.get("first_name") or greeting_name
except Exception:
    pass

formatted_date = date.today().strftime("%A, %B %d")

page_header("\u270f\ufe0f", "Daily Entry", formatted_date)

# Date selection
entry_date = st.date_input("Date", value=date.today(), max_value=date.today(), label_visibility="collapsed")
entry_date_str = entry_date.isoformat()

existing = db.get_entry_by_date(entry_date_str)
assignment = db.get_active_assignment()
suggestion = get_today_suggestion(entry_date, assignment)

if suggestion:
    st.markdown(f"""
    <div class="goal-banner">
        \U0001f4d6 Today's reading goal: <b>{suggestion['book']} {suggestion['range']}</b>
    </div>
    """, unsafe_allow_html=True)

# --- Tabs ---
tab_read, tab_log, tab_report = st.tabs(["\U0001f4d6 Read Bible", "\u270f\ufe0f Log Entry", "\U0001f4cb Report"])

# ==================== TAB 1: Read Bible ====================
with tab_read:
    book_names = get_book_names()

    if suggestion and suggestion["book"] in book_names:
        default_read_book = book_names.index(suggestion["book"])
    elif existing and existing.get("bible_book") and existing["bible_book"] in book_names:
        default_read_book = book_names.index(existing["bible_book"])
    else:
        default_read_book = book_names.index("Luke") if "Luke" in book_names else 0

    if "nav_chapter" in st.session_state:
        st.session_state["read_chapter"] = st.session_state.pop("nav_chapter")

    if "completed_book" not in st.session_state:
        st.session_state["completed_book"] = None
    if "completed_chapters" not in st.session_state:
        st.session_state["completed_chapters"] = set()

    col_book, col_ch = st.columns([3, 1])
    with col_book:
        read_book = st.selectbox("Book", options=book_names, index=default_read_book, key="read_book", label_visibility="collapsed")
    max_ch = get_chapter_count(read_book)
    default_ch = suggestion["chapters"][0] if suggestion and suggestion["book"] == read_book else 1
    default_ch_idx = min(default_ch - 1, max_ch - 1)
    with col_ch:
        read_chapter = st.selectbox("Ch", options=list(range(1, max_ch + 1)), index=default_ch_idx, key="read_chapter", label_visibility="collapsed")

    if st.session_state["completed_book"] != read_book:
        st.session_state["completed_book"] = read_book
        st.session_state["completed_chapters"] = set()
    completed = st.session_state["completed_chapters"]

    # Reading progress
    if suggestion and suggestion["book"] == read_book:
        target_chapters = suggestion["chapters"]
        done_count = len(completed.intersection(set(target_chapters)))
        total_target = len(target_chapters)
        progress = done_count / total_target if total_target > 0 else 0
        st.progress(progress, text=f"Today: {done_count}/{total_target} chapters")

    # Chapter heading
    st.markdown(f"""
    <div style="text-align:center; padding:8px 0 4px 0;">
        <span style="font-size:11px; color:#9E96AB; text-transform:uppercase; letter-spacing:2px;">{read_book}</span><br/>
        <span style="font-family:'DM Serif Display',Georgia,serif; font-size:26px; color:#2A2438;">Chapter {read_chapter}</span>
    </div>
    """, unsafe_allow_html=True)

    # Completed pills
    if completed:
        sorted_done = sorted(completed)
        pills = " ".join(f'<span style="display:inline-block; background:#E8F5E9; color:#2E7D32; border-radius:12px; padding:3px 10px; margin:2px; font-size:12px; font-weight:600;">Ch {c}</span>' for c in sorted_done)
        st.markdown(f"<div style='text-align:center; padding:4px 0 8px 0;'>{pills}</div>", unsafe_allow_html=True)

    # Font size + annotate mode controls
    font_sizes = {"Small": 14, "Medium": 17, "Large": 20, "Extra Large": 24}
    ctrl_col, ann_col = st.columns([3, 1])
    with ctrl_col:
        font_choice = st.segmented_control("Font", list(font_sizes.keys()), default="Medium",
                                           label_visibility="collapsed")
    with ann_col:
        annotate_mode = st.toggle("🔖 Annotate", value=False,
                                  help="Per-verse bookmarks and highlights")
    font_size = font_sizes.get(font_choice, 17)

    # Fetch chapter
    with st.spinner(""):
        chapter_data = fetch_chapter(read_book, read_chapter)

    if chapter_data:
        if annotate_mode:
            render_chapter_with_annotations(read_book, read_chapter, chapter_data, font_size)
        else:
            verses_html = ""
            if chapter_data.get("verses"):
                for verse in chapter_data["verses"]:
                    v_num = verse.get("verse", "")
                    v_text = verse.get("text", "").strip()
                    verses_html += (
                        f'<span style="color:#5B4FC4; font-weight:700; font-size:{max(font_size - 6, 10)}px; '
                        f'vertical-align:super; margin-right:2px;">{v_num}</span>'
                        f'<span>{v_text} </span>'
                    )
            elif chapter_data.get("text"):
                verses_html = chapter_data["text"]

            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #FFF9F0, #FFFEF8);
                        border:1px solid #E8DCC8; border-radius:14px;
                        padding:24px 22px; margin:8px 0;
                        font-family:'DM Serif Display',Georgia,'Times New Roman',serif;
                        font-size:{font_size}px; line-height:1.9; color:#3C2F1E;
                        max-height:480px; overflow-y:auto;
                        box-shadow:0 2px 8px rgba(0,0,0,0.03);">
                {verses_html}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Could not load chapter. Check your internet connection.")

    # Bottom bar
    spacer(8)
    is_completed = read_chapter in completed
    col_prev, col_mark, col_next = st.columns([1, 2, 1])

    with col_prev:
        if read_chapter > 1:
            if st.button("\u25c0 Prev", use_container_width=True):
                st.session_state["nav_chapter"] = read_chapter - 1
                st.rerun()
    with col_mark:
        if is_completed:
            st.markdown(f"""
            <div style="text-align:center; background:#E8F5E9; border-radius:10px;
                        padding:10px; color:#2E7D32; font-weight:600;">
                \u2705 Chapter {read_chapter} Done
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(f"Mark Chapter {read_chapter} Done", type="primary", use_container_width=True):
                st.session_state["completed_chapters"].add(read_chapter)
                # Q4: Save reading bookmark
                try:
                    from modules.supabase_client import get_admin_client
                    from modules.auth import get_current_user_id
                    get_admin_client().table("user_profiles") \
                        .update({"last_read_book": read_book, "last_read_chapter": read_chapter}) \
                        .eq("user_id", get_current_user_id()) \
                        .execute()
                except Exception:
                    pass
                if read_chapter < max_ch:
                    st.session_state["nav_chapter"] = read_chapter + 1
                st.rerun()
    with col_next:
        if read_chapter < max_ch:
            if st.button("Next \u25b6", use_container_width=True):
                st.session_state["nav_chapter"] = read_chapter + 1
                st.rerun()

# ==================== TAB 2: Log Entry ====================
with tab_log:
    with st.form("daily_entry_form"):
        # Prayer
        section_label("\U0001f64f Prayer")
        prayer_options = list(range(15, 195, 15))
        default_idx = (
            prayer_options.index(existing["prayer_minutes"])
            if existing and existing["prayer_minutes"] in prayer_options
            else prayer_options.index(default_prayer) if default_prayer in prayer_options else 3
        )
        prayer_minutes = st.select_slider("Duration (minutes)", options=prayer_options, value=prayer_options[default_idx],
                                          help="Slide to select how many minutes you prayed today")

        # Bible Reading
        section_label("\U0001f4d6 Bible Reading")

        read_completed = st.session_state.get("completed_chapters", set())
        read_completed_book = st.session_state.get("completed_book")

        if read_completed and read_completed_book and read_completed_book in book_names:
            default_book_idx = book_names.index(read_completed_book)
        elif existing and existing.get("bible_book") and existing["bible_book"] in book_names:
            default_book_idx = book_names.index(existing["bible_book"])
        elif suggestion and suggestion["book"] in book_names:
            default_book_idx = book_names.index(suggestion["book"])
        else:
            default_book_idx = 0

        bible_book = st.selectbox("Book", options=book_names, index=default_book_idx, key="log_book")
        max_chapters = get_chapter_count(bible_book)

        if read_completed and read_completed_book == bible_book:
            default_chapters = sorted(c for c in read_completed if 1 <= c <= max_chapters)
        elif existing and existing.get("chapters_read"):
            existing_chapters = json.loads(existing["chapters_read"]) if isinstance(existing["chapters_read"], str) else existing["chapters_read"]
            default_chapters = [c for c in existing_chapters if 1 <= c <= max_chapters]
        elif suggestion and suggestion["book"] == bible_book:
            default_chapters = suggestion["chapters"]
        else:
            default_chapters = []

        if read_completed and read_completed_book == bible_book:
            st.success(f"Auto-filled: {len(default_chapters)} chapters from Read Bible tab")

        chapters = st.multiselect("Chapters read", options=list(range(1, max_chapters + 1)), default=default_chapters)

        # Q8: Fasting
        section_label("\U0001f374 Fasting")
        fasted = st.checkbox("I fasted today", value=existing.get("fasted", False) if existing else False)
        fast_type = None
        if fasted:
            fast_type = st.selectbox("Fast Type", ["Full Day", "Partial", "Daniel Fast"],
                                     index=0 if not existing or not existing.get("fast_type") else
                                     ["Full Day", "Partial", "Daniel Fast"].index(existing["fast_type"])
                                     if existing and existing.get("fast_type") in ["Full Day", "Partial", "Daniel Fast"] else 0)

        # Sermon
        section_label("\U0001f3a7 Listening to the Word (optional)")
        sermon_title = st.text_input("Sermon Title", value=existing.get("sermon_title", "") if existing else "")
        sermon_speaker = st.text_input("Speaker", value=existing.get("sermon_speaker", "") if existing else "Ps. Samuel Patta")
        youtube_link = st.text_input("YouTube Link", value=existing.get("youtube_link", "") if existing else "")

        submitted = st.form_submit_button("Save & Generate Report", type="primary", use_container_width=True)

    if submitted:
        if not chapters:
            st.error("Please select at least one chapter.")
        elif youtube_link and not is_valid_youtube_url(youtube_link):
            st.error("Please enter a valid YouTube URL.")
        else:
            chapters_display = format_chapters_display(bible_book, chapters)
            db.upsert_daily_entry(
                entry_date=entry_date_str, prayer_minutes=prayer_minutes,
                bible_book=bible_book, chapters_read=sorted(chapters),
                chapters_display=chapters_display,
                sermon_title=sermon_title.strip() if sermon_title else "",
                sermon_speaker=sermon_speaker.strip() if sermon_speaker else "",
                youtube_link=youtube_link.strip() if youtube_link else "",
            )
            st.success("Entry saved! Go to the **Report** tab to copy your WhatsApp message.")

# ==================== TAB 3: Report ====================
with tab_report:
    entry_for_report = db.get_entry_by_date(entry_date_str)

    if entry_for_report:
        # Get today's confession line and weekly count for the report
        _confession_line = None
        _confession_week_count = None
        try:
            _active_plans = db.get_my_confession_plans(status="active")
            if _active_plans:
                _tpl = _active_plans[0].get("confession_templates", {})
                _confessions = _tpl.get("confessions", [])
                if isinstance(_confessions, str):
                    import json as _json
                    _confessions = _json.loads(_confessions)
                if _confessions:
                    _c = _confessions[0]
                    _ref = f' — {_c["scripture_ref"]}' if _c.get("scripture_ref") else ""
                    _confession_line = f'"{_c["text"]}"{_ref}'
                _confession_week_count = db.get_confession_count_this_week()
        except Exception:
            pass

        message = format_whatsapp_message(
            entry_date=entry_date,
            prayer_minutes=entry_for_report["prayer_minutes"],
            chapters_display=entry_for_report.get("chapters_display", ""),
            sermon_title=entry_for_report.get("sermon_title") or None,
            sermon_speaker=entry_for_report.get("sermon_speaker") or None,
            youtube_link=entry_for_report.get("youtube_link") or None,
            greeting_name=greeting_name,
            omit_empty_sermon=omit_sermon,
            confession_line=_confession_line,
            confession_week_count=_confession_week_count,
        )

        section_label("WhatsApp Report Preview")
        st.markdown(f'<div class="report-card">{message}</div>', unsafe_allow_html=True)

        spacer()
        copy_button(message, "\U0001f4cb Copy to Clipboard")
        db.mark_report_copied(entry_date_str)

        # Summary below
        duration = format_prayer_duration(entry_for_report["prayer_minutes"])
        st.markdown(f"""
        <div style="margin-top:16px; padding:14px 18px; background:#E8F5E9; border-radius:12px;">
            <div style="font-size:13px; font-weight:600; color:#2E7D32; margin-bottom:6px;">
                \u2705 Entry Summary
            </div>
            <div style="font-size:14px; color:#333; line-height:1.6;">
                Prayer: {duration}<br/>
                Reading: {entry_for_report.get('chapters_display', 'N/A')}<br/>
                {"Sermon: " + entry_for_report['sermon_title'] + "<br/>" if entry_for_report.get('sermon_title') else ""}
                Report: {"Copied" if entry_for_report.get('report_copied') else "Ready to copy"}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">\U0001f4cb</div>
            <div class="empty-state-title">No entry for this date yet</div>
            <div class="empty-state-sub">Fill in the "Log Entry" tab first</div>
        </div>
        """, unsafe_allow_html=True)