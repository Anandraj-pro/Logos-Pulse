# PRD: Prayer Engine — Logos Pulse Phase 3

**Document Version:** 2.0
**Date:** 2026-04-03
**Author:** Bhargavi Gunnam
**Status:** Approved (Post-Brainstorm)
**Stakeholder:** Bishop Samuel Patta & Pastor Leadership Team
**Brainstorm Session:** 2026-04-03 — Bishop Samuel, Pastor Grace, Pastor David, Pastor Emmanuel

---

## Table of Contents

1. [Overview & Objectives](#1-overview--objectives)
2. [Design Principles](#2-design-principles)
3. [Content Architecture](#3-content-architecture)
4. [Functional Requirements](#4-functional-requirements)
5. [User Flows](#5-user-flows)
6. [Database Schema](#6-database-schema)
7. [UI/UX Considerations](#7-uiux-considerations)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Integration Points](#9-integration-points)
10. [Implementation Phases](#10-implementation-phases)
11. [Success Metrics](#11-success-metrics)
12. [Content Standards & Review Process](#12-content-standards--review-process)
13. [Privacy & Visibility Model](#13-privacy--visibility-model)
14. [Out of Scope](#14-out-of-scope)
15. [Brainstorm Decisions Log](#15-brainstorm-decisions-log)

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
6. **No onboarding path** — New converts face a blank canvas with no spiritual formation guidance.

### 1.3 Objectives

| ID | Objective | Measurable Outcome |
|----|-----------|-------------------|
| OBJ-1 | Digitize and organize the church's confession library | 86 documents categorized into 16 categories, Tier 1 content (15-20 templates) live in-app within 3 weeks |
| OBJ-2 | Enable need-based confession discovery | 70%+ of active members engage with at least one confession template via "What are you believing for?" entry point |
| OBJ-3 | Support structured 21-day confession plans with AM/PM rhythm | Members can follow multi-day plans with morning confessions and evening declarations |
| OBJ-4 | Enable pastors to prescribe confessions with trackable engagement | Pastors can assign confession plans; individual completion metrics visible for prescribed confessions |
| OBJ-5 | Auto-onboard new believers with foundational confessions | Every new member receives a 7-day starter track on registration |
| OBJ-6 | Bridge digital and physical church through Confession of the Week | Bishop-selected weekly confession tied to Sunday sermon theme |

### 1.4 Relationship to Existing Features

| Existing Feature | Prayer Engine Extension |
|-----------------|----------------------|
| Prayer Templates (`prayer_templates` table) | Expand from 5 to 50+ templates with richer metadata, short-form + full text |
| Prayer Journal wizard | "Import from Library" in confession/declaration steps (Phase 2) |
| Wizard Assignments (REQ-5) | Confession plans become a first-class assignment component (Phase 2) |
| Daily Entry & WhatsApp Report | Include today's confession + single declaration line in report (MVP) |
| Streaks & Stats | Track confession engagement as a new discipline (Phase 3) |
| Pastor Dashboard | Show prescribed confession engagement metrics (MVP) |

---

## 2. Design Principles

These principles were established during the brainstorm session and guide all design decisions:

### P1: Meet Members at Their Need, Not a Catalog
> The entry point is "What are you believing God for?" — not a category grid. Taxonomy is for organizers; the member experience should feel like a conversation. — *Bishop Samuel*

### P2: Confession is Spoken, Not Just Read
> Romans 10:10 — "with the mouth confession is made unto salvation." The app must encourage vocal confession through the "Confess Aloud" mode. — *Bishop Samuel*

### P3: Invitational, Not Institutional
> Celebrate ANY engagement. Never penalize inconsistency. If someone confesses twice this week after doing zero last week, that is a win. — *Pastor Grace, Pastor Emmanuel*

### P4: Progressive Disclosure
> New users see 6 Tier 1 categories. "Explore More" reveals the full library. Don't overwhelm new believers with 16 doors on day one. — *Consensus*

### P5: Privacy by Design
> Pastors see engagement metrics for prescribed confessions. Self-selected browsing remains private between the member and God. — *Bishop Samuel*

### P6: Short-Form First, Full Text Available
> Default display is short-form confession cards optimized for mobile. "Read Full Confession" expands to the complete text. — *Pastor Grace + David compromise*

---

## 3. Content Architecture

### 3.1 Category Taxonomy (Approved)

#### Tier 1 — Core (Digitize Immediately, MVP Launch)

| ID | Category | Icon | Source Docs | Notes |
|----|----------|------|-------------|-------|
| CAT-01 | Health & Healing | 🏥 | 7 | Physical + emotional healing, anointing |
| CAT-02 | Finances, Business & Provision | 💰 | 7 | Prosperity, business, employment, Deuteronomy 28 |
| CAT-03 | Faith, Favor & Declarations | ✨ | 8 | Corporate Sunday confessions, favor, righteousness |
| CAT-04 | Identity in Christ & Personal Transformation | 🦋 | 5 | Who I am in Christ, breakthrough, letting go |
| CAT-05 | Salvation & Evangelism | 🌍 | 5 | Unsaved loved ones, new converts, Great Commission |
| CAT-06 | Daily Confessions & Morning/Evening Prayers | 🌅 | 7 | AM/PM daily rhythm, general daily prayers |

#### Tier 2 — Important (Digitize in 30 Days)

| ID | Category | Icon | Source Docs | Notes |
|----|----------|------|-------------|-------|
| CAT-07 | Marriage & Spouse | 💍 | 6 | Harmonious marriage, husbands, wives, infidelity |
| CAT-08 | Family & Parenting | 👨‍👩‍👧‍👦 | 5 | Teenagers, children's confessions, household blessings |
| CAT-09 | Daily Protection & Safety | 🛡️ | 4 | Traveling mercies, safety, protection from harm |
| CAT-10 | Church, Ministry & Kingdom Advancement | ⛪ | 8 | Pastors, church growth, revival, intercession |
| CAT-11 | Believing for Children & Family Expansion | 👶 | 4 | Conception, fertility, adoption, waiting on God |
| CAT-12 | Thanksgiving & Praise Confessions | 🙌 | NEW | Gratitude, declaring God's goodness, confessing FROM victory |

#### Tier 3 — Specialized (Digitize in 60 Days)

| ID | Category | Icon | Source Docs | Notes |
|----|----------|------|-------------|-------|
| CAT-13 | Spiritual Warfare & Deliverance | ⚔️ | 4 | Breaking curses, cleansing, territorial prayer. **Soft maturity warning displayed.** |
| CAT-14 | Justice, Legal Matters & Righteous Judgment | ⚖️ | 1+ | Court cases, immigration, custody. Needs new content drafted. |
| CAT-15 | Grief, Loss & Comfort | 🕊️ | NEW | Widows, loss of loved ones, processing grief. Pastor David to draft. |
| CAT-16 | Students, Exams & Academic Success | 📚 | NEW | Exams, scholarships, academic calling. Pastor Grace to draft. |

#### New Believer Track (Auto-Assigned, System-Driven)

| # | Confession | Focus |
|---|-----------|-------|
| NB-1 | Who I Am in Christ | Identity & acceptance |
| NB-2 | My Salvation is Secure | Assurance & foundation |
| NB-3 | I Walk by Faith | Basic faith declarations |
| NB-4 | God Loves Me | God's character & love |
| NB-5 | I Am Protected | Daily protection & safety |

- Auto-assigned to every new member for first **7 days**
- After completion, full library unlocked with progressive disclosure
- Drafted by Pastor Emmanuel + Bishop Samuel

#### Reference Sections (Not in Member-Facing Confession Browser)

| Section | Content | Audience | Location |
|---------|---------|----------|----------|
| Intercession Training & Guidelines | 4 docs | Pastors & Prayer Warriors | Pastor Resources page |
| Pastor Resources & Compiled References | 4+ docs (incl. Rev. Godwin Abba) | Pastors only | Pastor Dashboard |

#### Corporate Confessions (Bishop to Draft)

Not in the 86 documents but used verbally in church services:
- **"I Am" Declarations** — spoken every Sunday morning
- **Communion Confessions** — before the Lord's Supper
- **Pastoral Blessing Declarations** — spoken over congregation at dismissal
- **Tithing & Offering Confessions** — spoken during offering time

These will be digitized as Tier 1 content under CAT-03 (Faith, Favor & Declarations) and CAT-06 (Daily Confessions).

### 3.2 Content Structure Per Template

```
Template
├── name                    — Display title (plain language, e.g., "Breaking Financial Struggles")
├── description             — 1-2 sentence summary of when to use this
├── short_form_text         — 3-5 key confession lines for mobile card view
├── category_id             — FK to confession_categories
├── confessions[]           — Array of confession statements
│   ├── text                — "I confess that God is my provider..."
│   └── scripture_ref       — "Philippians 4:19"
├── declarations[]          — Array of declaration statements
│   ├── text                — "I declare that debt has no hold on my life..."
│   └── scripture_ref       — "Romans 13:8"
├── prayers[]               — Array of prayer paragraphs
│   └── text                — "Dear Lord, I bring my finances before you..."
├── scriptures[]            — Supporting scripture references (minimum 2-3 required)
├── tier                    — 1 (core), 2 (important), 3 (specialized)
├── difficulty_level        — beginner, intermediate, advanced
├── maturity_warning        — boolean (shows soft warning for advanced content)
├── recommended_duration    — "7_days", "21_days", "ongoing"
├── time_of_day             — morning, evening, anytime
├── created_by              — admin/bishop/pastor who curated
├── source_document         — original filename for traceability
├── is_published            — boolean (draft vs. live)
├── is_pastor_custom        — boolean (pastor-created, not in shared library without review)
└── source_attribution      — original author credit (e.g., "Rev. Godwin Abba")
```

### 3.3 Content Digitization Pipeline

```
Raw Files (86)
  → OCR (22 JPGs) + Text Extraction (44 DOCs, 6 DOCX, 5 PDFs)
  → De-duplication (~12 duplicates removed → ~60 unique documents)
  → Standardize to structured JSON
  → Plain-language title rewrite (Pastor Grace)
  → Short-form version creation (3-5 key lines per template)
  → Scripture reference validation (minimum 2-3 per template)
  → First-person, present-tense language check
  → Theological review (Bishop Samuel + 1 rotating pastor)
  → Plain-language accessibility review (Pastor Emmanuel)
  → Category assignment + tier classification
  → Publish to confession_templates table
```

**Digitization Timeline:**
| Phase | Content | Owner | Deadline |
|-------|---------|-------|----------|
| Week 1 | OCR + text extraction of all files | Bhargavi (tech) | Week 1 |
| Week 1 | Draft 5 New Believer Track confessions | Pastor Emmanuel + Bishop | Week 1 |
| Week 2 | Theological review of Tier 1 | Bishop + 1 pastor | Week 2 |
| Week 2 | Plain-language + short-form pass | Pastor Grace + Emmanuel | Week 2 |
| Week 2 | Marriage & Family specific review | Pastor David | Week 2 |
| Week 2 | Corporate confessions (I Am, communion, tithing) | Bishop Samuel | Week 2 |
| Week 3 | Draft new category content (Grief, Students, Thanksgiving) | Respective pastors | Week 3 |
| Week 3 | Expand Legal/Court confessions | Pastor Raju + Bishop | Week 3 |

---

## 4. Functional Requirements

### REQ-PE-1: Need-Based Discovery Entry Point

**Description:** Members are greeted with "What are you believing God for?" — a need-based entry that routes to relevant confessions before offering full library browse.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-1.1 | "What are you believing God for?" screen with quick-select chips: Healing, Finances, Family, Faith, Protection, Other | Must |
| PE-1.2 | Chip selection routes to relevant category with top confessions surfaced | Must |
| PE-1.3 | "Explore All Categories" link reveals full category grid | Must |
| PE-1.4 | Progressive disclosure: new users see 6 Tier 1 categories; "Explore More" reveals Tier 2/3 | Must |
| PE-1.5 | Search across all templates by keyword | Should |
| PE-1.6 | Confession of the Week displayed at top of entry point (when active) | Must |

**Acceptance Criteria:**
```
GIVEN a logged-in member navigating to the Prayer Engine
WHEN the page loads
THEN they see "What are you believing God for?" with quick-select chips
AND selecting "Healing" shows confessions from CAT-01 (Health & Healing)
AND "Explore All Categories" reveals the full category grid
AND new users see only Tier 1 categories until they tap "Explore More"
```

### REQ-PE-2: Confession Library Browser

**Description:** Full category-based browsing with short-form cards and expandable full text.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-2.1 | Display categories with icons, descriptions, and template counts | Must |
| PE-2.2 | Within a category, list templates as short-form cards (3-5 key lines) | Must |
| PE-2.3 | "Read Full Confession" expands to complete confessions, declarations, prayers, scriptures | Must |
| PE-2.4 | Spiritual Warfare (CAT-13) shows soft maturity warning on entry | Must |
| PE-2.5 | Filter templates by difficulty level, time of day, duration | Should |
| PE-2.6 | Source attribution displayed where applicable (e.g., "Rev. Godwin Abba") | Should |

### REQ-PE-3: "Confess Aloud" Mode

**Description:** A focused reading view designed for spoken confession — highlights one line at a time with large text and minimal UI. (Bishop Priority)

| ID | Requirement | Priority |
|----|------------|----------|
| PE-3.1 | Full-screen mode with large font, clean background, minimal chrome | Must |
| PE-3.2 | Highlights one confession/declaration line at a time | Must |
| PE-3.3 | Tap/swipe advances to next line; scripture ref shown alongside | Must |
| PE-3.4 | "Mark as Confessed" button appears only after scrolling through ALL statements | Must |
| PE-3.5 | Scripture reference displayed alongside each confession line | Must |
| PE-3.6 | Optional post-confession reflection prompt: "What spoke to you today?" | Should |

**Acceptance Criteria:**
```
GIVEN a member opens a confession in "Confess Aloud" mode
WHEN each line is displayed
THEN one confession statement is highlighted at a time with its scripture reference
AND the member taps/swipes to advance through all statements
AND "Mark as Confessed" only appears after the final statement
AND an optional reflection prompt appears after marking complete
```

### REQ-PE-4: Personal Confession Plan

**Description:** Members can add templates to their personal daily confession plan with 21-day structure.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-4.1 | "Add to My Plan" button on any template with duration picker (ongoing, 7-day, 21-day) | Must |
| PE-4.2 | Personal plan view shows all active confessions with progress (e.g., "Day 7 of 21") | Must |
| PE-4.3 | Mark confessions as completed each day via "Confess Aloud" mode or quick-check | Must |
| PE-4.4 | Support AM/PM time slot assignment (morning confessions vs. evening declarations) | Should |
| PE-4.5 | Remove or pause templates from plan | Must |
| PE-4.6 | Plan history — see past completed plans | Could |
| PE-4.7 | Smart nudge: "You read this confession today. Want to make it a 7-day practice?" | Should |

**Acceptance Criteria:**
```
GIVEN a member adds "Financial Breakthrough" to their plan as a 21-day confession
WHEN they view "My Plan" tab
THEN they see "Financial Breakthrough — Day 3 of 21" with a progress bar
AND they can open it in "Confess Aloud" mode
AND daily completion is tracked and shown
```

### REQ-PE-5: New Believer Auto-Track

**Description:** System-driven 7-day foundational confession plan auto-assigned on registration.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-5.1 | On new user registration, auto-assign 5 New Believer confessions as a 7-day plan | Must |
| PE-5.2 | New Believer plan appears prominently in dashboard and Prayer Engine | Must |
| PE-5.3 | After 7-day completion, show "Explore the Full Library" unlock message | Must |
| PE-5.4 | Before completion, show only Tier 1 categories in browse (progressive disclosure) | Should |
| PE-5.5 | No pastoral action needed — fully system-driven | Must |

### REQ-PE-6: Pastor Confession Assignment

**Description:** Pastors can prescribe specific confessions to individual members with engagement tracking.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-6.1 | Pastor can assign a confession template to a member from Pastor Dashboard | Must |
| PE-6.2 | Pastor can set duration (7-day, 21-day, ongoing) and add optional note | Must |
| PE-6.3 | Assigned confessions appear at TOP of member's plan with "Prescribed by Pastor [Name]" badge | Must |
| PE-6.4 | Pastor can see assignment list: which members have active assignments | Must |
| PE-6.5 | Pastor can see individual engagement for PRESCRIBED confessions (days completed, streak, last active) | Must |
| PE-6.6 | Pastor CANNOT see self-selected confession activity (privacy boundary) | Must |
| PE-6.7 | Integration with existing Wizard Assignments (REQ-5) as a component type | Should |
| PE-6.8 | Bishop can assign confessions across all pastors' members | Could |
| PE-6.9 | Pastor can create custom confessions for their members (flagged "Pastor-created") | Should |
| PE-6.10 | Pastor-created confessions do NOT appear in shared library without Bishop review | Must |

**Acceptance Criteria:**
```
GIVEN Pastor David assigns "Marriage Restoration Confession" to member Grace for 21 days
WHEN Grace logs in
THEN she sees "Prescribed by Pastor David" at the top of her plan with optional note
AND Pastor David can see "Grace — Day 14 of 21 — Last confessed: today" in his dashboard
AND Pastor David CANNOT see what Grace has self-selected from the library
```

### REQ-PE-7: Confession of the Week

**Description:** Bishop-selected weekly confession pushed to all members, tied to Sunday sermon theme.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-7.1 | Bishop/Admin can select one confession as "Confession of the Week" | Must |
| PE-7.2 | Appears at the top of every member's Prayer Engine entry point | Must |
| PE-7.3 | Active from Monday through Sunday (7-day auto-plan) | Must |
| PE-7.4 | Members can add it to their plan with one tap | Must |
| PE-7.5 | Shows anonymous community counter: "X believers are confessing with you this week" | Should (Phase 2) |
| PE-7.6 | Archive of past Confessions of the Week accessible | Could |

### REQ-PE-8: Confession Engagement Tracking

**Description:** Track confession practice as a spiritual discipline with tiered visibility.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-8.1 | Daily confession completion recorded in daily_entries | Must |
| PE-8.2 | "Today's Confessions" card on Dashboard (page 0) with count + quick-start button | Must |
| PE-8.3 | Include single declaration line + scripture ref in WhatsApp report | Must |
| PE-8.4 | Pastor dashboard: prescribed confession engagement per member | Must |
| PE-8.5 | Pastor dashboard: aggregate self-selected engagement (category trends, not individual detail) | Should |
| PE-8.6 | Basic activity indicator: "Last active X days ago" for all members | Should |
| PE-8.7 | Confession streak tracked alongside prayer/reading streaks | Could (Phase 3) |
| PE-8.8 | Monthly confession stats in Streaks & Stats page | Could (Phase 3) |
| PE-8.9 | Confession heatmap | Could (Phase 3) |
| PE-8.10 | Bishop dashboard: aggregate confession metrics across all churches | Could |

### REQ-PE-9: Content Management (Admin/Bishop)

**Description:** Admins and Bishops manage the confession library content.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-9.1 | Admin can create/edit/archive confession templates with full form | Must |
| PE-9.2 | Admin can create/edit confession categories | Must |
| PE-9.3 | Admin can set/change Confession of the Week | Must |
| PE-9.4 | Pastors can submit new confessions for Bishop review (flagged "pending review") | Should |
| PE-9.5 | Bishop review queue: approve/reject pastor-submitted confessions | Should |
| PE-9.6 | Bulk import from structured format (CSV/JSON) for batch template creation | Should |
| PE-9.7 | Template versioning — update content without breaking active member plans | Should |

### REQ-PE-10: Personal Reflection Notes

**Description:** Members can add private notes alongside confession completions.

| ID | Requirement | Priority |
|----|------------|----------|
| PE-10.1 | After "Mark as Confessed," optional prompt: "What spoke to you today?" | Should |
| PE-10.2 | Reflection saved alongside confession completion record | Should |
| PE-10.3 | Reflections are private — NOT visible to pastors | Must |
| PE-10.4 | Reflections linked to Prayer Journal for continuity | Could |

---

## 5. User Flows

### 5.1 New Member: First-Time Experience

```
Registration complete
  → System auto-assigns 7-day "New Believer Track" (5 confessions)
  → Dashboard shows "Welcome! Start your faith journey" card
  → Tap → Opens Day 1: "Who I Am in Christ"
  → "Confess Aloud" mode: one line at a time, scripture alongside
  → After all lines → "Mark as Confessed Today"
  → Optional reflection prompt: "What spoke to you?"
  → Dashboard updates: "Day 1 complete — 6 days to go!"
  → After 7 days → "You've completed the foundation! Explore the full library"
  → Full category browser unlocked with progressive disclosure
```

### 5.2 Member: Need-Based Discovery

```
Dashboard → "Today's Confessions" card or Prayer Engine nav
  → "What are you believing God for?"
  → Taps "Healing" chip
  → Sees CAT-01 (Health & Healing) with top confessions as short-form cards
  → Reads "Healing Confession" card (3-5 key lines)
  → Taps "Read Full Confession" → sees complete text with all scriptures
  → Taps "Confess Aloud" → focused mode, one line at a time
  → After confession → "Mark as Confessed Today"
  → Nudge: "Want to make this a 21-day practice?"
  → Taps "Yes" → Added to personal plan as 21-day confession
  → Next morning: Dashboard shows "Healing Confession — Day 2 of 21"
```

### 5.3 Pastor: Prescribe Confessions During Counseling

```
Pastor Dashboard → Member list → Select "Grace"
  → "Assign Confession" button
  → Browse/search confession library
  → Select "Financial Breakthrough Confession"
  → Set: 21 days, starting today
  → Add note: "Stay strong in faith, Grace. Philippians 4:19."
  → Submit assignment
  → Grace logs in → sees "Prescribed by Pastor David" at top of her plan
  → Grace confesses daily → Pastor sees progress:
    "Grace — Financial Breakthrough — Day 14/21 — Last confessed: today"
  → Grace completes 21 days → celebration + "Plan Completed" notification to pastor
```

### 5.4 Bishop: Set Confession of the Week

```
Admin Panel → Prayer Engine → "Confession of the Week" tab
  → Browse library → Select "Faith, Favor & Declarations: Walking in Victory"
  → Set active period: Monday Apr 7 → Sunday Apr 13
  → Link to Sunday sermon: "Victory in Christ — Hebrews 11"
  → Publish
  → All members see it at top of Prayer Engine:
    "This Week's Confession: Walking in Victory — 47 believers confessing with you"
  → Members tap → Add to plan → Confess daily
  → Next Sunday: Bishop references it in service
```

### 5.5 Admin: Add New Confession Template

```
Admin Panel → Prayer Engine → Templates tab → "New Template"
  → Category: Health & Healing
  → Title: "Emotional Healing Confession" (plain language)
  → Description: "For those processing past trauma and emotional wounds"
  → Short-form (3-5 key lines):
    - "By the stripes of Jesus, I am healed — spirit, soul, and body"
    - "I release every past hurt and receive God's restoration"
    - "My emotions are governed by the peace of God"
  → Full confessions: [line-by-line with scripture refs]
  → Full declarations: [line-by-line with scripture refs]
  → Prayers: [paragraph entry]
  → Scriptures: Isaiah 53:5, Psalm 147:3, Philippians 4:7 (minimum 2-3)
  → Difficulty: Beginner
  → Duration: 21 days
  → Time of day: Morning
  → Source attribution: "Rev. Godwin Abba"
  → Save as Draft → Theological Review → Publish
```

---

## 6. Database Schema

### 6.1 New Tables

```sql
-- ============================================
-- PRAYER ENGINE SCHEMA — Phase 3
-- ============================================

-- Confession categories (16 categories + progressive disclosure support)
CREATE TABLE confession_categories (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    icon TEXT DEFAULT '📖',
    color TEXT DEFAULT '#5B4FC4',
    tier INTEGER DEFAULT 1,                   -- 1=core, 2=important, 3=specialized
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Confession templates (core content library)
CREATE TABLE confession_templates (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    category_id BIGINT REFERENCES confession_categories(id),
    name TEXT NOT NULL,                        -- plain-language title
    description TEXT,                          -- 1-2 sentence "when to use"
    short_form_text TEXT,                      -- 3-5 key lines for mobile card
    confessions JSONB DEFAULT '[]',            -- [{text, scripture_ref}]
    declarations JSONB DEFAULT '[]',           -- [{text, scripture_ref}]
    prayers JSONB DEFAULT '[]',               -- [{text}]
    scriptures JSONB DEFAULT '[]',            -- ["Philippians 4:19", ...]
    tier INTEGER DEFAULT 2,                    -- 1=core, 2=important, 3=specialized
    difficulty_level TEXT DEFAULT 'beginner',   -- beginner, intermediate, advanced
    maturity_warning BOOLEAN DEFAULT FALSE,    -- soft warning for advanced content
    recommended_duration TEXT DEFAULT 'ongoing', -- ongoing, 7_days, 21_days
    time_of_day TEXT DEFAULT 'anytime',        -- morning, evening, anytime
    is_published BOOLEAN DEFAULT FALSE,
    is_pastor_custom BOOLEAN DEFAULT FALSE,    -- pastor-created, not in shared library
    review_status TEXT DEFAULT 'draft',        -- draft, pending_review, approved, rejected
    created_by UUID REFERENCES auth.users(id),
    source_document TEXT,                      -- original filename for traceability
    source_attribution TEXT,                   -- original author credit
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- New Believer Track templates (separate for clear auto-assignment)
CREATE TABLE new_believer_track (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    day_number INTEGER NOT NULL,               -- 1-7
    template_id BIGINT REFERENCES confession_templates(id) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Confession of the Week
CREATE TABLE confession_of_the_week (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    template_id BIGINT REFERENCES confession_templates(id) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    sermon_theme TEXT,                         -- linked Sunday sermon topic
    sermon_reference TEXT,                     -- e.g., "Hebrews 11"
    set_by UUID REFERENCES auth.users(id),    -- Bishop who selected
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Member's personal confession plan
CREATE TABLE member_confession_plans (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) NOT NULL,
    template_id BIGINT REFERENCES confession_templates(id) NOT NULL,
    assigned_by UUID REFERENCES auth.users(id),  -- NULL = self-selected, UUID = pastor-assigned
    assignment_note TEXT,                          -- optional pastor note
    plan_type TEXT DEFAULT 'ongoing',             -- ongoing, 7_days, 21_days, new_believer
    time_slot TEXT DEFAULT 'anytime',             -- morning, evening, anytime
    start_date DATE DEFAULT CURRENT_DATE,
    end_date DATE,                                -- NULL for ongoing
    status TEXT DEFAULT 'active',                 -- active, completed, paused, removed
    is_new_believer_track BOOLEAN DEFAULT FALSE,  -- auto-assigned onboarding
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
    reflection_note TEXT,                          -- private personal reflection
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, plan_id, completed_date, time_slot)
);
```

### 6.2 Indexes

```sql
CREATE INDEX idx_confession_categories_tier ON confession_categories(tier);
CREATE INDEX idx_confession_templates_category ON confession_templates(category_id);
CREATE INDEX idx_confession_templates_published ON confession_templates(is_published);
CREATE INDEX idx_confession_templates_tier ON confession_templates(tier);
CREATE INDEX idx_confession_templates_review ON confession_templates(review_status);
CREATE INDEX idx_cotw_active ON confession_of_the_week(is_active, start_date, end_date);
CREATE INDEX idx_member_plans_user ON member_confession_plans(user_id);
CREATE INDEX idx_member_plans_user_status ON member_confession_plans(user_id, status);
CREATE INDEX idx_member_plans_assigned_by ON member_confession_plans(assigned_by);
CREATE INDEX idx_member_plans_new_believer ON member_confession_plans(user_id, is_new_believer_track);
CREATE INDEX idx_completions_user_date ON confession_completions(user_id, completed_date);
CREATE INDEX idx_completions_plan ON confession_completions(plan_id);
```

### 6.3 RLS Policies

```sql
-- confession_categories: everyone can read active categories
ALTER TABLE confession_categories ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read active categories"
    ON confession_categories FOR SELECT USING (is_active = true);
CREATE POLICY "Admin can manage categories"
    ON confession_categories FOR ALL USING (is_admin(auth.uid()));

-- confession_templates: published readable by all; admin + creators manage
ALTER TABLE confession_templates ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read published templates"
    ON confession_templates FOR SELECT
    USING (is_published = true AND is_pastor_custom = false);
CREATE POLICY "Pastor sees own custom templates"
    ON confession_templates FOR SELECT
    USING (created_by = auth.uid() AND is_pastor_custom = true);
CREATE POLICY "Admin can manage all templates"
    ON confession_templates FOR ALL USING (is_admin(auth.uid()));
CREATE POLICY "Pastor can create custom templates"
    ON confession_templates FOR INSERT
    WITH CHECK (is_pastor_custom = true AND created_by = auth.uid());

-- new_believer_track: everyone can read
ALTER TABLE new_believer_track ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read track" ON new_believer_track FOR SELECT USING (true);
CREATE POLICY "Admin manages track" ON new_believer_track FOR ALL USING (is_admin(auth.uid()));

-- confession_of_the_week: everyone can read active
ALTER TABLE confession_of_the_week ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read active COTW"
    ON confession_of_the_week FOR SELECT USING (is_active = true);
CREATE POLICY "Admin manages COTW"
    ON confession_of_the_week FOR ALL USING (is_admin(auth.uid()));

-- member_confession_plans: user sees own; pastor sees assigned
ALTER TABLE member_confession_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "User sees own plans"
    ON member_confession_plans FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "User manages own plans"
    ON member_confession_plans FOR ALL USING (user_id = auth.uid());
CREATE POLICY "Pastor sees assigned plans"
    ON member_confession_plans FOR SELECT USING (assigned_by = auth.uid());
CREATE POLICY "Pastor can assign to viewable members"
    ON member_confession_plans FOR INSERT
    WITH CHECK (can_view_user(auth.uid(), user_id));

-- confession_completions: user manages own; pastor sees prescribed only
ALTER TABLE confession_completions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "User manages own completions"
    ON confession_completions FOR ALL USING (user_id = auth.uid());
CREATE POLICY "Pastor views completions for prescribed plans only"
    ON confession_completions FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM member_confession_plans mcp
        WHERE mcp.id = confession_completions.plan_id
        AND mcp.assigned_by = auth.uid()
    ));
-- NOTE: reflection_note is in the row but pastors accessing via prescribed plan policy
-- will see it. Application layer must EXCLUDE reflection_note from pastor queries.
```

### 6.4 Seed Data

```sql
-- Seed 16 categories
INSERT INTO confession_categories (name, description, icon, color, tier, sort_order) VALUES
('Health & Healing', 'Physical healing, emotional healing, divine health', '🏥', '#3A8F5C', 1, 1),
('Finances, Business & Provision', 'Financial breakthrough, employment, God''s provision', '💰', '#D4853A', 1, 2),
('Faith, Favor & Declarations', 'Corporate confessions, favor, righteousness', '✨', '#5B4FC4', 1, 3),
('Identity in Christ & Personal Transformation', 'Who I am in Christ, breakthrough, letting go', '🦋', '#C44B5B', 1, 4),
('Salvation & Evangelism', 'Unsaved loved ones, new converts, Great Commission', '🌍', '#2E7D32', 1, 5),
('Daily Confessions & Morning/Evening Prayers', 'AM/PM daily rhythm, general daily prayers', '🌅', '#FF8F00', 1, 6),
('Marriage & Spouse', 'Harmonious marriage, husbands, wives, restoration', '💍', '#C44B5B', 2, 7),
('Family & Parenting', 'Children, teenagers, household blessings', '👨‍👩‍👧‍👦', '#5B4FC4', 2, 8),
('Daily Protection & Safety', 'Traveling mercies, safety, protection from harm', '🛡️', '#1565C0', 2, 9),
('Church, Ministry & Kingdom Advancement', 'Pastors, church growth, revival, intercession', '⛪', '#6A1B9A', 2, 10),
('Believing for Children & Family Expansion', 'Conception, fertility, adoption, waiting on God', '👶', '#E91E63', 2, 11),
('Thanksgiving & Praise Confessions', 'Gratitude, declaring God''s goodness', '🙌', '#FFB300', 2, 12),
('Spiritual Warfare & Deliverance', 'Breaking curses, cleansing, territorial prayer', '⚔️', '#B71C1C', 3, 13),
('Justice, Legal Matters & Righteous Judgment', 'Court cases, immigration, custody', '⚖️', '#37474F', 3, 14),
('Grief, Loss & Comfort', 'Widows, loss of loved ones, processing grief', '🕊️', '#78909C', 3, 15),
('Students, Exams & Academic Success', 'Exams, scholarships, academic calling', '📚', '#00897B', 3, 16);
```

---

## 7. UI/UX Considerations

### 7.1 New Page: Prayer Engine (`pages/8_Prayer_Engine.py`)

**Three Tabs:**

| Tab | Content | Primary Action |
|-----|---------|---------------|
| **Discover** | "What are you believing for?" + Confession of the Week + Category browse | Find & start confessions |
| **My Plan** | Active confessions with daily checklist + progress bars | Confess & track |
| **Confess** | Focused "Confess Aloud" mode for today's confessions | Speak & complete |

### 7.2 Design System (Existing `modules/styles.py`)

- **Fonts:** DM Serif Display (headings) + DM Sans (body) — consistent with app
- **Category cards:** Icon + name + description + template count (same pattern as Prayer Journal)
- **Short-form cards:** 3-5 confession lines, scripture refs, "Read Full" expandable
- **Confess Aloud mode:** Large DM Serif Display font, cream/warm background, one line highlighted, scripture in muted DM Sans below
- **Progress bars:** Purple (#5B4FC4) for active plans, green (#3A8F5C) for completed
- **Badges:** "Prescribed by Pastor [Name]" (purple), "Confession of the Week" (gold), "New Believer" (blue)

### 7.3 Dashboard Integration (page 0)

**"Today's Confessions" card:**
- Shows count of active confessions due today
- Current plan progress: "Day 7 of 21 — Healing Confession"
- Quick "Start Confessing" button → opens Confess Aloud mode
- Confession of the Week banner if active

### 7.4 Soft Maturity Warning (CAT-13: Spiritual Warfare)

```
┌────────────────────────────────────────────┐
│  ⚔️ Spiritual Warfare & Deliverance       │
│                                            │
│  These are powerful declarations of        │
│  authority in Christ. We recommend          │
│  engaging with these under pastoral         │
│  guidance, especially if you are new        │
│  in your faith walk.                        │
│                                            │
│  [Continue]     [Ask My Pastor]            │
└────────────────────────────────────────────┘
```

"Ask My Pastor" creates a request visible in the Pastor Dashboard — a natural bridge between self-service and prescription.

### 7.5 Mobile-First Principles

- Short-form cards: confession fits on one phone screen without scrolling
- Confess Aloud: one statement per screen, large font, tap to advance
- Large tap targets for "Mark Complete" and "Add to Plan"
- WhatsApp-friendly text format for report inclusion

---

## 8. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-1 | Page load for library browse | < 2 seconds |
| NFR-2 | Template content cached per session | `@st.cache_data` with session-scoped TTL |
| NFR-3 | Support 100+ templates without UI degradation | Pagination (12 per page) + lazy load |
| NFR-4 | Confession text renders correctly with special characters | Unicode support, tested with accented text |
| NFR-5 | All pages follow existing auth guard pattern | `require_login()` + `require_password_changed()` |
| NFR-6 | Confess Aloud mode works on mobile browsers | Tested on iOS Safari + Android Chrome |
| NFR-7 | Reflection notes never exposed to pastor queries | Application-layer exclusion + verified in code review |

---

## 9. Integration Points

### 9.1 Daily Entry (page 1) — MVP

- Add "Confessions completed today" indicator to daily entry form
- Include single declaration line + scripture ref in WhatsApp report generation
- Example in report: `✝️ Today's Confession: "I declare that God is my provider" — Philippians 4:19`

### 9.2 Pastor Dashboard — MVP

- New "Confession Assignments" tab
- Table: Member | Confession | Duration | Progress | Last Active
- Aggregate view: category trends across all members (self-selected, anonymized)
- Alert badge for members who haven't confessed in 3+ days on a prescribed plan

### 9.3 Dashboard (page 0) — MVP

- "Today's Confessions" card with count, progress, quick-start button
- Confession of the Week banner when active

### 9.4 Prayer Journal (page 7) — Phase 2

- "Import from Library" button in confession/declaration steps of prayer wizard
- Link between prayer entries and confession templates

### 9.5 Wizard Assignments (REQ-5) — Phase 2

- Confession plans as a component type in wizard assignments
- Pastor can include confession templates alongside Bible reading and prayer templates

### 9.6 Streaks & Stats (page 4) — Phase 3

- Confession streak alongside prayer/reading streaks
- Monthly confession completion rate
- Confession heatmap

---

## 10. Implementation Phases

### Phase 3A: Foundation (MVP) — Weeks 1-3

**Goal:** Confession library live, need-based discovery, personal plans, new believer track, Confession of the Week, pastor assignments, daily entry + WhatsApp integration.

| # | Task | Description | Effort |
|---|------|-------------|--------|
| 1 | DB migration | Create 6 tables + RLS + indexes + seed categories | 4 SP |
| 2 | Content digitization | OCR + extract + structure Tier 1 docs (15-20 templates) | 5 SP |
| 3 | `modules/db.py` functions | CRUD for all new tables | 4 SP |
| 4 | Discovery entry point | "What are you believing for?" + chips + progressive disclosure | 4 SP |
| 5 | Library browser | Category grid + short-form cards + full text expand | 5 SP |
| 6 | Confess Aloud mode | Focused one-line-at-a-time reading + mark complete | 5 SP |
| 7 | Personal plan | Add to plan, view plan, progress tracking, daily completion | 5 SP |
| 8 | New Believer auto-track | Auto-assign on registration + 7-day progression + unlock | 3 SP |
| 9 | Confession of the Week | Admin set COTW + display at top + add-to-plan | 3 SP |
| 10 | Pastor assignment | Assign from dashboard + engagement tracking for prescribed | 5 SP |
| 11 | Dashboard card | "Today's Confessions" on page 0 | 2 SP |
| 12 | Daily Entry integration | Confession indicator + WhatsApp report line | 3 SP |
| | **Total** | | **48 SP** |

### Phase 3B: Pastoral & Content Management — Weeks 4-5

**Goal:** Content management UI, pastor-created confessions, review workflow, deeper integrations.

| # | Task | Description | Effort |
|---|------|-------------|--------|
| 1 | Content management UI | Admin CRUD for templates + categories in Admin Panel | 5 SP |
| 2 | Pastor custom confessions | Pastor creates + flags as custom + assign to own members | 4 SP |
| 3 | Review workflow | Bishop review queue: approve/reject pastor submissions | 3 SP |
| 4 | Bulk import | CSV/JSON import for batch template creation | 3 SP |
| 5 | Reflection notes | Post-confession prompt + private storage | 2 SP |
| 6 | Prayer Journal integration | "Import from Library" in wizard steps 4-5 | 3 SP |
| 7 | Wizard Assignment integration | Confession plans as component type | 3 SP |
| 8 | Soft maturity warning | Warning modal on CAT-13 + "Ask My Pastor" request | 2 SP |
| | **Total** | | **25 SP** |

### Phase 3C: Advanced Features — Weeks 6-8

**Goal:** Community features, advanced tracking, bishop-level analytics.

| # | Task | Description | Effort |
|---|------|-------------|--------|
| 1 | AM/PM scheduling | Morning vs. evening time slot assignment in plans | 3 SP |
| 2 | Community counter | Anonymous "X believers confessing with you" on COTW | 2 SP |
| 3 | Streaks integration | Confession streaks in stats page + heatmap | 4 SP |
| 4 | Bishop dashboard | Aggregate confession metrics across all churches | 4 SP |
| 5 | Template versioning | Update content without breaking active member plans | 3 SP |
| 6 | Plan history | View past completed confession plans | 2 SP |
| 7 | "Ask My Pastor" flow | Request from maturity warning → visible in Pastor Dashboard | 2 SP |
| | **Total** | | **20 SP** |

**Grand Total: 93 SP across 3 phases**

---

## 11. Success Metrics

| Metric | Target | Measurement | Phase |
|--------|--------|-------------|-------|
| Tier 1 content live | 15-20 templates published | Count of published, tier=1 confession_templates | MVP |
| New Believer completion | 60% of new members complete 7-day track | new_believer plans completed / total new members | MVP |
| Member adoption | 70% of active members have at least 1 active plan | member_confession_plans / active users | MVP |
| Daily engagement | 40% of plan holders complete daily confession | confession_completions / active plans per day | MVP |
| Confession of the Week uptake | 50% of members add COTW to plan weekly | COTW plan adds / active members | MVP |
| Pastoral assignments | Each pastor assigns 5+ confessions/month | prescribed plans created per pastor | MVP |
| WhatsApp inclusion | Confession line appears in 80% of daily reports | Reports with confession line / total reports | MVP |
| Full library size | 50+ published templates across all 16 categories | Count of published confession_templates | Phase 3B |
| Content coverage | All 16 categories have at least 2 templates | Count by category | Phase 3C |
| Average streak | > 7 consecutive days | Calculated from confession_completions | Phase 3C |

---

## 12. Content Standards & Review Process

### 12.1 Non-Negotiable Standards (Bishop-Mandated)

1. **Scripture-backed:** Every confession template MUST have minimum 2-3 scripture references. No confession enters the library without scriptural grounding.

2. **First-person, present-tense declarations:** "I am healed by the stripes of Jesus" — NOT "I hope God heals me." Confession declares what God has already done.

3. **Plain-language accessible:** Titles use everyday language ("Breaking Financial Struggles") not theological jargon ("Deuteronomy 28 Blessings"). Content should be understandable by a person who gave their life to Christ three weeks ago.

4. **Short-form + full text:** Every template must have both a 3-5 line mobile card version and the complete text.

### 12.2 Review Committee

| Role | Responsibility |
|------|---------------|
| **Bishop Samuel Patta** | Final approval authority on all published confessions |
| **1 Senior Pastor (rotating)** | Theological accuracy review |
| **1 Mature Prayer Warrior** | Member perspective and accessibility review |

Minimum 2 of 3 reviewers must sign off before a confession is published.

### 12.3 Review Workflow

```
Draft → Pastor submits
  → Status: "pending_review"
  → Bishop + 1 reviewer examine
  → Check: scripture refs? first-person? plain language? short-form?
  → Approve → Status: "approved" → Admin publishes
  → OR Reject with feedback → Status: "rejected" → Pastor revises
```

---

## 13. Privacy & Visibility Model

This section codifies the privacy boundary established in the brainstorm session.

### 13.1 What Each Role Can See

| Data | Member | Pastor | Bishop | Admin |
|------|--------|--------|--------|-------|
| Own confession plans & completions | Yes | — | — | — |
| Own reflection notes | Yes | **No** | **No** | **No** |
| Prescribed plan engagement (specific) | Yes (own) | Yes (assigned members) | Yes (all) | Yes |
| Self-selected plan engagement (individual) | Yes (own) | **No** | **No** | **No** |
| Self-selected engagement (aggregate trends) | — | Yes (own members) | Yes (all) | Yes |
| Basic activity indicator ("last active X days ago") | — | Yes (own members) | Yes (all) | Yes |
| Confession of the Week uptake count | Anonymous count | Yes (count) | Yes (count) | Yes |
| Pastor-created custom confessions | If assigned | Own creations | All | All |

### 13.2 Application-Layer Enforcement

- `reflection_note` field MUST be excluded from all pastor/bishop queries in `modules/db.py`
- Self-selected plans (where `assigned_by IS NULL`) must NOT expose `template_id` to pastor queries — only aggregate category counts
- RLS provides database-level enforcement; application layer adds the reflection note and self-selected detail exclusions

---

## 14. Out of Scope

- Audio recordings of confessions (future consideration post-Phase 3)
- Multi-language support (English only for all phases)
- AI-generated confessions or personalization
- Push notifications for confession reminders
- Offline mode / PWA support
- Integration with external prayer apps
- Member-created freestanding confessions (personal notes only — per Bishop decision)
- Hard content restrictions by maturity level (soft warnings only — per Bishop decision)

---

## 15. Brainstorm Decisions Log

All open questions from v1.0 have been resolved:

| # | Question | Decision | Decided By |
|---|----------|----------|-----------|
| 1 | Category taxonomy — 14 correct? | Expanded to 16 categories + New Believer Track. Split Marriage/Family, split Protection/Warfare. Added Grief, Students, Thanksgiving. | Consensus |
| 2 | Access control by maturity? | Soft warnings on Spiritual Warfare (CAT-13) + "Ask My Pastor" button. No hard locks. | Bishop (overruling David's hard gates) |
| 3 | Can pastors create confessions? | Yes — flagged as "Pastor-created," usable with own members. Shared library requires Bishop review. | Consensus |
| 4 | Can members edit/create confessions? | No freestanding confessions. Members can add personal reflection notes alongside completions. | Bishop (overruling Grace's full member creation) |
| 5 | Engagement visibility for pastors? | Individual tracking for prescribed confessions. Aggregate trends for self-selected. Basic activity for all. | Bishop (compromise across all 3 pastors) |
| 6 | Confession of the Week priority? | Yes — MVP feature. Bishop-selected, tied to Sunday sermon, weekly cadence. | Bishop (strong yes) |
| 7 | Language demand? | English only for all phases. | Consensus |
| 8 | Source attribution? | Yes — display where applicable (e.g., "Rev. Godwin Abba"). | Consensus |
| 9 | Theological review authority? | Bishop Samuel + 1 rotating pastor + 1 prayer warrior. Min 2 of 3 sign off. | Bishop |
| 10 | Digitization ownership? | Tech (Bhargavi): OCR + extraction. Pastors: review per category. Bishop: corporate confessions. | Consensus |

---

*This PRD supersedes version 1.0 (pre-brainstorm draft). All decisions reflect the consolidated outcome of the Bishop/Pastor brainstorm session held on 2026-04-03.*