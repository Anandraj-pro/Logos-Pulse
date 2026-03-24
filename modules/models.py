from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class DailyEntry:
    id: Optional[int] = None
    date: str = ""
    prayer_minutes: int = 60
    bible_book: Optional[str] = None
    chapters_read: list[int] = field(default_factory=list)
    chapters_display: Optional[str] = None
    sermon_title: Optional[str] = None
    sermon_speaker: Optional[str] = None
    youtube_link: Optional[str] = None
    report_copied: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "DailyEntry":
        return cls(
            id=row["id"],
            date=row["date"],
            prayer_minutes=row["prayer_minutes"],
            bible_book=row["bible_book"],
            chapters_read=json.loads(row["chapters_read"]) if row["chapters_read"] else [],
            chapters_display=row["chapters_display"],
            sermon_title=row["sermon_title"],
            sermon_speaker=row["sermon_speaker"],
            youtube_link=row["youtube_link"],
            report_copied=bool(row["report_copied"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )


@dataclass
class WeeklyAssignment:
    id: Optional[int] = None
    book: str = ""
    start_chapter: int = 1
    end_chapter: int = 1
    total_chapters: int = 0
    week_start_date: str = ""
    week_end_date: str = ""
    daily_breakdown: dict = field(default_factory=dict)
    status: str = "ACTIVE"
    created_at: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "WeeklyAssignment":
        return cls(
            id=row["id"],
            book=row["book"],
            start_chapter=row["start_chapter"],
            end_chapter=row["end_chapter"],
            total_chapters=row["total_chapters"],
            week_start_date=row["week_start_date"],
            week_end_date=row["week_end_date"],
            daily_breakdown=json.loads(row["daily_breakdown"]) if isinstance(row["daily_breakdown"], str) else row["daily_breakdown"],
            status=row["status"],
            created_at=row["created_at"],
        )
