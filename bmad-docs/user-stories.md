# User Stories - Spiritual Growth Daily Tracker

**Document Version:** 1.0
**Date:** 2026-03-23
**Status Legend:**
- **Built** -- Feature exists and works in the current codebase
- **Needs Work** -- Partially built but missing pieces or UX improvements needed
- **Not Started** -- Not yet implemented

---

## Section 1: Daily Assignment (Report to Ps. Deepak)

### US-01: Dashboard Overview
**As a** user, **I want to** see a dashboard with my current streak, longest streak, weekly completion count, and today's entry status, **so that** I can quickly assess my spiritual discipline at a glance.

**Acceptance Criteria:**
- [x] Dashboard displays current streak in days
- [x] Dashboard displays longest streak in days
- [x] Dashboard shows weekly completion count (e.g., 5/6 days)
- [x] Dashboard shows time-of-day greeting with configurable name
- [x] Dashboard shows today's entry summary if completed, or a warning if not
- [x] Dashboard shows weekly Bible reading progress bar if an active assignment exists

**Status:** Built

---

### US-02: Daily Entry Form - Prayer Duration
**As a** user, **I want to** log my prayer duration using a slider with 15-minute increments, **so that** I can quickly record how long I prayed.

**Acceptance Criteria:**
- [x] Prayer duration slider with 15-minute increments (15 to 180 minutes)
- [x] Default value loaded from settings (default 60 minutes)
- [x] Existing entry pre-fills the prayer value when editing

**Status:** Built

---

### US-03: Daily Entry Form - Bible Reading
**As a** user, **I want to** select the Bible book and chapters I read today, **so that** my reading is accurately logged.

**Acceptance Criteria:**
- [x] Book selector with all 66 Bible books
- [x] Chapter multi-select based on the selected book's chapter count
- [x] Auto-suggests today's chapters from the active weekly assignment
- [x] Validation: at least one chapter must be selected before saving
- [x] Existing entry pre-fills chapters when editing

**Status:** Built

---

### US-04: Daily Entry Form - Listening to the Word
**As a** user, **I want to** optionally log a sermon I watched (title, speaker, YouTube link), **so that** my sermon viewing is part of my daily report.

**Acceptance Criteria:**
- [x] Sermon title, speaker name, and YouTube link text fields
- [x] All fields are optional (sermon section is not required)
- [x] YouTube URL validation (accepts standard YouTube URL patterns)
- [x] Existing entry pre-fills values when editing

**Status:** Built

---

### US-05: In-App Bible Reader
**As a** user, **I want to** read Bible chapters directly within the app, **so that** I can read and log my progress in one place without switching apps.

**Acceptance Criteria:**
- [x] Book and chapter selector that defaults to today's assigned reading
- [x] Bible text fetched and displayed in a warm, readable format with verse numbers
- [x] "Mark Chapter Done" button to track completed chapters
- [x] Previous/Next chapter navigation buttons
- [x] Completed chapters shown as green pills
- [x] Reading progress bar showing how many of today's target chapters are done
- [x] Completed chapters auto-populate the Log Entry tab's chapter selection

**Status:** Built

---

### US-06: Save Entry and Generate Report
**As a** user, **I want to** save my daily entry and have the WhatsApp report message automatically generated, **so that** I don't have to manually compose the message.

**Acceptance Criteria:**
- [x] "Save & Generate Report" button saves entry to SQLite
- [x] WhatsApp message generated in the correct format (greeting, date with ordinal suffix, prayer duration, Bible reading, sermon info)
- [x] Greeting name pulled from settings
- [x] If sermon is empty and "omit empty sermon" setting is on, the line is omitted

**Status:** Built

---

### US-07: Report Preview and Copy to Clipboard
**As a** user, **I want to** preview the formatted WhatsApp message and copy it to my clipboard with one tap, **so that** I can paste it into WhatsApp quickly.

**Acceptance Criteria:**
- [x] Report tab shows the formatted message preview
- [x] "Copy to Clipboard" button using Clipboard API with fallback to execCommand
- [x] "Copied!" confirmation message appears after copying
- [x] Report marked as copied in the database

