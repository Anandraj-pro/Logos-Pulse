# Product Requirements Document (PRD)
# Spiritual Growth Daily Tracker

**Document Version:** 1.1
**Date:** 2026-03-23
**Author:** BMAD Business Analyst
**Status:** Draft — Pending Stakeholder Review

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Goals & Success Metrics](#3-goals--success-metrics)
4. [User Personas](#4-user-personas)
5. [Core Features](#5-core-features)
6. [Information Architecture](#6-information-architecture)
7. [Data Model](#7-data-model)
8. [WhatsApp Integration Approach](#8-whatsapp-integration-approach)
9. [YouTube Integration Approach](#9-youtube-integration-approach)
10. [Weekly Assignment Management Workflow](#10-weekly-assignment-management-workflow)
11. [Technical Requirements](#11-technical-requirements)
12. [UI/UX Requirements](#12-uiux-requirements)
13. [Non-Functional Requirements](#13-non-functional-requirements)
14. [MVP Scope vs Future Enhancements](#14-mvp-scope-vs-future-enhancements)
15. [Feature: Sermon Notes](#15-feature-sermon-notes)
16. [Feature: Prayer Journal (Redesign)](#16-feature-prayer-journal-redesign)
17. [Bible Scripture Auto-Fetch Service](#17-bible-scripture-auto-fetch-service)
18. [Risks & Mitigations](#18-risks--mitigations)

---

## 1. Executive Summary

The **Spiritual Growth Daily Tracker** is a personal web application (PWA) designed for a single user, Bhargavi, to consistently track three daily spiritual disciplines — Prayer, Bible Reading, and Listening to the Word — and automatically share a formatted daily report with her pastor, Ps. Deepak, via WhatsApp each morning.

The application replaces a manual reporting process that is prone to being missed. It provides a simple daily input form, intelligent weekly Bible reading assignment splitting, sermon logging with YouTube links, a historical prayer journal, streak tracking for motivation, and automated WhatsApp message generation.

**Target Launch:** MVP within 4-6 weeks of development start.
**Platform:** Progressive Web App (mobile-responsive), with potential React Native expansion later.
**Users:** Single user (Bhargavi) with one message recipient (Ps. Deepak).

---

## 2. Problem Statement

### Current Situation
Bhargavi is committed to daily spiritual disciplines — prayer, Bible reading, and listening to sermons — and sends a daily morning report to her pastor, Ps. Deepak, via WhatsApp summarizing her activities. This process is entirely manual: she must remember to compose and send the message every morning.

### The Problem
- **Inconsistency:** Manual reporting leads to missed days. Life gets busy and the message is forgotten.
- **No Historical Record:** There is no centralized log of past spiritual activity. Once a WhatsApp message is sent, it is buried in chat history and hard to review.
- **No Structure for Bible Reading:** When the pastor assigns a book to read over a week, there is no tool to break that into manageable daily chunks or track progress against the assignment.
- **No Accountability Mechanism:** Without streaks or visual progress indicators, there is no reinforcement loop to maintain consistency.

### Desired Outcome
A lightweight, mobile-friendly app that makes daily logging take under 60 seconds, automatically formats the WhatsApp report, and provides a personal journal of spiritual growth over time.

---

## 3. Goals & Success Metrics

### Primary Goals

| # | Goal | Description |
|---|------|-------------|
| G1 | Eliminate missed reports | Automate WhatsApp message generation so sending takes one tap |
| G2 | Build a prayer journal | Store all daily entries for historical reflection and review |
| G3 | Structure Bible reading | Auto-split weekly assignments into daily targets with progress tracking |
| G4 | Enable consistency | Streak tracking and reminders to reinforce daily discipline |
| G5 | Keep it simple | Daily input should take less than 60 seconds |

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Daily report completion rate | 95%+ over any 30-day window | App analytics — entries logged per day |
| Time to complete daily entry | Under 60 seconds | UX observation / user feedback |
| Weekly Bible reading completion rate | 90%+ of assigned chapters read by Sunday | Assignment completion tracking |
| Streak length | Maintain 30+ day streaks regularly | Streak tracker data |
| User satisfaction | User continues using the app daily after 3 months | Retention observation |

---

## 4. User Personas

### Primary User: Bhargavi (App User)

- **Role:** Single user of the application
- **Demographics:** Young professional, committed Christian, tech-comfortable
- **Daily Routine:** Prays for at least 1 hour daily, reads assigned Bible chapters, watches sermons on YouTube
- **Pain Points:**
  - Forgets to send the daily WhatsApp report to her pastor
  - Has no centralized record of her spiritual activities
  - Manually splits weekly Bible reading assignments into daily goals
- **Goals:**
  - Never miss sending a daily report
  - Build a personal prayer/spiritual journal
  - See her consistency over time via streaks
- **Tech Comfort:** Comfortable with web apps and smartphones; uses WhatsApp and YouTube daily

### Recipient: Pastor Ps. Deepak

- **Role:** Receives the daily formatted report via WhatsApp
- **Interaction with App:** None — purely a recipient
- **Expectations:** Receives a clean, consistent daily message in the established format
- **Secondary Role:** Assigns weekly Bible reading on Sundays (this assignment is entered into the app by Bhargavi, not by the pastor directly)

---

## 5. Core Features

### F1: Daily Entry Form

**Description:** A single-screen form where Bhargavi logs her daily spiritual activities across all three tracking areas.

**Functional Requirements:**

| ID | Requirement | Priority |
|----|-------------|----------|
| F1.1 | The form SHALL display the current date, pre-filled and editable (to allow backdating if the entry is done the next morning) | Must |
| F1.2 | The Prayer section SHALL default to "1 Hour" with the ability to increase in 15-minute increments | Must |
| F1.3 | The Bible Reading section SHALL show the day's suggested chapters (derived from the weekly assignment) and allow the user to confirm or modify what was actually read | Must |
| F1.4 | The Listening to the Word section SHALL have fields for: sermon title, speaker name, and YouTube link | Must |
| F1.5 | The Listening to the Word section SHALL be optional (some days the user may not watch a sermon) | Must |
| F1.6 | The form SHALL have a single "Save & Generate Report" button | Must |
| F1.7 | The form SHALL validate that Prayer duration is greater than 0 and Bible Reading has at least one chapter logged before allowing save | Must |
| F1.8 | If an entry already exists for the selected date, the form SHALL load it for editing | Should |

**Acceptance Criteria:**
- Given the user opens the app, when it is a new day with no entry, then the form is blank with defaults applied (prayer = 1 hour, Bible reading = today's suggested chapters pre-checked).
- Given the user modifies the prayer duration to 1.5 hours, when they save, then the report shows "1 Hour 30 Minutes."
- Given the user has not watched a sermon, when they leave Listening to the Word empty and save, then the report omits that line or shows "None."

---

### F2: WhatsApp Report Generation & Sharing

**Description:** After saving a daily entry, the app generates a formatted message and provides a **"Copy to Clipboard"** button so the user can easily paste it into WhatsApp and send to Ps. Deepak. The app does NOT send via WhatsApp directly — the user copies the message and pastes it manually.

**Report Format:**
```
Good Morning Anna,
Praise the Lord!

Date: [Day]th/st/nd [Month]
Prayer: [Duration]
Bible Reading: [Book] [Start Chapter]-[End Chapter]
Listening to the Word: [Title] - [Speaker]
```

**Functional Requirements:**

| ID | Requirement | Priority |
|----|-------------|----------|
| F2.1 | The system SHALL generate the message in the exact format specified above | Must |
| F2.2 | The date SHALL use ordinal suffixes (1st, 2nd, 3rd, 4th, ..., 23rd) and full month name | Must |
| F2.3 | The greeting name ("Anna") SHALL be configurable in settings | Must |
| F2.4 | The system SHALL provide a prominent **"Copy to Clipboard"** button that copies the formatted message to the device clipboard | Must |
| F2.5 | On successful copy, the system SHALL show a visual confirmation (e.g., "Copied!" toast/snackbar) | Must |
| F2.6 | If the Listening to the Word entry includes a YouTube link, the link SHALL be included in the message on a new line below the sermon info | Should |
| F2.7 | After generating, the app SHALL show a **preview of the message** before the user taps "Copy to Clipboard" | Must |
| F2.8 | Optionally, the system MAY provide a secondary "Open WhatsApp" button using `wa.me` deep link as a convenience shortcut | Nice |
| F2.9 | The greeting name ("Anna") and pastor's name SHALL be configurable in settings | Must |

**Acceptance Criteria:**
- Given a completed daily entry for March 23 with Prayer = 1 Hour, Bible Reading = Luke 1-4, Sermon = "Faith that overcomes" by Ps. Samuel Patta, when the user taps "Copy to Clipboard," then the formatted message is copied and a "Copied!" confirmation appears. The user can then paste it directly into WhatsApp chat with Ps. Deepak.
- Given no sermon was logged, when the report is generated, then the "Listening to the Word" line reads "None" or is omitted entirely (configurable in settings).

---

### F3: Weekly Bible Reading Assignment Management

**Description:** Each Sunday, the pastor assigns a Bible reading goal for the upcoming week (Monday-Saturday). Bhargavi enters the assignment into the app, and the system automatically breaks it into daily reading targets.

**Functional Requirements:**

| ID | Requirement | Priority |
|----|-------------|----------|
| F3.1 | The system SHALL provide a "New Weekly Assignment" screen where the user enters: Bible book name, starting chapter, ending chapter, and week start date (defaults to next Monday) | Must |
| F3.2 | The system SHALL contain a reference database of Bible books with their chapter counts for validation | Must |
| F3.3 | Given a range of chapters and 6 reading days (Mon-Sat), the system SHALL auto-calculate daily reading targets, distributing chapters as evenly as possible | Must |
| F3.4 | The user SHALL be able to manually adjust the auto-generated daily split before confirming | Should |
| F3.5 | The daily entry form (F1) SHALL display the current day's assigned chapters from the active weekly assignment | Must |
| F3.6 | The system SHALL track progress against the weekly assignment: chapters completed vs. total assigned | Must |
| F3.7 | If the user reads ahead or falls behind, the system SHALL recalculate remaining daily targets for the rest of the week | Should |
| F3.8 | The system SHALL support assignments spanning multiple books (e.g., "Read Luke and John") | Could |
| F3.9 | Past weekly assignments SHALL be stored and viewable in the journal | Should |

**Acceptance Criteria:**
- Given the pastor assigns "Read all chapters of Luke by next Sunday," when Bhargavi enters Book = Luke, Start = 1, End = 24, then the system generates: Mon = Ch 1-4, Tue = Ch 5-8, Wed = Ch 9-12, Thu = Ch 13-16, Fri = Ch 17-20, Sat = Ch 21-24.
- Given Bhargavi reads 6 chapters on Monday instead of 4, when she opens Tuesday's form, then Tuesday's suggested chapters are recalculated to reflect the adjusted remaining chapters.

---

### F4: Prayer Journal / Historical Log

**Description:** All daily entries are saved and browsable as a personal spiritual journal.

**Functional Requirements:**

| ID | Requirement | Priority |
|----|-------------|----------|
| F4.1 | The system SHALL store every daily entry persistently | Must |
| F4.2 | The journal SHALL provide a calendar view where dates with entries are visually marked | Must |
| F4.3 | Tapping a date in the calendar SHALL open that day's full entry in read-only mode | Must |
| F4.4 | The journal SHALL provide a list view sorted by date (newest first) with summary cards showing date, prayer duration, chapters read, and sermon title | Must |
| F4.5 | The journal SHALL support filtering by: date range, Bible book, speaker name | Should |
| F4.6 | The journal SHALL support searching entries by keyword (sermon title, speaker, Bible book) | Should |
| F4.7 | The system SHALL allow exporting journal data as JSON or CSV | Could |

**Acceptance Criteria:**
- Given 30 days of entries exist, when the user opens the journal calendar view, then 30 dates are highlighted and each is tappable to view that entry.
- Given the user searches for "Samuel Patta," then all entries where the speaker is Samuel Patta are returned.

---

### F5: Streak Tracking & Consistency View

**Description:** Visual indicators showing the user's consistency in completing daily entries, designed to motivate continued discipline.

**Functional Requirements:**

| ID | Requirement | Priority |
|----|-------------|----------|
| F5.1 | The system SHALL calculate and display the current streak (consecutive days with a completed entry) | Must |
| F5.2 | The system SHALL display the longest streak ever achieved | Must |
| F5.3 | The dashboard SHALL show a weekly completion indicator (e.g., 6/6 days this week) | Must |
| F5.4 | The system SHALL display a monthly heatmap (similar to GitHub contribution graph) showing entry completion intensity | Should |
| F5.5 | The system SHALL show Bible reading progress as a percentage of the weekly assignment completed | Must |
| F5.6 | The system SHOULD show a congratulatory message when milestones are hit (7-day streak, 30-day streak, 100-day streak) | Should |

**Acceptance Criteria:**
- Given the user has logged entries for 15 consecutive days, when they view the dashboard, then "Current Streak: 15 days" is displayed.
- Given the user missed yesterday but logged today, then the current streak resets to 1 and the previous streak is preserved if it was the longest.

---

### F6: Morning Reminder / Push Notification

**Description:** A daily notification reminding the user to fill in their spiritual growth report.

**Functional Requirements:**

| ID | Requirement | Priority |
|----|-------------|----------|
| F6.1 | The PWA SHALL request notification permission on first use | Must |
| F6.2 | The system SHALL send a push notification at a configurable time each morning (default: 7:00 AM) | Must |
| F6.3 | The notification text SHALL be encouraging and spiritually themed (e.g., "Time to log your spiritual growth for today. Keep the streak going!") | Should |
| F6.4 | Tapping the notification SHALL open the app directly to the daily entry form | Must |
| F6.5 | If the user has already completed today's entry, the notification SHALL either not fire or show a different message (e.g., "Great job! Your report for today is ready.") | Should |
| F6.6 | The reminder time SHALL be configurable in settings | Should |

**Acceptance Criteria:**
- Given it is 7:00 AM and no entry exists for today, when the notification fires, then it reads an encouraging reminder and opens to the daily entry form on tap.

---

### F7: Settings & Configuration

**Description:** A settings screen for app personalization.

**Functional Requirements:**

| ID | Requirement | Priority |
|----|-------------|----------|
| F7.1 | The user SHALL be able to set the pastor's name, greeting name (e.g., "Anna"), and WhatsApp phone number | Must |
| F7.2 | The user SHALL be able to set the default prayer duration | Should |
| F7.3 | The user SHALL be able to configure the morning reminder time | Should |
| F7.4 | The user SHALL be able to toggle whether "Listening to the Word" is shown as "None" or omitted when empty | Should |
| F7.5 | The user SHALL be able to export/import all data (backup and restore) | Should |
| F7.6 | The settings SHALL persist in local storage and optionally sync to a backend | Must |

---

## 6. Information Architecture

```
Spiritual Growth Daily Tracker
|
+-- Dashboard (Home)
|   +-- Today's Status (entry complete / pending)
|   +-- Current Streak
|   +-- Weekly Bible Reading Progress Bar
|   +-- Quick Action: "Log Today's Entry"
|
+-- Daily Entry Form
|   +-- Date Selector
|   +-- Prayer Duration Input
|   +-- Bible Reading Input (with suggested chapters)
|   +-- Listening to the Word Input
|   +-- Save & Generate Report
|   +-- Message Preview + Send via WhatsApp
|
+-- Weekly Assignment
|   +-- Current Assignment Overview
|   +-- Daily Breakdown (auto-calculated)
|   +-- Progress Tracker
|   +-- New Assignment Form
|   +-- Assignment History
|
+-- Sermon Notes (NEW)
|   +-- Create New Sermon Note
|   |   +-- Title, Speaker, Date
|   |   +-- Two-Column Notes Area (Notes + Bible References)
|   |   +-- Learnings Section
|   |   +-- Key Takeaways Section
|   |   +-- Additional Thoughts Section
|   +-- Browse / Search Sermon Notes
|   +-- View Sermon Note (Read-Only)
|
+-- Prayer Journal (REDESIGNED)
|   +-- Category Tabs / Folders
|   |   +-- Personal
|   |   +-- Finance & Breakthroughs
|   |   +-- Spouse
|   |   +-- Job & Career
|   |   +-- Custom Categories
|   +-- Create New Prayer (Wizard)
|   |   +-- Step 1: Select Category
|   |   +-- Step 2: Purpose / Title
|   |   +-- Step 3: Prayer Text
|   |   +-- Step 4: Bible Scriptures
|   |   +-- Step 5: Confessions & Declarations
|   +-- Prayer Entry Detail View
|   +-- Prayer Status Tracking (Ongoing / Answered / Standing in Faith)
|
+-- Journal (Daily Entry History)
|   +-- Calendar View
|   +-- List View
|   +-- Entry Detail View
|   +-- Search & Filter
|
+-- Streaks & Stats
|   +-- Current Streak
|   +-- Longest Streak
|   +-- Monthly Heatmap
|   +-- Weekly Completion Rate
|
+-- Settings
    +-- Profile (greeting name, pastor info)
    +-- WhatsApp Configuration
    +-- Notification Preferences
    +-- Data Export / Import
    +-- About
```

---

## 7. Data Model

### Entity: DailyEntry

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | UUID | Unique identifier | Yes |
| date | Date | Entry date (YYYY-MM-DD), unique constraint | Yes |
| prayerDurationMinutes | Integer | Prayer duration in minutes (default: 60) | Yes |
| chaptersRead | JSON Array | List of chapters read, e.g., `[{"book": "Luke", "chapter": 1}, {"book": "Luke", "chapter": 2}]` | Yes |
| chaptersReadDisplay | String | Human-readable format, e.g., "Luke 1-4" | Yes (derived) |
| sermonTitle | String | Title of sermon watched | No |
| sermonSpeaker | String | Speaker name | No |
| sermonYoutubeUrl | String | YouTube URL | No |
| reportSent | Boolean | Whether the WhatsApp report was sent | Yes |
| reportSentAt | DateTime | Timestamp when report was sent | No |
| createdAt | DateTime | Entry creation timestamp | Yes |
| updatedAt | DateTime | Last modification timestamp | Yes |

### Entity: WeeklyAssignment

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | UUID | Unique identifier | Yes |
| weekStartDate | Date | Monday of the assignment week | Yes |
| weekEndDate | Date | Saturday of the assignment week | Yes |
| book | String | Bible book name (e.g., "Luke") | Yes |
| startChapter | Integer | First chapter in assignment | Yes |
| endChapter | Integer | Last chapter in assignment | Yes |
| totalChapters | Integer | Total chapters to read | Yes (derived) |
| dailyBreakdown | JSON | `{"monday": [1,2,3,4], "tuesday": [5,6,7,8], ...}` | Yes |
| status | Enum | ACTIVE, COMPLETED, PARTIAL | Yes |
| createdAt | DateTime | Assignment creation timestamp | Yes |

### Entity: AppSettings

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | UUID | Singleton record | Yes |
| greetingName | String | Name used in WhatsApp greeting (e.g., "Anna") | Yes |
| pastorName | String | Pastor's name (e.g., "Ps. Deepak") | Yes |
| pastorPhone | String | WhatsApp number with country code | Yes |
| defaultPrayerMinutes | Integer | Default prayer duration (default: 60) | Yes |
| reminderTimeHour | Integer | Hour for morning reminder (0-23) | Yes |
| reminderTimeMinute | Integer | Minute for morning reminder (0-59) | Yes |
| omitEmptySermon | Boolean | If true, omit "Listening to the Word" line when empty; if false, show "None" | Yes |

### Entity: BibleReference (Static / Seed Data)

| Field | Type | Description |
|-------|------|-------------|
| book | String | Bible book name (e.g., "Genesis") |
| chapterCount | Integer | Total chapters in the book (e.g., 50 for Genesis) |
| testament | Enum | OLD, NEW |
| orderIndex | Integer | Canonical order (1-66) |

### Entity: SermonNote (NEW)

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | UUID | Unique identifier | Yes |
| title | String | Title of the sermon or message | Yes |
| speaker | String | Pastor/speaker name | Yes |
| sermonDate | Date | Date the sermon was heard/watched | Yes |
| notesText | Text | Free-form notes taken during the sermon (left column content) | No |
| bibleReferences | JSON | Array of reference objects, e.g., `[{"reference": "Mark 1:1", "text": "The beginning of the gospel..."}, {"reference": "Luke 4:18-19", "text": "The Spirit of the Lord..."}]` | No |
| learnings | Text | "What I learned from this" free text reflection | No |
| keyTakeaways | Text | Bullet-point key takeaways (stored as newline-separated or JSON array) | No |
| additionalThoughts | Text | Any innovative or extra thoughts the user wants to add | No |
| createdAt | DateTime | Record creation timestamp | Yes |
| updatedAt | DateTime | Last modification timestamp | Yes |

### Entity: PrayerCategory (NEW)

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | UUID | Unique identifier | Yes |
| name | String | Category name (e.g., "Personal", "Finance & Breakthroughs") | Yes |
| icon | String | Icon identifier or emoji for the category | No |
| color | String | Hex color code for visual distinction (e.g., "#4A90D9") | No |
| isDefault | Boolean | Whether this is a system-provided default category | Yes |
| sortOrder | Integer | Display order of categories | Yes |
| createdAt | DateTime | Record creation timestamp | Yes |

### Entity: PrayerEntry (NEW)

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| id | UUID | Unique identifier | Yes |
| categoryId | UUID | Foreign key to PrayerCategory | Yes |
| title | String | Purpose or title of the prayer | Yes |
| prayerText | Text | The actual prayer text the user prays | Yes |
| scriptures | JSON | Array of scripture reference objects, e.g., `[{"reference": "Philippians 4:19", "text": "And my God will meet all your needs..."}]` | No |
| confessions | Text | Confession statements with mapped Bible verses | No |
| declarations | Text | Faith declaration statements with supporting verses | No |
| status | Enum | ONGOING, ANSWERED, STANDING_IN_FAITH | Yes |
| answeredDate | Date | Date when prayer was marked as answered | No |
| createdAt | DateTime | Record creation timestamp | Yes |
| updatedAt | DateTime | Last modification timestamp | Yes |

### Relationships

- **DailyEntry** has an implicit relationship to **WeeklyAssignment** through the date and book/chapter overlap.
- **WeeklyAssignment** generates suggested chapters for each **DailyEntry** during its active week.
- **PrayerEntry** belongs to one **PrayerCategory** (many-to-one).
- **SermonNote** is a standalone entity with no direct foreign key relationships to other tables.

---

## 8. WhatsApp Integration Approach

### Primary Approach: Copy to Clipboard (MVP)

**Method:** The app generates the formatted report message and copies it to the user's clipboard. The user then manually pastes it into WhatsApp and sends it to Ps. Deepak.

**Why Copy-Paste, Not Deep Links or API:**
- The user explicitly prefers a copy-paste workflow over automated WhatsApp integration.
- No dependency on `wa.me` deep link behavior (which varies across devices/browsers).
- No WhatsApp Business API, no backend, no cost.
- Works universally — any device, any browser, any WhatsApp version.

**How It Works:**
1. User completes daily entry and taps **"Save"**.
2. App constructs the formatted message string.
3. App shows a **message preview** with the exact text that will be copied.
4. User taps **"Copy to Clipboard"** button.
5. App copies the message using the Clipboard API (`navigator.clipboard.writeText()`).
6. App shows a **"Copied!"** confirmation toast/snackbar.
7. User switches to WhatsApp, opens chat with Ps. Deepak, pastes, and sends.
8. User can optionally return to the app and mark the report as sent (or it auto-marks after copy).

**Generated Message Example:**
```
Good Morning Anna,
Praise the Lord!

Date: 23rd March
Prayer: 1 Hour
Bible Reading: Luke 1-4
Listening to the Word: Faith that overcomes - Ps. Samuel Patta
https://youtu.be/DUgdZlAO3n4
```

**Advantages:**
- Zero cost — no API, no infrastructure.
- Works on every platform (mobile, desktop, any browser).
- User has full control — can edit the message before pasting if needed.
- No permissions or phone number configuration required.
- Simple, reliable, no edge cases.

**Clipboard API Fallback:**
- If `navigator.clipboard.writeText()` is unavailable (older browsers), fall back to `document.execCommand('copy')` with a temporary textarea.
- If all clipboard methods fail, show the message in a selectable text area so the user can manually select-all and copy.

### Optional Convenience: "Open WhatsApp" Button

As a secondary (non-primary) option, the app may also offer an "Open WhatsApp" button using `wa.me` deep links. This is a convenience shortcut, not the main workflow.

### Future Enhancement: WhatsApp Business API

For fully automated sending (no user action required), a future version could integrate with:
- **WhatsApp Business API** via providers like Twilio, MessageBird, or Meta's Cloud API.
- This would require a WhatsApp Business account, message template approval, and a backend server.
- This is explicitly out of scope for MVP.

---

## 9. YouTube Integration Approach

### MVP Approach: Manual Entry with Link Validation

**Method:** The user manually enters the sermon title, speaker name, and YouTube URL. The app validates and optionally enriches the data.

**Functional Flow:**
1. User types or pastes a YouTube URL into the "YouTube Link" field.
2. The app validates the URL format (must match `youtube.com/watch?v=`, `youtu.be/`, or `youtube.com/shorts/` patterns).
3. Optionally, the app uses the YouTube oEmbed endpoint (no API key required) to fetch the video title and auto-fill the sermon title field: `https://www.youtube.com/oembed?url={videoUrl}&format=json`
4. The user confirms or edits the auto-filled title and enters the speaker name.

**Advantages:**
- No YouTube API key required for oEmbed.
- Simple, low-complexity implementation.
- User retains control over the data.

**Validation Rules:**
- YouTube URL must be a valid URL matching known YouTube patterns.
- Sermon title is required if a YouTube link is provided.
- Speaker name is required if a YouTube link is provided.

### Future Enhancement: YouTube API Integration

A future version could use the YouTube Data API v3 to:
- Auto-fetch video title, channel name, thumbnail, and duration.
- Allow searching for videos within the app.
- This would require a Google API key (free tier: 10,000 quota units/day, more than sufficient).

---

## 10. Weekly Assignment Management Workflow

### Workflow Overview

```
Sunday: Pastor gives assignment verbally
           |
           v
Bhargavi opens app -> "New Weekly Assignment"
           |
           v
Enters: Book = "Luke", Chapters = 1 to 24
           |
           v
App calculates: 24 chapters / 6 days = 4 chapters/day
           |
           v
App shows daily breakdown:
  Mon: Luke 1-4
  Tue: Luke 5-8
  Wed: Luke 9-12
  Thu: Luke 13-16
  Fri: Luke 17-20
  Sat: Luke 21-24
           |
           v
User confirms or adjusts -> Assignment saved as ACTIVE
           |
           v
Mon-Sat: Daily entry form shows suggested chapters
           |
           v
User logs actual chapters read each day
           |
           v
If user reads ahead: remaining days recalculated
If user falls behind: remaining days recalculated
           |
           v
Saturday night: Assignment marked COMPLETED or PARTIAL
           |
           v
Sunday: New assignment cycle begins
```

### Chapter Distribution Algorithm

```
Input: totalChapters, readingDays (default: 6, Mon-Sat)

basePerDay = floor(totalChapters / readingDays)
remainder = totalChapters % readingDays

For each day (1 to readingDays):
  if day <= remainder:
    assign basePerDay + 1 chapters
  else:
    assign basePerDay chapters
```

**Example — Luke (24 chapters, 6 days):**
- 24 / 6 = 4 per day, remainder 0
- Each day gets exactly 4 chapters

**Example — Romans (16 chapters, 6 days):**
- 16 / 6 = 2 per day, remainder 4
- Days 1-4 get 3 chapters, Days 5-6 get 2 chapters
- Mon: 1-3, Tue: 4-6, Wed: 7-9, Thu: 10-12, Fri: 13-14, Sat: 15-16

### Dynamic Recalculation

When the user reads more or fewer chapters than suggested:
1. Calculate remaining unread chapters.
2. Calculate remaining reading days in the week.
3. Re-run the distribution algorithm with the remaining values.
4. Update the daily breakdown for the remaining days.

---

## 11. Technical Requirements

### Recommended Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Framework** | Streamlit (Python) | User already has Streamlit experience and existing hosted project; rapid development, built-in UI components |
| **Language** | Python 3.10+ | Native Streamlit language, rich ecosystem for date handling and data |
| **Data Storage (MVP)** | SQLite via `sqlite3` | Lightweight, file-based, zero-config, persistent on server |
| **Data Storage (Future)** | PostgreSQL (Supabase/Neon) or Firebase | If multi-device access or cloud backup is needed later |
| **UI Components** | Streamlit native (`st.form`, `st.metric`, `st.date_input`, `st.columns`) | No custom frontend code needed |
| **Charts/Visuals** | Streamlit + Plotly or Altair | Streak heatmaps, progress charts |
| **Clipboard** | `streamlit-clipboard` or custom JS via `st.components.v1.html()` | Copy-to-clipboard for WhatsApp message |
| **Hosting** | Streamlit Community Cloud | Already in use by the user; free, auto-deploy from GitHub |
| **Date Handling** | Python `datetime` + `calendar` | Built-in, no extra dependencies |
| **Bible API** | API.Bible or Bible-API.com (free tier) | Auto-fetch scripture text for Sermon Notes and Prayer Journal |

### Architecture: Streamlit Server-Side App

```
[Streamlit Community Cloud]
  +-- Streamlit App (Python)
  +-- SQLite Database (persistent file storage)
  +-- Session State (in-memory per session)
  +-- Copy-to-Clipboard (JS snippet for WhatsApp message)
  +-- Bible Scripture API Client (HTTP calls to fetch verse text)
```

**Key Architecture Decisions:**
- **Server-side rendering:** Streamlit handles all UI rendering server-side; the browser displays the result.
- **SQLite for persistence:** Data stored in a `.db` file on the server. Simple, reliable, no external DB needed for MVP.
- **No authentication for MVP:** Single-user app; Streamlit Cloud URL acts as access control (can add `st.secrets` password later).
- **Copy-to-clipboard via JS:** Streamlit doesn't have native clipboard support, so we inject a small JS snippet using `st.components.v1.html()` or use the `streamlit-clipboard` package.
- **No offline support:** Streamlit requires internet connectivity. This is acceptable since the primary use case (morning report) assumes the user is online.
- **Bible API integration:** External API used to resolve scripture references to full text. Cached locally in SQLite to minimize repeat API calls.

### Platform Support

| Platform | Support | Notes |
|----------|---------|-------|
| Mobile browser (Android/iOS) | Must | Streamlit is mobile-responsive by default |
| Desktop browser (Chrome/Safari/Edge) | Must | Full support |
| Offline | Not supported | Streamlit requires connectivity; acceptable for MVP |

---

## 12. UI/UX Requirements

### Design Principles

1. **Mobile-Responsive:** Streamlit is responsive by default; ensure all layouts work well on phone screens.
2. **Minimal Friction:** Daily entry should take fewer taps than typing a WhatsApp message manually.
3. **Warm & Spiritual Aesthetic:** Use Streamlit theming for soft, warm colors. Not clinical or corporate.
4. **Sidebar Navigation:** Use Streamlit's sidebar for page navigation (Dashboard, Entry, Journal, Sermon Notes, Prayer Journal, Assignment, Settings).

### Key Screens

#### Screen 1: Dashboard (Home)

```
+----------------------------------+
|  Spiritual Growth Tracker        |
|  Good Morning, Bhargavi          |
+----------------------------------+
|                                  |
|  [Current Streak: 15 days]      |
|                                  |
|  Today: March 23, 2026           |
|  Status: [ ] Not yet logged      |
|                                  |
|  +----------------------------+  |
|  |  LOG TODAY'S ENTRY  ->     |  |
|  +----------------------------+  |
|                                  |
|  Weekly Reading: Luke            |
|  [=========>        ] 12/24 ch   |
|                                  |
|  This Week: 5/6 days completed   |
+----------------------------------+
|  [Home] [Entry] [Journal] [Set]  |
+----------------------------------+
```

#### Screen 2: Daily Entry Form

```
+----------------------------------+
|  <- Back         March 23, 2026  |
+----------------------------------+
|                                  |
|  PRAYER                          |
|  Duration: [ - ]  1 Hour  [ + ] |
|                                  |
|  BIBLE READING                   |
|  Today's Goal: Luke 9-12        |
|  [x] Chapter 9                   |
|  [x] Chapter 10                  |
|  [x] Chapter 11                  |
|  [x] Chapter 12                  |
|                                  |
|  LISTENING TO THE WORD           |
|  Title: [Faith that overcomes  ] |
|  Speaker: [Ps. Samuel Patta   ] |
|  YouTube: [https://youtu.be/...] |
|                                  |
|  +----------------------------+  |
|  |   SAVE & GENERATE REPORT   |  |
|  +----------------------------+  |
+----------------------------------+
```

#### Screen 3: Report Preview & Send

```
+----------------------------------+
|  <- Back        Report Preview   |
+----------------------------------+
|                                  |
|  +----------------------------+  |
|  | Good Morning Anna,         |  |
|  | Praise the Lord!           |  |
|  |                            |  |
|  | Date: 23rd March           |  |
|  | Prayer: 1 Hour             |  |
|  | Bible Reading: Luke 9-12   |  |
|  | Listening to the Word:     |  |
|  | Faith that overcomes -     |  |
|  | Ps. Samuel Patta           |  |
|  +----------------------------+  |
|                                  |
|  +----------------------------+  |
|  | COPY TO CLIPBOARD          |  |
|  +----------------------------+  |
|                                  |
|  Copied! Paste in WhatsApp      |
|                                  |
+----------------------------------+
```

#### Screen 4: Weekly Assignment Setup

```
+----------------------------------+
|  <- Back     Weekly Assignment   |
+----------------------------------+
|                                  |
|  New Assignment                  |
|  Book: [Luke              v]     |
|  From Chapter: [1]               |
|  To Chapter: [24]                |
|  Week Starting: [Mon, Mar 23]    |
|                                  |
|  Suggested Breakdown:            |
|  Mon: Ch 1-4    [ Edit ]        |
|  Tue: Ch 5-8    [ Edit ]        |
|  Wed: Ch 9-12   [ Edit ]        |
|  Thu: Ch 13-16  [ Edit ]        |
|  Fri: Ch 17-20  [ Edit ]        |
|  Sat: Ch 21-24  [ Edit ]        |
|                                  |
|  +----------------------------+  |
|  |   CONFIRM ASSIGNMENT        |  |
|  +----------------------------+  |
+----------------------------------+
```

#### Screen 5: Journal (Calendar View)

```
+----------------------------------+
|  Prayer Journal     [List View]  |
+----------------------------------+
|                                  |
|       << March 2026 >>           |
|  Mo Tu We Th Fr Sa Su            |
|                          1       |
|   2  3  4  5  6  7  8           |
|   9 10 11 12 13 14 15           |
|  16 17 18 19 20 21 22           |
|  [23] 24 25 26 27 28 29         |
|  30 31                           |
|                                  |
|  (Filled dates highlighted)      |
|                                  |
|  March 23 - Entry Detail:        |
|  Prayer: 1 Hour                  |
|  Reading: Luke 9-12              |
|  Sermon: Faith that overcomes    |
+----------------------------------+
```

#### Screen 6: Streaks & Stats

```
+----------------------------------+
|  Your Progress                   |
+----------------------------------+
|                                  |
|  Current Streak    Longest       |
|  [ 15 days ]      [ 42 days ]   |
|                                  |
|  March 2026 Heatmap              |
|  (GitHub-style grid with         |
|   color intensity per day)       |
|                                  |
|  This Month: 22/23 days logged   |
|  Bible Reading: 95% on target    |
|  Total Prayer Hours: 24.5 hrs    |
|                                  |
+----------------------------------+
```

#### Screen 7: Sermon Notes — Create New (NEW)

```
+------------------------------------------+
|  <- Back           New Sermon Note        |
+------------------------------------------+
|                                           |
|  Title: [The Power of Faith            ]  |
|                                           |
|  Speaker: [v Bishop Samuel Patta      ]   |
|    ( ) Bishop Samuel Patta                |
|    ( ) Merlyn Patta                       |
|    ( ) Ps. Deepak Avinash                |
|    ( ) Custom: [________________]         |
|                                           |
|  Date: [March 23, 2026]                  |
|                                           |
|  +------------------+------------------+  |
|  |  MY NOTES        | BIBLE REFERENCES |  |
|  +------------------+------------------+  |
|  |                  |                  |  |
|  | Jesus showed us  | Mark 1:1        |  |
|  | that faith is    | "The beginning  |  |
|  | the key to       |  of the gospel  |  |
|  | miracles...      |  of Jesus..."   |  |
|  |                  |                  |  |
|  | The anointing    | Luke 4:18-19    |  |
|  | breaks every     | "The Spirit of  |  |
|  | yoke and sets    |  the Lord is    |  |
|  | captives free.   |  upon me..."    |  |
|  |                  |                  |  |
|  +------------------+------------------+  |
|                                           |
|  WHAT I LEARNED FROM THIS                 |
|  +--------------------------------------+ |
|  | Faith is not just belief but action.  | |
|  | When we step out in faith, God meets  | |
|  | us where we are...                    | |
|  +--------------------------------------+ |
|                                           |
|  KEY TAKEAWAYS                            |
|  * Faith requires action, not just words  |
|  * The anointing is for service           |
|  * God's power is made perfect in weak... |
|  [+ Add takeaway]                         |
|                                           |
|  ADDITIONAL THOUGHTS                      |
|  +--------------------------------------+ |
|  | I want to study more about the       | |
|  | anointing in the Old Testament...     | |
|  +--------------------------------------+ |
|                                           |
|  +--------------------------------------+ |
|  |          SAVE SERMON NOTE             | |
|  +--------------------------------------+ |
+------------------------------------------+
```

#### Screen 8: Sermon Notes — Browse (NEW)

```
+------------------------------------------+
|  Sermon Notes        [+ New Note]         |
+------------------------------------------+
|                                           |
|  Search: [________________________]       |
|  Filter by speaker: [All speakers  v]     |
|                                           |
|  +--------------------------------------+ |
|  | The Power of Faith                   | |
|  | Bishop Samuel Patta | Mar 23, 2026   | |
|  | 3 Bible references | 4 takeaways     | |
|  +--------------------------------------+ |
|  | Walking in the Spirit                | |
|  | Ps. Deepak Avinash | Mar 16, 2026   | |
|  | 5 Bible references | 3 takeaways     | |
|  +--------------------------------------+ |
|  | The Grace of God                     | |
|  | Merlyn Patta | Mar 9, 2026           | |
|  | 2 Bible references | 5 takeaways     | |
|  +--------------------------------------+ |
|                                           |
+------------------------------------------+
```

#### Screen 9: Prayer Journal — Category View (NEW)

```
+------------------------------------------+
|  Prayer Journal      [+ New Prayer]       |
+------------------------------------------+
|                                           |
| [Personal] [Finance] [Spouse] [Job] [+]  |
|                                           |
|  -- Personal Prayers --                   |
|                                           |
|  +--------------------------------------+ |
|  | Daily Strength & Guidance            | |
|  | Status: ONGOING                      | |
|  | Philippians 4:13, Isaiah 40:31       | |
|  +--------------------------------------+ |
|  | Spiritual Growth                     | |
|  | Status: STANDING IN FAITH            | |
|  | Ephesians 3:16-19, Colossians 1:10   | |
|  +--------------------------------------+ |
|  | Healing for my back pain             | |
|  | Status: ANSWERED (Mar 10)            | |
|  | James 5:15, Isaiah 53:5             | |
|  +--------------------------------------+ |
|                                           |
+------------------------------------------+
```

#### Screen 10: Prayer Journal — Create Prayer Wizard (NEW)

```
+------------------------------------------+
|  <- Back      New Prayer Entry            |
+------------------------------------------+
|  Step 2 of 5                              |
|  [====>                        ]          |
|                                           |
|  PURPOSE / TITLE                          |
|  What is this prayer about?               |
|  +--------------------------------------+ |
|  | Financial breakthrough for the       | |
|  | new business venture                 | |
|  +--------------------------------------+ |
|                                           |
|  +--------------------------------------+ |
|  |       <- Previous    Next ->          | |
|  +--------------------------------------+ |
+------------------------------------------+

--- Step 3: Prayer Text ---

+------------------------------------------+
|  Step 3 of 5                              |
|  [=========>                   ]          |
|                                           |
|  YOUR PRAYER                              |
|  Write your prayer below:                 |
|  +--------------------------------------+ |
|  | Lord, I come before You asking for   | |
|  | financial breakthrough. Open doors   | |
|  | of opportunity and bless the work    | |
|  | of my hands...                       | |
|  +--------------------------------------+ |
|                                           |
+------------------------------------------+

--- Step 4: Scriptures ---

+------------------------------------------+
|  Step 4 of 5                              |
|  [===============>             ]          |
|                                           |
|  BIBLE SCRIPTURES                         |
|  Add scripture references:                |
|  +--------------------------------------+ |
|  | Philippians 4:19                     | |
|  | "And my God will meet all your       | |
|  |  needs according to the riches of    | |
|  |  his glory in Christ Jesus."         | |
|  +--------------------------------------+ |
|  | Malachi 3:10                         | |
|  | "Bring the whole tithe into the      | |
|  |  storehouse... and see if I will     | |
|  |  not throw open the floodgates..."   | |
|  +--------------------------------------+ |
|  [+ Add Scripture Reference]              |
|                                           |
+------------------------------------------+

--- Step 5: Confessions & Declarations ---

+------------------------------------------+
|  Step 5 of 5                              |
|  [=======================>     ]          |
|                                           |
|  CONFESSIONS                              |
|  +--------------------------------------+ |
|  | I confess that God is my provider.   | |
|  | (Philippians 4:19)                   | |
|  | I confess that I am blessed going    | |
|  | in and blessed going out.            | |
|  | (Deuteronomy 28:6)                   | |
|  +--------------------------------------+ |
|                                           |
|  DECLARATIONS                             |
|  +--------------------------------------+ |
|  | I declare that no weapon formed      | |
|  | against my finances shall prosper.   | |
|  | (Isaiah 54:17)                       | |
|  | I declare that God opens doors that  | |
|  | no man can shut.                     | |
|  | (Revelation 3:8)                     | |
|  +--------------------------------------+ |
|                                           |
|  +--------------------------------------+ |
|  |          SAVE PRAYER ENTRY            | |
|  +--------------------------------------+ |
+------------------------------------------+
```

### Navigation

- **Streamlit Sidebar:** Dashboard, Daily Entry, Sermon Notes, Prayer Journal, Journal (Daily History), Weekly Assignment, Streaks, Settings
- Uses `st.sidebar.radio()` or Streamlit's multi-page app feature (`pages/` directory)

---

## 13. Non-Functional Requirements

### Performance

| Requirement | Target |
|-------------|--------|
| Page load time | Under 3 seconds on Streamlit Community Cloud |
| Daily entry save time | Under 500ms (SQLite write) |
| Time to generate report message | Under 200ms |
| Clipboard copy action | Under 100ms |
| Bible scripture auto-fetch | Under 2 seconds per reference (with caching) |

### Reliability

| Requirement | Target |
|-------------|--------|
| Data durability | SQLite database persisted on Streamlit Cloud. User advised to export backups periodically. |
| App availability | Dependent on Streamlit Community Cloud uptime (generally reliable). |
| Session state | Streamlit session state for in-progress form data; SQLite for permanent storage. |
| Bible API fallback | If Bible API is unreachable, allow manual entry of scripture text. Cached verses remain available. |

### Security & Privacy

| Requirement | Description |
|-------------|-------------|
| Data location | Data stored on Streamlit Community Cloud server (SQLite file). |
| Authentication (MVP) | No authentication for MVP. App URL is private/unlisted. |
| Authentication (Future) | Add simple password gate via `st.secrets` or Streamlit's built-in auth. |
| HTTPS | Streamlit Community Cloud provides HTTPS by default. |

### Accessibility

| Requirement | Description |
|-------------|-------------|
| Font sizing | Use Streamlit default sizing (already mobile-friendly) |
| Touch targets | Streamlit components are touch-friendly by default |
| Color contrast | Use high-contrast Streamlit theme |

---

## 14. MVP Scope vs Future Enhancements

### MVP (Phase 1) — Target: 2-3 Weeks

| Feature | Included |
|---------|----------|
| Daily entry form (prayer, Bible reading, sermon) | Yes |
| Message preview + **Copy to Clipboard** button | Yes |
| Weekly Bible reading assignment with auto-split | Yes |
| Suggested daily chapters on entry form | Yes |
| Prayer journal — calendar view and list view | Yes |
| Entry detail view (read-only) | Yes |
| Current streak and longest streak display | Yes |
| Weekly completion count | Yes |
| Settings (greeting name, pastor name) | Yes |
| SQLite persistent storage | Yes |
| Mobile-responsive (Streamlit default) | Yes |
| Bible book chapter count reference data | Yes |
| Hosted on Streamlit Community Cloud | Yes |

### Phase 1.5 — Sermon Notes & Prayer Journal — Target: 2-3 Weeks After Phase 1

| Feature | Included |
|---------|----------|
| Sermon Notes page — create, view, browse, search | Yes |
| Two-column notes layout (notes + Bible references) | Yes |
| Bible scripture auto-fetch for sermon notes | Yes |
| Speaker dropdown with defaults + custom entry | Yes |
| Sermon note sections (learnings, takeaways, thoughts) | Yes |
| Prayer Journal redesign — category-based organization | Yes |
| Wizard-style prayer entry creation (5-step flow) | Yes |
| Default prayer categories (Personal, Finance, Spouse, Job) | Yes |
| Custom prayer categories | Yes |
| Prayer status tracking (Ongoing, Answered, Standing in Faith) | Yes |
| Confessions and declarations with mapped verses | Yes |
| Bible scripture auto-fetch for prayer entries | Yes |
| Scripture text caching in SQLite | Yes |

### Phase 2 — Post-MVP Enhancements

| Feature | Description |
|---------|-------------|
| Monthly heatmap | GitHub-style contribution visualization using Plotly |
| Dynamic recalculation | Adjust remaining daily targets when user reads ahead/behind |
| YouTube oEmbed auto-fill | Fetch video title from YouTube URL automatically |
| Data export (JSON/CSV) | Backup and restore functionality |
| Multi-book assignments | Support assignments spanning multiple Bible books |
| Search and filter in journal | Keyword search across all entries |
| Streak milestone celebrations | Congratulatory messages at 7, 30, 100 days |
| Editable past entries | Modify previously saved entries |
| Simple password protection | Gate access via `st.secrets` or Streamlit auth |

### Phase 3 — Future Vision

| Feature | Description |
|---------|-------------|
| Cloud database (PostgreSQL) | Migrate from SQLite to cloud DB for reliability |
| WhatsApp Business API integration | Fully automated sending (no manual copy-paste) |
| React/React Native app | If Streamlit limitations become a blocker |
| Pastor dashboard | Read-only view for Ps. Deepak to see Bhargavi's progress |
| Multiple tracking categories | Add fasting, church attendance, or other disciplines |
| Devotional content integration | Surface daily Bible verses or devotional readings |
| Shared accountability groups | Multiple users in a group with shared visibility |
| Multi-user authentication via email | Allow other users to register and use the app independently |
| User-level data isolation | Each authenticated user sees only their own data |

---

## 15. Feature: Sermon Notes

### Overview

A dedicated sermon note-taking page, separate from the daily report. This is a journaling tool designed for capturing insights, scripture references, and reflections when the user attends sermons in person or watches sermon videos online.

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| F8.1 | The app SHALL provide a dedicated "Sermon Notes" page accessible from the sidebar navigation | Must |
| F8.2 | The user SHALL be able to create a new sermon note by entering: title, speaker, and sermon date | Must |
| F8.3 | The speaker field SHALL provide a dropdown with default options: "Bishop Samuel Patta", "Merlyn Patta", "Ps. Deepak Avinash" | Must |
| F8.4 | The speaker field SHALL allow custom entry if the speaker is not in the default list | Must |
| F8.5 | The sermon date SHALL default to today's date and be editable | Must |
| F8.6 | The note-taking area SHALL be displayed in a two-column layout: left column for free-form notes, right column for Bible references | Must |
| F8.7 | When the user types a Bible reference (e.g., "Mark 1:1", "Luke 4:18-19", "John 3:16") in the right column, the system SHALL auto-fetch and display the actual scripture text beside the reference | Must |
| F8.8 | The system SHALL recognize standard Bible reference formats including: "Book Chapter:Verse", "Book Chapter:StartVerse-EndVerse", and multi-chapter ranges like "Book StartChapter:StartVerse - EndChapter:EndVerse" | Must |
| F8.9 | Each sermon note SHALL include a "What I learned from this" section for free-text reflection | Must |
| F8.10 | Each sermon note SHALL include a "Key Takeaways" section for bullet-point items | Must |
| F8.11 | Each sermon note SHALL include an "Additional thoughts" section for innovative or supplementary ideas | Must |
| F8.12 | The user SHALL be able to save a sermon note and return to it later for editing | Must |
| F8.13 | The system SHALL provide a browse/list view of all past sermon notes, sorted by date (newest first) | Must |
| F8.14 | The list view SHALL show: title, speaker, date, count of Bible references, and count of key takeaways | Must |
| F8.15 | The system SHALL support searching sermon notes by title, speaker name, or content within notes | Should |
| F8.16 | The system SHALL support filtering sermon notes by speaker | Should |
| F8.17 | Sermon notes SHALL be viewable in a clean, read-only format suitable for review and reflection | Must |
| F8.18 | The user SHALL be able to delete a sermon note with a confirmation prompt | Should |
| F8.19 | If the Bible scripture API is unavailable, the user SHALL be able to manually type the scripture text | Must |
| F8.20 | Fetched scripture texts SHALL be cached locally in SQLite to avoid redundant API calls | Should |

### Data Model

**Table: sermon_notes**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique identifier |
| title | TEXT | NOT NULL | Title of the sermon or message |
| speaker | TEXT | NOT NULL | Name of the pastor or speaker |
| sermon_date | DATE | NOT NULL | Date the sermon was heard or watched |
| notes_text | TEXT | NULLABLE | Free-form notes taken during the sermon |
| bible_references | TEXT (JSON) | NULLABLE | JSON array of objects: `[{"reference": "Mark 1:1", "text": "The beginning of the gospel of Jesus Christ..."}, ...]` |
| learnings | TEXT | NULLABLE | Free text: "What I learned from this" |
| key_takeaways | TEXT | NULLABLE | Newline-separated bullet points or JSON array of strings |
| additional_thoughts | TEXT | NULLABLE | Free text for extra or innovative thoughts |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update time |

**Indexes:**
- `idx_sermon_notes_date` on `sermon_date` (for date-based sorting and filtering)
- `idx_sermon_notes_speaker` on `speaker` (for speaker-based filtering)

### Bible Reference Auto-Fetch Workflow

```
User types "Luke 4:18-19" in the Bible References column
        |
        v
System parses the reference string
        |
        v
System checks local SQLite cache for this reference
        |
    [Cached?]
    /       \
  Yes        No
   |          |
   v          v
Display    Call Bible API
cached     (e.g., API.Bible
text       or bible-api.com)
              |
              v
          Store response
          in cache table
              |
              v
          Display scripture
          text next to reference
```

### Acceptance Criteria

1. **AC-8.1:** Given the user navigates to "Sermon Notes" and taps "New Note," when they enter title = "The Power of Faith", speaker = "Bishop Samuel Patta" (from dropdown), date = March 23, 2026, then a new sermon note form is created with those fields populated.

2. **AC-8.2:** Given the user is in the two-column notes area, when they type "Mark 1:1" in the Bible References column and press Enter or tab away, then within 2 seconds the actual text of Mark 1:1 appears below the reference ("The beginning of the gospel of Jesus Christ, the Son of God.").

3. **AC-8.3:** Given the user types "Luke 4:18-19" as a reference, when the system fetches the scripture, then the full text of both verses 18 and 19 is displayed as a single block.

4. **AC-8.4:** Given the user has filled in all sections (notes, references, learnings, takeaways, thoughts), when they tap "Save," then the sermon note is persisted to SQLite and appears in the browse list.

5. **AC-8.5:** Given 10 sermon notes exist, when the user opens the Sermon Notes browse view, then all 10 notes are listed with title, speaker, date, reference count, and takeaway count visible.

6. **AC-8.6:** Given the user searches for "faith" in the search bar, then all sermon notes containing "faith" in the title or notes text are returned.

7. **AC-8.7:** Given the user taps a sermon note in the browse list, then it opens in a clean, readable view with all sections displayed: header info, two-column notes/references, learnings, takeaways, and additional thoughts.

8. **AC-8.8:** Given the Bible API is unreachable, when the user types a reference, then the system shows a message "Could not fetch scripture. Enter text manually." and provides an editable text field for the verse text.

---

## 16. Feature: Prayer Journal (Redesign)

### Overview

Transform the existing simple daily log viewer (F4) into a purpose-driven, categorized prayer journal system. Instead of merely reviewing past daily entries, the user can create structured prayer entries organized by life areas (categories), each with purpose, prayer text, scripture references, confessions, and faith declarations. This is a significant upgrade from the original F4 specification and becomes the primary prayer management tool.

**Note:** The original F4 (Prayer Journal / Historical Log) remains as a daily entry history browser. This new Prayer Journal (F9) is a separate, dedicated prayer management system.

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| F9.1 | The app SHALL provide a dedicated "Prayer Journal" page accessible from the sidebar navigation | Must |
| F9.2 | The Prayer Journal SHALL support multiple prayer categories displayed as tabs or a folder-like UI | Must |
| F9.3 | The system SHALL provide the following default categories pre-seeded on first use: "Personal", "Finance & Breakthroughs", "Spouse", "Job & Career" | Must |
| F9.4 | The user SHALL be able to create custom prayer categories with a name, optional icon, and optional color | Must |
| F9.5 | The user SHALL be able to rename or delete custom categories (default categories can be renamed but not deleted) | Should |
| F9.6 | Creating a new prayer entry SHALL follow a wizard-style flow with the following steps: (1) Select Category, (2) Enter Purpose/Title, (3) Write Prayer Text, (4) Add Bible Scriptures, (5) Add Confessions & Declarations | Must |
| F9.7 | Each wizard step SHALL be navigable with "Previous" and "Next" buttons, and a progress indicator showing the current step | Must |
| F9.8 | The wizard SHALL allow the user to skip optional steps (scriptures, confessions, declarations) and come back to them later | Should |
| F9.9 | Each prayer entry SHALL have a title/purpose field describing what the prayer is about | Must |
| F9.10 | Each prayer entry SHALL have a prayer text field where the user writes the actual prayer | Must |
| F9.11 | Each prayer entry SHALL support adding Bible scripture references with auto-fetch of the actual verse text (same mechanism as Sermon Notes) | Must |
| F9.12 | Each prayer entry SHALL have a "Confessions" section where the user writes confession statements, each optionally mapped to a Bible verse | Must |
| F9.13 | Each prayer entry SHALL have a "Declarations" section where the user writes faith declaration statements, each optionally mapped to a Bible verse | Must |
| F9.14 | Each prayer entry SHALL have a status field with the following options: "Ongoing", "Answered", "Standing in Faith" | Must |
| F9.15 | The default status for new prayer entries SHALL be "Ongoing" | Must |
| F9.16 | The user SHALL be able to update the status of a prayer entry at any time | Must |
| F9.17 | When a prayer is marked as "Answered," the system SHALL prompt for (or auto-fill) the answered date | Should |
| F9.18 | The Prayer Journal SHALL display all prayers within a selected category, sorted by status (Ongoing first, then Standing in Faith, then Answered) and by creation date | Must |
| F9.19 | Each prayer entry in the list view SHALL show: title, status badge (color-coded), scripture count, and last updated date | Must |
| F9.20 | The user SHALL be able to view a prayer entry in a full, clean read-only format with all sections displayed | Must |
| F9.21 | The user SHALL be able to edit an existing prayer entry (add more scriptures, update prayer text, modify confessions/declarations) | Must |
| F9.22 | The user SHALL be able to delete a prayer entry with a confirmation prompt | Should |
| F9.23 | The system SHALL display a summary count on each category tab showing: total prayers, ongoing count, and answered count | Should |
| F9.24 | Fetched scripture texts for prayer entries SHALL use the same cache as Sermon Notes to avoid duplicate API calls | Should |

### Data Model

**Table: prayer_categories**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique identifier |
| name | TEXT | NOT NULL, UNIQUE | Category name (e.g., "Personal") |
| icon | TEXT | NULLABLE | Icon identifier or emoji |
| color | TEXT | NULLABLE | Hex color code for visual distinction |
| is_default | INTEGER | NOT NULL, DEFAULT 0 | 1 if system-provided default, 0 if user-created |
| sort_order | INTEGER | NOT NULL | Display ordering |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation time |

**Default Seed Data:**

| name | icon | color | is_default | sort_order |
|------|------|-------|------------|------------|
| Personal | (person icon) | #4A90D9 | 1 | 1 |
| Finance & Breakthroughs | (money icon) | #7ED321 | 1 | 2 |
| Spouse | (heart icon) | #E91E63 | 1 | 3 |
| Job & Career | (briefcase icon) | #FF9800 | 1 | 4 |

**Table: prayer_entries**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT (UUID) | PRIMARY KEY | Unique identifier |
| category_id | TEXT (UUID) | NOT NULL, FOREIGN KEY -> prayer_categories.id | Category this prayer belongs to |
| title | TEXT | NOT NULL | Purpose or title of the prayer |
| prayer_text | TEXT | NOT NULL | The actual prayer text |
| scriptures | TEXT (JSON) | NULLABLE | JSON array: `[{"reference": "Philippians 4:19", "text": "And my God will meet all your needs..."}]` |
| confessions | TEXT | NULLABLE | Confession statements with inline verse references |
| declarations | TEXT | NULLABLE | Faith declaration statements with inline verse references |
| status | TEXT | NOT NULL, DEFAULT 'ONGOING' | One of: ONGOING, ANSWERED, STANDING_IN_FAITH |
| answered_date | DATE | NULLABLE | Date when prayer was marked as answered |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Record creation time |
| updated_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Last update time |

**Indexes:**
- `idx_prayer_entries_category` on `category_id` (for category-based queries)
- `idx_prayer_entries_status` on `status` (for status-based sorting)
- `idx_prayer_entries_created` on `created_at` (for date-based sorting)

### Prayer Entry Creation Wizard Flow

```
Step 1: SELECT CATEGORY
  User sees category tabs/cards
  Taps one to select (e.g., "Finance & Breakthroughs")
  Or taps [+ New Category] to create one
        |
        v
Step 2: PURPOSE / TITLE
  Text input: "What is this prayer about?"
  Example: "Financial breakthrough for new business"
        |
        v
Step 3: PRAYER TEXT
  Large text area: "Write your prayer"
  Example: "Lord, I come before You asking for..."
        |
        v
Step 4: BIBLE SCRIPTURES
  Add one or more scripture references
  Each reference auto-fetches verse text
  User can add, remove, or manually enter
  [Skip for now] option available
        |
        v
Step 5: CONFESSIONS & DECLARATIONS
  Two text areas:
    Confessions: "I confess that God is my provider (Phil 4:19)..."
    Declarations: "I declare no weapon formed against me... (Isa 54:17)"
  [Skip for now] option available
        |
        v
SAVE -> Prayer entry created with status = ONGOING
```

### Status Tracking

| Status | Color Badge | Description |
|--------|-------------|-------------|
| Ongoing | Blue | Active prayer; still being prayed for |
| Standing in Faith | Gold/Amber | Believing for this specific outcome; actively declaring |
| Answered | Green | God has answered this prayer; record the date |

### Acceptance Criteria

1. **AC-9.1:** Given the user opens the Prayer Journal page for the first time, then 4 default categories are displayed: "Personal", "Finance & Breakthroughs", "Spouse", "Job & Career".

2. **AC-9.2:** Given the user taps [+ New Prayer], when the wizard opens, then Step 1 shows all available categories for selection. The user selects "Finance & Breakthroughs" and proceeds.

3. **AC-9.3:** Given the user is on Step 2 of the wizard, when they enter "Financial breakthrough for new business" as the title and tap Next, then Step 3 (Prayer Text) is displayed.

4. **AC-9.4:** Given the user is on Step 4 (Scriptures), when they type "Philippians 4:19" and the system fetches the verse, then the text "And my God will meet all your needs according to the riches of his glory in Christ Jesus" is displayed beside the reference.

5. **AC-9.5:** Given the user completes all 5 wizard steps and taps Save, then the prayer entry is saved with status "Ongoing" and appears in the "Finance & Breakthroughs" category list.

6. **AC-9.6:** Given 5 prayer entries exist in the "Personal" category (3 Ongoing, 1 Standing in Faith, 1 Answered), when the user views the Personal tab, then entries are sorted: Ongoing first (3), then Standing in Faith (1), then Answered (1).

7. **AC-9.7:** Given the user taps on a prayer entry, when it opens in view mode, then all sections are displayed: title, prayer text, scriptures with full verse text, confessions, declarations, and status.

8. **AC-9.8:** Given the user changes a prayer's status from "Ongoing" to "Answered," then the system prompts for the answered date (defaults to today) and updates the entry. The category tab summary count reflects the change.

9. **AC-9.9:** Given the user taps [+ New Category], when they enter name = "Ministry", icon = (church icon), color = "#9C27B0", then the new category appears as a new tab in the Prayer Journal.

10. **AC-9.10:** Given the user skips Step 4 (Scriptures) and Step 5 (Confessions & Declarations) during creation, when they view the prayer later, then those sections show "Not yet added" with an [Edit] button to add them later.

---

## 17. Bible Scripture Auto-Fetch Service

### Overview

Both Sermon Notes (F8) and Prayer Journal (F9) require the ability to auto-fetch Bible scripture text when the user types a reference. This section defines the shared service that powers this functionality.

### Reference Parsing

The system SHALL recognize the following Bible reference formats:

| Format | Example | Parsed As |
|--------|---------|-----------|
| Book Chapter:Verse | John 3:16 | Book=John, Chapter=3, Verse=16 |
| Book Chapter:StartVerse-EndVerse | Luke 4:18-19 | Book=Luke, Chapter=4, Verses=18-19 |
| Book Chapter | Psalm 23 | Book=Psalm, Chapter=23 (all verses) |
| Numbered Book Chapter:Verse | 1 Corinthians 13:4 | Book=1 Corinthians, Chapter=13, Verse=4 |
| Range across chapters | Genesis 1:1-2:3 | Book=Genesis, Chapter 1 Verse 1 through Chapter 2 Verse 3 |

### API Options (Evaluated)

| API | Cost | Auth Required | Notes |
|-----|------|---------------|-------|
| **API.Bible** (api.scripture.api.bible) | Free tier available | API key (free registration) | Multiple translations, reliable |
| **bible-api.com** | Free | No key needed | Simple REST API, limited translations |
| **ESV API** (api.esv.org) | Free for personal use | API key | English Standard Version only |

**Recommended for MVP:** bible-api.com (no API key, simple REST, sufficient for personal use). Fallback: API.Bible with free-tier key.

### Caching Strategy

**Table: scripture_cache**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| reference | TEXT | PRIMARY KEY | Normalized reference string (e.g., "John 3:16") |
| text | TEXT | NOT NULL | Full scripture text |
| translation | TEXT | NOT NULL, DEFAULT 'KJV' | Bible translation used |
| fetched_at | DATETIME | NOT NULL | When this was fetched from API |

- Cache is shared between Sermon Notes and Prayer Journal.
- Cache entries never expire (scripture text does not change).
- Reduces API calls to one per unique reference across the entire app lifetime.

### Error Handling

| Scenario | Behavior |
|----------|----------|
| API unreachable (network error) | Show inline message: "Could not fetch scripture. Enter text manually." Provide editable text field. |
| Invalid reference (API returns 404) | Show inline message: "Reference not found. Check formatting." Allow manual entry. |
| Rate limited | Queue request and retry after delay. Show loading indicator. |
| Cached reference available | Return immediately from SQLite cache. No API call. |

### Acceptance Criteria

1. **AC-S.1:** Given the user types "John 3:16" in any scripture reference field, when the system has no cached entry, then it calls the Bible API, displays the verse text within 2 seconds, and caches the result.

2. **AC-S.2:** Given "John 3:16" has been fetched previously, when the user types it again (in any context), then the cached text is displayed immediately with no API call.

3. **AC-S.3:** Given the Bible API is unreachable, when the user types a reference, then the system shows a fallback manual entry field within 3 seconds.

---

## 18. Risks & Mitigations

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Streamlit Community Cloud downtime** | Low | Medium | Mitigation: Streamlit Cloud is generally reliable. Data persists in SQLite file. Export feature allows local backups. |
| **SQLite data loss** (Streamlit Cloud resets file system) | Medium | High | Mitigation: Streamlit Cloud persists files between reboots. Add CSV/JSON export for manual backups. Phase 2: migrate to cloud database. |
| **Clipboard API not available on some mobile browsers** | Low | Medium | Mitigation: Fallback to displaying message in a selectable text area for manual copy. |
| **No push notifications in Streamlit** | High | Medium | Mitigation: User sets a personal phone alarm/reminder to open the app each morning. Not a Streamlit capability. |
| **Bible API unavailability or deprecation** | Low | Medium | Mitigation: Local caching reduces dependency. Manual entry fallback always available. Can switch between multiple free Bible APIs. |
| **Bible reference parsing edge cases** | Medium | Low | Mitigation: Support common formats first. Allow manual text entry as fallback. Iteratively improve parser based on user input patterns. |
| **Two-column layout on mobile screens** | Medium | Medium | Mitigation: On narrow screens, stack columns vertically (notes above, references below) using Streamlit responsive columns. |

### Product Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **User stops using the app after initial enthusiasm** | Medium | High | Mitigation: Streak tracking, morning reminders, and milestone celebrations create habit loops. Keep the daily flow ultra-simple (under 60 seconds). |
| **Pastor changes the reporting format** | Low | Low | Mitigation: Message template is configurable in settings (Phase 2). MVP format is based on the established pattern. |
| **User wants to use on multiple devices** | Medium | Medium | Mitigation: MVP is single-device. Phase 3 adds cloud sync. In the interim, export/import provides manual transfer. |
| **Sermon Notes become underused** | Medium | Low | Mitigation: Keep the creation flow simple. Allow partially filled notes. The user can add learnings and takeaways later. |
| **Prayer Journal wizard feels too long** | Medium | Medium | Mitigation: Allow skipping optional steps. Allow saving at any step and completing later. Show clear progress indicator. |

### Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **SQLite file corruption** | Low | High | Mitigation: Regular CSV export. Phase 2 adds cloud database backup. |
| **Streamlit Community Cloud storage limits** | Low | Low | Mitigation: SQLite file for a single user's daily entries will stay small (< 1MB for years of data). |
| **Scripture cache grows large** | Low | Low | Mitigation: Even thousands of cached verses would be under 5MB. Not a concern for single-user app. |

---

## Appendix A: Bible Books Reference Data

The app will include a complete reference dataset of all 66 Bible books with chapter counts. Sample:

| Book | Chapters | Testament |
|------|----------|-----------|
| Genesis | 50 | Old |
| Exodus | 40 | Old |
| ... | ... | ... |
| Matthew | 28 | New |
| Mark | 16 | New |
| Luke | 24 | New |
| John | 21 | New |
| Acts | 28 | New |
| Romans | 16 | New |
| ... | ... | ... |
| Revelation | 22 | New |

Full dataset (all 66 books) will be embedded as a static JSON file in the application.

---

## Appendix B: WhatsApp Message Template

```
Good Morning {greetingName},
Praise the Lord!

Date: {ordinalDay} {monthName}
Prayer: {prayerDuration}
Bible Reading: {bookName} {startChapter}-{endChapter}
Listening to the Word: {sermonTitle} - {speakerName}
```

**Variable Definitions:**

| Variable | Source | Example |
|----------|--------|---------|
| `{greetingName}` | Settings.greetingName | "Anna" |
| `{ordinalDay}` | Entry date, formatted with ordinal suffix | "23rd" |
| `{monthName}` | Entry date, full month name | "March" |
| `{prayerDuration}` | Derived from prayerDurationMinutes | "1 Hour", "1 Hour 30 Minutes" |
| `{bookName}` | From chapters read | "Luke" |
| `{startChapter}` | First chapter in today's reading | "1" |
| `{endChapter}` | Last chapter in today's reading | "4" |
| `{sermonTitle}` | DailyEntry.sermonTitle | "Faith that overcomes" |
| `{speakerName}` | DailyEntry.sermonSpeaker | "Ps. Samuel Patta" |

**Duration Formatting Rules:**
- 60 minutes = "1 Hour"
- 90 minutes = "1 Hour 30 Minutes"
- 120 minutes = "2 Hours"
- 45 minutes = "45 Minutes"

---

*End of PRD*
*Document prepared by BMAD Business Analyst*
*Next step: Review with stakeholder, then hand off to Architect for technical design.*
