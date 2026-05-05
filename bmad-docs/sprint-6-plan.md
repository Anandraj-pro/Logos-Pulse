# Sprint 6 Plan -- Logos Pulse

**Sprint Goal:** Equip pastors with automated care tooling and members with richer Bible engagement through daily reminders, reading plans, an advanced Bible reader, and a pastor care workflow.

**Sprint Dates:** 2026-05-01 to 2026-05-15 (2 weeks)
**Capacity:** 1 developer, ~6 hrs/day, 5 days/week = 60 hrs total
**Velocity Estimate:** ~30 story points (based on 1 SP ~ 2 hrs avg)

---

## Sprint Backlog Summary

| #  | Story | Points | Priority | Week |
|----|-------|--------|----------|------|
| 1  | Daily Reminder System (pg_cron + Edge Function) | 8 | P0 | 1 |
| 2  | Pastor Care Workflow (inactivity alerts + care tasks) | 8 | P0 | 1–2 |
| 3  | Bible Reading Plans (structured multi-week plans) | 8 | P1 | 2 |
| 4  | Advanced Bible Reader (bookmarks, highlights, notes) | 6 | P1 | 2 |
| **Total** | | **30** | | |

Stretch goal (if time permits): Bulk account creation CSV import in Admin Panel (deferred from backlog, estimated 3 SP).

---

## User Stories -- Detail

---

### Story 1: Daily Reminder System

**Priority:** P0
**Points:** 8

> **As a** Prayer Warrior who sometimes forgets to log my disciplines,
> **I want** to receive a daily email reminder if I haven't logged by a configurable time,
> **so that** I maintain consistency and don't break my streak unintentionally.

**Acceptance Criteria:**
1. A Supabase pg_cron job fires once daily at 7:00 PM church local time (UTC+5:30, i.e., 13:30 UTC).
2. The cron job calls a Supabase Edge Function named `send-daily-reminders`.
3. The Edge Function queries all active Prayer Warriors who have not submitted a daily entry for today's date and whose `reminder_opt_in` profile flag is `true`.
4. For each unlogged member, the Edge Function sends a reminder email via the existing SMTP credentials (same secrets used by `modules/digest_email.py`).
5. The reminder email body includes the member's preferred name, the current date, a direct link to the app, and an encouraging scripture verse (one of 7 rotating verses, one per day of the week).
6. Admins can toggle the daily reminder system on/off from Admin Panel without redeploying (stored as a row in a `system_settings` table, key `reminders_enabled`).
7. Members can opt in or opt out of reminders from their Settings page (`reminder_opt_in` boolean, default `true` for new accounts).
8. The Edge Function logs each send attempt to the existing `audit_log` table with action `reminder_email_sent` and the target user_id.
9. If SMTP delivery fails for a given member, the failure is logged to `audit_log` with action `reminder_email_failed` and the error message; the function continues to the next member.
10. Admin Panel shows a read-only "Last reminder run" timestamp pulled from `audit_log` (most recent `reminder_email_sent` entry).

**Tasks:**
- [ ] Add `reminder_opt_in boolean default true` column to `profiles` table; add to `migrations/001_schema.sql`.
- [ ] Add `system_settings` table (`key text primary key, value text, updated_at timestamptz`); insert default row `('reminders_enabled', 'true', now())`; add to migrations.
- [ ] Create Supabase Edge Function `supabase/functions/send-daily-reminders/index.ts` that reads unlogged members, iterates, and sends SMTP email using `Deno.env` for SMTP credentials.
- [ ] Write the 7 rotating scripture strings as a constant array inside the Edge Function.
- [ ] Configure pg_cron in Supabase SQL Editor: `SELECT cron.schedule('daily-reminders', '30 13 * * *', $$SELECT net.http_post(...)$$);` targeting the Edge Function URL with the service role key as bearer token.
- [ ] Add `db.get_system_setting(key)` and `db.set_system_setting(key, value)` helper functions in `modules/db.py` using the admin client.
- [ ] Add "Reminder opt-in" toggle to `views/5_Settings.py` that reads/writes `reminder_opt_in` on the current user's profile row.
- [ ] Add "Daily Reminders" section to `views/Admin_Panel.py` with an on/off toggle (reads/writes `system_settings`) and a "Last run" display from `audit_log`.
- [ ] Smoke test: disable reminders toggle, verify Edge Function returns early; re-enable, verify at least one test email arrives in sandbox.
- [ ] Update `migrations/001_schema.sql` with both new table/column definitions and RLS: `system_settings` readable by admin only for writes, readable by service role for Edge Function.

