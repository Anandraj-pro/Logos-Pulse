# Sprint 3 Plan -- Logos Pulse

**Sprint Goal:** Make the app stickier for daily use, improve performance under growth, and polish the experience to build trust as user base scales from 100 toward 1,500.

**Sprint Dates:** 2026-03-31 to 2026-04-13 (2 weeks)
**Capacity:** 1 developer, ~6 hrs/day, 5 days/week = 60 hrs total
**Velocity Estimate:** ~30 story points (based on 1 SP ~ 2 hrs avg)

---

## Sprint Backlog Summary

| #  | Story                                      | Points | Priority | Week |
|----|--------------------------------------------|--------|----------|------|
| 1  | Data analytics/charts for Prayer Warriors  | 5      | P0       | 1    |
| 2  | Supabase query caching (performance)       | 3      | P0       | 1    |
| 3  | Bible Reader caching                       | 3      | P0       | 1    |
| 4  | Dashboard nudge reminders                  | 3      | P1       | 1    |
| 5  | Streak leaderboard on Pastor Dashboard     | 3      | P1       | 2    |
| 6  | Pastor edit/delete group assignments        | 3      | P1       | 2    |
| 7  | Error recovery and connection resilience   | 5      | P1       | 2    |
| 8  | Settings page integration with Profile     | 3      | P2       | 2    |
|    | **Total**                                  | **28** |          |      |

Stretch goal (if time permits):
- Seed Data Management admin UI (5 pts, P2)

---

## User Stories -- Detail

---

### Story 1: Data Analytics / Charts for Prayer Warriors

**Priority:** P0
**Points:** 5
**Backlog Item:** #8 (Data analytics/charts)

> **As a** Prayer Warrior,
> **I want** to see charts of my prayer time trends, Bible reading progress, and streak history over time,
> **so that** I can visualize my spiritual growth and stay motivated.

**Acceptance Criteria:**

1. Dashboard shows a line chart of daily prayer minutes for the last 30 days.
2. Dashboard shows a bar chart of Bible chapters read per week for the last 8 weeks.
3. Dashboard shows a streak history chart (current streak, longest streak, streak over time).
4. Charts render in under 2 seconds on a typical connection.
5. Charts are mobile responsive (readable on 375px-width screens).
6. Pastor Dashboard shows an aggregate engagement chart (avg prayer minutes across group, daily active users over time).

**Tasks:**

- [ ] Install/confirm Plotly available in requirements
- [ ] Create `modules/charts.py` with reusable chart builders: `prayer_trend_chart()`, `reading_progress_chart()`, `streak_history_chart()`
- [ ] Query helpers in `modules/supabase_client.py` for aggregated data (last 30 days prayer, last 8 weeks reading)
- [ ] Integrate charts into Prayer Warrior dashboard
- [ ] Add pastor-level aggregate engagement chart to Pastor Dashboard
- [ ] Mobile responsive styling for chart containers
- [ ] Manual test on desktop and mobile viewports

---

### Story 2: Supabase Query Caching (Performance)

**Priority:** P0
**Points:** 3
**Backlog Item:** #11 (Performance optimization)

> **As a** user,
> **I want** pages to load faster,
> **so that** the app feels responsive even as user count grows.

**Acceptance Criteria:**

1. Read-only Supabase queries on Dashboard, Daily Log, Streaks & Stats, and Sermon Notes pages use `st.cache_data` with a TTL of 5 minutes.
2. Write operations (inserts/updates) clear relevant caches immediately.
3. No stale data shown after a user submits a new entry (cache invalidated on write).
4. Page load time for Dashboard drops by at least 40% on repeat visits (measured via browser dev tools).
5. No caching applied to auth/session calls.

**Tasks:**

- [ ] Audit all Supabase read queries across pages -- identify cacheable calls
- [ ] Wrap cacheable queries with `@st.cache_data(ttl=300)` in query helper functions
- [ ] Add `st.cache_data.clear()` calls after write operations in relevant pages
- [ ] Exclude auth and RLS-sensitive queries from caching
- [ ] Load-test Dashboard page before/after -- document timing improvement
- [ ] Regression test: submit daily entry, confirm it appears immediately

---

### Story 3: Bible Reader Caching

**Priority:** P0
**Points:** 3
**Backlog Item:** #2 (Bible Reader Caching)

> **As a** Prayer Warrior,
> **I want** Bible text to load instantly after the first read,
> **so that** I can read without waiting for external API calls every time.

**Acceptance Criteria:**

1. When a Bible chapter is fetched from the external API, it is stored in a `bible_cache` Supabase table.
2. Subsequent requests for the same chapter are served from the cache table, not the external API.
3. Cache entries include `book`, `chapter`, `version`, `content`, and `cached_at` columns.
4. If the external API is unreachable, cached content is served with a notice: "Loaded from cache."
5. Cache has no expiry (Bible text is immutable).
6. RLS policy: `bible_cache` is readable by all authenticated users, writable only by service role.

