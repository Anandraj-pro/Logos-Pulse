from datetime import date, timedelta
import re


def format_ordinal_date(d: date) -> str:
    day = d.day
    suffix = _ordinal_suffix(day)
    month_name = d.strftime("%B")
    return f"{day}{suffix} {month_name}"


def _ordinal_suffix(day: int) -> str:
    if 11 <= day <= 13:
        return "th"
    last_digit = day % 10
    if last_digit == 1:
        return "st"
    elif last_digit == 2:
        return "nd"
    elif last_digit == 3:
        return "rd"
    return "th"


def get_next_monday(from_date: date = None) -> date:
    d = from_date or date.today()
    days_ahead = 0 - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days=days_ahead)


def get_day_of_week(d: date) -> str:
    return d.strftime("%A").lower()


def get_week_dates(monday: date) -> list[date]:
    return [monday + timedelta(days=i) for i in range(6)]


def format_prayer_duration(minutes: int) -> str:
    if minutes <= 0:
        return "0 mins"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    parts = []
    if hours > 0:
        parts.append(f"{hours} hrs")
    if remaining_minutes > 0:
        parts.append(f"{remaining_minutes} mins")
    return " ".join(parts)


def format_chapters_display(book: str, chapters: list[int]) -> str:
    if not chapters or not book:
        return ""
    chapters_sorted = sorted(chapters)
    if _is_consecutive(chapters_sorted):
        if len(chapters_sorted) == 1:
            return f"{book} {chapters_sorted[0]}"
        return f"{book} {chapters_sorted[0]}\u2013{chapters_sorted[-1]}"
    else:
        chapter_str = ", ".join(str(c) for c in chapters_sorted)
        return f"{book} {chapter_str}"


def _is_consecutive(nums: list[int]) -> bool:
    if len(nums) <= 1:
        return True
    return nums[-1] - nums[0] == len(nums) - 1


def is_valid_youtube_url(url: str) -> bool:
    if not url:
        return True
    patterns = [
        r'https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'https?://youtu\.be/[\w-]+',
        r'https?://(www\.)?youtube\.com/shorts/[\w-]+',
    ]
    return any(re.match(p, url) for p in patterns)


def calculate_streaks(entry_dates: list[str]) -> tuple[int, int]:
    if not entry_dates:
        return 0, 0

    dates = sorted(set(date.fromisoformat(d) for d in entry_dates), reverse=True)
    today = date.today()

    # Current streak
    current_streak = 0
    check_date = today
    if dates and dates[0] < today:
        check_date = today - timedelta(days=1)

    for d in dates:
        if d == check_date:
            current_streak += 1
            check_date -= timedelta(days=1)
        elif d < check_date:
            break

    # Longest streak
    dates_asc = sorted(dates)
    longest_streak = 1 if dates_asc else 0
    current_run = 1
    for i in range(1, len(dates_asc)):
        if (dates_asc[i] - dates_asc[i - 1]).days == 1:
            current_run += 1
            longest_streak = max(longest_streak, current_run)
        else:
            current_run = 1

    return current_streak, longest_streak
