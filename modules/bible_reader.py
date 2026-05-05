import requests
import streamlit as st
from modules.supabase_client import get_supabase_client, get_admin_client

API_BASE = "https://bible-api.com"

# Mapping our book names to bible-api.com format
BOOK_NAME_MAP = {
    "1 Samuel": "1 Samuel",
    "2 Samuel": "2 Samuel",
    "1 Kings": "1 Kings",
    "2 Kings": "2 Kings",
    "1 Chronicles": "1 Chronicles",
    "2 Chronicles": "2 Chronicles",
    "Song of Solomon": "Song of Solomon",
    "1 Corinthians": "1 Corinthians",
    "2 Corinthians": "2 Corinthians",
    "1 Thessalonians": "1 Thessalonians",
    "2 Thessalonians": "2 Thessalonians",
    "1 Timothy": "1 Timothy",
    "2 Timothy": "2 Timothy",
    "1 Peter": "1 Peter",
    "2 Peter": "2 Peter",
    "1 John": "1 John",
    "2 John": "2 John",
    "3 John": "3 John",
}


def _api_book_name(book: str) -> str:
    return BOOK_NAME_MAP.get(book, book)


def _get_from_cache(book: str, chapter: int) -> dict | None:
    """Check Supabase cache for a Bible chapter."""
    try:
        client = get_supabase_client()
        result = client.table("bible_cache") \
            .select("content") \
            .eq("book", book) \
            .eq("chapter", chapter) \
            .execute()
        if result.data:
            return result.data[0]["content"]
    except Exception:
        pass
    return None


def _save_to_cache(book: str, chapter: int, content: dict):
    """Save a Bible chapter to Supabase cache."""
    try:
        admin = get_admin_client()
        admin.table("bible_cache").upsert({
            "book": book,
            "chapter": chapter,
            "content": content,
        }, on_conflict="book,chapter").execute()
    except Exception:
        pass  # Non-critical — cache miss just means another API call next time


HIGHLIGHT_COLORS = {
    "yellow": ("rgba(255,230,50,0.30)", "🟡"),
    "green": ("rgba(80,200,80,0.22)", "🟢"),
}


def render_chapter_with_annotations(
    book: str,
    chapter: int,
    chapter_data: dict,
    font_size: int = 17,
) -> None:
    """Render a Bible chapter with per-verse bookmark and highlight toggle buttons.
    Loads bookmarks and highlights in two bulk queries (not one per verse).
    """
    import streamlit as st
    from modules.db import (
        get_bookmarks_for_chapter, get_highlights_for_chapter,
        toggle_bookmark, cycle_highlight,
    )

    if not chapter_data or not chapter_data.get("verses"):
        st.warning("Verse data not available for annotation view.")
        return

    bookmarks = get_bookmarks_for_chapter(book, chapter)
    highlights = get_highlights_for_chapter(book, chapter)

    bookmarked = {bm["verse_number"] for bm in bookmarks}
    hl_map = {hl["verse_number"]: hl["color"] for hl in highlights}

    for verse in chapter_data["verses"]:
        v_num = verse.get("verse", 0)
        v_text = verse.get("text", "").strip()
        is_bm = v_num in bookmarked
        hl_color = hl_map.get(v_num)
        bg, _ = HIGHLIGHT_COLORS.get(hl_color, ("transparent", "○"))

        col_text, col_bm, col_hl = st.columns([14, 1, 1])
        with col_text:
            st.markdown(
                f'<div style="background:{bg}; border-radius:6px; padding:3px 6px;'
                f' font-family:\'DM Serif Display\',Georgia,serif;'
                f' font-size:{font_size}px; line-height:1.9; color:#3C2F1E;">'
                f'<span style="color:#5B4FC4; font-weight:700;'
                f' font-size:{max(font_size - 6, 10)}px; vertical-align:super;'
                f' margin-right:4px;">{v_num}</span>{v_text}</div>',
                unsafe_allow_html=True,
            )
        with col_bm:
            bm_icon = "🔖" if is_bm else "☆"
            if st.button(bm_icon, key=f"bm_{book}_{chapter}_{v_num}",
                         help="Toggle bookmark", use_container_width=True):
                toggle_bookmark(book, chapter, v_num)
                st.rerun()
        with col_hl:
            hl_icon = "🟡" if hl_color == "yellow" else "🟢" if hl_color == "green" else "○"
            if st.button(hl_icon, key=f"hl_{book}_{chapter}_{v_num}",
                         help="Cycle highlight colour", use_container_width=True):
                cycle_highlight(book, chapter, v_num)
                st.rerun()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_chapter(book: str, chapter: int) -> dict | None:
    """Fetch a Bible chapter. Checks Supabase cache first, falls back to API."""

    # 1. Check Supabase persistent cache
    cached = _get_from_cache(book, chapter)
    if cached:
        return cached

    # 2. Fetch from external API
    try:
        api_book = _api_book_name(book)
        url = f"{API_BASE}/{api_book} {chapter}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            content = {
                "reference": data.get("reference", f"{book} {chapter}"),
                "text": data.get("text", ""),
                "verses": data.get("verses", []),
            }

            # 3. Save to Supabase cache for future requests
            _save_to_cache(book, chapter, content)

            return content
        return None
    except Exception:
        return None