**Tasks:**

- [ ] Create `bible_cache` table in Supabase with columns: `id`, `book`, `chapter`, `version`, `content`, `cached_at`
- [ ] Add RLS policy: SELECT for authenticated, INSERT/UPDATE for service role only
- [ ] Create migration SQL script in `migrations/`
- [ ] Modify Bible reader module: check cache first, fall back to API, store result on miss
- [ ] Add "Loaded from cache" indicator when API is unreachable but cache hit succeeds
- [ ] Test with API disabled (network off) to confirm graceful fallback

---

### Story 4: Dashboard Nudge Reminders

**Priority:** P1
**Points:** 3
**Backlog Item:** #4 (Notifications/Reminders)

> **As a** Prayer Warrior,
> **I want** to see a reminder on my dashboard if I have not logged today's entry,
> **so that** I am nudged to maintain my daily habit and streak.

**Acceptance Criteria:**

1. If the user has not submitted a daily entry for today, the dashboard shows a prominent reminder card at the top: "You haven't logged today's entry yet. Keep your streak alive!"
2. The reminder includes a direct link/button to the Daily Entry page.
3. If the user has already logged today, the reminder is replaced with an encouragement: "Great job today! Streak: X days."
4. Pastors see a summary nudge: "X of Y members have not logged today."
5. Nudge logic does not add extra API calls (piggybacks on existing dashboard data fetch).

**Tasks:**

- [ ] Add check in dashboard load: query today's entry status for current user
- [ ] Design nudge card component (Streamlit container with color styling)
- [ ] Add "Go to Daily Entry" button that navigates to the entry page
- [ ] Add encouragement variant when entry exists
- [ ] Pastor dashboard: count members without today's entry from existing group data
- [ ] Test edge cases: timezone handling, first day with no history

---

### Story 5: Streak Leaderboard on Pastor Dashboard

**Priority:** P1
**Points:** 3
**Backlog Item:** #6 (Streak leaderboard)

> **As a** Pastor,
> **I want** to see a ranked leaderboard of my group members by streak length,
> **so that** I can recognize consistent members and encourage those falling behind.

**Acceptance Criteria:**

1. Pastor Dashboard shows a "Streak Leaderboard" section with members ranked by current streak (descending).
2. Each row shows: rank, member name, current streak (days), longest streak.
3. Members with zero streak are shown at the bottom with visual distinction.
4. Leaderboard is limited to the pastor's assigned group members only (RLS enforced).
5. Leaderboard data is cached (Story 2 caching pattern) with 5-minute TTL.

**Tasks:**

- [ ] Create query helper: fetch streak data for all members in pastor's group
- [ ] Build leaderboard UI component with `st.dataframe` or styled table
- [ ] Add rank column, sort by current streak descending
- [ ] Visual styling: highlight top 3, gray out zero-streak members
- [ ] Integrate into Pastor Dashboard page
- [ ] Apply `st.cache_data` with TTL to the leaderboard query
- [ ] Test with pastor account having 5+ members

---

### Story 6: Pastor Edit/Delete Group Assignments

**Priority:** P1
**Points:** 3
**Backlog Item:** #5 (Pastor edit/delete assignments)

> **As a** Pastor,
> **I want** to edit or cancel group assignments I have created,
> **so that** I can correct mistakes and manage my group flexibly.

**Acceptance Criteria:**

1. On the group assignments page, each existing assignment shows "Edit" and "Delete" action buttons.
2. Edit opens a form pre-filled with current assignment data; pastor can modify and save.
3. Delete shows a confirmation dialog before removing the assignment.
4. Changes are reflected immediately in the UI after save/delete.
5. RLS enforced: pastors can only edit/delete assignments they own.
6. Deleted assignments are soft-deleted (status column set to "cancelled", not hard-deleted).

**Tasks:**

- [ ] Add `status` column to assignments table if not present (migration script)
- [ ] Create update and soft-delete query helpers
- [ ] Add Edit button per assignment row -- opens editable form in expander or modal
- [ ] Add Delete button with `st.warning` confirmation step
- [ ] Update RLS policy to allow UPDATE on own assignments
- [ ] Refresh UI after mutation (clear cache, rerun)
- [ ] Test: create, edit, delete assignment as pastor; verify as another pastor that foreign assignments are not visible

---

### Story 7: Error Recovery and Connection Resilience

**Priority:** P1
**Points:** 5
**Backlog Item:** #10 (Error recovery)

> **As a** user,
> **I want** the app to handle connection failures gracefully,
> **so that** I do not lose my work or see confusing error messages.

