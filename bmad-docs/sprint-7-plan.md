# Sprint 7 Plan -- Logos Pulse

**Sprint Goal:** Close the Sprint 6 self-enrollment gap, add bulk account creation for admins, give pastors private per-member notes and a one-tap WhatsApp group digest, auto-wire daily entry data into personal goals, and deliver church-wide bishop analytics with a group engagement chart.

**Sprint Dates:** 2026-05-16 to 2026-05-30 (2 weeks)
**Capacity:** 1 developer, ~6 hrs/day, 5 days/week = 60 hrs total
**Velocity Estimate:** ~30 story points (based on 1 SP ~ 2 hrs avg)

---

## Sprint Backlog Summary

| #  | Story | Points | Priority | Week |
|----|-------|--------|----------|------|
| 1  | Reading Plan Self-Enrollment (close Sprint 6 gap) | 3 | P0 | 1 |
| 2  | Bulk Account Creation via CSV Import | 4 | P0 | 1 |
| 3  | Pastor Notes per Member | 5 | P1 | 1–2 |
| 4  | Group WhatsApp Digest for Pastors | 5 | P1 | 2 |
| 5  | Personal Goal Auto-Progress from Daily Entry | 6 | P1 | 2 |
| 6  | Church-Wide Stats and Group Engagement Chart for Bishop | 7 | P2 | 2 |
| **Total** | | **30** | | |

---

## User Stories -- Detail

---

### Story 1: Reading Plan Self-Enrollment

**Priority:** P0
**Points:** 3

> **As a** Prayer Warrior who wants to follow a structured Bible reading plan,
> **I want** to browse available reading plans and enroll myself without waiting for my pastor,
> **so that** I can start a plan immediately and take ownership of my Bible engagement.

**Acceptance Criteria:**
1. `views/Bible_Reading_Plan.py` shows a "Browse Plans" section when the member has no active plan, listing all available plans from `reading_plans` with name, description, total days, and a "Start This Plan" button.
2. Clicking "Start This Plan" calls `db.enroll_in_plan(user_id, plan_id)` and immediately shows the Day 1 reading assignment without requiring a page reload beyond Streamlit's natural rerun.
3. If the member already has an active (incomplete) plan, the "Browse Plans" section is hidden and a "Switch Plan" expander is shown instead; switching unenrolls the current plan (sets `completed_at = 'abandoned'` status) and creates a new progress row for the chosen plan.
4. The `reading_plan_progress` table gains a `status` column (`active`, `completed`, `abandoned`, default `active`) to distinguish abandoned enrollments from genuine completions; the migration is updated accordingly.
5. Self-enrollment creates an `audit_log` entry with action `reading_plan_self_enrolled`, the user's ID, and the plan ID in the metadata field.
6. Pastors can still assign plans from Pastor Dashboard; if a pastor assigns a plan to a member who already has an active plan, a confirmation warning is shown ("Member is currently enrolled in X — assigning will replace it") and requires explicit confirmation before proceeding.
7. The plan picker shows a "Already completed" badge next to any plan the member finished before, so they can repeat it knowingly.
8. All plan enrollment state changes (enroll, abandon, complete) are reflected on the Dashboard "Reading Plan" card within the same session without needing a manual refresh.
9. `db.enroll_in_plan()` uses an upsert pattern that first marks any existing active row as `abandoned` before inserting the new row, preventing duplicate active enrollments at the database level.