**Status:** Built

---

### US-08: Editable Entry Date
**As a** user, **I want to** select a past date when logging an entry, **so that** I can backfill entries I missed (e.g., logging the next morning).

**Acceptance Criteria:**
- [x] Date picker defaults to today, max value is today (no future dates)
- [x] If an entry exists for the selected date, it loads for editing
- [x] Report tab generates message for the selected date

**Status:** Built

---

### US-09: Daily Log - Calendar View
**As a** user, **I want to** browse my past entries on a calendar, **so that** I can see which days I logged and review specific entries.

**Acceptance Criteria:**
- [x] Calendar grid with month/year navigation (Prev/Next buttons)
- [x] Days with entries marked with a green checkmark and are clickable
- [x] Clicking a date shows entry details (prayer, reading, sermon info)
- [x] Past days without entries shown as disabled

**Status:** Built

---

### US-10: Daily Log - List View
**As a** user, **I want to** browse my past entries in a filterable list, **so that** I can review a range of entries quickly.

**Acceptance Criteria:**
- [x] List view with date range filter (From/To)
- [x] Each entry shown as an expandable card with summary (date, prayer, reading)
- [x] Expanded view shows full detail including sermon info and report-copied status

**Status:** Built

---

### US-11: Weekly Bible Reading Assignment Creation
**As a** user, **I want to** enter a weekly Bible reading assignment (book, start chapter, end chapter, week start), **so that** the app splits it into daily targets.

**Acceptance Criteria:**
- [x] Form with book selector, start/end chapter inputs, and week start date
- [x] Week start defaults to next Monday (or today if today is Monday)
- [x] Chapter distribution algorithm splits chapters evenly across 6 days (Mon-Sat)
- [x] Preview breakdown before confirming
- [x] Confirm button saves the assignment as ACTIVE

**Status:** Built

---

### US-12: Weekly Assignment Progress Tracking
**As a** user, **I want to** see my progress against the weekly assignment, **so that** I know how many chapters I have left.

**Acceptance Criteria:**
- [x] Current assignment tab shows book name, chapter range, and week dates
- [x] Daily breakdown with completion status icons (checkmark vs hourglass)
- [x] Progress bar showing chapters completed vs total assigned
- [x] Balloons animation when assignment is fully completed

**Status:** Built

---

### US-13: Weekly Assignment History
**As a** user, **I want to** view past weekly assignments, **so that** I can see my history of Bible reading goals.

**Acceptance Criteria:**
- [x] History tab lists all past assignments
- [x] Each assignment shown with status icon (completed/active/partial), book, chapter range, and week start
- [x] Expandable to show daily breakdown details

**Status:** Built

---

### US-14: Dynamic Recalculation of Weekly Assignment
**As a** user, **I want** the app to recalculate remaining daily targets if I read ahead or fall behind, **so that** the daily suggestions stay accurate.

**Acceptance Criteria:**
- [ ] When user reads more chapters than suggested, remaining days are recalculated
- [ ] When user reads fewer chapters, remaining days pick up the slack
- [ ] Recalculation runs automatically when daily entry is saved

**Status:** Not Started

---

### US-15: Streaks and Stats Page
**As a** user, **I want to** see my streak data and monthly activity heatmap, **so that** I stay motivated to maintain consistency.

**Acceptance Criteria:**
- [x] Current streak and longest streak displayed as metrics
- [x] Monthly heatmap calendar with colored cells (purple for logged, pink for missed)
- [x] Month navigation (Prev/Next)
- [x] Monthly summary: days logged, total prayer hours, total Bible chapters
- [x] Milestone celebrations at 7, 30, 50, 100, and 365 day streaks

**Status:** Built

---

### US-16: YouTube Auto-Fill via oEmbed
**As a** user, **I want** the sermon title to auto-fill when I paste a YouTube URL, **so that** I save time on data entry.

