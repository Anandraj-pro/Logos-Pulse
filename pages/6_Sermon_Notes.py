import streamlit as st
import json
from datetime import date
from modules import db
from modules.scripture_lookup import parse_references, render_reference_with_text

db.init_db()

st.title("\U0001f4dd Sermon Notes")

DEFAULT_SPEAKERS = [
    "Bishop Samuel Patta",
    "Merlyn Patta",
    "Ps. Deepak Avinash",
]

# Collect unique speakers from existing notes for filter
all_notes = db.get_all_sermon_notes()
all_speakers = sorted(set(n.get("speaker", "") for n in all_notes if n.get("speaker")))
# Merge with defaults
for s in DEFAULT_SPEAKERS:
    if s not in all_speakers:
        all_speakers.insert(0, s)


def _count_refs(note):
    if not note.get("bible_references"):
        return 0
    refs = json.loads(note["bible_references"]) if isinstance(note["bible_references"], str) else note["bible_references"]
    return len(refs) if isinstance(refs, list) else 0


def _count_takeaways(note):
    text = note.get("key_takeaways", "") or ""
    lines = [l.strip() for l in text.strip().split("\n") if l.strip() and l.strip() != "-"]
    return len(lines)


def _render_scripture_card(ref, color="#7B68EE"):
    enriched = render_reference_with_text(ref)
    if enriched.get("scripture_text"):
        st.markdown(f"""
        <div style="background:#FFF9F0; border-left:3px solid {color};
                    padding:10px 14px; margin:8px 0; border-radius:6px;
                    font-family:Georgia,'Times New Roman',serif; font-size:15px;
                    color:#3C2F1E; line-height:1.7;">
            <b style="color:{color}; font-size:13px; letter-spacing:0.5px;">{enriched['reference']}</b><br/>
            <i>{enriched['scripture_text']}</i>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption(f"{ref.get('reference', '')} — could not load")


# --- View mode: if a note is selected for full view ---
if "view_sermon_id" in st.session_state:
    note = db.get_sermon_note(st.session_state["view_sermon_id"])
    if note:
        # Back button
        if st.button("\u2190 Back to Notes"):
            st.session_state.pop("view_sermon_id", None)
            st.rerun()

        # --- Full-page read-only view ---
        # Header
        st.markdown(f"""
        <div style="text-align:center; padding:20px 0 10px 0;">
            <div style="font-size:12px; color:#999; text-transform:uppercase; letter-spacing:2px;">
                Sermon Notes
            </div>
            <div style="font-size:28px; font-weight:700; color:#4A3728; margin:8px 0;">
                {note['title']}
            </div>
            <div style="font-size:15px; color:#7B68EE; font-weight:500;">
                {note['speaker']}
            </div>
            <div style="font-size:13px; color:#aaa; margin-top:4px;">
                {note['sermon_date']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Notes + References side by side
        if note.get("notes_text") or note.get("bible_references"):
            col_notes, col_refs = st.columns([3, 2])

            with col_notes:
                if note.get("notes_text"):
                    st.markdown(f"""
                    <div style="background:#FAFAFA; border-radius:10px; padding:20px;
                                font-size:16px; line-height:1.8; color:#333;">
                        {note['notes_text'].replace(chr(10), '<br/>')}
                    </div>
                    """, unsafe_allow_html=True)

            with col_refs:
                refs = json.loads(note["bible_references"]) if isinstance(
                    note["bible_references"], str
                ) else note.get("bible_references", [])
                if refs and isinstance(refs, list):
                    st.markdown(f"""
                    <div style="font-size:12px; color:#999; text-transform:uppercase;
                                letter-spacing:1px; margin-bottom:8px;">
                        Scripture References ({len(refs)})
                    </div>
                    """, unsafe_allow_html=True)
                    for ref in refs:
                        if isinstance(ref, dict):
                            _render_scripture_card(ref)

        # Reflection sections
        if note.get("learnings"):
            st.divider()
            st.markdown(f"""
            <div style="margin:10px 0;">
                <div style="font-size:12px; color:#7B68EE; text-transform:uppercase;
                            letter-spacing:1.5px; font-weight:600; margin-bottom:8px;">
                    What I Learned
                </div>
                <div style="background:linear-gradient(135deg, #F5F0FF, #FFF9F0);
                            border-radius:10px; padding:16px 20px;
                            font-size:16px; line-height:1.8; color:#3C2F1E;">
                    {note['learnings'].replace(chr(10), '<br/>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if note.get("key_takeaways"):
            st.markdown(f"""
            <div style="margin:10px 0;">
                <div style="font-size:12px; color:#4CAF50; text-transform:uppercase;
                            letter-spacing:1.5px; font-weight:600; margin-bottom:8px;">
                    Key Takeaways
                </div>
                <div style="background:#F1F8E9; border-radius:10px; padding:16px 20px;
                            font-size:16px; line-height:1.8; color:#33691E;">
                    {note['key_takeaways'].replace(chr(10), '<br/>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if note.get("additional_thoughts"):
            st.markdown(f"""
            <div style="margin:10px 0;">
                <div style="font-size:12px; color:#FF9800; text-transform:uppercase;
                            letter-spacing:1.5px; font-weight:600; margin-bottom:8px;">
                    Additional Thoughts
                </div>
                <div style="background:#FFF3E0; border-radius:10px; padding:16px 20px;
                            font-size:16px; line-height:1.8; color:#E65100;">
                    {note['additional_thoughts'].replace(chr(10), '<br/>')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Bottom actions
        st.divider()
        col_edit, col_del = st.columns(2)
        with col_edit:
            if st.button("\u270f\ufe0f Edit This Note", use_container_width=True):
                st.session_state["editing_sermon_id"] = note["id"]
                st.session_state.pop("view_sermon_id", None)
                st.rerun()
        with col_del:
            if st.button("\U0001f5d1\ufe0f Delete This Note", use_container_width=True):
                st.session_state["confirm_delete_sermon"] = note["id"]
                st.rerun()

        # Delete confirmation
        if st.session_state.get("confirm_delete_sermon") == note["id"]:
            st.warning(f"Are you sure you want to delete **\"{note['title']}\"**? This cannot be undone.")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("Yes, Delete", type="primary", use_container_width=True):
                    db.delete_sermon_note(note["id"])
                    st.session_state.pop("confirm_delete_sermon", None)
                    st.session_state.pop("view_sermon_id", None)
                    st.rerun()
            with col_no:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.pop("confirm_delete_sermon", None)
                    st.rerun()

    else:
        st.session_state.pop("view_sermon_id", None)
        st.rerun()

else:
    # --- Normal mode: tabs ---
    tab_new, tab_browse = st.tabs(["\u270f\ufe0f Write Note", "\U0001f4da Browse Notes"])

    # ==================== WRITE NOTE ====================
    with tab_new:
        editing_id = st.session_state.get("editing_sermon_id")
        editing_note = None
        if editing_id:
            editing_note = db.get_sermon_note(editing_id)
            if editing_note:
                st.markdown(f"""
                <div style="background:#FFF3E0; border-left:4px solid #FF9800;
                            padding:10px 16px; border-radius:6px; margin-bottom:16px;">
                    <b style="color:#E65100;">Editing:</b> {editing_note['title']}
                </div>
                """, unsafe_allow_html=True)
                if st.button("Cancel Editing"):
                    st.session_state.pop("editing_sermon_id", None)
                    st.rerun()

        # --- Sermon details ---
        st.markdown("""
        <div style="font-size:12px; color:#999; text-transform:uppercase;
                    letter-spacing:1.5px; margin-bottom:4px;">
            Sermon Details
        </div>
        """, unsafe_allow_html=True)

        title = st.text_input(
            "Sermon Title",
            value=editing_note["title"] if editing_note else "",
            placeholder="e.g., The Prayer That Attracts the Presence of God",
        )

        col1, col2 = st.columns(2)
        with col1:
            # Speaker with default options + custom
            speaker_options = DEFAULT_SPEAKERS + ["Other"]
            existing_speaker = editing_note["speaker"] if editing_note else ""
            if existing_speaker in DEFAULT_SPEAKERS:
                speaker_idx = DEFAULT_SPEAKERS.index(existing_speaker)
            elif existing_speaker:
                speaker_idx = len(DEFAULT_SPEAKERS)  # "Other"
            else:
                speaker_idx = 0
            speaker_choice = st.selectbox("Speaker", options=speaker_options, index=speaker_idx)

            if speaker_choice == "Other":
                speaker = st.text_input(
                    "Speaker Name",
                    value=existing_speaker if existing_speaker not in DEFAULT_SPEAKERS else "",
                    placeholder="Enter speaker name",
                )
            else:
                speaker = speaker_choice

        with col2:
            sermon_date = st.date_input(
                "Date",
                value=date.fromisoformat(editing_note["sermon_date"]) if editing_note else date.today(),
            )

        st.divider()

        # --- Notes: Left / Right ---
        st.markdown("""
        <div style="font-size:12px; color:#999; text-transform:uppercase;
                    letter-spacing:1.5px; margin-bottom:4px;">
            Notes & Scripture
        </div>
        """, unsafe_allow_html=True)
        st.caption("Write notes on the left. Add Bible references on the right — scripture appears automatically.")

        col_notes, col_refs = st.columns([3, 2])

        with col_notes:
            st.markdown("**\U0001f4d3 My Notes**")
            notes_text = st.text_area(
                "Notes",
                value=editing_note["notes_text"] if editing_note else "",
                height=300,
                placeholder="Write your notes from the sermon here...",
                label_visibility="collapsed",
            )

        with col_refs:
            st.markdown("**\U0001f4d6 Bible References**")
            existing_refs = ""
            if editing_note and editing_note.get("bible_references"):
                refs_data = json.loads(editing_note["bible_references"]) if isinstance(
                    editing_note["bible_references"], str
                ) else editing_note["bible_references"]
                if isinstance(refs_data, list):
                    existing_refs = "\n".join(
                        r.get("reference", "") if isinstance(r, dict) else str(r)
                        for r in refs_data
                    )

            bible_refs_text = st.text_area(
                "References",
                value=existing_refs,
                height=120,
                placeholder="Mark 1:1\nLuke 4:18-19\nJohn 3:16",
                label_visibility="collapsed",
            )

            if bible_refs_text.strip():
                parsed_refs = parse_references(bible_refs_text)
                if parsed_refs:
                    for ref in parsed_refs:
                        _render_scripture_card(ref)

        st.divider()

        # --- Reflections ---
        st.markdown("""
        <div style="font-size:12px; color:#999; text-transform:uppercase;
                    letter-spacing:1.5px; margin-bottom:4px;">
            Reflection
        </div>
        """, unsafe_allow_html=True)

        learnings = st.text_area(
            "\U0001f4a1 What I learned from this",
            value=editing_note["learnings"] if editing_note else "",
            height=120,
            placeholder="What spoke to you? What revelation did you receive?",
        )

        key_takeaways = st.text_area(
            "\u2705 Key Takeaways",
            value=editing_note["key_takeaways"] if editing_note else "",
            height=120,
            placeholder="- Point 1\n- Point 2\n- Point 3",
        )

        additional = st.text_area(
            "\U0001f4ad Additional Thoughts",
            value=editing_note["additional_thoughts"] if editing_note else "",
            height=100,
            placeholder="Anything else innovative or extra...",
        )

        # --- Save ---
        st.divider()
        save_label = "Update Sermon Note" if editing_note else "Save Sermon Note"
        if st.button(save_label, type="primary", use_container_width=True):
            if not title.strip():
                st.error("Please enter a sermon title.")
            elif not speaker.strip():
                st.error("Please select or enter a speaker name.")
            else:
                refs_list = []
                if bible_refs_text.strip():
                    parsed = parse_references(bible_refs_text)
                    refs_list = [{"reference": r["reference"], "book": r["book"],
                                  "chapter": r["chapter"],
                                  "start_verse": r.get("start_verse"),
                                  "end_verse": r.get("end_verse")} for r in parsed]

                if editing_id and editing_note:
                    db.update_sermon_note(
                        note_id=editing_id,
                        title=title.strip(), speaker=speaker.strip(),
                        sermon_date=sermon_date.isoformat(),
                        notes_text=notes_text, bible_references=refs_list,
                        learnings=learnings, key_takeaways=key_takeaways,
                        additional_thoughts=additional,
                    )
                    st.session_state.pop("editing_sermon_id", None)
                    st.success("Sermon note updated!")
                else:
                    db.create_sermon_note(
                        title=title.strip(), speaker=speaker.strip(),
                        sermon_date=sermon_date.isoformat(),
                        notes_text=notes_text, bible_references=refs_list,
                        learnings=learnings, key_takeaways=key_takeaways,
                        additional_thoughts=additional,
                    )
                    st.success("Sermon note saved!")
                st.rerun()

    # ==================== BROWSE NOTES ====================
    with tab_browse:
        notes = db.get_all_sermon_notes()

        if not notes:
            st.markdown("""
            <div style="text-align:center; padding:40px 20px; color:#aaa;">
                <div style="font-size:48px; margin-bottom:12px;">\U0001f4dd</div>
                <div style="font-size:18px; font-weight:500;">No sermon notes yet</div>
                <div style="font-size:14px; margin-top:4px;">
                    Create your first note in the "Write Note" tab
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # --- Filters row ---
            col_search, col_speaker_filter = st.columns([3, 2])
            with col_search:
                search = st.text_input(
                    "Search",
                    placeholder="Search by title, speaker, or content...",
                    label_visibility="collapsed",
                )
            with col_speaker_filter:
                filter_speakers = ["All Speakers"] + all_speakers
                selected_speaker = st.selectbox(
                    "Filter by Speaker",
                    options=filter_speakers,
                    label_visibility="collapsed",
                )

            # Apply filters
            filtered = notes
            if search:
                search_lower = search.lower()
                filtered = [n for n in filtered if (
                    search_lower in n.get("title", "").lower() or
                    search_lower in n.get("speaker", "").lower() or
                    search_lower in n.get("notes_text", "").lower() or
                    search_lower in n.get("learnings", "").lower() or
                    search_lower in n.get("key_takeaways", "").lower()
                )]
            if selected_speaker != "All Speakers":
                filtered = [n for n in filtered if n.get("speaker") == selected_speaker]

            st.caption(f"{len(filtered)} note(s)")

            # --- Note cards ---
            for note in filtered:
                ref_count = _count_refs(note)
                takeaway_count = _count_takeaways(note)

                # Badges
                badges = []
                if ref_count > 0:
                    badges.append(f'<span style="background:#E8EAF6; color:#3F51B5; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600;">\U0001f4d6 {ref_count} ref{"s" if ref_count != 1 else ""}</span>')
                if takeaway_count > 0:
                    badges.append(f'<span style="background:#E8F5E9; color:#2E7D32; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600;">\u2705 {takeaway_count} takeaway{"s" if takeaway_count != 1 else ""}</span>')
                if note.get("learnings"):
                    badges.append(f'<span style="background:#FFF3E0; color:#E65100; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600;">\U0001f4a1 Reflection</span>')
                badges_html = " ".join(badges)

                # Preview text
                preview = ""
                if note.get("notes_text"):
                    preview = note["notes_text"][:120].replace("\n", " ")
                    if len(note["notes_text"]) > 120:
                        preview += "..."

                st.markdown(f"""
                <div style="background:linear-gradient(135deg, #FEFEFE, #FFF9F0);
                            border:1px solid #E8DCC8; border-radius:12px;
                            padding:18px 22px; margin:10px 0;
                            box-shadow:0 1px 4px rgba(0,0,0,0.04);
                            transition: box-shadow 0.2s;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div style="font-size:18px; font-weight:600; color:#4A3728;">
                                {note['title']}
                            </div>
                            <div style="font-size:14px; color:#7B68EE; font-weight:500; margin-top:2px;">
                                {note['speaker']}
                            </div>
                        </div>
                        <div style="font-size:13px; color:#aaa; white-space:nowrap;">
                            {note['sermon_date']}
                        </div>
                    </div>
                    {"<div style='font-size:14px; color:#777; margin-top:8px; line-height:1.5;'>" + preview + "</div>" if preview else ""}
                    <div style="margin-top:10px;">
                        {badges_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Action buttons
                col_view, col_edit, col_del = st.columns([2, 1, 1])
                with col_view:
                    if st.button("Open", key=f"view_{note['id']}", use_container_width=True):
                        st.session_state["view_sermon_id"] = note["id"]
                        st.rerun()
                with col_edit:
                    if st.button("Edit", key=f"edit_{note['id']}", use_container_width=True):
                        st.session_state["editing_sermon_id"] = note["id"]
                        st.rerun()
                with col_del:
                    if st.button("Delete", key=f"del_{note['id']}", use_container_width=True):
                        st.session_state["confirm_delete_sermon"] = note["id"]

                # Delete confirmation inline
                if st.session_state.get("confirm_delete_sermon") == note["id"]:
                    st.warning(f"Delete **\"{note['title']}\"**? This cannot be undone.")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("Yes, Delete", key=f"confirm_del_{note['id']}", type="primary"):
                            db.delete_sermon_note(note["id"])
                            st.session_state.pop("confirm_delete_sermon", None)
                            st.rerun()
                    with col_no:
                        if st.button("Cancel", key=f"cancel_del_{note['id']}"):
                            st.session_state.pop("confirm_delete_sermon", None)
                            st.rerun()
