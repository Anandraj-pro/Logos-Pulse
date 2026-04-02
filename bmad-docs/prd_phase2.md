# Logos Pulse Phase 2 -- Product Requirements Document

**Author:** Bhargavi Gunnam
**Status:** Draft
**Created:** 2026-03-31
**Last Updated:** 2026-03-31
**Deployment:** https://logos-pulse.streamlit.app/
**Tech Stack:** Streamlit, Supabase (PostgreSQL), Python

---

## 1. Overview / Problem Statement

Logos Pulse is a spiritual growth tracking application used by a church community with a four-tier role hierarchy: Admin, Bishop, Pastor, and Prayer Warrior. Phase 1 delivered core tracking features -- Daily Entry, Bible Reader, Sermon Notes, Prayer Journal, Weekly Assignments, and role-based dashboards.

Phase 2 addresses five areas of friction and capability gaps surfaced by stakeholders:

1. **Admins cannot verify the experience of other roles.** There is no way for an Admin to see the application as a Bishop, Pastor, or Prayer Warrior would. This makes QA, support, and change validation difficult.

2. **Assignments are limited to a single book of the Bible.** Pastors frequently assign cross-book reading plans (e.g., "Hebrews 7-13 and 1 Corinthians 7-11") but the current system only supports one book per assignment.

3. **Sermon note-taking is slow.** Users attending a live sermon cannot quickly type full Bible book names. There is no autocomplete for Bible references, causing friction during time-sensitive note-taking.

4. **Prayer topics lack structure.** There are no standardized templates for common prayer patterns (confession, prayers, declaration). Users must create everything from scratch, and Admins have no way to manage shared templates.

5. **Assignment creation is rigid.** Bishop and Pastor roles cannot create composite assignments that combine prayer templates, sermon series, Bible reading, and prayer time commitments into a single guided assignment.

> **Note:** A sixth item -- "Preferred Name on Dashboard" -- was identified during stakeholder interviews but has already been fixed in Phase 1 via session state. It is excluded from this PRD's scope.

---

## 2. Goals and Non-Goals

### Goals

| ID | Goal |
|----|------|
| G1 | Enable Admins to impersonate any role for testing and support without compromising security or audit integrity |
| G2 | Allow Pastors to create multi-book Bible reading assignments in a single assignment entity |
| G3 | Provide fast Bible reference autocomplete that supports both abbreviated and full book names |
| G4 | Introduce a template system for prayer topics with both standard (Admin-managed) and custom (user-created) templates |
| G5 | Build a wizard-based composite assignment creator for Bishop and Pastor roles |
| G6 | Maintain backward compatibility with all Phase 1 data and features |

### Non-Goals

| ID | Non-Goal |
|----|----------|
| NG1 | Mobile-native app development (Streamlit web remains the target) |
| NG2 | Automated WhatsApp integration (copy-to-clipboard workflow is intentional) |
| NG3 | Real-time collaborative editing of assignments |
| NG4 | Migration away from Supabase or Streamlit |
| NG5 | User self-registration (Admin-managed onboarding is retained) |
| NG6 | Multi-church / multi-tenant architecture |

---

## 3. Detailed Requirements

---

### REQ-1: Admin Impersonation

**Priority:** P0
**Effort Estimate:** 5 story points (~3 days)

#### User Story

> As a **System Admin**, I want to **impersonate up to two test accounts per role** so that I can **see exactly how Bishop, Pastor, and Prayer Warrior users experience the application**, validate UI changes, and troubleshoot issues without needing their credentials.

#### Functional Requirements

| ID | Requirement |
|----|-------------|
| R1.1 | Admin users see an "Impersonate" control in the sidebar when logged in |
| R1.2 | The control presents a dropdown of designated test accounts, organized by role (Bishop, Pastor, Prayer Warrior) |
| R1.3 | Each role has exactly 1-2 pre-designated test accounts eligible for impersonation |
| R1.4 | When impersonation is active, the entire UI renders as it would for the impersonated user's role, including RBAC-gated pages, dashboard data, and navigation |
| R1.5 | A persistent banner at the top of the page reads: "Viewing as [Test Account Name] ([Role]) -- Admin Impersonation Active" with a "Stop Impersonating" button |
| R1.6 | All database writes during impersonation are tagged with `impersonated_by: admin_user_id` in an audit column |
| R1.7 | Impersonation sessions are logged in an `impersonation_log` table with start time, end time, admin ID, and target account ID |
| R1.8 | Non-Admin users cannot access impersonation functionality under any circumstances |
| R1.9 | Impersonation does not affect the actual test account's session if they happen to be logged in simultaneously |

#### Acceptance Criteria