**Acceptance Criteria:**
- [ ] When a valid YouTube URL is pasted, the app calls the oEmbed endpoint
- [ ] Video title is auto-filled into the sermon title field
- [ ] User can edit the auto-filled title
- [ ] Graceful fallback if oEmbed fails

**Status:** Not Started

---

### US-17: Report Includes YouTube Link
**As a** user, **I want** the YouTube link included in the WhatsApp report when I log a sermon, **so that** my pastor can click through to watch.

**Acceptance Criteria:**
- [x] YouTube link appears on a new line below the sermon info in the generated message
- [ ] Link is only included if a valid YouTube URL was entered

**Status:** Needs Work

---

### US-18: Journal Search and Filtering
**As a** user, **I want to** search my daily log entries by keyword (sermon title, speaker, Bible book), **so that** I can find specific entries.

**Acceptance Criteria:**
- [ ] Search bar on the Daily Log page
- [ ] Search across sermon title, speaker name, and Bible book
- [x] Filter by date range (list view)
- [ ] Filter by Bible book
- [ ] Filter by speaker name

**Status:** Needs Work

---

---

## Section 2: Sermon Notes

### US-19: Create New Sermon Note
**As a** user, **I want to** create a sermon note with title, speaker, and date, **so that** I can capture sermon insights in a structured format.

**Acceptance Criteria:**
- [x] Sermon title text input
- [x] Speaker dropdown with defaults: Bishop Samuel Patta, Merlyn Patta, Ps. Deepak Avinash, Other
- [x] "Other" option reveals a custom text input
- [x] Date picker defaulting to today
- [x] Validation: title and speaker are required

**Status:** Built

---

### US-20: Two-Column Notes Layout (Notes + Bible References)
**As a** user, **I want to** type free-form notes on the left and Bible references on the right, **so that** my notes and supporting scriptures are side by side.

**Acceptance Criteria:**
- [x] Left column: large text area for free-form notes
- [x] Right column: text area for Bible references (one per line)
- [x] Helper caption explaining the two-column layout

**Status:** Built

---

### US-21: Bible Reference Auto-Fetch in Sermon Notes
**As a** user, **I want** the app to automatically fetch and display the actual scripture text when I type a reference like "Mark 1:1", **so that** I can see the verse without leaving the app.

**Acceptance Criteria:**
- [x] References parsed from text area input (supports Book Ch:V, Book Ch:V-V formats)
- [x] Scripture text fetched via Bible API and displayed in styled cards
- [x] Fetched text cached via st.cache_data to reduce API calls
- [ ] SQLite-based persistent cache across sessions (currently uses in-memory/session cache only)
- [x] Graceful fallback if API is unreachable (shows "could not load" message)
- [x] Supports numbered books (e.g., 1 Corinthians)

**Status:** Needs Work

---

### US-22: Sermon Note Reflection Sections
**As a** user, **I want to** record "What I Learned", "Key Takeaways", and "Additional Thoughts" for each sermon note, **so that** I capture my personal reflections.

**Acceptance Criteria:**
- [x] "What I learned from this" text area
- [x] "Key Takeaways" text area (bullet-point style)
- [x] "Additional Thoughts" text area
- [x] All sections are optional
- [x] Placeholders guide the user on what to write

**Status:** Built

---

### US-23: Save and Edit Sermon Notes
**As a** user, **I want to** save a sermon note and return to edit it later, **so that** I can refine my notes over time.

**Acceptance Criteria:**
- [x] Save button persists note to SQLite
- [x] Edit button on browse view loads note into the New Note tab for editing
- [x] Cancel editing button to discard changes
- [x] Updated note re-saves to the same record

**Status:** Built

---

### US-24: Browse and Search Sermon Notes
**As a** user, **I want to** browse all my sermon notes in a list and search by title, speaker, or content, **so that** I can find past notes easily.

**Acceptance Criteria:**
- [x] Browse tab lists all notes sorted by date (newest first)
- [x] Each note shown as a styled card with title, speaker, and date
- [x] Expandable to show full note details (notes, references, reflections)
- [x] Text search across title, speaker, notes text, learnings, and takeaways
- [ ] Filter by speaker dropdown (currently only text search)

