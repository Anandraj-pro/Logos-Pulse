# Sprint 2 Plan -- Logos Pulse

**Sprint Goal:** Make the app ready for real-user onboarding by enabling pastor-led group workflows, polishing the mobile experience, and cleaning up test artifacts.

**Sprint Dates:** 2026-03-31 to 2026-04-13 (2 weeks)
**Capacity:** 1 developer, ~6 hrs/day, 5 days/week = 60 hrs total
**Velocity estimate:** ~30 story points (based on Sprint 1 actuals)

---

## Sprint Backlog Summary

| # | Story | Points | Priority | Status |
|---|-------|--------|----------|--------|
| S2-01 | Group Bible Reading Assignments (Pastor) | 8 | P0 | To Do |
| S2-02 | Member View of Group Assignments | 5 | P0 | To Do |
| S2-03 | WhatsApp Report -- Dynamic Pastor Name | 3 | P0 | To Do |
| S2-04 | Pastor Dashboard -- Member Report Status | 3 | P0 | To Do |
| S2-05 | Mobile UI Polish -- Login and Navigation | 3 | P1 | To Do |
| S2-06 | Mobile UI Polish -- Core Pages | 5 | P1 | To Do |
| S2-07 | Empty States for New Users | 2 | P1 | To Do |
| S2-08 | Clean Up Test Data and Dead Code | 2 | P1 | To Do |
| S2-09 | Bible Reader Caching in Supabase | 3 | P2 | To Do |
| **Total** | | **34** | | |

> 34 points is slightly above the 30-point estimate. S2-09 (P2) is the overflow buffer -- it moves to Sprint 3 if velocity is tight.

---

## User Stories

---

### S2-01: Group Bible Reading Assignments (Pastor Creates)

**Priority:** P0
**Points:** 8
**Epic:** Group Assignments

> As a **Pastor**, I want to create Bible reading assignments for my entire group so that my members have a shared daily reading plan.

**Acceptance Criteria:**

1. Pastor sees an "Assignments" section on the Pastor Dashboard.
2. Pastor can create an assignment with: title, Bible book/chapter/verse range, due date, and optional notes.
3. Assignment is stored in a new `group_assignments` table scoped to the pastor's `group_id`.
4. Pastor can view, edit, and delete their own assignments.
5. RLS policy ensures a pastor can only manage assignments for their own group.
6. Assignments are listed in reverse chronological order with status (active / past due).

**Task Breakdown:**