**Acceptance Criteria:**

1. All Supabase calls are wrapped in try/except with user-friendly error messages (no raw tracebacks shown).
2. On connection failure, the app shows: "Connection issue. Your data is safe. Please try again." with a retry button.
3. Token expiry mid-session is detected; user is prompted to re-login with a clear message (not a crash).
4. Form submissions that fail due to network issues preserve the user's input in session state so they can retry without re-entering data.
5. A `modules/error_handler.py` utility provides a reusable decorator/context manager for Supabase calls.

**Tasks:**

- [ ] Create `modules/error_handler.py` with `@safe_supabase_call` decorator and `SupabaseError` context manager
- [ ] Wrap all Supabase calls in pages with error handler (audit every page file)
- [ ] Add token expiry detection: catch 401/JWT errors, redirect to login with message
- [ ] Add form input preservation: store form values in `st.session_state` before submission
- [ ] Add retry button component that re-executes the failed operation
- [ ] Test: simulate network failure (invalid Supabase URL), verify graceful handling on each page
- [ ] Test: simulate expired token, verify re-login prompt

---

### Story 8: Settings Page Integration with Profile

**Priority:** P2
**Points:** 3
**Backlog Item:** #9 (Improve Settings page)

> **As a** user,
> **I want** the Settings page to be merged with my Profile page,
> **so that** all my preferences are in one place and the navigation is simpler.

**Acceptance Criteria:**

1. Profile page has a new "Preferences" tab/section containing all current Settings functionality.
2. The standalone Settings page is removed from the sidebar navigation.
3. Existing settings values are preserved during migration (no data loss).
4. Profile page tabs: Personal Info | Password | Preferences.
5. "Notification preferences" placeholder toggle is added (for future use, stored in user settings).

**Tasks:**

- [ ] Read current Settings page logic and identify all settings fields
- [ ] Add "Preferences" tab to Profile page with the same fields
- [ ] Move settings read/write logic into Profile page
- [ ] Add notification preference toggle (stored in settings table, no backend action yet)
- [ ] Remove or redirect the old Settings page file
- [ ] Update sidebar navigation to remove Settings entry
- [ ] Test: change a setting via new Profile Preferences tab, confirm persistence

---

## Sprint Schedule

### Week 1 (March 31 -- April 4)

| Day | Focus                                          | Hours |
|-----|------------------------------------------------|-------|
| Tue | Story 2: Supabase caching -- audit + implement | 6     |
| Wed | Story 2: finish caching + Story 3: Bible cache table + migration | 6     |
| Thu | Story 3: Bible reader cache logic + fallback   | 6     |
| Fri | Story 1: Chart module + prayer trend chart      | 6     |
| Sat | Story 1: Reading + streak charts, pastor aggregate chart | 6     |

### Week 2 (April 7 -- April 11)

| Day | Focus                                          | Hours |
|-----|------------------------------------------------|-------|
| Mon | Story 4: Dashboard nudge reminders             | 6     |
| Tue | Story 5: Streak leaderboard                    | 6     |
| Wed | Story 6: Pastor edit/delete assignments         | 6     |
| Thu | Story 7: Error handler module + wrap pages (part 1) | 6     |
| Fri | Story 7: Finish error wrapping + Story 8: Settings merge | 6     |

---

## Definition of Done

- [ ] Code is committed to `main` branch
- [ ] All acceptance criteria verified manually
- [ ] No new `st.error` tracebacks visible to end users
- [ ] Mobile responsive (tested at 375px width)
- [ ] No regression in existing features (login, daily entry, streaks, sermon notes, prayer journal)
- [ ] Deployed to https://logos-pulse.streamlit.app/ and smoke-tested

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Plotly charts too heavy for Streamlit Cloud free tier | Medium | High | Use `st.plotly_chart(use_container_width=True)` with lightweight configs; fall back to `st.bar_chart`/`st.line_chart` if needed |
| Bible API caching table grows large | Low | Low | Bible text is finite (~1,200 chapters); total cache < 50 MB |
| Error handler refactor touches every page | Medium | Medium | Use decorator pattern to minimize code changes per file; do not refactor business logic |
| Caching causes stale data bugs | Medium | High | Always clear cache on writes; keep TTL short (5 min); test write-then-read flows |

---

## Backlog Items Deferred to Sprint 4+

| Item | Reason |
|------|--------|
| Seed Data Management (admin UI) | Lower impact on daily stickiness; stretch goal if Sprint 3 finishes early |
| User Documentation | Important for onboarding at scale but no feature dependency yet |
| Prayer Sharing | Needs UX design discussion; not urgent for current user base |
| WhatsApp Business API | Requires budget; not feasible at zero cost |