**Status:** Needs Work

---

### US-25: Delete Sermon Notes
**As a** user, **I want to** delete a sermon note, **so that** I can remove notes I no longer need.

**Acceptance Criteria:**
- [x] Delete button on each note in the browse view
- [ ] Confirmation prompt before deletion (currently deletes immediately on click)

**Status:** Needs Work

---

### US-26: Sermon Note Read-Only View
**As a** user, **I want to** view a sermon note in a clean, read-only format, **so that** I can review and reflect without accidentally editing.

**Acceptance Criteria:**
- [x] Expandable view shows all sections: notes, Bible references with scripture text, learnings, takeaways, additional thoughts
- [x] Bible reference cards rendered with fetched scripture text
- [ ] Dedicated full-page read-only view (separate from the expander-based browse list)

**Status:** Needs Work

---

---

## Section 3: Prayer Journal

### US-27: Default Prayer Categories
**As a** user, **I want** four default prayer categories (Personal, Finance & Breakthroughs, Spouse, Job & Career) available on first use, **so that** I have an organized starting structure.

**Acceptance Criteria:**
- [x] Four default categories seeded on database initialization
- [x] Each category has a name, emoji icon, and color
- [x] Categories displayed as a horizontal radio selector

**Status:** Built

---

### US-28: Create Custom Prayer Categories
**As a** user, **I want to** create custom prayer categories with a name, icon, and color, **so that** I can organize prayers for any area of my life.

**Acceptance Criteria:**
- [x] "+ New Category" option in the category selector
- [x] Form with name, emoji icon, and color picker (preset color options)
- [x] New category appears immediately after creation

**Status:** Built

---

### US-29: Category Management (Rename/Delete)
**As a** user, **I want to** rename or delete custom categories, **so that** I can keep my prayer journal organized.

**Acceptance Criteria:**
- [ ] Rename option for any category (default or custom)
- [ ] Delete option for custom categories only (default categories protected)
- [ ] Warning if deleting a category with existing prayers

**Status:** Not Started

---

### US-30: Prayer Entry Creation Wizard
**As a** user, **I want to** create a new prayer using a guided step-by-step wizard, **so that** I fill in all important sections without feeling overwhelmed.

**Acceptance Criteria:**
- [x] Step 1: Category is pre-selected (user is already on a category tab)
- [x] Step 2: Title/purpose text input
- [x] Step 3: Prayer text area
- [x] Step 4: Bible scriptures (references with auto-fetch)
- [x] Step 5: Confessions and declarations text areas
- [ ] True multi-step wizard with Previous/Next buttons and progress indicator (currently all steps shown on a single page)
- [ ] Ability to skip optional steps and return later

**Status:** Needs Work

---

### US-31: Bible Scripture Auto-Fetch in Prayer Journal
**As a** user, **I want** the app to automatically fetch and display scripture text when I type references in a prayer entry, **so that** I can see God's promises alongside my prayers.

**Acceptance Criteria:**
- [x] References parsed from text area (one per line)
- [x] Scripture text fetched and displayed in styled cards with category color
- [x] Shared scripture lookup module with Sermon Notes
- [x] Graceful fallback for API failures

**Status:** Built

---

### US-32: Prayer Status Tracking
**As a** user, **I want to** set and update the status of each prayer (Ongoing, Answered, Standing in Faith), **so that** I can track God's faithfulness.

**Acceptance Criteria:**
- [x] Default status is "Ongoing" for new prayers
- [x] Status dropdown on each prayer entry to change status
- [x] Status updates immediately on change
- [x] Color-coded status badges (orange=Ongoing, green=Answered, purple=Standing in Faith)
- [ ] Prompt for answered date when marking as "Answered" (currently no date prompt)

**Status:** Needs Work

---

### US-33: View Prayers by Category
**As a** user, **I want to** view all prayers within a selected category, **so that** I can focus on one area of prayer at a time.