| Task | Est. |
|------|------|
| Design and create `group_assignments` table + RLS policies in Supabase | 1.5 hr |
| Add `db.py` functions: `create_assignment`, `update_assignment`, `delete_assignment`, `get_group_assignments` | 2 hr |
| Build Pastor Dashboard UI section for assignment CRUD | 3 hr |
| Input validation and sanitization for assignment fields | 0.5 hr |
| Unit/manual testing of RLS (pastor A cannot see pastor B's assignments) | 1 hr |

---

### S2-02: Member View of Group Assignments

**Priority:** P0
**Points:** 5
**Epic:** Group Assignments

> As a **Prayer Warrior (member)**, I want to see the Bible reading assignments my pastor has created so that I know what to read each day.

**Acceptance Criteria:**

1. Members see an "Assignments" card/section on their Dashboard.
2. Only active (not past-due) assignments are shown by default, with a toggle for "Show past."
3. Each assignment shows title, scripture reference (linked to Bible Reader page), due date, and notes.
4. Member can mark an assignment as "completed" for themselves (tracked in `assignment_completions` table).
5. Completion status persists across sessions.
6. RLS ensures members see only their own group's assignments.

**Task Breakdown:**

| Task | Est. |
|------|------|
| Create `assignment_completions` table + RLS policies | 1 hr |
| Add `db.py` functions: `get_my_assignments`, `mark_assignment_complete`, `get_completion_status` | 1.5 hr |
| Build member Dashboard section -- assignment list with completion toggle | 2.5 hr |
| Deep-link scripture reference to Bible Reader page | 0.5 hr |
| Test as Prayer Warrior: see only own group, mark complete, re-login persists | 1 hr |

---

### S2-03: WhatsApp Report -- Dynamic Pastor Name

**Priority:** P0
**Points:** 3
**Epic:** WhatsApp Report Enhancement

> As a **Prayer Warrior**, I want the WhatsApp report to address my pastor by name (from the database) so that I do not have to edit it manually every time.

**Acceptance Criteria:**

1. WhatsApp report greeting uses the pastor's `preferred_name` from the `profiles` table (looked up via the member's `group_id` -> pastor's profile).
2. If no pastor is assigned, falls back to "Pastor" as the default.
3. The old hardcoded pastor name from `settings` is no longer used for report generation.
4. Existing report format and content are otherwise unchanged.

**Task Breakdown:**

| Task | Est. |
|------|------|
| Add `db.py` function: `get_my_pastor_name(user_id)` -- join profiles via groups | 1 hr |
| Update WhatsApp report generation to call `get_my_pastor_name` | 0.5 hr |
| Remove/deprecate the hardcoded pastor-name setting path | 0.5 hr |
| Test with member who has a pastor, and member with no pastor assigned | 0.5 hr |

---

### S2-04: Pastor Dashboard -- Member Report Status

**Priority:** P0
**Points:** 3
**Epic:** WhatsApp Report Enhancement

> As a **Pastor**, I want to see which of my group members have sent their WhatsApp report today so that I can follow up with those who have not.

**Acceptance Criteria:**

1. Pastor Dashboard shows a "Today's Reports" section with a list of group members.
2. Each member shows a green check if `report_copied` is true for today, gray otherwise.
3. List is sorted: members who have NOT reported appear first.
4. Data comes from the existing `report_copied` tracking (no new tables needed).
5. RLS ensures pastor sees only their own group's members.

**Task Breakdown:**

| Task | Est. |
|------|------|
| Add `db.py` function: `get_group_report_status(pastor_id, date)` | 1 hr |
| Build "Today's Reports" UI component on Pastor Dashboard | 1.5 hr |
| Style: green/gray indicators, sort unreported first | 0.5 hr |
| Test with multiple members, some with reports, some without | 0.5 hr |

---

### S2-05: Mobile UI Polish -- Login and Navigation

**Priority:** P1
**Points:** 3
**Epic:** UI Polish

> As a **user on a mobile phone**, I want the login page and sidebar navigation to work well on small screens so that I can use the app comfortably from my phone.

**Acceptance Criteria:**

1. Login page renders cleanly on 375px-width screens (iPhone SE baseline).
2. Input fields and buttons are full-width on mobile, with adequate tap targets (min 44px height).
3. Sidebar collapses properly; page content does not overflow horizontally.
4. Custom CSS is injected via `st.markdown` (no external dependencies).
5. Tested on Chrome mobile emulator for iPhone SE, iPhone 14, and Galaxy S21.

**Task Breakdown:**

| Task | Est. |
|------|------|
| Audit current login page on mobile emulator, document issues | 0.5 hr |
| Write responsive CSS overrides for login form | 1.5 hr |
| Fix sidebar/nav overflow issues | 1 hr |
| Cross-device testing and adjustments | 0.5 hr |

---

### S2-06: Mobile UI Polish -- Core Pages

**Priority:** P1
**Points:** 5
**Epic:** UI Polish

> As a **user on a mobile phone**, I want the Dashboard, Prayer Journal, Bible Reader, and WhatsApp Report pages to display properly on small screens.

**Acceptance Criteria:**

1. Dashboard cards stack vertically on screens < 768px.
2. Prayer Journal text areas are full-width; timer controls are thumb-friendly.
3. Bible Reader text is readable without horizontal scrolling.
4. WhatsApp Report copy button is prominently placed and easy to tap.
5. Tables (if any) scroll horizontally rather than breaking layout.
6. Consistent loading spinners on all pages (replace any bare `st.spinner` text).

**Task Breakdown:**

| Task | Est. |
|------|------|
| Dashboard responsive layout fixes | 1.5 hr |
| Prayer Journal mobile fixes | 1 hr |
| Bible Reader mobile fixes | 1 hr |
| WhatsApp Report mobile fixes | 0.5 hr |
| Add consistent loading states across pages | 1 hr |
| Full regression on mobile emulator | 1 hr |

---

### S2-07: Empty States for New Users

**Priority:** P1
**Points:** 2
**Epic:** UI Polish

> As a **new user** who has just been onboarded, I want to see helpful guidance instead of blank pages so that I understand what to do first.

**Acceptance Criteria:**

1. Dashboard shows a welcome message and "Getting Started" checklist when no entries exist.
2. Prayer Journal shows a prompt to start the first prayer session (not a blank page).
3. Bible Reader shows a suggested starting passage (e.g., Psalm 1).
4. Empty states include a clear call-to-action button.

**Task Breakdown:**

| Task | Est. |
|------|------|
| Design empty-state messages for Dashboard, Prayer Journal, Bible Reader | 0.5 hr |
| Implement conditional rendering on each page (check for zero data) | 1.5 hr |
| Test with a fresh user account | 0.5 hr |

---

### S2-08: Clean Up Test Data and Dead Code

**Priority:** P1
**Points:** 2
**Epic:** Technical Debt

> As a **developer**, I want to remove test accounts, dead code, and unrelated files so that the codebase is clean before onboarding real users.

**Acceptance Criteria:**

1. Test accounts (bishop.test@, pastor.test@, warrior.test@) are deleted from Supabase (or documented in a cleanup script that can be run before production).
2. All `db.init_db()` calls are removed from page files (it is a no-op).
3. The `menu_style` file in root is removed.
4. No functional regressions after cleanup.

**Task Breakdown:**

| Task | Est. |
|------|------|
| Write a Supabase cleanup script to remove test accounts | 0.5 hr |
| Grep and remove all `db.init_db()` calls | 0.5 hr |
| Remove `menu_style` file | 0.1 hr |
| Regression test: login, dashboard, prayer journal, report | 1 hr |

---

### S2-09: Bible Reader Caching in Supabase (Stretch)

**Priority:** P2
**Points:** 3
**Epic:** Performance

> As a **user**, I want Bible chapters to load quickly even on slow connections so that my reading experience is smooth.

**Acceptance Criteria:**

1. When a Bible chapter is fetched from the external API, it is cached in a `bible_cache` table in Supabase.
2. Subsequent reads of the same chapter hit the cache first.
3. Cache entries include a `fetched_at` timestamp; entries older than 30 days are re-fetched.
4. If the external API is down, cached content is served without error.
5. Cache table has no RLS (public read, service-role write).

**Task Breakdown:**

| Task | Est. |
|------|------|
| Create `bible_cache` table in Supabase (book, chapter, version, content, fetched_at) | 0.5 hr |
| Add cache-read logic before API call in Bible Reader module | 1 hr |
| Add cache-write logic after successful API fetch | 0.5 hr |
| Handle stale cache (> 30 days) and API-down fallback | 0.5 hr |
| Test with network throttling | 0.5 hr |

---

## Sprint Calendar (Suggested)

### Week 1 (Mar 31 -- Apr 4): Core Features

| Day | Focus | Stories |
|-----|-------|---------|
| Tue Mar 31 | Group assignments DB + RLS + pastor CRUD | S2-01 |
| Wed Apr 1 | Finish pastor CRUD, start member view | S2-01, S2-02 |
| Thu Apr 2 | Member assignment view + completion tracking | S2-02 |
| Fri Apr 3 | WhatsApp dynamic pastor name + pastor report status | S2-03, S2-04 |
| Sat Apr 4 | Buffer / testing catch-up | S2-01 through S2-04 |

### Week 2 (Apr 7 -- Apr 11): Polish and Cleanup

| Day | Focus | Stories |
|-----|-------|---------|
| Mon Apr 7 | Mobile polish: login + nav | S2-05 |
| Tue Apr 8 | Mobile polish: core pages | S2-06 |
| Wed Apr 9 | Finish mobile polish + empty states | S2-06, S2-07 |
| Thu Apr 10 | Test data cleanup + dead code removal | S2-08 |
| Fri Apr 11 | Bible caching (stretch) + sprint demo prep | S2-09 |

---

## Definition of Done

A story is **Done** when:

1. Code is committed to `main` branch.
2. Acceptance criteria are verified manually (and via test script where applicable).
3. RLS policies are verified for any new tables.
4. Input sanitization is applied to any new user inputs.
5. Mobile rendering is checked on Chrome DevTools (375px width minimum).
6. No console errors or unhandled exceptions in Streamlit logs.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Group assignment schema may need iteration after pastor feedback | Medium | Build MVP schema first, plan a follow-up story in Sprint 3 for enhancements |
| Mobile CSS in Streamlit is limited (no full control over framework elements) | Medium | Focus on injectable CSS; accept Streamlit sidebar limitations |
| Bible API rate limits may complicate caching testing | Low | S2-09 is P2 stretch; can defer without impact |
| Single developer bottleneck | High | Strict priority ordering; P2 is explicitly deferrable |

---

## Deferred to Sprint 3+

These items remain in the backlog and were deliberately excluded from Sprint 2:

- **Seed Data Management UI** (Admin manages default prayers/confessions) -- not blocking onboarding
- **User Documentation** (Admin guide, Prayer Warrior guide) -- plan for Sprint 3
- **Notifications/Reminders** (email or in-app) -- requires infrastructure decisions, zero budget constraint
- **Consistent loading states** -- partially addressed in S2-06; full audit in Sprint 3