**Tasks:**
- [ ] Add `status text not null default 'active'` column to `reading_plan_progress` in `migrations/001_schema.sql`; add a `check` constraint allowing only `active`, `completed`, `abandoned`.
- [ ] Update `db.enroll_in_plan(user_id, plan_id)` to mark any existing `active` row as `abandoned` before inserting the new row.
- [ ] Update `db.get_member_active_plan(user_id)` to filter on `status = 'active'`.
- [ ] Build "Browse Plans" UI block in `views/Bible_Reading_Plan.py` that fetches all plans, renders a card per plan, and handles the "Start This Plan" button with confirmation dialog.
- [ ] Add "Switch Plan" expander logic when a member is already enrolled.
- [ ] Add `audit_log` write for `reading_plan_self_enrolled`.
- [ ] Update Pastor Dashboard "Reading Plans" tab to show the confirmation warning before overwriting an active plan.
- [ ] Add "Already completed" badge logic by checking `reading_plan_progress` rows with `status = 'completed'` for the current user.
- [ ] Smoke test: enroll, complete Day 1, switch plan, verify old row is `abandoned`, new row is `active`.

---

### Story 2: Bulk Account Creation via CSV Import

**Priority:** P0
**Points:** 4

> **As an** Admin who needs to onboard a new group of Prayer Warriors at once,
> **I want** to upload a CSV file with member names, emails, and roles and have all accounts created in one action,
> **so that** I do not have to fill out the "Create Account" form dozens of times manually.

**Acceptance Criteria:**
1. Admin Panel gains a "Bulk Import" tab (alongside existing tabs) containing a CSV upload widget and a template download link.
2. The expected CSV format is: `preferred_name, email, role, pastor_email` (one row per account); `pastor_email` is optional and used to auto-assign the new member to an existing pastor.
3. A "Download Template" button renders and triggers download of a pre-filled example CSV file with one sample row and a header comment explaining each column.
4. After uploading, a preview table is shown before any accounts are created, listing all parsed rows with a validation status column: "Ready", "Invalid email", "Role not allowed", "Pastor not found", or "Email already exists".
5. Rows with validation errors are highlighted in amber and excluded from creation; the admin must explicitly choose to proceed with only valid rows.
6. Clicking "Create Valid Accounts" iterates over valid rows, calls `modules/rbac.create_account()` for each, sets `must_change_password = True`, and streams a live progress counter ("3 of 12 created...").
7. After the run completes, a summary card shows: total rows, accounts created, skipped (errors), and any per-row error messages for failed creates.
8. Each successful creation is written to `audit_log` with action `bulk_account_created` and the new user's email and role in metadata.
9. The entire import operation is idempotent at the row level: if a second upload contains an email that already exists, that row is skipped with an "Email already exists" validation error rather than raising an exception.
10. The `pastor_email` lookup uses the admin client to find the pastor's `user_id` in `profiles`; if not found, the row is marked "Pastor not found" but the account can still be created without a pastor assignment if the admin proceeds.

**Tasks:**
- [ ] Add "Bulk Import" tab to `views/Admin_Panel.py` with `st.file_uploader(type=['csv'])`.
- [ ] Write `modules/bulk_import.py` with functions: `parse_csv(file)` → list of row dicts; `validate_rows(rows)` → list of rows with `status` field appended; `create_accounts(valid_rows, progress_callback)` → summary dict.
- [ ] Implement row-level validation in `validate_rows()`: email format check (regex), role whitelist check, duplicate email lookup via admin client, pastor_email lookup via admin client.
- [ ] Wire `create_accounts()` to `modules/rbac.create_account()` per row; catch per-row exceptions and record in summary rather than aborting the batch.
- [ ] Build preview table UI using `st.dataframe()` with row-level color coding (green/amber/red) based on `status` field.
- [ ] Add "Download Template" button that writes a hardcoded CSV string to `st.download_button`.
- [ ] Add live progress display using `st.progress()` and a status text placeholder updated inside the creation loop.
- [ ] Add `audit_log` write per successful creation inside `create_accounts()`.
- [ ] Add `pastor_email` → `user_id` resolution in validation; propagate `pastor_id` into `rbac.create_account()` if present.
- [ ] Smoke test: upload 5-row CSV with 1 duplicate email and 1 invalid role; verify 3 accounts created, 2 skipped with correct error labels.

---

### Story 3: Pastor Notes per Member

**Priority:** P1
**Points:** 5