**Acceptance Criteria:**
- [x] Selecting a category shows only prayers in that category
- [x] Prayers displayed as expandable cards with status icon and title
- [x] Expanded view shows prayer text, scriptures, confessions, and declarations
- [x] Status filter (All, Ongoing, Answered, Standing in Faith)
- [ ] Sorting by status (Ongoing first, then Standing in Faith, then Answered) -- currently sorted by creation order

**Status:** Needs Work

---

### US-34: Edit Existing Prayer Entries
**As a** user, **I want to** edit an existing prayer entry to add scriptures, update text, or modify confessions/declarations, **so that** my prayers can grow over time.

**Acceptance Criteria:**
- [ ] Edit button on each prayer entry that loads it into an edit form
- [ ] All fields editable: title, prayer text, scriptures, confessions, declarations
- [ ] Save updates to existing record

**Status:** Not Started

---

### US-35: Delete Prayer Entries
**As a** user, **I want to** delete a prayer entry I no longer need, **so that** my journal stays clean.

**Acceptance Criteria:**
- [x] Delete button on each prayer entry
- [ ] Confirmation prompt before deletion (currently deletes immediately)

**Status:** Needs Work

---

### US-36: Prayer Entry Full Read-Only View
**As a** user, **I want to** view a prayer entry in a clean, full read-only format, **so that** I can use it during prayer time.

**Acceptance Criteria:**
- [x] Expanded view shows all sections: prayer text, scriptures with verse text, confessions, declarations
- [x] Styled display with appropriate colors and formatting
- [ ] Dedicated full-page view with large, readable text optimized for prayer time
- [ ] "Not yet added" message with edit prompt for sections left empty during creation

**Status:** Needs Work

---

### US-37: Category Summary Counts
**As a** user, **I want to** see a summary count on each category showing total prayers, ongoing count, and answered count, **so that** I have an overview without clicking into each.

**Acceptance Criteria:**
- [ ] Each category tab/button shows counts (e.g., "Personal (3 ongoing, 1 answered)")
- [ ] Counts update in real-time as statuses change

**Status:** Not Started

---

### US-38: Confessions and Declarations with Mapped Verses
**As a** user, **I want to** write confession and declaration statements with Bible verse references mapped to each, **so that** my faith declarations are grounded in Scripture.

**Acceptance Criteria:**
- [x] Confessions text area with placeholder guidance
- [x] Declarations text area with placeholder guidance
- [x] Styled display in green (confessions) and amber (declarations) containers
- [ ] Inline verse mapping: ability to link a specific Bible reference to each confession/declaration line
- [ ] Auto-fetch of inline verse references within confessions/declarations text

**Status:** Needs Work

---

---

## Section 4: Cross-Cutting Concerns

### US-39: App Settings - Greeting and Pastor Name
**As a** user, **I want to** configure the greeting name and pastor's name used in the WhatsApp message, **so that** the report format matches my needs.

**Acceptance Criteria:**
- [x] Text inputs for greeting name and pastor's name
- [x] Settings persist in SQLite
- [x] Greeting name used in dashboard greeting and WhatsApp message

**Status:** Built

---

### US-40: App Settings - Default Prayer Duration
**As a** user, **I want to** set my default prayer duration, **so that** the daily entry form pre-fills with my usual prayer time.

**Acceptance Criteria:**
- [x] Select slider for default prayer minutes
- [x] Setting persists and is loaded by the daily entry form

**Status:** Built

---

### US-41: App Settings - Omit Empty Sermon Line
**As a** user, **I want to** choose whether the "Listening to the Word" line is omitted or shows "None" when I don't log a sermon, **so that** my report format matches my preference.

**Acceptance Criteria:**
- [x] Checkbox toggle for omitting the sermon line when empty
- [x] Setting applied during message generation

**Status:** Built

---

### US-42: Data Export (JSON)
**As a** user, **I want to** export all my data as a JSON file, **so that** I have a backup and can restore it if needed.

**Acceptance Criteria:**
- [x] "Export Data (JSON)" download button on the Settings page
- [x] Export includes all entries, assignments, settings, sermon notes, prayer categories, and prayer entries
- [ ] CSV export option in addition to JSON