```gherkin
GIVEN I am logged in as Admin
WHEN I select a Bishop test account from the impersonation dropdown
THEN the sidebar, dashboard, and all pages render as they would for a Bishop user
AND a yellow banner shows "Viewing as [name] (Bishop) -- Admin Impersonation Active"
AND I can click "Stop Impersonating" to return to my Admin view

GIVEN I am logged in as a Pastor
WHEN I navigate to any page
THEN no impersonation controls are visible

GIVEN I am impersonating a Prayer Warrior test account
WHEN I submit a Daily Entry
THEN the entry is saved with the test account's user_id
AND the entry row includes impersonated_by = my admin user_id
AND a row is written to impersonation_log
```

#### Technical Approach

1. **Session State Override:** Store `st.session_state.impersonated_user` with the target user's profile. All RBAC checks and data queries reference this object when set, falling back to the real user when `None`.

2. **Test Account Designation:** Add a boolean column `is_test_account` to the `profiles` table. Admin UI allows toggling this flag (max 2 per role enforced in application logic).

3. **Audit Trail:** Add nullable column `impersonated_by UUID REFERENCES profiles(id)` to all write-path tables (`daily_entries`, `sermon_notes`, `prayer_journal`, `assignments`). Create `impersonation_log` table.

4. **Security:** Supabase RLS policies must allow Admin to read data for impersonated users. Impersonation is an application-layer feature; the Supabase JWT still belongs to the Admin. Queries during impersonation filter by impersonated user ID explicitly.

---

### REQ-2: Multi-Book Assignments

**Priority:** P0
**Effort Estimate:** 5 story points (~3 days)

#### User Story

> As a **Pastor**, I want to **create a reading assignment that spans multiple Bible books and chapter ranges** so that I can **assign realistic weekly reading plans** like "Hebrews 7-13 and 1 Corinthians 7-11" instead of being limited to one book.

#### Functional Requirements

| ID | Requirement |
|----|-------------|
| R2.1 | The assignment creation form supports adding multiple book-chapter-range entries |
| R2.2 | Each entry consists of: Book Name (dropdown), Start Chapter (number), End Chapter (number) |
| R2.3 | A "+ Add Another Book" button appends additional book-range rows (no upper limit, but UI should remain usable up to at least 5) |
| R2.4 | Each book-range row has a remove button (except when only one row remains) |
| R2.5 | The assignment displays as a combined string in the assignment list, e.g., "Hebrews 7-13, 1 Corinthians 7-11" |
| R2.6 | Progress tracking shows completion per book-range segment and overall percentage |
| R2.7 | Existing single-book assignments continue to work without migration |
| R2.8 | Assignment title can be auto-generated from the book list or manually overridden |

#### Acceptance Criteria

```gherkin
GIVEN I am a Pastor on the Create Assignment page
WHEN I add "Hebrews 7-13" and click "+ Add Another Book" and add "1 Corinthians 7-11"
AND I click "Create Assignment"
THEN the assignment is saved with both book-range entries
AND Prayer Warriors see the full multi-book assignment on their dashboard

GIVEN a Prayer Warrior has a multi-book assignment
WHEN they complete Hebrews 7-13 but not 1 Corinthians 7-11
THEN the progress shows 50% overall (1 of 2 segments complete)
AND the Pastor dashboard reflects the partial completion

GIVEN an existing single-book assignment from Phase 1
WHEN viewed after Phase 2 deployment
THEN it displays and functions identically to before
```

#### Technical Approach

1. **Schema Change:** Create a new `assignment_books` junction table rather than modifying the existing `assignments` table. This preserves backward compatibility.

   ```
   assignment_books (
     id UUID PRIMARY KEY,
     assignment_id UUID REFERENCES assignments(id) ON DELETE CASCADE,
     book_name TEXT NOT NULL,
     start_chapter INT NOT NULL,
     end_chapter INT NOT NULL,
     sort_order INT DEFAULT 0,
     created_at TIMESTAMPTZ DEFAULT now()
   )
   ```

2. **Migration:** Existing assignments with `book_name`, `start_chapter`, `end_chapter` columns get a corresponding row inserted into `assignment_books` via a one-time migration script.

3. **Progress Tracking:** Create `assignment_book_progress` table or extend existing progress tracking to reference `assignment_books.id`.

4. **UI:** Use `st.session_state` to manage a dynamic list of book-range entries in the form. Render with a `for` loop and unique keys.

---

### REQ-3: Bible Reference Autocomplete

**Priority:** P1
**Effort Estimate:** 3 story points (~2 days)

#### User Story

> As a **user taking sermon notes**, I want the **Bible reference field to autocomplete book names from abbreviations** so that I can **quickly enter references like "Heb 7:14" during a live sermon** without typing "Hebrews" in full.