> **As a** Pastor tracking the spiritual journey of each member,
> **I want** to record private notes about each member (e.g., prayer needs, counseling observations, follow-up reminders),
> **so that** I have a running log of pastoral context that only I and my bishop can see.

**Acceptance Criteria:**
1. A new `pastor_notes` table stores notes: `id, pastor_id, member_id, note_text (max 1000 chars), note_date (default today), created_at, updated_at`.
2. `views/Member_Detail.py` gains a "Pastor Notes" tab visible only to pastors and admins/bishops; Prayer Warriors see no trace of this tab.
3. The tab shows all existing notes for that member in reverse-chronological order, each displaying the note date, note text, and an "Edit" / "Delete" button.
4. A "New Note" form at the top of the tab has a `st.text_area` (max 1000 chars) and a date picker (default today); submitting saves the note via `db.create_pastor_note()`.
5. Editing a note opens an inline form replacing the note card; saving updates the `note_text` and `updated_at` fields via `db.update_pastor_note()`.
6. Deleting a note requires a confirmation (`st.checkbox("Confirm delete")`) before calling `db.delete_pastor_note()`.
7. A pastor can only read and write notes they personally authored (`pastor_id = auth.uid()` in RLS); a bishop can read (but not edit or delete) all notes written by pastors under them.
8. All note text is passed through `sanitize_html()` before any DB write.
9. Member Detail's side-summary card shows a "Notes" badge with the count of existing notes for quick reference, visible to the pastoral viewer only.
10. Note creation and deletion are written to `audit_log` with actions `pastor_note_created` and `pastor_note_deleted`.

**Tasks:**
- [ ] Create `pastor_notes` table in `migrations/001_schema.sql`; write RLS: `pastor_id = auth.uid()` for all writes and pastor reads; bishop read-only via `can_view_user()` join.
- [ ] Add `db.get_pastor_notes(pastor_id, member_id)`, `db.create_pastor_note(pastor_id, member_id, note_text, note_date)`, `db.update_pastor_note(note_id, note_text)`, `db.delete_pastor_note(note_id)` to `modules/db.py`.
- [ ] Add "Pastor Notes" tab to `views/Member_Detail.py` gated behind `st.session_state["role"] in ["pastor", "admin", "bishop"]`.
- [ ] Build the note list with reverse-chronological rendering, inline edit form, and delete-with-confirm pattern.
- [ ] Build "New Note" form with text area, date picker, and submit button.
- [ ] Add "Notes" count badge to Member Detail side-summary card (conditional on viewer role).
- [ ] Verify RLS: pastor A cannot query notes created by pastor B; bishop can read both.
- [ ] Sanitize all note text inputs before insert and update.
- [ ] Write `audit_log` entries for create and delete actions.
- [ ] Smoke test: create a note as pastor, verify it appears; log in as bishop, verify read-only; log in as another pastor, verify note is invisible.

---

### Story 4: Group WhatsApp Digest for Pastors

**Priority:** P1
**Points:** 5

> **As a** Pastor who sends weekly updates to my congregation's WhatsApp group,
> **I want** to generate a single formatted text block showing all my members' stats for the past 7 days,
> **so that** I can copy-paste it into WhatsApp in one click without manually compiling numbers.

**Acceptance Criteria:**
1. Pastor Dashboard gains a "WhatsApp Digest" tab (or expander in an existing tab) containing a date-range selector (default: last 7 days ending today) and a "Generate Digest" button.
2. Clicking "Generate Digest" fetches, for each of the pastor's members, their total prayer minutes, chapters read, sermons logged, and current streak for the selected date range using existing `db.py` query functions and the admin client.
3. The generated output is a pre-formatted plain-text block using WhatsApp-friendly formatting (bold via `*text*`, line breaks, emoji bullet points) structured as:
   ```
   *Logos Pulse Weekly Report*
   *[Church Name] | [date range]*

   [Member Name]
   Prayer: X mins | Chapters: Y | Sermons: Z | Streak: N days

   ...

   Total Members Active: N/M
   ```
