"""
Spiritual Growth Score — composite metric for tracking spiritual maturity.

Score Components (0-100 each, weighted average):
1. Consistency (40%) — streak length + weekly completion rate
2. Quantity (30%) — prayer minutes + chapters read (vs benchmarks)
3. Diversity (20%) — variety of books read, sermon notes, prayer entries
4. Engagement (10%) — fasting, goals, testimonies, journal activity

Growth Levels:
  0-19:  Seed       🌱
  20-39: Sprout     🌿
  40-59: Sapling    🌳
  60-79: Tree       🌲
  80-100: Forest    🌟
"""

from datetime import date, timedelta
from modules.supabase_client import get_admin_client


LEVELS = [
    (0, "\U0001f331", "Seed", "Every journey starts with a seed of faith"),
    (20, "\U0001f33f", "Sprout", "Your faith is taking root"),
    (40, "\U0001f333", "Sapling", "Growing stronger every day"),
    (60, "\U0001f332", "Tree", "Deeply rooted and bearing fruit"),
    (80, "\U0001f31f", "Forest", "A beacon of faithfulness"),
]


def get_level(score: int) -> tuple:
    """Returns (emoji, name, description) for a score."""
    for threshold, emoji, name, desc in reversed(LEVELS):
        if score >= threshold:
            return emoji, name, desc
    return LEVELS[0][1], LEVELS[0][2], LEVELS[0][3]


def calculate_growth_score(user_id: str) -> dict:
    """Calculate the spiritual growth score for a user.
    Returns dict with total score, component scores, and level info.
    """
    admin = get_admin_client()
    today = date.today()
    thirty_days_ago = (today - timedelta(days=29)).isoformat()
    today_str = today.isoformat()

    # Fetch 30 days of entries
    entries = admin.table("daily_entries") \
        .select("date, prayer_minutes, bible_book, chapters_read, sermon_title, fasted") \
        .eq("user_id", user_id) \
        .gte("date", thirty_days_ago) \
        .lte("date", today_str) \
        .order("date") \
        .execute()
    entries_data = entries.data or []

    # Get prayer benchmark
    profile = admin.table("user_profiles") \
        .select("prayer_benchmark_min") \
        .eq("user_id", user_id) \
        .execute()
    benchmark = 60
    if profile.data:
        benchmark = profile.data[0].get("prayer_benchmark_min", 60)

    # --- 1. Consistency Score (0-100) ---
    days_logged = len(entries_data)
    days_possible = min(30, (today - date.fromisoformat(thirty_days_ago)).days + 1)
    completion_rate = days_logged / days_possible if days_possible > 0 else 0

    # Streak bonus
    entry_dates = sorted(set(e["date"] for e in entries_data))
    streak = 0
    for i in range(len(entry_dates) - 1, -1, -1):
        d = date.fromisoformat(entry_dates[i])
        expected = today - timedelta(days=len(entry_dates) - 1 - i)
        if d == expected or (today - d).days <= 1:
            streak += 1
        else:
            break

    streak_bonus = min(streak / 30 * 40, 40)  # Up to 40 points for 30-day streak
    consistency = min(int(completion_rate * 60 + streak_bonus), 100)

    # --- 2. Quantity Score (0-100) ---
    total_prayer = sum(e.get("prayer_minutes", 0) for e in entries_data)
    total_chapters = 0
    for e in entries_data:
        cr = e.get("chapters_read")
        if cr:
            if isinstance(cr, list):
                total_chapters += len(cr)
            elif isinstance(cr, str):
                import json
                try:
                    total_chapters += len(json.loads(cr))
                except Exception:
                    pass

    prayer_target = benchmark * days_possible
    prayer_score = min(total_prayer / prayer_target * 100, 100) if prayer_target > 0 else 0

    # ~3 chapters/day target
    chapters_target = days_possible * 3
    chapters_score = min(total_chapters / chapters_target * 100, 100) if chapters_target > 0 else 0

    quantity = int((prayer_score + chapters_score) / 2)

    # --- 3. Diversity Score (0-100) ---
    unique_books = set()
    has_sermons = 0
    for e in entries_data:
        if e.get("bible_book"):
            unique_books.add(e["bible_book"])
        if e.get("sermon_title"):
            has_sermons += 1

    # Get prayer and sermon note counts
    prayer_count = admin.table("prayer_entries") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .execute()
    sermon_count = admin.table("sermon_notes") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .execute()

    books_score = min(len(unique_books) / 5 * 40, 40)  # 5 books = 40 points
    sermon_score = min((sermon_count.count or 0) / 3 * 30, 30)  # 3 notes = 30 points
    prayer_diversity = min((prayer_count.count or 0) / 5 * 30, 30)  # 5 prayers = 30 points

    diversity = int(books_score + sermon_score + prayer_diversity)
    diversity = min(diversity, 100)

    # --- 4. Engagement Score (0-100) ---
    fasting_days = sum(1 for e in entries_data if e.get("fasted"))
    goals = admin.table("personal_goals") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .eq("status", "active") \
        .execute()
    testimonies = admin.table("testimonies") \
        .select("id", count="exact") \
        .eq("user_id", user_id) \
        .execute()

    fasting_score = min(fasting_days / 4 * 40, 40)  # 4 fasts/month = 40 points
    goals_score = min((goals.count or 0) / 2 * 30, 30)  # 2 active goals = 30 points
    testimony_score = min((testimonies.count or 0) * 30, 30)  # 1 testimony = 30 points

    engagement = int(fasting_score + goals_score + testimony_score)
    engagement = min(engagement, 100)

    # --- Weighted Total ---
    total = int(consistency * 0.4 + quantity * 0.3 + diversity * 0.2 + engagement * 0.1)
    total = min(total, 100)

    emoji, level_name, level_desc = get_level(total)

    return {
        "total": total,
        "consistency": consistency,
        "quantity": quantity,
        "diversity": diversity,
        "engagement": engagement,
        "level_emoji": emoji,
        "level_name": level_name,
        "level_desc": level_desc,
        "stats": {
            "days_logged": days_logged,
            "streak": streak,
            "total_prayer_minutes": total_prayer,
            "total_chapters": total_chapters,
            "unique_books": len(unique_books),
            "fasting_days": fasting_days,
        },
    }