#### Functional Requirements

| ID | Requirement |
|----|-------------|
| R3.1 | The Bible reference input field provides typeahead suggestions as the user types |
| R3.2 | Suggestions match against both full names and standard abbreviations (e.g., "Heb" matches "Hebrews", "1 Cor" matches "1 Corinthians", "Gen" matches "Genesis") |
| R3.3 | The abbreviation dictionary covers all 66 books of the Bible with at least the most common abbreviated forms |
| R3.4 | Matching is case-insensitive |
| R3.5 | After selecting a book, the cursor advances to a chapter:verse input (or the user can type the full reference inline) |
| R3.6 | The autocomplete works on the Sermon Notes page and anywhere else a Bible reference is entered (Daily Entry, Prayer Journal) |
| R3.7 | Performance: suggestions appear within 100ms of keystroke (client-side filtering, no network round-trip) |

#### Acceptance Criteria

```gherkin
GIVEN I am on the Sermon Notes page
WHEN I type "Heb" in the Bible reference field
THEN I see "Hebrews" as a suggestion
AND I can select it to populate "Hebrews" in the field

GIVEN I type "1 cor" (lowercase) in the reference field
WHEN suggestions appear
THEN "1 Corinthians" is shown as a match

GIVEN I type "Ge" in the reference field
WHEN suggestions appear
THEN "Genesis" is shown (not "Judges" or other non-matching books)

GIVEN I select "Hebrews" from autocomplete
WHEN I continue typing
THEN I can append chapter:verse (e.g., "Hebrews 7:14") as free text
```

#### Technical Approach

1. **Book Dictionary:** A static Python dictionary mapping abbreviations to canonical names:
   ```python
   BIBLE_BOOKS = {
       "gen": "Genesis", "ge": "Genesis", "gn": "Genesis",
       "exo": "Exodus", "ex": "Exodus",
       "heb": "Hebrews", "hebr": "Hebrews",
       "1 cor": "1 Corinthians", "1cor": "1 Corinthians",
       # ... all 66 books with common abbreviations
   }
   ```

2. **Streamlit Component:** Use `st.selectbox` with search enabled, or use `streamlit-searchbox` community component for true typeahead. If neither meets the UX bar, fall back to `st.text_input` with a filtered `st.dataframe`-style suggestion popover via session state.

3. **Reusable Component:** Create a `bible_reference_input(key)` function in a shared `components/` module that can be dropped into any page.

4. **Chapter/Verse Validation:** After book selection, validate that chapter and verse numbers are within the valid range for that book (using a static chapter-count dictionary).

---

### REQ-4: Standard Prayer Topic Templates

**Priority:** P1
**Effort Estimate:** 5 story points (~3 days)

#### User Story

> As a **Prayer Warrior**, I want to **select from pre-built prayer topic templates** (confession, prayers, declaration) so that I can **follow a structured prayer pattern without creating everything from scratch**.

> As an **Admin**, I want to **create and manage standard prayer topic templates** so that I can **provide consistent prayer structures to all users** and allow them to also create their own custom templates.

#### Functional Requirements

| ID | Requirement |
|----|-------------|
| R4.1 | The system ships with default standard templates: Confession, Intercessory Prayer, Declaration, Thanksgiving, Supplication |
| R4.2 | Each template defines a name, description, and an ordered list of prompt sections (e.g., "Confession" template has sections: "What to confess", "Scripture reference", "Declaration of forgiveness") |
| R4.3 | Admin can create, edit, archive (soft-delete), and reorder standard templates via an Admin-only management page |
| R4.4 | Standard templates are visible to all users; archived templates are hidden from users but retained in the database |
| R4.5 | Users can create personal custom templates that are visible only to themselves |
| R4.6 | When starting a new Prayer Journal entry, users see a "Use Template" option that lists standard templates first, then their custom templates |
| R4.7 | Selecting a template pre-fills the journal entry form with the template's section structure |
| R4.8 | Users can modify the pre-filled content freely; the template is a starting point, not a constraint |
| R4.9 | Each prayer journal entry optionally records which template was used (for analytics) |

#### Acceptance Criteria

```gherkin
GIVEN I am an Admin on the Prayer Template Management page
WHEN I create a new template "Morning Confession" with 3 sections
THEN the template appears in the standard templates list
AND all users see it when starting a new prayer journal entry

GIVEN I am a Prayer Warrior starting a new prayer journal entry
WHEN I click "Use Template" and select "Confession"
THEN the entry form is pre-filled with the Confession template's sections
AND I can edit each section freely before saving

GIVEN I am a Prayer Warrior
WHEN I create a custom template "My Evening Prayer"
THEN only I can see and use this template
AND Admins do not see it in the standard template management page

GIVEN an Admin archives the "Supplication" template
WHEN a Prayer Warrior opens the template selector
THEN "Supplication" is no longer listed
AND existing journal entries that used "Supplication" are unchanged
```