4. The text is rendered inside a `st.text_area` (read-only, height ~300px) so the pastor can select-all and copy.
5. A "Copy to Clipboard" button uses `st.components.v1.html` to execute a JavaScript `navigator.clipboard.writeText()` call and shows a success toast "Copied to clipboard".
6. Members with zero activity in the date range are listed separately at the bottom of the digest under a "No Activity This Week" section rather than being omitted, so the pastor is aware of them.
7. The pastor can choose to exclude inactive members from the digest using a checkbox ("Include members with no activity"); default is include.
8. The digest respects the current impersonation context in Admin Panel: if an admin is impersonating a pastor, the digest uses that pastor's member list.
9. Generating the digest is logged to `audit_log` with action `whatsapp_digest_generated`, the pastor's ID, and the date range in metadata.
10. The page shows a spinner with text "Compiling stats for N members..." during the fetch so the pastor knows work is in progress.

**Tasks:**
- [ ] Add "WhatsApp Digest" tab (or expander) to `views/Pastor_Dashboard.py` with date-range selector using two `st.date_input` widgets.
- [ ] Write `modules/whatsapp_digest.py` with function `build_group_digest(pastor_id, start_date, end_date)` → formatted string; pull member list via admin client; aggregate prayer minutes, chapters, sermons, streak per member using existing db query patterns.
- [ ] Build the plain-text formatter inside `build_group_digest()` following the structure in AC3; handle zero-activity members in a separate section.
- [ ] Add `st.text_area` with `disabled=True` to display the output and a "Copy to Clipboard" button using `st.components.v1.html` with inline JavaScript.
- [ ] Add "Include members with no activity" checkbox; filter output accordingly.
- [ ] Wire spinner around the `build_group_digest()` call.
- [ ] Add `audit_log` write for `whatsapp_digest_generated` with date range metadata.
- [ ] Verify impersonation context: test as admin impersonating a pastor, confirm digest uses the impersonated pastor's members.
- [ ] Test copy-to-clipboard button in Chrome and Safari (clipboard API requires HTTPS; confirm Streamlit Cloud environment satisfies this).
- [ ] Smoke test end-to-end: generate digest for a 7-day window with at least one active and one inactive member; verify structure matches AC3.

---

### Story 5: Personal Goal Auto-Progress from Daily Entry

**Priority:** P1
**Points:** 6

> **As a** Prayer Warrior tracking a personal goal like "Pray 60 hours this month",
> **I want** my daily logged prayer minutes and chapters to automatically count toward matching goals,
> **so that** I do not have to manually update goal progress after every log.

**Acceptance Criteria:**
1. When a Daily Entry is saved, the system checks the user's active personal goals and auto-increments progress for goals whose `goal_type` matches the logged disciplines: `prayer_minutes` goals increment by the logged prayer minutes, `chapters_read` goals increment by the count of chapters logged, `sermons_logged` goals increment by 1 if a sermon was logged.
2. Auto-progress only applies to goals with a `tracking_mode` of `auto`; goals with `tracking_mode = manual` continue to require the user to update progress by hand as today.
3. A `tracking_mode` column (`auto` or `manual`, default `manual`) is added to the `personal_goals` table; existing goals remain `manual` so no behavior changes for current users.
4. When creating or editing a goal in `views/Personal_Goals.py`, the user can choose the tracking mode via a radio button; if `auto` is selected, the `goal_type` dropdown is restricted to the three automatable types (`prayer_minutes`, `chapters_read`, `sermons_logged`).
5. The auto-increment logic lives in a helper function `modules/goal_tracker.auto_update_goals(user_id, prayer_minutes, chapters_count, sermon_logged)` called at the end of the Daily Entry save flow.
6. `auto_update_goals()` caps progress at the goal's `target_value` so a goal does not overflow past 100%.
7. If the same entry is edited (not created fresh), `auto_update_goals()` computes the delta between old and new values and adjusts goal progress by the delta, not by the raw new value, to avoid double-counting.
8. The Personal Goals page shows a small "Auto" badge next to the progress bar for goals in auto-tracking mode so the user knows progress is managed automatically.
9. All goal progress updates from `auto_update_goals()` are written to the `goal_progress_log` table (if it exists) or to `audit_log` with action `goal_auto_updated`, including the user ID, goal ID, and delta value.
10. Auto-updates do not fire for goals that are already `completed` (`progress >= target_value`).