---

### Story 2: Pastor Care Workflow

**Priority:** P0
**Points:** 8

> **As a** Pastor responsible for my congregation's spiritual health,
> **I want** to see which members have been inactive for 3 or more days and manage follow-up care tasks,
> **so that** no member silently falls away without a personal check-in.

**Acceptance Criteria:**
1. Any Prayer Warrior who has not submitted a daily entry in the past 3 or more calendar days is automatically surfaced as an "inactivity alert" visible to their assigned pastor.
2. The inactivity detection runs as a database view (`inactive_members_view`) that computes `days_since_last_entry` per user using `max(entry_date)` from `daily_entries`, filtered to the pastor's own members via `can_view_user()`.
3. Pastor Dashboard displays a "Care Alerts" tab (alongside existing tabs) listing each inactive member, days since last log, streak before inactivity, and a "Create Care Task" button.
4. Clicking "Create Care Task" opens a form allowing the pastor to enter a care note (free text, max 500 chars), set a follow-up due date, and choose a care type from a dropdown: `Check-In Call`, `Prayer Visit`, `Message`, `Escalate to Bishop`.
5. Care tasks are stored in a new `care_tasks` table: `id, pastor_id, member_id, care_type, note, due_date, status (open/done), created_at, completed_at`.
6. Pastor Dashboard "Care Alerts" tab shows two sub-sections: "Open Tasks" (sortable by due date) and "Inactive Members Without Tasks."
7. Each open task has a "Mark Done" button; clicking it sets `status = done` and `completed_at = now()`.
8. Bishop Dashboard shows an aggregate "Care Overview" card: total open care tasks across all their pastors, and count of members inactive 7+ days.
9. All care task writes are sanitized through `sanitize_html()` before insert.
10. Care task creation and completion are both written to `audit_log`.

**Tasks:**
- [ ] Create `care_tasks` table and `inactive_members_view` in `migrations/001_schema.sql`; write RLS: pastors can read/write their own tasks; bishops can read all tasks under their pastors; members have no access.
- [ ] Add `db.get_inactive_members(pastor_id, threshold_days=3)` function in `modules/db.py` using the admin client (queries `inactive_members_view`).
- [ ] Add `db.create_care_task(pastor_id, member_id, care_type, note, due_date)` in `modules/db.py`.
- [ ] Add `db.get_care_tasks(pastor_id, status=None)` in `modules/db.py`.
- [ ] Add `db.complete_care_task(task_id)` in `modules/db.py` that sets `status='done'` and `completed_at=now()`.
- [ ] Add "Care Alerts" tab to `views/Pastor_Dashboard.py` with inactive members list and open tasks list.
- [ ] Build "Create Care Task" form inside the Care Alerts tab with care type dropdown, note textarea, and due date picker; call `db.create_care_task()` on submit.
- [ ] Add "Mark Done" button per task row in the Open Tasks sub-section.
- [ ] Add "Care Overview" summary card to `views/Bishop_Dashboard.py` showing aggregate open task count and 7-day inactive member count across all pastors.
- [ ] Write `audit_log` entries for task creation and completion (reuse existing audit helper).
- [ ] Verify RLS: logged-in pastor cannot read another pastor's care tasks; bishop can see all.

---

### Story 3: Bible Reading Plans

**Priority:** P1
**Points:** 8

