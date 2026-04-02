"""
Bible reference autocomplete — supports short/full book names.
Used in Sermon Notes and anywhere Bible references are typed.
"""

from modules.bible_data import get_book_names

# Short forms → full book names
ABBREVIATIONS = {
    "gen": "Genesis", "ex": "Exodus", "lev": "Leviticus", "num": "Numbers",
    "deut": "Deuteronomy", "josh": "Joshua", "judg": "Judges", "ruth": "Ruth",
    "1sam": "1 Samuel", "2sam": "2 Samuel", "1ki": "1 Kings", "2ki": "2 Kings",
    "1chr": "1 Chronicles", "2chr": "2 Chronicles", "ezra": "Ezra",
    "neh": "Nehemiah", "est": "Esther", "job": "Job",
    "ps": "Psalms", "psa": "Psalms", "psalm": "Psalms",
    "prov": "Proverbs", "pro": "Proverbs",
    "eccl": "Ecclesiastes", "ecc": "Ecclesiastes",
    "song": "Song of Solomon", "sos": "Song of Solomon",
    "isa": "Isaiah", "jer": "Jeremiah", "lam": "Lamentations",
    "ezek": "Ezekiel", "eze": "Ezekiel",
    "dan": "Daniel", "hos": "Hosea", "joel": "Joel", "amos": "Amos",
    "obad": "Obadiah", "jonah": "Jonah", "mic": "Micah", "nah": "Nahum",
    "hab": "Habakkuk", "zeph": "Zephaniah", "hag": "Haggai",
    "zech": "Zechariah", "zec": "Zechariah",
    "mal": "Malachi",
    "matt": "Matthew", "mat": "Matthew", "mk": "Mark", "mar": "Mark",
    "lk": "Luke", "luk": "Luke", "jn": "John", "joh": "John",
    "acts": "Acts", "rom": "Romans",
    "1cor": "1 Corinthians", "2cor": "2 Corinthians",
    "gal": "Galatians", "eph": "Ephesians", "phil": "Philippians",
    "col": "Colossians",
    "1thess": "1 Thessalonians", "1th": "1 Thessalonians",
    "2thess": "2 Thessalonians", "2th": "2 Thessalonians",
    "1tim": "1 Timothy", "2tim": "2 Timothy",
    "tit": "Titus", "phm": "Philemon", "phlm": "Philemon",
    "heb": "Hebrews", "jas": "James", "jam": "James",
    "1pet": "1 Peter", "1pe": "1 Peter",
    "2pet": "2 Peter", "2pe": "2 Peter",
    "1jn": "1 John", "1jo": "1 John",
    "2jn": "2 John", "3jn": "3 John",
    "jude": "Jude", "rev": "Revelation",
}


def get_book_suggestions(query: str) -> list[str]:
    """Return matching book names for a partial query."""
    if not query or len(query) < 2:
        return []

    q = query.strip().lower()
    books = get_book_names()

    # Check abbreviations first
    if q in ABBREVIATIONS:
        return [ABBREVIATIONS[q]]

    # Prefix match on full names
    matches = [b for b in books if b.lower().startswith(q)]
    if matches:
        return matches

    # Fuzzy: contains match
    matches = [b for b in books if q in b.lower()]
    return matches[:5]


def resolve_book_name(text: str) -> str:
    """Resolve a potentially abbreviated book name to its full name."""
    if not text:
        return text

    t = text.strip().lower()

    # Exact abbreviation match
    if t in ABBREVIATIONS:
        return ABBREVIATIONS[t]

    # Check full names (case-insensitive)
    books = get_book_names()
    for b in books:
        if b.lower() == t:
            return b

    # Prefix match — return first
    for b in books:
        if b.lower().startswith(t):
            return b

    return text  # Return as-is if no match