#### Technical Approach

1. **Schema:**
   ```
   prayer_templates (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     name TEXT NOT NULL,
     description TEXT,
     template_type TEXT NOT NULL CHECK (template_type IN ('standard', 'custom')),
     created_by UUID REFERENCES profiles(id),
     is_archived BOOLEAN DEFAULT FALSE,
     sort_order INT DEFAULT 0,
     created_at TIMESTAMPTZ DEFAULT now(),
     updated_at TIMESTAMPTZ DEFAULT now()
   )

   prayer_template_sections (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     template_id UUID REFERENCES prayer_templates(id) ON DELETE CASCADE,
     section_name TEXT NOT NULL,
     section_prompt TEXT,
     sort_order INT DEFAULT 0
   )
   ```

2. **RLS Policies:**
   - Standard templates: readable by all authenticated users, writable by Admin only.
   - Custom templates: readable and writable only by the creating user.

3. **Prayer Journal Integration:** Add optional `template_id UUID REFERENCES prayer_templates(id)` to the `prayer_journal` table. Pre-fill logic reads template sections and creates form fields dynamically.

4. **Seed Data:** Ship default templates via a Supabase migration SQL file.

---

### REQ-5: Custom Wizard Assignments (Bishop/Pastor)

**Priority:** P1
**Effort Estimate:** 8 story points (~5 days)

#### User Story

> As a **Bishop or Pastor**, I want to **create a composite assignment using a step-by-step wizard** that combines prayer templates, sermon series, Bible reading plans, and prayer time commitments so that I can **give my congregation a holistic spiritual growth assignment** and **track their progress across all components**.

#### Functional Requirements