**Status:** Needs Work

---

### US-43: Data Import (JSON)
**As a** user, **I want to** import data from a JSON backup file, **so that** I can restore my data if something goes wrong.

**Acceptance Criteria:**
- [x] File uploader for JSON files
- [x] "Confirm Import" button to execute the import
- [x] Error handling for invalid JSON
- [ ] Merge strategy (currently unclear if import overwrites or merges)
- [ ] Preview of what will be imported before confirmation

**Status:** Needs Work

---

### US-44: Warm Spiritual Theme and Styling
**As a** user, **I want** the app to have a warm, spiritual aesthetic with soft colors, **so that** using the app feels like a devotional experience.

**Acceptance Criteria:**
- [x] Bible reader uses a warm parchment-like container (FFF9F0 background, Georgia serif font)
- [x] Purple accent color (7B68EE) used consistently
- [x] Scripture reference cards styled with warm backgrounds and accent borders
- [x] Prayer journal categories have distinct colors
- [ ] Streamlit custom theme configuration (.streamlit/config.toml) for app-wide warm colors
- [ ] Consistent font and color palette across all pages

**Status:** Needs Work

---

### US-45: Mobile Responsiveness
**As a** user, **I want** the app to work well on my phone, **so that** I can log entries and read the Bible on mobile.

**Acceptance Criteria:**
- [x] Streamlit default responsive layout
- [x] Bible reader has max-height with scroll for long chapters
- [ ] Two-column sermon notes layout stacks vertically on narrow screens
- [ ] Touch-friendly button sizes verified on mobile
- [ ] Tested on both Android and iOS mobile browsers

**Status:** Needs Work

---

### US-46: Sidebar Navigation with Sections
**As a** user, **I want** clear sidebar navigation organized by section (Daily Assignment, Sermon Notes, Prayer Journal, Settings), **so that** I can easily find what I need.

**Acceptance Criteria:**
- [x] Sidebar navigation using Streamlit's multi-page st.navigation with sections
- [x] Pages grouped under: Daily Assignment, Sermon Notes, Prayer Journal, Settings
- [x] Each page has an icon and descriptive title
- [x] Dashboard is the default home page

**Status:** Built

---

### US-47: Bible Book Reference Data
**As a** user, **I want** the app to have a complete reference of all 66 Bible books with chapter counts, **so that** book selectors and chapter validation work correctly.

**Acceptance Criteria:**
- [x] All 66 Bible books with chapter counts available
- [x] Used in book selectors (Daily Entry, Weekly Assignment)
- [x] Used for chapter count validation

**Status:** Built

---

### US-48: Simple Password Protection
**As a** user, **I want** basic password protection for the app, **so that** only I can access my spiritual data.

**Acceptance Criteria:**
- [ ] Password gate using st.secrets or Streamlit built-in auth
- [ ] Password stored securely (not in source code)
- [ ] Session persists after login

**Status:** Not Started

---

### US-49: Multi-User Authentication via Email
**As the** app owner, **I want** to allow other users to register and use the app with email-based authentication, **so that** others can benefit from the tool.

**Acceptance Criteria:**
- [ ] Email-based registration and login
- [ ] User-level data isolation (each user sees only their data)
- [ ] User session management

**Status:** Not Started

---

### US-50: Morning Reminder / Push Notification
**As a** user, **I want** a daily morning notification reminding me to log my entry, **so that** I maintain consistency.

**Acceptance Criteria:**
- [ ] Configurable reminder time in settings
- [ ] Push notification with encouraging spiritual message
- [ ] Notification links directly to the daily entry form
- [ ] Different message if today's entry is already complete

**Status:** Not Started
**Note:** Streamlit does not natively support push notifications. This would require PWA service worker setup or an external notification service.

---

### US-51: Multi-Book Weekly Assignments
**As a** user, **I want to** create weekly assignments that span multiple Bible books (e.g., "Read Luke and John"), **so that** I can handle more complex reading goals.