> **As a** Prayer Warrior who wants structured Bible engagement,
> **I want** to follow a multi-week reading plan assigned by my pastor with daily chapter targets,
> **so that** I read the Bible systematically rather than at random.

**Acceptance Criteria:**
1. A library of pre-seeded reading plans exists, each with a name, description, total days, and an ordered list of daily reading targets (e.g., "NT in 90 Days", "Psalms in 30 Days", "Gospels in 28 Days"). At least 3 plans are seeded at launch.
2. Plans are stored in `reading_plans` (`id, name, description, total_days, created_by`) and `reading_plan_days` (`id, plan_id, day_number, book, chapter_start, chapter_end`).
3. Member enrollment is stored in `reading_plan_progress` (`id, user_id, plan_id, enrolled_at, current_day, completed_at`). A member can only have one active plan at a time.
4. Pastors can assign a reading plan to one or more of their members from Pastor Dashboard via a new "Reading Plans" tab; the assignment creates a `reading_plan_progress` row with `current_day = 1`.
5. Members can also self-enroll from a new `views/Bible_Reading_Plan.py` page (visible to all authenticated users).
6. The Bible Reading Plan page shows the current day's assignment (book + chapter range), a "Mark Today Complete" button, and a progress bar (current_day / total_days).
7. Clicking "Mark Today Complete" increments `current_day` by 1; if `current_day` exceeds `total_days`, sets `completed_at = now()` and shows a congratulations message.
8. The page also shows the full plan schedule as a collapsible table (day, reading, status: complete/today/upcoming) so the member can see what's ahead.
9. Dashboard shows a "Reading Plan" card if the member is enrolled, displaying today's target and a progress percentage.
10. If today's entry has already been marked complete (same calendar day), the "Mark Today Complete" button is disabled with a "Already completed today" label.
11. Plan completion is logged to `audit_log` with action `reading_plan_completed`.
12. All new pages call `apply_shared_styles()` and `require_login()`.