| ID | Requirement |
|----|-------------|
| R5.1 | Bishop and Pastor roles see a "Create Custom Assignment" wizard accessible from their dashboard or assignments page |
| R5.2 | The wizard consists of sequential steps: (1) Assignment Basics, (2) Select Components, (3) Configure Components, (4) Review and Publish |
| R5.3 | **Step 1 -- Basics:** Title, description, start date, end date, target audience (specific users, role group, or "all") |
| R5.4 | **Step 2 -- Select Components:** Checkboxes for component types: Prayer Template, Sermon Series, Bible Reading, Prayer Time Commitment |
| R5.5 | **Step 3a -- Prayer Template:** Select one or more prayer templates (from REQ-4) to include |
| R5.6 | **Step 3b -- Sermon Series:** Select from a list of Bishop Samuel Patta sermon series (pre-loaded or Admin-managed). Each series entry has a title, YouTube URL or playlist reference, and episode count |
| R5.7 | **Step 3c -- Bible Reading:** Multi-book reading plan (uses REQ-2's multi-book input component) |
| R5.8 | **Step 3d -- Prayer Time:** Specify minimum prayer duration commitment (e.g., "1 hour daily", "2 hours total this week") with unit selection (daily/weekly/total) |
| R5.9 | **Step 4 -- Review:** Summary of all selected components. Confirm and publish, or go back to edit |
| R5.10 | Published wizard assignments appear on the assigned users' dashboards with a progress tracker showing completion per component |
| R5.11 | The dashboard progress view shows: overall percentage, per-component status (not started / in progress / completed), and days remaining |
| R5.12 | Bishop/Pastor dashboards show an aggregate view of all assignees' progress for each wizard assignment |

#### Acceptance Criteria

```gherkin
GIVEN I am a Bishop on the Create Custom Assignment wizard
WHEN I select Prayer Template ("Morning Confession"), Bible Reading ("Romans 1-8"), and Prayer Time ("1 hour daily")
AND I set the audience to "All Prayer Warriors" for next week
AND I click "Publish"
THEN all Prayer Warriors see the composite assignment on their dashboard
AND the progress tracker shows 3 components with 0% completion each

GIVEN I am a Prayer Warrior with a wizard assignment
WHEN I complete the Bible Reading component (Romans 1-8)
THEN my progress shows Bible Reading as "Completed"
AND overall progress updates to 33% (1 of 3 components)
AND my Pastor's dashboard reflects my updated progress

GIVEN I am a Pastor viewing a wizard assignment's progress
WHEN I see the aggregate view
THEN I see each Prayer Warrior's name, overall %, and per-component status
AND I can sort by completion percentage

GIVEN a wizard assignment has a Sermon Series component
WHEN a Prayer Warrior marks individual sermons as watched
THEN the Sermon Series component progress reflects episodes watched / total episodes
```

#### Technical Approach

1. **Schema:**
   ```
   wizard_assignments (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     title TEXT NOT NULL,
     description TEXT,
     created_by UUID REFERENCES profiles(id),
     target_type TEXT CHECK (target_type IN ('all', 'role', 'specific')),
     target_role TEXT,  -- nullable, used when target_type = 'role'
     start_date DATE NOT NULL,
     end_date DATE NOT NULL,
     is_published BOOLEAN DEFAULT FALSE,
     created_at TIMESTAMPTZ DEFAULT now(),
     updated_at TIMESTAMPTZ DEFAULT now()
   )

   wizard_assignment_targets (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     wizard_assignment_id UUID REFERENCES wizard_assignments(id) ON DELETE CASCADE,
     user_id UUID REFERENCES profiles(id)
   )

   wizard_components (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     wizard_assignment_id UUID REFERENCES wizard_assignments(id) ON DELETE CASCADE,
     component_type TEXT NOT NULL CHECK (component_type IN ('prayer_template', 'sermon_series', 'bible_reading', 'prayer_time')),
     config JSONB NOT NULL,  -- type-specific configuration
     sort_order INT DEFAULT 0
   )

   wizard_component_progress (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     wizard_component_id UUID REFERENCES wizard_components(id) ON DELETE CASCADE,
     user_id UUID REFERENCES profiles(id),
     status TEXT DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
     progress_data JSONB,  -- type-specific progress details
     updated_at TIMESTAMPTZ DEFAULT now(),
     UNIQUE(wizard_component_id, user_id)
   )

   sermon_series (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     title TEXT NOT NULL,
     speaker TEXT DEFAULT 'Bishop Samuel Patta',
     playlist_url TEXT,
     episode_count INT NOT NULL,
     created_by UUID REFERENCES profiles(id),
     created_at TIMESTAMPTZ DEFAULT now()
   )

   sermon_series_episodes (
     id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     series_id UUID REFERENCES sermon_series(id) ON DELETE CASCADE,
     title TEXT NOT NULL,
     video_url TEXT,
     sort_order INT DEFAULT 0
   )
   ```

2. **Component Config JSONB Examples:**
   - Prayer Template: `{"template_ids": ["uuid1", "uuid2"]}`
   - Sermon Series: `{"series_id": "uuid", "episodes": [1,2,3]}`
   - Bible Reading: `{"books": [{"name": "Romans", "start": 1, "end": 8}]}`
   - Prayer Time: `{"duration_minutes": 60, "frequency": "daily"}`

3. **Wizard UI:** Use Streamlit's `st.form` with session state to track wizard step. Each step renders conditionally based on `st.session_state.wizard_step`. Back/Next buttons manage navigation. A progress indicator (step 1 of 4) is shown at the top.

4. **Progress Aggregation:** Pastor/Bishop dashboard queries `wizard_component_progress` with JOINs to compute per-user and per-component completion rates. Use Supabase SQL functions or views for efficient aggregation.

---

## 4. Database Schema Changes -- Summary

### New Tables

| Table | Purpose | Related REQ |
|-------|---------|-------------|
| `impersonation_log` | Audit trail for Admin impersonation sessions | REQ-1 |
| `assignment_books` | Junction table for multi-book assignments | REQ-2 |
| `prayer_templates` | Standard and custom prayer topic templates | REQ-4 |
| `prayer_template_sections` | Ordered sections within a prayer template | REQ-4 |
| `wizard_assignments` | Composite assignment definitions | REQ-5 |
| `wizard_assignment_targets` | User targeting for wizard assignments | REQ-5 |
| `wizard_components` | Individual components within a wizard assignment | REQ-5 |
| `wizard_component_progress` | Per-user, per-component progress tracking | REQ-5 |
| `sermon_series` | Sermon series metadata (Bishop Samuel Patta etc.) | REQ-5 |
| `sermon_series_episodes` | Individual episodes within a sermon series | REQ-5 |

### Modified Tables

| Table | Change | Related REQ |
|-------|--------|-------------|
| `profiles` | Add `is_test_account BOOLEAN DEFAULT FALSE` | REQ-1 |
| `daily_entries` | Add `impersonated_by UUID REFERENCES profiles(id)` (nullable) | REQ-1 |
| `sermon_notes` | Add `impersonated_by UUID REFERENCES profiles(id)` (nullable) | REQ-1 |
| `prayer_journal` | Add `impersonated_by UUID REFERENCES profiles(id)` (nullable), Add `template_id UUID REFERENCES prayer_templates(id)` (nullable) | REQ-1, REQ-4 |
| `assignments` | No structural changes; existing book/chapter fields retained for backward compatibility | REQ-2 |

### Migration Strategy

- All schema changes are additive (new tables, new nullable columns). No destructive changes.
- One-time data migration: existing `assignments` rows with book/chapter data get corresponding `assignment_books` rows.
- Default prayer templates are seeded via migration SQL.
- Migrations are idempotent and can be re-run safely.

### Entity Relationship Diagram (Text)

```
profiles
  |-- 1:N --> impersonation_log (as admin)
  |-- 1:N --> impersonation_log (as target)
  |-- 1:N --> prayer_templates (created_by)
  |-- 1:N --> wizard_assignments (created_by)
  |-- M:N --> wizard_assignments (via wizard_assignment_targets)
  |-- 1:N --> wizard_component_progress (user_id)

assignments
  |-- 1:N --> assignment_books

prayer_templates
  |-- 1:N --> prayer_template_sections
  |-- 1:N --> prayer_journal (template_id)

wizard_assignments
  |-- 1:N --> wizard_components
  |-- 1:N --> wizard_assignment_targets

wizard_components
  |-- 1:N --> wizard_component_progress

sermon_series
  |-- 1:N --> sermon_series_episodes
```

---

## 5. UI/UX Design

### REQ-1: Admin Impersonation

- **Location:** Sidebar, below user profile section, Admin-only.
- **Controls:** `st.selectbox("Impersonate User", options=test_accounts, format_func=lambda u: f"{u.name} ({u.role})")` with a "Start Impersonation" button.
- **Active State:** Yellow `st.warning` banner pinned to the top of every page: "Viewing as [Name] ([Role]) -- Admin Impersonation Active [Stop]".
- **Visual Cue:** Sidebar background tint changes subtly during impersonation (using custom CSS via `st.markdown`).

### REQ-2: Multi-Book Assignments

- **Location:** Assignment creation form (Pastor/Bishop pages).
- **Pattern:** Dynamic form rows. Each row: `[Book Dropdown] [Start Chapter] [End Chapter] [X Remove]`. Below: `[+ Add Another Book]` button.
- **Display:** Assignment cards show combined reference string: "Hebrews 7-13, 1 Corinthians 7-11".
- **Progress:** Segmented progress bar with book labels.

### REQ-3: Bible Reference Autocomplete

- **Component:** Reusable `bible_reference_input()` rendered as `st.selectbox` with search, or a `streamlit-searchbox` widget.
- **Behavior:** User types, suggestions filter in real-time. On selection, book name populates. User then types chapter:verse as free text.
- **Integration Points:** Sermon Notes page, Daily Entry page, Prayer Journal page.

### REQ-4: Prayer Templates

- **Admin Management Page:** New page `pages/8_Prayer_Templates.py` (Admin-only). CRUD table with inline editing. Template preview panel.
- **User Selection:** Prayer Journal page gains a "Start from Template" button at the top. Opens a modal/expander listing templates grouped as "Standard" and "My Templates". Clicking a template pre-fills the form.
- **Custom Template Creation:** Users can save any journal entry's structure as a new custom template via a "Save as Template" button.

### REQ-5: Wizard Assignments

- **Wizard Layout:** Full-page multi-step form. Top: step indicator ("Step 2 of 4: Select Components"). Left: component checklist. Right: component configuration.
- **Step 1 (Basics):** Standard form fields with date pickers and audience selector.
- **Step 2 (Components):** Checkbox grid with icons: Prayer, Sermon, Bible, Clock.
- **Step 3 (Configure):** Tab-like interface, one tab per selected component. Each tab uses the component-specific input (reuses REQ-2's multi-book input, REQ-4's template selector, etc.).
- **Step 4 (Review):** Card-based summary. Each component is a card with its details. "Publish Assignment" button with confirmation dialog.
- **Dashboard Widget:** Assigned users see a card with the assignment title, date range, and a stacked bar chart showing component completion.

---

## 6. Implementation Plan

### Phase 2a -- Foundation (Week 1-2)

| Task | REQ | Est. | Dependencies |
|------|-----|------|--------------|
| Create `impersonation_log` table and RLS policies | REQ-1 | 0.5d | None |
| Add `is_test_account` column to `profiles` | REQ-1 | 0.5d | None |
| Add `impersonated_by` columns to write-path tables | REQ-1 | 0.5d | None |
| Implement impersonation session state logic | REQ-1 | 1d | Schema changes |
| Build impersonation sidebar controls and banner | REQ-1 | 0.5d | Session state logic |
| Build Bible book abbreviation dictionary | REQ-3 | 0.5d | None |
| Create reusable `bible_reference_input()` component | REQ-3 | 1d | Dictionary |
| Integrate autocomplete into Sermon Notes, Daily Entry, Prayer Journal | REQ-3 | 0.5d | Component |

**Phase 2a Deliverable:** Admin impersonation fully functional. Bible reference autocomplete live on all relevant pages.

### Phase 2b -- Assignments and Templates (Week 3-4)

| Task | REQ | Est. | Dependencies |
|------|-----|------|--------------|
| Create `assignment_books` table and migrate existing data | REQ-2 | 1d | None |
| Refactor assignment creation form for multi-book input | REQ-2 | 1d | Schema |
| Update assignment display and progress tracking | REQ-2 | 1d | Schema |
| Create `prayer_templates` and `prayer_template_sections` tables | REQ-4 | 0.5d | None |
| Seed default prayer templates | REQ-4 | 0.5d | Schema |
| Build Admin template management page | REQ-4 | 1d | Schema |
| Integrate template selector into Prayer Journal | REQ-4 | 1d | Schema, Admin page |
| Build custom template creation ("Save as Template") | REQ-4 | 0.5d | Template selector |

**Phase 2b Deliverable:** Multi-book assignments functional. Prayer templates manageable by Admin and usable by all roles.

### Phase 2c -- Wizard Assignments (Week 5-6)

| Task | REQ | Est. | Dependencies |
|------|-----|------|--------------|
| Create wizard-related tables (`wizard_assignments`, `wizard_components`, `wizard_component_progress`, `sermon_series`) | REQ-5 | 1d | None |
| Build wizard Step 1 (Basics) and Step 2 (Component Selection) | REQ-5 | 1d | Schema |
| Build wizard Step 3 (Component Configuration) | REQ-5 | 1.5d | REQ-2 multi-book component, REQ-4 template selector |
| Build wizard Step 4 (Review and Publish) | REQ-5 | 0.5d | Steps 1-3 |
| Build assignee dashboard widget (progress tracker) | REQ-5 | 1d | Publish flow |
| Build Bishop/Pastor aggregate progress view | REQ-5 | 1d | Progress tracker |
| Seed Bishop Samuel Patta sermon series data | REQ-5 | 0.5d | Schema |

**Phase 2c Deliverable:** Wizard assignment creation and progress tracking fully functional.

### Phase 2d -- QA, Polish, Deploy (Week 7)

| Task | REQ | Est. | Dependencies |
|------|-----|------|--------------|
| End-to-end testing across all roles | All | 2d | All features |
| Performance testing (autocomplete, dashboard aggregation) | REQ-3, REQ-5 | 0.5d | All features |
| Edge case handling and error states | All | 1d | All features |
| Deploy to Streamlit Community Cloud | All | 0.5d | QA complete |

**Total Estimated Duration:** 7 weeks
**Total Story Points:** 26

---

## 7. Dependencies and Risks

### Dependencies

| ID | Dependency | Impact | Mitigation |
|----|-----------|--------|------------|
| D1 | `streamlit-searchbox` or equivalent community component for true typeahead | REQ-3 UX quality | Fall back to `st.selectbox` with search if community component is unstable or unsupported |
| D2 | Supabase RLS policy complexity for impersonation | REQ-1 security model | Test RLS policies extensively in staging. Consider using Supabase service role key for impersonation queries if RLS becomes unmanageable (with application-layer RBAC enforcement) |
| D3 | REQ-4 (Prayer Templates) must be completed before REQ-5 wizard can include prayer template components | REQ-5 scheduling | Phased implementation plan already accounts for this. If REQ-4 slips, REQ-5 wizard can ship without prayer template component initially |
| D4 | REQ-2 (Multi-Book) input component is reused in REQ-5 wizard | REQ-5 implementation | Same as D3; phased plan accounts for this |
| D5 | Bishop Samuel Patta sermon series data must be curated and entered | REQ-5 sermon component | Can be entered manually by Admin. Start data collection in parallel with Phase 2a |

### Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| K1 | Streamlit session state limitations with complex wizard forms | Medium | High | Prototype wizard early. If session state is insufficient, consider multi-page wizard with database-backed draft state |
| K2 | Impersonation security vulnerability (privilege escalation) | Low | Critical | Restrict to pre-designated test accounts only. Never allow impersonation of real user accounts. Audit log all impersonation sessions. Code review all RBAC check paths |
| K3 | JSONB config in `wizard_components` becomes hard to maintain | Medium | Medium | Define strict JSON schemas per component type. Validate on write. Consider separate config tables if complexity grows beyond Phase 2 |
| K4 | Performance degradation on dashboard with complex wizard progress aggregation queries | Medium | Medium | Create Supabase database views or materialized views for progress aggregation. Index `wizard_component_progress(wizard_component_id, user_id)` |
| K5 | User confusion with template system (standard vs. custom, template vs. actual entry) | Low | Medium | Clear UI labeling. "Standard Templates (from Admin)" vs "My Templates". Template selection is always optional |

---

## 8. Success Metrics

### Quantitative Metrics

| Metric | Target | Measurement Method | REQ |
|--------|--------|--------------------|-----|
| Admin impersonation sessions per week | >= 3 (indicates active QA usage) | Count rows in `impersonation_log` per week | REQ-1 |
| Multi-book assignments created vs. single-book | >= 40% of new assignments use multi-book | Query `assignment_books` count per assignment | REQ-2 |
| Autocomplete usage rate | >= 80% of new sermon notes use autocomplete-selected books | Track whether book name matches canonical dictionary entry exactly | REQ-3 |
| Prayer template adoption rate | >= 50% of new prayer journal entries use a template within 30 days of launch | Count `prayer_journal` rows where `template_id IS NOT NULL` | REQ-4 |
| Custom templates created per user per month | >= 0.5 (users finding value in customization) | Count `prayer_templates` where `template_type = 'custom'` | REQ-4 |
| Wizard assignments created per month | >= 2 per Bishop/Pastor | Count `wizard_assignments` per creator | REQ-5 |
| Wizard assignment completion rate | >= 60% of assigned users complete all components | `wizard_component_progress` where all components `status = 'completed'` / total assigned users | REQ-5 |

### Qualitative Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Admin satisfaction with impersonation flow | "Saves significant time vs. asking users for screenshots" | Direct feedback from Admin (Bhargavi) |
| Pastor satisfaction with multi-book assignments | "Finally matches how we actually assign reading" | Feedback from Ps. Deepak |
| Sermon note-taking speed improvement | "Noticeably faster to enter references during live sermons" | User interviews after 2 weeks |
| Prayer structure satisfaction | "Templates help me pray more thoroughly" | User survey after 30 days |
| Assignment creation satisfaction | "Wizard makes it easy to create holistic assignments" | Bishop/Pastor feedback |

### Monitoring and Alerting

- Track Supabase database row counts weekly for all new tables to identify adoption trends.
- Monitor Streamlit app error logs for any new exceptions in Phase 2 code paths.
- Set up a simple analytics dashboard (within the Admin view) showing the quantitative metrics above.

---

## Appendix A: Bible Book Abbreviation Reference (Partial)

| Abbreviation(s) | Full Name |
|-----------------|-----------|
| Gen, Ge, Gn | Genesis |
| Exo, Ex | Exodus |
| Lev, Le, Lv | Leviticus |
| Num, Nu, Nm | Numbers |
| Deut, Dt | Deuteronomy |
| ... | ... |
| Matt, Mt | Matthew |
| Mk | Mark |
| Lk | Luke |
| Jn, Jhn | John |
| ... | ... |
| Heb, Hebr | Hebrews |
| Jas | James |
| 1 Pet, 1Pe | 1 Peter |
| 2 Pet, 2Pe | 2 Peter |
| Rev, Re | Revelation |

*Full dictionary to be defined in implementation.*

---

## Appendix B: Default Prayer Templates (Seed Data)

### Template 1: Confession

| Section | Prompt |
|---------|--------|
| Examine | "Reflect on areas where you have fallen short. What is the Holy Spirit revealing?" |
| Confess | "Write your confession openly before God." |
| Scripture | "Find a scripture that speaks to God's forgiveness (e.g., 1 John 1:9)." |
| Declaration | "Declare God's forgiveness and your freedom in Christ." |

### Template 2: Intercessory Prayer

| Section | Prompt |
|---------|--------|
| Person/Situation | "Who or what are you interceding for today?" |
| Scripture Foundation | "What scripture guides this prayer?" |
| Prayer | "Write your intercessory prayer." |
| Declaration | "Declare God's will over this situation." |

### Template 3: Thanksgiving

| Section | Prompt |
|---------|--------|
| Gratitude | "List what you are thankful for today." |
| Testimony | "Recall a recent answer to prayer or blessing." |
| Scripture | "A verse of praise or thanksgiving." |
| Declaration | "Declare God's goodness and faithfulness." |

### Template 4: Supplication

| Section | Prompt |
|---------|--------|
| Need | "What are you asking God for?" |
| Scripture Promise | "What promise of God applies to this need?" |
| Prayer | "Write your prayer of supplication." |
| Trust Declaration | "Declare your trust in God's timing and provision." |

### Template 5: Declaration

| Section | Prompt |
|---------|--------|
| Identity | "Declare who you are in Christ." |
| Authority | "Declare the authority you have in Jesus' name." |
| Victory | "Declare victory over specific areas of struggle." |
| Blessing | "Declare blessings over your family, church, and community." |

---

*End of PRD*