**Acceptance Criteria:**
- [ ] Support for entering multiple books in a single assignment
- [ ] Chapter distribution across books handled in daily breakdown
- [ ] Daily suggestions reference the correct book as chapters span across

**Status:** Not Started

---

### US-52: Editable Daily Breakdown in Weekly Assignment
**As a** user, **I want to** manually adjust the auto-generated daily chapter breakdown before confirming, **so that** I can customize my reading pace.

**Acceptance Criteria:**
- [ ] Each day's chapter range is editable in the preview
- [ ] Adjusted breakdown is validated (all chapters still covered)
- [ ] Confirmed breakdown saved as the final assignment

**Status:** Not Started

---

### US-53: Scripture Cache Persistence in SQLite
**As a** user, **I want** fetched scripture texts to be cached permanently in SQLite, **so that** repeated lookups are instant and work even when the Bible API is slow.

**Acceptance Criteria:**
- [ ] Dedicated scripture_cache table in SQLite with reference, text, translation, and fetch timestamp
- [ ] Cache checked before any API call
- [ ] Cache shared between Sermon Notes and Prayer Journal
- [ ] Cache never expires (scripture text does not change)

**Status:** Not Started
**Note:** Currently caching is done via st.cache_data with a 1-hour TTL, which is session-scoped and not persistent.

---

### US-54: Delete Confirmation Dialogs
**As a** user, **I want** a confirmation prompt before any destructive action (deleting sermon notes, prayer entries, categories), **so that** I don't accidentally lose data.

**Acceptance Criteria:**
- [ ] All delete buttons require a second confirmation step
- [ ] Confirmation shows what will be deleted
- [ ] Option to cancel the deletion

**Status:** Not Started

---

### US-55: Sermon Note Reference and Takeaway Counts in Browse List
**As a** user, **I want to** see the count of Bible references and key takeaways on each sermon note card in the browse list, **so that** I can gauge the depth of each note at a glance.

**Acceptance Criteria:**
- [ ] Bible reference count shown on each note card (e.g., "3 Bible references")
- [ ] Key takeaway count shown on each note card (e.g., "4 takeaways")

**Status:** Not Started

---

### US-56: WhatsApp Deep Link Convenience Button
**As a** user, **I want** an optional "Open WhatsApp" button alongside "Copy to Clipboard", **so that** I can quickly jump to the WhatsApp chat after copying.

**Acceptance Criteria:**
- [ ] "Open WhatsApp" button using wa.me deep link with pastor's phone number
- [ ] Phone number configurable in settings
- [ ] Button is secondary/optional, not the primary action

**Status:** Not Started

---

### US-57: Configurable Message Template
**As a** user, **I want to** customize the WhatsApp message template (greeting, format), **so that** I can adapt if the reporting format changes.

**Acceptance Criteria:**
- [ ] Message template editor in settings
- [ ] Template supports variables ({greetingName}, {date}, {prayerDuration}, etc.)
- [ ] Preview of the generated message with current template

**Status:** Not Started

---

### US-58: Streak Milestone Celebrations
**As a** user, **I want** congratulatory messages and animations when I hit streak milestones (7, 30, 100 days), **so that** I feel encouraged and motivated.

**Acceptance Criteria:**
- [x] Balloons animation at milestone streaks (7, 30, 50, 100, 365 days) on the Streaks page
- [ ] Milestone celebration shown on the Dashboard when logging in on a milestone day
- [ ] Persistent milestone badges or achievements view

**Status:** Needs Work

---

---

## Summary

| Section                           | Built | Needs Work | Not Started | Total |
|-----------------------------------|-------|------------|-------------|-------|
| Section 1: Daily Assignment       | 13    | 2          | 3           | 18    |
| Section 2: Sermon Notes           | 3     | 4          | 1           | 8     |
| Section 3: Prayer Journal         | 3     | 5          | 4           | 12    |
| Section 4: Cross-Cutting          | 5     | 6          | 9           | 20    |
| **Total**                         | **24**| **17**     | **17**      | **58**|
