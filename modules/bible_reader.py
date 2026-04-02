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