**Tasks:**
- [ ] Add `tracking_mode text not null default 'manual'` column with check constraint to `personal_goals` in `migrations/001_schema.sql`.
- [ ] Update `views/Personal_Goals.py` goal creation and edit forms to show tracking mode radio buttons; add conditional goal_type restriction for `auto` mode.
- [ ] Add "Auto" badge rendering next to progress bars for `auto`-mode goals in Personal Goals page.
- [ ] Write `modules/goal_tracker.py` with `auto_update_goals(user_id, prayer_minutes, chapters_count, sermon_logged)`: fetch active auto goals, compute increments, cap at target, update via `db.update_goal_progress()`.
- [ ] Handle the edit-delta case: `auto_update_goals()` accepts optional `old_prayer_minutes`, `old_chapters_count`, `old_sermon_logged` params; computes delta when provided.
- [ ] Add `db.update_goal_progress(goal_id, new_progress)` to `modules/db.py` if not already present; add `db.get_active_auto_goals(user_id)` using admin client.
- [ ] Call `goal_tracker.auto_update_goals()` at the end of the Daily Entry save handler in `views/1_Daily_Entry.py`.
- [ ] Write `audit_log` entries for each auto-updated goal.
- [ ] Verify completed goals are skipped (progress already at target).
- [ ] Smoke test: create an `auto` prayer_minutes goal with target 120; log 45 mins on Day 1, log 80 mins on Day 2 (edit); verify progress is 45 then 80 (delta applied), not 125.

---

### Story 6: Church-Wide Stats and Group Engagement Chart for Bishop

**Priority:** P2
**Points:** 7

> **As a** Bishop overseeing multiple pastor groups,
> **I want** to see church-wide prayer hours, chapters read, and active member counts for the current week alongside a bar chart comparing engagement across my pastoral groups,
> **so that** I can identify which groups are thriving and which need extra encouragement.

