import requests
import streamlit as st

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


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_chapter(book: str, chapter: int) -> dict | None:
    """Fetch a single Bible chapter from bible-api.com. Returns dict with 'text' and 'reference'."""
    try:
        api_book = _api_book_name(book)
        url = f"{API_BASE}/{api_book} {chapter}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "reference": data.get("reference", f"{book} {chapter}"),
                "text": data.get("text", ""),
                "verses": data.get("verses", []),
            }
        return None
    except Exception:
        return None
