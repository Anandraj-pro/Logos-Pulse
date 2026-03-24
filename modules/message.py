from datetime import date, datetime
from modules.utils import format_ordinal_date, format_prayer_duration


def _get_greeting() -> str:
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"


def format_whatsapp_message(
    entry_date: date,
    prayer_minutes: int,
    chapters_display: str,
    sermon_title: str | None,
    sermon_speaker: str | None,
    youtube_link: str | None,
    greeting_name: str,
    omit_empty_sermon: bool,
) -> str:
    date_str = format_ordinal_date(entry_date)
    duration_str = format_prayer_duration(prayer_minutes)
    greeting = _get_greeting()

    lines = [
        f"{greeting} {greeting_name},",
        "Praise the Lord! \U0001f64f",
        "",
        f"Date: {date_str}",
        f"Prayer: {duration_str}",
        f"Bible Reading: {chapters_display}",
    ]

    has_sermon = sermon_title and sermon_title.strip()
    if has_sermon:
        speaker_part = f" - {sermon_speaker}" if sermon_speaker else ""
        lines.append(f"Listening to the Word: {sermon_title}{speaker_part}")
        if youtube_link and youtube_link.strip():
            lines.append(youtube_link.strip())
    elif not omit_empty_sermon:
        lines.append("Listening to the Word: None")

    return "\n".join(lines)
