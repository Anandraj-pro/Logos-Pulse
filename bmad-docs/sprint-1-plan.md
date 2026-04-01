# Sprint 1 Plan -- Logos Pulse

**Sprint Duration:** 2 weeks (April 1 -- April 14, 2026)
**Team:** 1 developer (Bhargavi), ~6 hours/day, 5 days/week
**Total Capacity:** 60 hours / ~40 story points (assuming ~1.5 hrs per point)

---

## Sprint Goal

Stabilize the multi-user auth system by completing end-to-end testing across all four roles, fixing critical bugs, migrating existing data to Supabase, and delivering a functional Profile page -- so that the app is reliable enough for the first 100 real users.

---

## Sprint Backlog

### Epic 1: Testing and Bug Fixes (Critical Foundation)

---

#### Story 1.1 -- Admin Account Creation E2E Testing
**Priority:** P0
**Story Points:** 3

> **As an** Admin,
> **I want to** create Bishop, Pastor, and Prayer Warrior accounts end-to-end,
> **So that** I can onboard the initial 100 users with confidence.

**Acceptance Criteria:**
- [ ] Admin can create a Bishop account; Bishop receives default password and can log in
- [ ] Admin can create a Pastor account and assign to a Bishop; Pastor can log in
- [ ] Admin can create a Prayer Warrior account and assign to a Pastor; Prayer Warrior can log in
- [ ] First-login mandatory password change works for all three roles
- [ ] Admin can edit and deactivate any user account
- [ ] Admin analytics page loads without errors

**Tasks:**
1. Write manual test script covering all Admin CRUD operations (0.5 hr)
2. Execute test script for Bishop creation flow (0.5 hr)
3. Execute test script for Pastor creation flow (0.5 hr)
4. Execute test script for Prayer Warrior creation flow (0.5 hr)
5. Test account edit and deactivation (0.5 hr)
6. Log bugs found, fix, and re-test (2 hrs)

---

#### Story 1.2 -- Role-Based Login Flow Verification
**Priority:** P0
**Story Points:** 2

> **As a** user of any role,
> **I want to** log in and be routed to the correct dashboard for my role,
> **So that** I see only the features and data relevant to me.

**Acceptance Criteria:**
- [ ] Admin login redirects to Admin Panel
- [ ] Bishop login shows Bishop Dashboard with pastor oversight and aggregate stats
- [ ] Pastor login shows Pastor Dashboard with member tracking and daily log status
- [ ] Prayer Warrior login shows standard feature pages (Daily Entry, Streaks, etc.)
- [ ] Sidebar navigation shows only role-appropriate pages
- [ ] Logout fully clears session state

**Tasks:**
1. Test login for each of the 4 roles, document results (1 hr)
2. Verify sidebar menu items per role (0.5 hr)
3. Test logout and session clearing (0.5 hr)
4. Fix routing or guard bugs found (1 hr)

---

#### Story 1.3 -- Data Isolation Verification
**Priority:** P0
**Story Points:** 3

> **As a** Prayer Warrior,
> **I want** my personal data (daily entries, prayer journal, sermon notes) to be invisible to other Prayer Warriors,
> **So that** my spiritual life remains private.

