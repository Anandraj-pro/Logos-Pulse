# PRD: Prayer Engine — Logos Pulse Phase 3

**Document Version:** 1.0
**Date:** 2026-04-03
**Author:** Bhargavi Gunnam
**Status:** Draft (Pre-Brainstorm)
**Stakeholder:** Bishop & Pastor Leadership Team

---

## Table of Contents

1. [Overview & Objectives](#1-overview--objectives)
2. [Content Architecture](#2-content-architecture)
3. [Functional Requirements](#3-functional-requirements)
4. [User Flows](#4-user-flows)
5. [Database Schema](#5-database-schema)
6. [UI/UX Considerations](#6-uiux-considerations)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Integration Points](#8-integration-points)
9. [Implementation Phases](#9-implementation-phases)
10. [Success Metrics](#10-success-metrics)
11. [Out of Scope](#11-out-of-scope)
12. [Open Questions (For Brainstorm)](#12-open-questions)

---

## 1. Overview & Objectives

### 1.1 Background

Logos Pulse currently supports prayer journaling with 5 standard templates (Morning Confession, Evening Gratitude, Spiritual Warfare, Financial Breakthrough, Healing & Health). The church has accumulated **86 confession and prayer documents** across 14 life categories — rich, pastor-curated content built over years of ministry. This content is currently stored as offline files (DOC, PDF, JPG) and is inaccessible to members digitally.

### 1.2 Problem Statement

1. **Content is locked in files** — Members cannot access the church's confession library from their phones or daily spiritual routine.
2. **Templates are too generic** — 5 templates cannot address the breadth of life situations (marriage crisis, court cases, children's health, infidelity, etc.).
3. **No guided confession practice** — Members log prayers but have no structured daily confession/declaration routine.
4. **Pastoral prescription gap** — Pastors counsel members and recommend specific confessions verbally, but there's no way to digitally assign and track confession engagement.
5. **Content discovery** — New believers don't know which confessions are relevant to their situation.

### 1.3 Objectives

| ID | Objective | Measurable Outcome |
|----|-----------|-------------------|
| OBJ-1 | Digitize and organize the church's confession library | 86 documents categorized, Tier 1 content live in-app |
| OBJ-2 | Enable members to discover and adopt confessions by life situation | 70%+ of active members engage with at least one confession template |
| OBJ-3 | Support structured daily confession routines | Members can follow AM/PM and multi-day confession plans |
| OBJ-4 | Enable pastors to prescribe confessions to members | Pastors can assign confession plans; members see them in their dashboard |
| OBJ-5 | Track confession engagement alongside existing spiritual disciplines | Confession streaks visible in stats; engagement visible to pastors |

### 1.4 Relationship to Existing Features

| Existing Feature | Prayer Engine Extension |
|-----------------|----------------------|
| Prayer Templates (`prayer_templates` table) | Expand from 5 to 50+ templates with richer metadata |
| Prayer Journal wizard | Add "From Library" step to pull confessions from the engine |
| Wizard Assignments (REQ-5) | Confession plans become a first-class assignment type |
| Daily Entry & WhatsApp Report | Include today's confession in daily log and report |
| Streaks & Stats | Track confession engagement as a new discipline |
| Pastor Dashboard | Show member confession engagement metrics |

---

## 2. Content Architecture

### 2.1 Category Taxonomy (Draft — Pending Brainstorm)

| ID | Category | Sub-Categories | Source Docs | Priority |
|----|----------|---------------|-------------|----------|
| CAT-01 | Health & Healing | Physical Healing, Emotional Healing, Anointing | 7 | Tier 1 |
| CAT-02 | Marriage & Family | Harmonious Marriage, Husbands, Wives, Infidelity, Household Blessings | 11 | Tier 1 |
| CAT-03 | Financial & Business | Prosperity, Business, Employment, Deuteronomy 28 | 7 | Tier 1 |
| CAT-04 | Protection & Spiritual Warfare | Breaking Curses, Cleansing, Defeating Worry, Protection | 8 | Tier 1 |
| CAT-05 | Faith & Favor | Faith Confessions, Favor, Righteousness, Words of My Mouth | 8 | Tier 1 |
| CAT-06 | Children & Family Desires | Conception, Children, Teenagers, Purity | 6 | Tier 1 |
| CAT-07 | Salvation & Evangelism | Unsaved Loved Ones, Unsaved Parents, New Converts | 5 | Tier 2 |
| CAT-08 | Church Growth & Ministry | Pastors, Church Establishment, Revival, Intercession | 8 | Tier 2 |
| CAT-09 | Intercession & Outreach | Prayer Guidelines, Commission, Dedication, Consecration | 4 | Tier 2 |
| CAT-10 | Personal Growth | Breakthrough, Letting Go, Consecration, Daily Warfare | 5 | Tier 1 |
| CAT-11 | Daily Confessions | AM Confessions, PM Confessions, Daily Prayer | 7 | Tier 1 |
| CAT-12 | Legal & Justice | Court Cases | 1 | Tier 3 |
| CAT-13 | Pastoral Care | Comfort, Grief, Commonly Asked Questions | 4 | Tier 2 |
| CAT-14 | Compiled References | Rev. Godwin Abba Collection, BW Confessions List | 4 | Tier 3 |

### 2.2 Content Structure Per Template

Each confession/prayer template in the engine will have:

```
Template
├── name              — Display title (e.g., "Financial Breakthrough Confession")
├── description       — 1-2 sentence summary of when to use this
├── category_id       — FK to confession_categories
├── confessions[]     — Array of confession statements
│   ├── text          — "I confess that God is my provider..."
│   └── scripture_ref — "Philippians 4:19"
├── declarations[]    — Array of declaration statements
│   ├── text          — "I declare that debt has no hold on my life..."
│   └── scripture_ref — "Romans 13:8"
├── prayers[]         — Array of prayer paragraphs
│   └── text          — "Dear Lord, I bring my finances before you..."
├── scriptures[]      — Supporting scripture references
├── tier              — 1 (core), 2 (important), 3 (archive)
├── difficulty_level  — beginner, intermediate, advanced
├── recommended_duration — "7 days", "21 days", "ongoing"
├── time_of_day       — morning, evening, anytime
├── created_by        — admin/bishop/pastor who curated
└── is_published      — boolean (draft vs. live)
```

### 2.3 Content Digitization Pipeline

```
Raw Files (86)
  → OCR (22 JPGs) + Text Extraction (44 DOCs, 6 DOCX, 5 PDFs)
  → De-duplication (~12 duplicates removed)
  → Standardize format (structured JSON/text)
  → Theological review (Bishop/Pastor approval)
  → Category assignment
  → Scripture reference validation
  → Publish to prayer_engine_templates table
```

---

## 3. Functional Requirements

### REQ-PE-1: Confession Library Browser

**Description:** Members can browse the full confession library organized by category.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-1.1 | Display all published categories with icons, descriptions, and template counts | Must |
| PE-1.2 | Within a category, list all templates with title, description, and difficulty | Must |
| PE-1.3 | Template detail view shows confessions, declarations, prayers, and scriptures | Must |
| PE-1.4 | Search across all templates by keyword | Should |
| PE-1.5 | Filter templates by difficulty level, time of day, duration | Should |
| PE-1.6 | "Recommended for You" section based on active prayer journal categories | Could |

**Acceptance Criteria:**
```
GIVEN a logged-in member
WHEN they navigate to the Prayer Engine page
THEN they see all published categories with template counts
AND can expand any category to browse its templates
AND can open a template to see full confessions, declarations, and scriptures
```

### REQ-PE-2: Personal Confession Plan

**Description:** Members can add templates to their personal daily confession plan.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-2.1 | "Add to My Plan" button on any template | Must |
| PE-2.2 | Personal plan view shows all active confessions in order | Must |
| PE-2.3 | Mark confessions as completed each day | Must |
| PE-2.4 | Support AM/PM assignment (morning confessions vs. evening declarations) | Should |
| PE-2.5 | Support multi-day plans (7-day, 21-day, custom) | Should |
| PE-2.6 | Remove templates from plan | Must |
| PE-2.7 | Plan history — see past completed plans | Could |

**Acceptance Criteria:**
```
GIVEN a member viewing a confession template
WHEN they click "Add to My Plan"
THEN the template appears in their personal confession plan
AND they can mark it as completed daily
AND completion is tracked in their spiritual disciplines
```

### REQ-PE-3: Daily Confession View

**Description:** A focused, distraction-free view for members to read through their daily confessions.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-3.1 | "Today's Confessions" card on Dashboard (page 0) | Must |
| PE-3.2 | Full-screen confession reading mode with large text | Must |
| PE-3.3 | Swipe/navigate between confession statements | Should |
| PE-3.4 | Option to display scripture reference alongside each confession | Must |
| PE-3.5 | "Mark as Confessed Today" button | Must |
| PE-3.6 | Include in Daily Entry log and WhatsApp report | Should |

### REQ-PE-4: Pastor Confession Assignment

**Description:** Pastors can assign specific confessions to individual members or groups.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-4.1 | Pastor can assign a confession template to a member | Must |
| PE-4.2 | Pastor can assign a multi-day confession plan to a member | Should |
| PE-4.3 | Assigned confessions appear in member's plan with "Pastor Assigned" badge | Must |
| PE-4.4 | Pastor can see which members have active assignments | Must |
| PE-4.5 | Pastor can see engagement metrics (days completed, streak) | Should |
| PE-4.6 | Integration with existing Wizard Assignments (REQ-5) | Should |
| PE-4.7 | Bishop can assign confessions across all pastors' members | Could |

**Acceptance Criteria:**
```
GIVEN a pastor viewing a member's profile
WHEN they assign a confession template with a 21-day duration
THEN the member sees it in their plan labeled "Assigned by Pastor [Name]"
AND the pastor can track the member's daily completion progress
```

### REQ-PE-5: Confession Engagement Tracking

**Description:** Track confession practice as a spiritual discipline alongside prayer, reading, and sermons.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-5.1 | Daily confession completion recorded in daily_entries | Must |
| PE-5.2 | Confession streak tracked alongside prayer/reading streaks | Should |
| PE-5.3 | Monthly confession stats in Streaks & Stats page | Should |
| PE-5.4 | Confession heatmap (similar to existing prayer heatmap) | Could |
| PE-5.5 | Pastor dashboard shows member confession engagement | Must |
| PE-5.6 | Bishop dashboard shows aggregate confession metrics | Could |

### REQ-PE-6: Content Management (Admin/Bishop)

**Description:** Admins and Bishops can manage the confession library content.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-6.1 | Admin can create/edit/archive confession templates | Must |
| PE-6.2 | Admin can create/edit confession categories | Must |
| PE-6.3 | Bishop can submit new confession templates for admin approval | Should |
| PE-6.4 | Pastor can submit new confessions for review | Could |
| PE-6.5 | Template versioning — update without breaking active plans | Should |
| PE-6.6 | Bulk import from structured format (CSV/JSON) | Should |
| PE-6.7 | "Confession of the Week" — Bishop-selected, pushed to all members | Could |

---

## 4. User Flows

### 4.1 Member: Discover & Adopt Confessions

```
Dashboard
  → "Explore Confessions" button
  → Prayer Engine Library (category grid)
  → Select category (e.g., "Health & Healing")
  → Browse templates in category
  → Open "Healing Confession" template
  → Read confessions, declarations, scriptures
  → Click "Add to My Plan" (choose: ongoing / 7-day / 21-day)
  → Redirected to personal plan view
  → Next morning: Dashboard shows "Today's Confessions" card
  → Open focused confession reading view
  → Read through confessions → "Mark as Confessed Today"
  → Completion logged in daily entry
```

### 4.2 Pastor: Assign Confessions to Member

```
Pastor Dashboard
  → View member list
  → Select member (e.g., "Grace")
  → "Assign Confession" button
  → Browse/search confession library
  → Select "Financial Breakthrough Confession"
  → Set duration: 21 days, starting today
  → Add optional note: "Stay strong in faith, Grace"
  → Submit assignment
  → Grace sees assignment in her plan next login
  → Pastor tracks Grace's progress in dashboard
```

### 4.3 Admin: Add New Confession Template

```
Admin Panel
  → "Prayer Engine" tab
  → "New Template" button
  → Fill form:
    - Category: Health & Healing
    - Title: Emotional Healing Confession
    - Description: For those dealing with past trauma and emotional wounds
    - Confessions: [line-by-line entry with optional scripture refs]
    - Declarations: [line-by-line entry with optional scripture refs]
    - Prayers: [paragraph entry]
    - Scriptures: [reference list]
    - Difficulty: Beginner
    - Recommended Duration: 21 days
    - Time of Day: Morning
  → Save as Draft → Preview → Publish
```

---

## 5. Database Schema

### 5.1 New Tables

```sql
-- Confession categories (separate from prayer_categories for library organization)
CREATE TABLE confession_categories (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT DEFAULT '📖',
    color TEXT DEFAULT '#5B4FC4',
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Confession templates (extends existing prayer_templates concept)
CREATE TABLE confession_templates (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    category_id BIGINT REFERENCES confession_categories(id),
    name TEXT NOT NULL,
    description TEXT,
    confessions JSONB DEFAULT '[]',       -- [{text, scripture_ref}]
    declarations JSONB DEFAULT '[]',      -- [{text, scripture_ref}]
    prayers JSONB DEFAULT '[]',           -- [{text}]
    scriptures JSONB DEFAULT '[]',        -- ["Philippians 4:19", ...]
    tier INTEGER DEFAULT 2,               -- 1=core, 2=important, 3=archive
    difficulty_level TEXT DEFAULT 'beginner',  -- beginner, intermediate, advanced
    recommended_duration TEXT DEFAULT 'ongoing', -- ongoing, 7_days, 21_days, custom
    time_of_day TEXT DEFAULT 'anytime',   -- morning, evening, anytime
    is_published BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES auth.users(id),
    source_document TEXT,                 -- original filename for traceability
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Member's personal confession plan
CREATE TABLE member_confession_plans (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    template_id BIGINT REFERENCES confession_templates(id) NOT NULL,
    assigned_by UUID REFERENCES auth.users(id),  -- NULL = self-selected, UUID = pastor-assigned
    assignment_note TEXT,                          -- optional pastor note
    plan_type TEXT DEFAULT 'ongoing',             -- ongoing, 7_days, 21_days
    time_slot TEXT DEFAULT 'anytime',             -- morning, evening, anytime
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE,                                -- NULL for ongoing
    status TEXT DEFAULT 'active',                 -- active, completed, paused, removed
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Daily confession completion log
CREATE TABLE confession_completions (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    plan_id BIGINT REFERENCES member_confession_plans(id) NOT NULL,
    completed_date DATE NOT NULL DEFAULT CURRENT_DATE,
    time_slot TEXT,                                -- morning, evening
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, plan_id, completed_date, time_slot)
);
```

### 5.2 Indexes

```sql
CREATE INDEX idx_confession_templates_category ON confession_templates(category_id);
CREATE INDEX idx_confession_templates_published ON confession_templates(is_published);
CREATE INDEX idx_member_plans_user ON member_confession_plans(user_id);
CREATE INDEX idx_member_plans_assigned_by ON member_confession_plans(assigned_by);
CREATE INDEX idx_completions_user_date ON confession_completions(user_id, completed_date);
```

### 5.3 RLS Policies

```sql
-- confession_categories: everyone can read
ALTER TABLE confession_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read categories" ON confession_categories FOR SELECT USING (true);
CREATE POLICY "Admin can manage categories" ON confession_categories FOR ALL
    USING (is_admin(auth.uid()));

-- confession_templates: published templates readable by all, admin manages
ALTER TABLE confession_templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read published templates" ON confession_templates FOR SELECT
    USING (is_published = true);
CREATE POLICY "Admin can manage templates" ON confession_templates FOR ALL
    USING (is_admin(auth.uid()));

-- member_confession_plans: user sees own, pastor sees assigned
ALTER TABLE member_confession_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "User sees own plans" ON member_confession_plans FOR SELECT
    USING (user_id = auth.uid());
CREATE POLICY "Pastor sees assigned plans" ON member_confession_plans FOR SELECT
    USING (assigned_by = auth.uid());
CREATE POLICY "User manages own plans" ON member_confession_plans FOR ALL
    USING (user_id = auth.uid());
CREATE POLICY "Pastor can assign" ON member_confession_plans FOR INSERT
    USING (can_view_user(auth.uid(), user_id));

-- confession_completions: user's own only
ALTER TABLE confession_completions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "User manages own completions" ON confession_completions FOR ALL
    USING (user_id = auth.uid());
CREATE POLICY "Pastor can view member completions" ON confession_completions FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM member_confession_plans mcp
        WHERE mcp.id = confession_completions.plan_id
        AND mcp.assigned_by = auth.uid()
    ));
```

---

## 6. UI/UX Considerations

### 6.1 New Page: Prayer Engine (`pages/8_Prayer_Engine.py`)

**Tabs:**
1. **Library** — Browse categories and templates (grid layout)
2. **My Plan** — Personal active confessions with daily checklist
3. **Today** — Focused reading view for today's confessions

### 6.2 Design Principles

- Use existing `modules/styles.py` design system (DM Serif Display + DM Sans)
- Category cards with icons and colors (same pattern as Prayer Journal categories)
- Confession reading view: large font, clean background, minimal UI
- Progress indicators for multi-day plans (e.g., "Day 7 of 21")
- Consistent status badges (active=green, completed=purple, paused=gray)

### 6.3 Dashboard Integration

Add "Today's Confessions" card to Dashboard (page 0):
- Shows count of active confessions for today
- Quick "Start Confessing" button
- Small streak indicator

### 6.4 Mobile-First

- Confession reading optimized for phone screens
- Swipeable confession cards (one statement per screen in focused mode)
- Large tap targets for "Mark Complete"

---

## 7. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-1 | Page load for library browse | < 2 seconds |
| NFR-2 | Template content cached per session | Reduce DB queries |
| NFR-3 | Support 100+ templates without UI degradation | Pagination/lazy load |
| NFR-4 | Confession text renders correctly with special characters | Unicode support |
| NFR-5 | All pages follow existing auth guard pattern | require_login + require_password_changed |

---

## 8. Integration Points

### 8.1 Daily Entry (page 1)

- Add "Confessions completed today" indicator to daily entry form
- Include confession summary in WhatsApp report generation

### 8.2 Prayer Journal (page 7)

- "Import from Library" button in confession/declaration steps of prayer wizard
- Link between prayer entries and confession templates

### 8.3 Wizard Assignments (REQ-5)

- Confession plans as a component type in wizard assignments
- Pastor can include confession templates alongside Bible reading and prayer templates

### 8.4 Streaks & Stats (page 4)

- Confession streak alongside prayer/reading streaks
- Monthly confession completion rate
- Heatmap for confession engagement

### 8.5 Pastor Dashboard

- "Confession Assignments" tab showing all active assignments
- Per-member engagement metrics (days completed / total days)
- Alert for members who haven't confessed in 3+ days

---

## 9. Implementation Phases

### Phase 3A: Foundation (MVP)

**Goal:** Confession library live and browsable with personal plans.

| Task | Description | Effort |
|------|-------------|--------|
| DB migration | Create 4 new tables + RLS + indexes | 3 SP |
| Content digitization | Extract & structure Tier 1 documents (~30 templates) | 5 SP |
| Confession categories seed | Populate confession_categories from taxonomy | 1 SP |
| Library browser page | Category grid + template list + detail view | 5 SP |
| Personal plan | Add to plan, view plan, mark complete | 5 SP |
| Dashboard card | "Today's Confessions" on dashboard | 2 SP |
| db.py functions | CRUD for all new tables | 3 SP |
| **Total** | | **24 SP** |

### Phase 3B: Pastoral & Tracking

**Goal:** Pastors can assign confessions; engagement tracked.

| Task | Description | Effort |
|------|-------------|--------|
| Pastor assignment flow | Assign template to member with duration | 5 SP |
| Pastor dashboard tab | Confession assignments + engagement metrics | 5 SP |
| Daily Entry integration | Log confession completion in daily entry | 3 SP |
| Streaks integration | Confession streaks in stats page | 3 SP |
| WhatsApp report | Include confession summary | 2 SP |
| **Total** | | **18 SP** |

### Phase 3C: Advanced Features

**Goal:** Structured plans, content management, bishop features.

| Task | Description | Effort |
|------|-------------|--------|
| Multi-day plans | 7-day, 21-day structured plans with progression | 5 SP |
| AM/PM scheduling | Morning vs. evening confession assignments | 3 SP |
| Content management UI | Admin CRUD for templates + categories | 5 SP |
| Bulk import | CSV/JSON import for batch template creation | 3 SP |
| Confession of the Week | Bishop-pushed weekly confession to all members | 3 SP |
| Wizard Assignment integration | Confession plans as wizard component | 3 SP |
| **Total** | | **22 SP** |

---

## 10. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Template library size | 50+ published templates | Count of published confession_templates |
| Member adoption | 70% of active members add at least 1 template to plan | member_confession_plans / active users |
| Daily engagement | 40% of plan holders complete daily confession | confession_completions / active plans |
| Pastoral assignments | Each pastor assigns at least 5 confessions/month | member_confession_plans WHERE assigned_by IS NOT NULL |
| Confession streaks | Average streak > 7 days | Calculated from confession_completions |
| Content coverage | All 14 categories have at least 2 templates | Count by category |

---

## 11. Out of Scope

- Audio recordings of confessions (future consideration)
- Multi-language support (English only for MVP)
- AI-generated confessions or personalization
- Community/social features (sharing confessions between members)
- Offline mode / PWA support
- Push notifications for confession reminders
- Integration with external prayer apps

---

## 12. Open Questions (For Brainstorm)

These questions will be resolved during the Bishop/Pastor brainstorm session:

1. **Category taxonomy** — Are the 14 categories correct? Merge/split/add?
2. **Access control** — Should any confessions be restricted by spiritual maturity level?
3. **Content authority** — Can pastors create new confessions, or admin-only?
4. **Customization** — Can members edit confession text, or keep it as curated?
5. **Engagement visibility** — How much should pastors see? Just completion counts, or which specific confessions?
6. **Confession of the Week** — Is this a priority for the Bishop team?
7. **Language** — Any demand for non-English confessions?
8. **Source attribution** — Should templates credit original authors (e.g., Rev. Godwin Abba)?
9. **Theological review process** — Who has final approval authority on confession content?
10. **Digitization ownership** — Who will handle OCR and text extraction for the 22 JPG files?