**Tasks:**
- [ ] Create `reading_plans`, `reading_plan_days`, and `reading_plan_progress` tables in `migrations/001_schema.sql` with appropriate RLS (members read their own progress; pastors read all members' progress; admin full access).
- [ ] Write seed SQL for 3 plans: "NT in 90 Days" (Acts through Revelation, 90 days), "Psalms in 30 Days" (5 psalms/day), "Gospels in 28 Days" (Matthew, Mark, Luke, John, 28 days); add seed to `modules/seed.py` or a standalone migration file.
- [ ] Add `db.get_reading_plans()`, `db.get_plan_days(plan_id)`, `db.get_member_active_plan(user_id)`, `db.enroll_in_plan(user_id, plan_id)`, `db.mark_plan_day_complete(progress_id)` functions to `modules/db.py`.
- [ ] Create `views/Bible_Reading_Plan.py` with auth guards, current-day display, "Mark Today Complete" button logic, progress bar, and full collapsible schedule table.
- [ ] Add "Reading Plans" tab to `views/Pastor_Dashboard.py` showing each member's active plan and progress, plus an "Assign Plan" dropdown + button.
- [ ] Add "Reading Plan" card to `views/0_Dashboard.py` (show only if member has an active plan).
- [ ] Register `views/Bible_Reading_Plan.py` in `app.py` navigation for all authenticated roles.
- [ ] Verify that self-enrollment correctly prevents double-enrollment (upsert or check before insert).
- [ ] Smoke test the plan day boundary: completing day 90 of "NT in 90 Days" sets `completed_at` correctly.

---

### Story 4: Advanced Bible Reader

**Priority:** P1
**Points:** 6

> **As a** Prayer Warrior doing my daily Bible reading,
> **I want** to bookmark verses, highlight passages, and add personal notes directly in the Bible reader,
> **so that** I can revisit meaningful scripture and my reflections are saved alongside the text.

**Acceptance Criteria:**
1. A bookmark icon appears next to each verse in the existing Bible reader (`modules/bible_reader.py` / `views/1_Daily_Entry.py`). Clicking it saves a bookmark for that verse (book, chapter, verse, timestamp).
2. Bookmarks are stored in `bible_bookmarks` (`id, user_id, book, chapter, verse_number, note, created_at`).
3. A highlight button (or color swatch) appears per verse. Clicking it cycles through three highlight colors: yellow, green, none. The active highlight is stored in `bible_highlights` (`id, user_id, book, chapter, verse_number, color, created_at`).
4. A "Add Note" text input (max 300 chars) appears inline below a bookmarked verse when the bookmark is active. Submitting saves the note text to the bookmark row.
5. A new "My Bible Notes" sub-section appears in `views/7_Prayer_Journal.py` (or as a standalone tab) showing all bookmarks sorted by most recent, each displaying the scripture reference, note text, and a "Delete" button.
6. The existing Bible reader respects current bookmarks and highlights when the same chapter is re-opened — previously highlighted verses render with their color, bookmarked verses show a filled bookmark icon.
7. Bookmarks and highlights are user-scoped (RLS: users see only their own rows).
8. All note text passes through `sanitize_html()` before insert/update.
9. Deleting a bookmark also removes the associated highlight row for that verse if one exists.
10. Bookmark and highlight counts per user are visible in the "Streaks & Stats" page as two new stat cards ("Verses Bookmarked", "Verses Highlighted").

**Tasks:**
- [ ] Create `bible_bookmarks` and `bible_highlights` tables in `migrations/001_schema.sql` with RLS (user reads/writes own rows only).
- [ ] Add `db.add_bookmark(user_id, book, chapter, verse_number, note='')`, `db.get_bookmarks(user_id)`, `db.get_bookmarks_for_chapter(user_id, book, chapter)`, `db.delete_bookmark(bookmark_id)`, `db.update_bookmark_note(bookmark_id, note)` to `modules/db.py`.
- [ ] Add `db.set_highlight(user_id, book, chapter, verse_number, color)`, `db.get_highlights_for_chapter(user_id, book, chapter)`, `db.remove_highlight(user_id, book, chapter, verse_number)` to `modules/db.py`.
- [ ] Modify `modules/bible_reader.py` to accept and render per-verse bookmark icons and highlight color overlays; load chapter bookmarks and highlights once at render time (single query each, cached in session state).
- [ ] Implement bookmark toggle logic (add if not exists, remove if exists) and highlight cycle logic (yellow → green → none → yellow) in the reader component.
- [ ] Add inline note input that appears beneath a verse when its bookmark is active; wire to `db.update_bookmark_note()` on submit.
- [ ] Add "My Bible Notes" tab to `views/7_Prayer_Journal.py` listing all bookmarks with reference, note, created date, and delete button.
- [ ] Add "Verses Bookmarked" and "Verses Highlighted" stat cards to `views/4_Streaks_and_Stats.py`.
- [ ] Verify no visual regression in existing Bible reader layout at 375px mobile width.
- [ ] Ensure bookmark/highlight queries use session-state cache and are invalidated on write.

---

## Sprint Schedule

### Week 1 (2026-05-01 to 2026-05-07)

| Day | Focus | Hours |
|-----|-------|-------|
| Fri May 1 | Story 1: `system_settings` + `profiles.reminder_opt_in` schema; Edge Function scaffold and SMTP wiring | 6 |
| Mon May 5 | Story 1: pg_cron configuration; admin panel toggle + last-run display; Settings opt-in toggle | 6 |
| Tue May 6 | Story 1: End-to-end smoke test reminder flow; audit log integration; fix any SMTP/cron issues | 6 |
| Wed May 7 | Story 2: `care_tasks` table + `inactive_members_view` schema; db helper functions | 6 |
| Thu May 8 | Story 2: Pastor Dashboard "Care Alerts" tab — inactive members list + Create Care Task form | 6 |

### Week 2 (2026-05-08 to 2026-05-15)

| Day | Focus | Hours |
|-----|-------|-------|
| Fri May 9 | Story 2: Open Tasks sub-section, Mark Done button, Bishop Dashboard Care Overview card, audit log wiring | 6 |
| Mon May 12 | Story 3: `reading_plans` / `reading_plan_days` / `reading_plan_progress` schema + 3-plan seed data | 6 |
| Tue May 13 | Story 3: `views/Bible_Reading_Plan.py` — full page build; db helpers; Dashboard card | 6 |
| Wed May 14 | Story 3: Pastor Dashboard "Reading Plans" tab (assign + view progress); nav registration; smoke tests | 6 |
| Thu May 15 | Story 4: `bible_bookmarks` + `bible_highlights` schema; db helpers; Bible reader integration; My Bible Notes tab; Streaks stat cards; final regression sweep | 6 |

---

## Definition of Done

- [ ] Code committed to main branch
- [ ] All acceptance criteria verified manually
- [ ] No new st.error tracebacks visible to end users
- [ ] Mobile responsive (tested at 375px width)
- [ ] No regression in existing features
- [ ] Deployed and smoke-tested on https://logos-pulse.streamlit.app/
- [ ] New tables and columns present in `migrations/001_schema.sql` with RLS policies
- [ ] All user text inputs pass through `sanitize_html()` before DB write
- [ ] New pages call `require_login()`, `require_password_changed()`, and `apply_shared_styles()` at the top
- [ ] Supabase Edge Function deployed and visible in Supabase dashboard
- [ ] pg_cron job verified in Supabase SQL Editor (`SELECT * FROM cron.job;`)

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Supabase pg_cron not enabled on free-tier project | Medium | High (Story 1 blocked) | Check `pg_cron` availability in Supabase dashboard before Day 1; fallback is a lightweight Supabase Edge Function triggered via a scheduled GitHub Actions workflow using `cron:` syntax at no cost |
| SMTP credentials not available inside Supabase Edge Function environment | Medium | High (Story 1 emails won't send) | Store SMTP host/user/password as Supabase Edge Function secrets (`supabase secrets set`); test Deno SMTP fetch on Day 1 before building full logic |
| Bible reader verse-level rendering becomes slow with bookmark/highlight queries | Medium | Medium (Story 4 UX) | Load all bookmarks and highlights for the current chapter in two bulk queries cached in `st.session_state`; never query per-verse |
| Pastor Dashboard becomes too wide/cluttered with new tabs (Care Alerts + Reading Plans) | Low | Medium | Use `st.tabs()` with short labels; test at 375px; collapse infrequently-used sections with `st.expander()` |
| Reading plan seed data (90-day NT chapter list) is time-consuming to manually author | Medium | Medium (Story 3 delayed) | Write a Python seed script that generates `reading_plan_days` rows programmatically from `modules/bible_data.py` chapter counts rather than manually listing 90 rows |
| `inactive_members_view` query is slow for large congregations due to `max(entry_date)` scan | Low | Low (current congregation size is small) | Add a Postgres index on `daily_entries(user_id, entry_date)` in the migration; revisit if congregation grows |
| Edge Function cold start delays reminder delivery timing | Low | Low | Acceptable; reminder is best-effort, not mission-critical; log actual send time to audit_log |

---

## Backlog Items Deferred to Sprint 7+

| Item | Reason |
|------|--------|
| Multi-Church Tenancy | Large architectural change requiring schema-level tenant isolation across every table and RLS policy; estimated 40+ SP; needs its own planning spike before scheduling |
| WhatsApp Bot | Requires WhatsApp Business API approval and monthly budget; no API credentials available; not feasible without external procurement |
| Bulk Account Creation (CSV import) | Low urgency given current congregation size; stretch goal for Sprint 6, otherwise scheduled for Sprint 7 as a quick P2 item (~3 SP) |
| Prayer Request Sharing | Requires a moderation workflow (approve/reject before public visibility) to prevent inappropriate content; design work needed before building |
| Group Engagement Chart for Bishop | Bishop Dashboard already has aggregate stats; this is a visualization enhancement; schedule as a Sprint 7 polish item alongside any other dashboard improvements |