**Acceptance Criteria:**
- [ ] Prayer Warrior A cannot see Prayer Warrior B's daily entries
- [ ] Prayer Warrior A cannot see Prayer Warrior B's prayer journal entries
- [ ] Prayer Warrior A cannot see Prayer Warrior B's sermon notes
- [ ] Pastor can see aggregated status of their own members only (not other pastors' members)
- [ ] Bishop can see aggregated stats for their own pastors only (not other bishops' pastors)
- [ ] RLS policies are verified via direct Supabase query as well as app UI

**Tasks:**
1. Create 2 test Prayer Warrior accounts under different Pastors (0.5 hr)
2. Add sample data for both accounts (0.5 hr)
3. Log in as each and verify data isolation in every feature page (1.5 hr)
4. Verify Pastor Dashboard scoping (1 hr)
5. Verify Bishop Dashboard scoping (0.5 hr)
6. Fix any RLS or query-level isolation bugs (1 hr)

---

#### Story 1.4 -- Original Feature Regression Testing with Supabase
**Priority:** P0
**Story Points:** 5

> **As a** Prayer Warrior,
> **I want** all original features (Daily Entry, Daily Log, Weekly Assignment, Streaks and Stats, Sermon Notes, Prayer Journal, Settings) to work correctly with the Supabase backend,
> **So that** the migration from SQLite did not break my daily spiritual practice tools.

**Acceptance Criteria:**
- [ ] Daily Entry: can create, save, and view past entries
- [ ] Daily Log: log renders correctly for current and past dates
- [ ] Weekly Assignment: can view and complete weekly assignments
- [ ] Streaks and Stats: streak count is accurate; stats charts render
- [ ] Sermon Notes: can create, edit, delete sermon notes
- [ ] Prayer Journal: can add prayers, mark answered, view history
- [ ] Settings: all settings save and persist across sessions
- [ ] WhatsApp report generation still works

**Tasks:**
1. Create a detailed regression test checklist for all 7 feature pages (1 hr)
2. Execute Daily Entry + Daily Log tests (1 hr)
3. Execute Weekly Assignment + Streaks tests (1 hr)
4. Execute Sermon Notes + Prayer Journal tests (1 hr)
5. Execute Settings + WhatsApp report tests (0.5 hr)
6. Log all bugs with severity (0.5 hr)
7. Fix critical and high bugs (3 hrs)

---

### Epic 2: Data Migration

---

#### Story 2.1 -- Migrate Existing SQLite Data to Supabase
**Priority:** P0
**Story Points:** 5

> **As** Bhargavi (the original user),
> **I want** all my existing spiritual data (daily entries, prayer journal entries, sermon notes, streaks, settings) migrated from the old SQLite database to Supabase,
> **So that** I do not lose months of personal spiritual tracking history.

**Acceptance Criteria:**
- [ ] Migration script reads all tables from the SQLite database
- [ ] Data is transformed to match the new Supabase schema (including user_id foreign key)
- [ ] All daily entries are migrated with correct dates and content
- [ ] All prayer journal entries are migrated with status (answered/unanswered)
- [ ] All sermon notes are migrated
- [ ] Streak history is preserved or recalculated accurately
- [ ] Settings are migrated
- [ ] Migration script is idempotent (can be re-run safely)
- [ ] Post-migration verification query confirms row counts match

**Tasks:**
1. Audit SQLite schema vs Supabase schema, document mapping (1 hr)
2. Write migration script (Python) with table-by-table transfer (2.5 hrs)
3. Add idempotency checks (upsert or delete-before-insert) (0.5 hr)
4. Run migration against staging/test Supabase project first (0.5 hr)
5. Run migration against production Supabase (0.5 hr)
6. Verify data in app UI -- spot-check 10 entries per table (1 hr)
7. Archive SQLite file (0.5 hr)

---

#### Story 2.2 -- Verify Import/Export with Supabase
**Priority:** P1
**Story Points:** 2

> **As a** user,
> **I want** the Import/Export feature to work correctly with the Supabase backend,
> **So that** I can back up my data or move it if needed.

**Acceptance Criteria:**
- [ ] Export generates a valid file (CSV or JSON) with all user data
- [ ] Import reads the file and writes data correctly to Supabase
- [ ] Import does not duplicate existing records
- [ ] Export only includes the logged-in user's data (not other users')

**Tasks:**
1. Test export for a user with data; verify file contents (0.5 hr)
2. Test import with exported file into a fresh account (0.5 hr)
3. Test import idempotency (re-import same file) (0.5 hr)
4. Fix any issues (1.5 hrs)

---

### Epic 3: Profile Page

---

#### Story 3.1 -- User Profile View and Edit
**Priority:** P1
**Story Points:** 5

> **As a** user of any role,
> **I want to** view and edit my profile information (name, preferred name, prayer benchmark, membership card ID),
> **So that** my account reflects my identity and personal goals.

**Acceptance Criteria:**
- [ ] New "Profile" page accessible from the sidebar for all roles
- [ ] Displays current values: full name, preferred name, role (read-only), email (read-only), prayer benchmark, membership card ID
- [ ] User can edit: preferred name, prayer benchmark, membership card ID
- [ ] Changes save to Supabase and persist across sessions
- [ ] Validation: prayer benchmark must be a positive integer; membership card ID is optional
- [ ] Success/error toast messages on save

**Tasks:**
1. Create `pages/Profile.py` with form layout (1.5 hrs)
2. Add read query to fetch current profile from Supabase `users` table (0.5 hr)
3. Add update query to save edited fields (0.5 hr)
4. Add form validation (0.5 hr)
5. Add auth guard (role-agnostic, just needs login) (0.25 hr)
6. Test for all 4 roles (0.5 hr)
7. Add sidebar navigation entry (0.25 hr)

---

#### Story 3.2 -- Password Change from Profile
**Priority:** P1
**Story Points:** 3

> **As a** user,
> **I want to** change my password from my Profile page at any time (not just on first login),
> **So that** I can maintain good security practices.

**Acceptance Criteria:**
- [ ] "Change Password" section on the Profile page
- [ ] Requires current password for verification
- [ ] New password must be entered twice (confirmation)
- [ ] Minimum password length: 8 characters
- [ ] Success message on change; error if current password is wrong
- [ ] User remains logged in after password change

**Tasks:**
1. Add password change form to Profile page (1 hr)
2. Implement current password verification against Supabase auth (1 hr)
3. Implement password update via Supabase auth API (0.5 hr)
4. Add validation (min length, match confirmation) (0.5 hr)
5. Test happy path and error paths (0.5 hr)

---

### Epic 4: Security Hardening (Foundational)

---

#### Story 4.1 -- RLS Policy Audit and Hardening
**Priority:** P0
**Story Points:** 3

> **As a** system administrator,
> **I want** all Supabase Row-Level Security policies to be thoroughly tested and verified,
> **So that** user data is protected at the database level regardless of application bugs.

**Acceptance Criteria:**
- [ ] Every table with user data has RLS enabled
- [ ] SELECT policies restrict rows to the owning user (or Pastor for their members, Bishop for their pastors)
- [ ] INSERT policies ensure user_id matches the authenticated user
- [ ] UPDATE policies prevent users from modifying other users' data
- [ ] DELETE policies prevent users from deleting other users' data
- [ ] Verified by running direct Supabase API calls with different user JWT tokens
- [ ] service_role_key is confirmed absent from any client-side code or Streamlit secrets exposed to browser

**Tasks:**
1. Document all tables and their current RLS policies (1 hr)
2. Write test queries for each table using different role JWTs (1 hr)
3. Execute tests and document results (1 hr)
4. Fix any missing or incorrect policies (1 hr)
5. Verify service_role_key is only used server-side (0.5 hr)

---

#### Story 4.2 -- Input Validation and Sanitization
**Priority:** P1
**Story Points:** 2

> **As a** developer,
> **I want** all user inputs to be validated and sanitized before being sent to Supabase,
> **So that** the app is protected against injection attacks and bad data.

**Acceptance Criteria:**
- [ ] All text inputs are stripped of leading/trailing whitespace
- [ ] All text inputs have a reasonable max length enforced
- [ ] Numeric inputs (prayer benchmark, etc.) reject non-numeric values
- [ ] Date inputs are validated for correct format
- [ ] No raw SQL is constructed anywhere (parameterized queries or Supabase client only)
- [ ] HTML/script tags in text inputs are escaped or rejected

**Tasks:**
1. Audit all `st.text_input`, `st.text_area`, `st.number_input` calls across all pages (1 hr)
2. Add validation utility functions in a shared module (1 hr)
3. Apply validation to all input points (1 hr)

---

## Sprint Summary

| # | Story | Points | Priority | Week |
|---|-------|--------|----------|------|
| 1.1 | Admin Account Creation E2E Testing | 3 | P0 | 1 |
| 1.2 | Role-Based Login Flow Verification | 2 | P0 | 1 |
| 1.3 | Data Isolation Verification | 3 | P0 | 1 |
| 1.4 | Original Feature Regression Testing | 5 | P0 | 1 |
| 2.1 | Migrate SQLite Data to Supabase | 5 | P0 | 1-2 |
| 4.1 | RLS Policy Audit and Hardening | 3 | P0 | 1 |
| 3.1 | User Profile View and Edit | 5 | P1 | 2 |
| 3.2 | Password Change from Profile | 3 | P1 | 2 |
| 2.2 | Verify Import/Export with Supabase | 2 | P1 | 2 |
| 4.2 | Input Validation and Sanitization | 2 | P1 | 2 |
| | **Total** | **33** | | |

---

## Week-by-Week Plan

### Week 1 (April 1--7): Stabilize and Validate

**Goal:** Confirm every existing feature works correctly with multi-user auth and Supabase. Fix all critical bugs. Begin data migration.

| Day | Focus | Hours | Stories |
|-----|-------|-------|---------|
| Tue Apr 1 | Admin E2E testing, login flow testing | 6 | 1.1, 1.2 |
| Wed Apr 2 | Data isolation testing, RLS audit | 6 | 1.3, 4.1 |
| Thu Apr 3 | Feature regression testing (Daily Entry, Log, Assignments, Streaks) | 6 | 1.4 |
| Fri Apr 4 | Feature regression testing (Sermon Notes, Prayer Journal, Settings, WhatsApp) | 6 | 1.4 |
| Sat Apr 5 | Bug fixes from all testing + SQLite migration script | 6 | 1.1-1.4, 2.1 |

**Week 1 Deliverables:**
- Complete test results document with pass/fail per feature
- All P0 bugs fixed
- RLS policies documented and verified
- Migration script written and tested against staging

### Week 2 (April 8--14): Migrate, Build Profile, Harden

**Goal:** Complete data migration, deliver the Profile page, and harden security.

| Day | Focus | Hours | Stories |
|-----|-------|-------|---------|
| Mon Apr 7 | Run production migration, verify data, archive SQLite | 6 | 2.1 |
| Tue Apr 8 | Build Profile page (view/edit) | 6 | 3.1 |
| Wed Apr 9 | Build password change, test Profile for all roles | 6 | 3.2 |
| Thu Apr 10 | Import/Export verification, input validation audit | 6 | 2.2, 4.2 |
| Fri Apr 11 | Apply validation fixes, final integration test, deploy | 6 | 4.2, all |

**Week 2 Deliverables:**
- All existing data migrated to Supabase
- Profile page live with edit and password change
- Import/Export verified
- Input validation applied across all pages
- Production deployment updated

---

## Definition of Done (Sprint Level)

- [ ] All P0 stories completed and verified
- [ ] All P1 stories completed or explicitly deferred with justification
- [ ] No open critical or high-severity bugs
- [ ] App deployed to Streamlit Cloud and smoke-tested
- [ ] Existing user data (Bhargavi) fully migrated and verified
- [ ] RLS policies audited and documented

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Regression testing reveals many Supabase bugs | High | High | Budget 3 extra hours for bug fixes; defer P1 stories if needed |
| SQLite schema significantly mismatches Supabase | Medium | High | Audit schemas on Day 1; adjust migration script early |
| RLS policies have gaps allowing data leaks | Medium | Critical | Test with real JWT tokens, not just app UI; fix before any user onboarding |
| Profile page takes longer than estimated | Low | Medium | Defer password change (3.2) to Sprint 2 if needed |

---

## Items Explicitly Deferred to Sprint 2+

These items from the backlog are **not** in Sprint 1:

| Item | Reason for Deferral |
|------|---------------------|
| Group Assignments (Pastor assigns to group) | Needs Profile and role stability first |
| WhatsApp Report Enhancement | Lower priority; current version works |
| Seed Data Management (Admin) | Not blocking 100-user launch |
| UI Polish (login design, badges, empty states) | Functional correctness first |
| Mobile Responsiveness Testing | Defer until UI polish sprint |
| Documentation (user guides) | Write after features stabilize |

---

## Sprint Ceremonies

| Ceremony | When | Duration |
|----------|------|----------|
| Sprint Planning | April 1 (start of day) | 30 min |
| Daily Standup (self) | Every working day, start of day | 10 min |
| Mid-Sprint Check | April 7 | 15 min |
| Sprint Review | April 14 | 30 min |
| Sprint Retrospective | April 14 | 20 min |

---

## Success Metrics for Sprint 1

1. **Zero critical bugs** in production after deployment
2. **100% of P0 stories** completed
3. **Data isolation verified** for all role combinations
4. **Migration complete** with zero data loss
5. **Profile page live** and functional for all roles