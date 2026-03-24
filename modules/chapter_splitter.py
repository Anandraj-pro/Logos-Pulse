import json
from datetime import date, timedelta
from modules.utils import get_day_of_week

READING_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]


def split_chapters(start_chapter: int, end_chapter: int, num_days: int = 6) -> dict:
    total = end_chapter - start_chapter + 1
    if total <= 0:
        return {day: [] for day in READING_DAYS[:num_days]}
    if num_days <= 0:
        return {}

    base_per_day = total // num_days
    remainder = total % num_days

    breakdown = {}
    current_chapter = start_chapter

    for i, day in enumerate(READING_DAYS[:num_days]):
        count = base_per_day + (1 if i < remainder else 0)
        day_chapters = list(range(current_chapter, current_chapter + count))
        breakdown[day] = day_chapters
        current_chapter += count

    return breakdown


def get_today_suggestion(entry_date: date, assignment: dict | None) -> dict | None:
    if not assignment:
        return None

    week_start = date.fromisoformat(assignment["week_start_date"])
    week_end = date.fromisoformat(assignment["week_end_date"])

    if not (week_start <= entry_date <= week_end):
        return None

    day_name = get_day_of_week(entry_date)
    breakdown = (
        json.loads(assignment["daily_breakdown"])
        if isinstance(assignment["daily_breakdown"], str)
        else assignment["daily_breakdown"]
    )

    chapters = breakdown.get(day_name, [])
    if not chapters:
        return None

    range_str = f"{chapters[0]}-{chapters[-1]}" if len(chapters) > 1 else str(chapters[0])

    return {
        "book": assignment["book"],
        "chapters": chapters,
        "range": range_str,
    }