**Acceptance Criteria:**
1. Bishop Dashboard gains a "Church Overview" section at the top (above the existing pastor list) showing four KPI metric cards: Total Prayer Hours This Week, Total Chapters Read This Week, Active Members This Week (at least 1 log), and Total Members in Diocese.
2. All four metrics are computed using the admin client, scoped to users whose assigned pastor has `bishop_id = current_bishop_id`; data is for the current ISO calendar week (Monday to today).
3. A "Group Engagement" horizontal bar chart is shown below the KPI cards using `plotly.express.bar`; each bar represents one of the bishop's pastoral groups (pastor name on Y-axis) with bar length equal to total prayer minutes logged by that group this week.
4. The chart has a secondary trace (grouped bars or hover data) showing chapters read per group this week so the bishop can compare both disciplines side-by-side.
5. The chart renders responsively using `use_container_width=True` and applies the `COLORS` design tokens from `modules/styles.py` for bar fills so it matches the existing visual design.
6. A week selector (`st.date_input` or a "Previous Week" / "Current Week" toggle) lets the bishop look at prior weeks without being locked to the current week.
7. Each bar in the chart is clickable (via Plotly's click event captured with `st.plotly_chart(on_select="rerun")`) to drill down into the individual member stats for that pastor's group, displayed in an expandable table below the chart.
8. Metrics and chart data are cached in `st.session_state` with a 5-minute TTL using a `last_fetched` timestamp check so repeated navigations do not hammer the database.
9. If a bishop has no pastors assigned, a friendly empty-state card is shown instead of blank metrics.
10. All data queries use the admin client (`get_admin_client()`) and are isolated to the current bishop's hierarchy; no cross-bishop data leakage is possible.

**Tasks:**
- [ ] Write `db.get_church_wide_stats(bishop_id, week_start, week_end)` in `modules/db.py` using admin client; returns dict with `total_prayer_hours`, `total_chapters`, `active_members`, `total_members`.
- [ ] Write `db.get_group_engagement(bishop_id, week_start, week_end)` returning a list of dicts `{pastor_name, pastor_id, total_prayer_minutes, total_chapters}` for Plotly consumption.
- [ ] Add "Church Overview" KPI cards section to `views/Bishop_Dashboard.py` using `st.columns(4)` and `st.metric`.
- [ ] Build Plotly grouped horizontal bar chart in `views/Bishop_Dashboard.py` using `COLORS` tokens for consistent theming.
- [ ] Add week selector UI with current/previous week toggle and manual date picker.
- [ ] Implement `st.plotly_chart(on_select="rerun")` click-to-drilldown; on selection, fetch and display member-level stats for the selected pastor in a `st.dataframe` expander.
- [ ] Add session-state TTL caching (5-minute freshness check) for `church_wide_stats` and `group_engagement` fetch results.
- [ ] Add empty-state card for bishops with no pastors.
- [ ] Verify no cross-bishop data leak: create two test bishops each with one pastor; confirm each bishop's chart shows only their own pastors.
- [ ] Test chart rendering at 375px mobile width; confirm horizontal bar orientation does not overflow on small screens.

---

## Sprint Schedule

### Week 1 (2026-05-16 to 2026-05-22)

| Day | Focus | Hours |
|-----|-------|-------|
| Fri May 16 | Story 1: Add `status` column migration; update `enroll_in_plan()` and `get_member_active_plan()`; build Browse Plans UI with plan cards and Start button | 6 |
| Mon May 19 | Story 1: Switch Plan expander, audit log wiring, Pastor Dashboard assign-override confirmation, Already Completed badges; smoke test enrollment flow | 6 |
| Tue May 20 | Story 2: `modules/bulk_import.py` scaffold — `parse_csv()`, `validate_rows()` with all validation checks; Admin Panel Bulk Import tab, template download button | 6 |
| Wed May 21 | Story 2: `create_accounts()` with progress streaming, preview table UI with row color coding, audit log integration; smoke test 5-row mixed CSV | 6 |
| Thu May 22 | Story 3: `pastor_notes` table + RLS migration; db helper functions; "Pastor Notes" tab scaffold in Member Detail with role gate | 6 |

### Week 2 (2026-05-23 to 2026-05-30)

| Day | Focus | Hours |
|-----|-------|-------|
| Fri May 23 | Story 3: Note list (reverse-chron), inline edit form, delete-with-confirm, Notes count badge on summary card, audit log; RLS smoke test | 6 |
| Mon May 26 | Story 4: `modules/whatsapp_digest.py` — member stat aggregation, plain-text formatter, inactive member section; Pastor Dashboard WhatsApp Digest tab | 6 |
| Tue May 27 | Story 4: Copy-to-clipboard JS component, "Include inactive" checkbox, spinner, audit log; cross-browser clipboard test; impersonation context test | 6 |
| Wed May 28 | Story 5: `tracking_mode` column migration; `modules/goal_tracker.py` with delta logic; Personal Goals form updates (radio + type restriction + Auto badge) | 6 |
| Thu May 29 | Story 5: Wire `auto_update_goals()` into Daily Entry save; edit-delta handling; audit log; smoke test over-target cap and completed-goal skip | 3 |
|            | Story 6: `db.get_church_wide_stats()` and `db.get_group_engagement()`; Bishop Dashboard KPI cards; week selector | 3 |
| Fri May 30 | Story 6: Plotly grouped bar chart with COLORS theming; click-to-drilldown; TTL session cache; empty-state card; mobile regression; final full-app smoke test | 6 |

---

## Definition of Done

- [ ] Code committed to main branch
- [ ] All acceptance criteria verified manually
- [ ] No new `st.error` tracebacks visible to end users
- [ ] Mobile responsive (tested at 375px width)
- [ ] No regression in existing features (Daily Entry, Bible Reader, Prayer Journal, Reading Plan daily flow)
- [ ] Deployed and smoke-tested on https://logos-pulse.streamlit.app/
- [ ] New tables and columns present in `migrations/001_schema.sql` with RLS policies
- [ ] All user text inputs pass through `sanitize_html()` before DB write
- [ ] New pages and tabs call `require_login()`, `require_password_changed()`, and `apply_shared_styles()` at the top
- [ ] Admin-only features guarded with `require_role(["admin"])` at the page or tab level
- [ ] Role-gated UI elements (Pastor Notes tab, WhatsApp Digest tab, Bulk Import tab) verified invisible to lower roles
- [ ] All bulk/batch operations handle per-row exceptions without aborting the entire operation
- [ ] Audit log entries present for every write action introduced in this sprint

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `navigator.clipboard.writeText()` blocked in some browsers or non-HTTPS environments | Medium | Medium (Story 4 copy button) | Detect clipboard API availability; fallback to selecting all text in the `st.text_area` automatically so the user can manually Ctrl+C; show a tooltip explaining the fallback |
| Daily Entry edit-delta logic for auto-goals is complex and error-prone with multiple discipline types | Medium | Medium (Story 5 correctness) | Unit-test `auto_update_goals()` in isolation with fixed inputs before wiring to the UI; write explicit test cases for the zero-old-value, non-zero-old-value, and completed-goal cases as inline assertions or a test script |
| CSV import performance: creating 50+ accounts sequentially via the Supabase admin API may time out in Streamlit | Low | Medium (Story 2 usability) | Process rows in a loop with a progress bar rather than async; add a per-row 200ms sleep to avoid Supabase rate limiting; document a max recommended import size of 100 rows per batch |
| `reading_plan_progress` rows left in ambiguous state if browser closes mid-enrollment | Low | Low (Story 1 data integrity) | The upsert-then-insert pattern is a single atomic operation per call; abandoned row is written before new row; no partial state is possible within a single `db.enroll_in_plan()` call |
| Bishop chart Plotly click event (`on_select="rerun"`) requires Streamlit >= 1.33; version mismatch could break the page | Medium | Medium (Story 6 drilldown) | Check `streamlit.__version__` at app startup and fall back to a selectbox-based group picker if `on_select` is unavailable; note the Streamlit version requirement in `requirements.txt` comment |
| `get_group_engagement()` query over large `daily_entries` table (joined to profiles and users) may be slow without proper indexes | Low | Medium (Story 6 performance) | Add a composite index on `daily_entries(entry_date, user_id)` if not already present from Sprint 6's care view migration; confirm query plan in Supabase SQL Editor before shipping |
| Personal Goals page already has a manual progress slider; auto-mode users may be confused if they also try to drag the slider | Low | Low (Story 5 UX) | Disable the manual progress slider for goals in `auto` tracking mode and show a tooltip: "Progress is updated automatically from your daily log entries" |

---

## Backlog Items Deferred to Sprint 8+

| Item | Reason |
|------|--------|
| Prayer Request Sharing | Requires a full moderation workflow (submit → pastor review → approve/reject → public wall) with RLS policies for pending vs approved states; needs its own design session before scheduling |
| Multi-Church Tenancy | Architectural change requiring tenant isolation across every table, RLS policy, and auth flow; estimated 40+ SP; not feasible without a dedicated planning spike |
| WhatsApp Bot | Requires WhatsApp Business API approval and ongoing message costs; no credentials available; not feasible without external procurement |
| Reading Plan: custom plan builder | Pastors authoring their own reading plans with a day-by-day editor is valuable but non-urgent given 3 built-in plans are live; schedule when a pastor explicitly requests it |
| Sermon Note AI Summary | LLM-assisted summarization of sermon notes requires external API key budget approval and privacy review; deferred pending decision |
