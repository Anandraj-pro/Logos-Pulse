"""
Parse Bible references from text (e.g., "Mark 1:1", "Luke 4:18-19")
and fetch the actual scripture text.
"""
import re
import streamlit as st
from modules.bible_reader import fetch_chapter

# Pattern to match references like: John 3:16, Mark 1:1-5, 1 John 2:3, Luke 4:18-19
REF_PATTERN = re.compile(
    r'(\d?\s?[A-Za-z]+(?:\s+of\s+[A-Za-z]+)?)\s+'  # Book name
    r'(\d+)'                                          # Chapter
    r'(?::(\d+))?'                                    # Optional start verse
    r'(?:\s*[-\u2013]\s*(\d+))?'                      # Optional end verse
)


def parse_references(text: str) -> list[dict]:
    """Parse Bible references from free-form text. Returns list of dicts with book, chapter, start_verse, end_verse."""
    refs = []
    for match in REF_PATTERN.finditer(text):
        book = match.group(1).strip()
        chapter = int(match.group(2))
        start_verse = int(match.group(3)) if match.group(3) else None
        end_verse = int(match.group(4)) if match.group(4) else start_verse
        refs.append({
            "book": book,
            "chapter": chapter,
            "start_verse": start_verse,
            "end_verse": end_verse,
            "reference": match.group(0).strip(),
        })
    return refs


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_scripture_text(book: str, chapter: int, start_verse: int = None, end_verse: int = None) -> str | None:
    """Fetch scripture text for a specific reference."""
    chapter_data = fetch_chapter(book, chapter)
    if not chapter_data:
        return None

    verses = chapter_data.get("verses", [])
    if not verses:
        return chapter_data.get("text", "")

    if start_verse is None:
        # Return full chapter
        return " ".join(v.get("text", "").strip() for v in verses)

    # Filter to requested verse range
    end = end_verse or start_verse
    filtered = [v for v in verses if start_verse <= v.get("verse", 0) <= end]
    if not filtered:
        return None

    return " ".join(v.get("text", "").strip() for v in filtered)


def render_reference_with_text(ref: dict) -> dict:
    """Given a parsed reference dict, fetch and return with scripture text."""
    text = fetch_scripture_text(
        ref["book"], ref["chapter"],
        ref.get("start_verse"), ref.get("end_verse")
    )
    return {**ref, "scripture_text": text}
