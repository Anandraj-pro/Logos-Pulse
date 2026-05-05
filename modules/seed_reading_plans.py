"""
Seed the 3 built-in Bible reading plans into reading_plans + reading_plan_days.
Idempotent — skips any plan whose name already exists.
"""

from modules.supabase_client import get_admin_client

NT_BOOKS = [
    ("Matthew", 28), ("Mark", 16), ("Luke", 24), ("John", 21),
    ("Acts", 28), ("Romans", 16), ("1 Corinthians", 16), ("2 Corinthians", 13),
    ("Galatians", 6), ("Ephesians", 6), ("Philippians", 4), ("Colossians", 4),
    ("1 Thessalonians", 5), ("2 Thessalonians", 3), ("1 Timothy", 6), ("2 Timothy", 4),
    ("Titus", 3), ("Philemon", 1), ("Hebrews", 13), ("James", 5),
    ("1 Peter", 5), ("2 Peter", 3), ("1 John", 5), ("2 John", 1),
    ("3 John", 1), ("Jude", 1), ("Revelation", 22),
]

PSALMS_BOOKS = [("Psalms", 150)]

GOSPELS_BOOKS = [
    ("Matthew", 28), ("Mark", 16), ("Luke", 24), ("John", 21),
]

PLANS = [
    {
        "name": "NT in 90 Days",
        "description": "Read the entire New Testament in 90 days — about 3 chapters daily.",
        "total_days": 90,
        "books": NT_BOOKS,
    },
    {
        "name": "Psalms in 30 Days",
        "description": "Read all 150 Psalms in 30 days — 5 chapters daily.",
        "total_days": 30,
        "books": PSALMS_BOOKS,
    },
    {
        "name": "Gospels in 28 Days",
        "description": "Read all 4 Gospels in 28 days — Matthew, Mark, Luke, and John.",
        "total_days": 28,
        "books": GOSPELS_BOOKS,
    },
]


def _make_days(books, total_days):
    """Distribute book chapters across total_days. Each day reads from one book only."""
    total_chapters = sum(ch for _, ch in books)
    days_per_book = []
    remaining_days = total_days

    for i, (book, chapters) in enumerate(books):
        if i == len(books) - 1:
            d = max(1, remaining_days)
        else:
            d = max(1, min(chapters, round(chapters / total_chapters * total_days)))
        days_per_book.append(d)
        remaining_days -= d

    rows = []
    day_num = 1
    for (book, chapters), num_days in zip(books, days_per_book):
        num_days = max(1, min(num_days, chapters))
        base = chapters // num_days
        extra = chapters % num_days
        ch = 1
        for d in range(num_days):
            count = base + (1 if d < extra else 0)
            end = ch + count - 1
            rows.append((day_num, book, ch, end))
            ch = end + 1
            day_num += 1

    return rows


def seed_reading_plans() -> dict:
    """Insert the 3 built-in plans. Returns {inserted, skipped}."""
    admin = get_admin_client()
    inserted = 0
    skipped = 0

    for plan_def in PLANS:
        existing = admin.table("reading_plans") \
            .select("id") \
            .eq("name", plan_def["name"]) \
            .execute()
        if existing.data:
            skipped += 1
            continue

        plan_result = admin.table("reading_plans").insert({
            "name": plan_def["name"],
            "description": plan_def["description"],
            "total_days": plan_def["total_days"],
            "created_by": None,
        }).execute()

        if not plan_result.data:
            continue

        plan_id = plan_result.data[0]["id"]
        day_rows = _make_days(plan_def["books"], plan_def["total_days"])

        batch = [
            {"plan_id": plan_id, "day_number": dn, "book": book,
             "chapter_start": cs, "chapter_end": ce}
            for dn, book, cs, ce in day_rows
        ]
        # Insert in chunks to stay within Supabase limits
        chunk_size = 50
        for i in range(0, len(batch), chunk_size):
            admin.table("reading_plan_days").insert(batch[i:i + chunk_size]).execute()

        inserted += 1

    return {"inserted": inserted, "skipped": skipped}
