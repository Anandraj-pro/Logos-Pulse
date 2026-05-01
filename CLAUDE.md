# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Logos Pulse is a Streamlit multi-user web app for tracking daily spiritual disciplines (prayer, Bible reading, sermon listening). It supports role-based access for Admins, Bishops, Pastors, and Prayer Warriors, with WhatsApp report generation, confession plans, sermon notes, and a categorized prayer journal.

## Running the App
```bash
streamlit run app.py
```

Dependencies: `pip install -r requirements.txt` (streamlit, plotly, requests, supabase, toml)

Secrets live in `.streamlit/secrets.toml` (gitignored):
```toml
[supabase]
url = "..."
anon_key = "..."
service_role_key = "..."
```

There is no test suite. Validate changes by running the app and exercising the affected page.

## Architecture

### Auth Flow (app.py)
`app.py` is the entry point and sole navigation controller. It has four mutually exclusive states:
1. **Unauthenticated** → shows only `views/Login.py`, sidebar hidden
2. **`must_change_password`** → shows only `views/Change_Password.py`, sidebar hidden
3. **`onboarding_completed == False`** → shows only `views/Onboarding.py`, sidebar hidden
4. **Authenticated** → shows full nav; role-gated pages appended to `all_pages` list

Admin impersonation is handled entirely in `app.py` — it overwrites `st.session_state["user_id"]`, `["role"]`, and `["preferred_name"]` with the target user's values, storing the real values under `_real_*` keys. All downstream code reads from session state, so impersonation is transparent.

### Two Supabase Clients
`modules/supabase_client.py` provides two cached clients:
- `get_supabase_client()` — anon key, respects Row Level Security. Used for all user-owned data reads/writes in `modules/db.py`.
- `get_admin_client()` — service role key, bypasses RLS. Used for cross-user queries (pastor → members, bishop → pastors), account creation in `modules/rbac.py`, and audit/seeding operations.

**Rule:** Use `_client()` (the session-aware wrapper in `db.py`) for user-owned data. Use `get_admin_client()` directly only when you need to read/write another user's data.

### Data Layer (modules/db.py)
All Supabase queries go through `db.py`. Key patterns:
- `_client()` — sets the user's JWT session before each request; auto-refreshes expired tokens.
- `_safe_execute(op, fallback)` — wraps any operation; handles JWT expiry (retries once), RLS violations, and connection errors with user-visible error messages.
- Session-scoped cache — read results are stored in `st.session_state` with `_db_cache_{uid}_{name}` keys. Write functions call `_clear_cache(prefix)` to invalidate. This avoids duplicate API calls within a single Streamlit rerun.
- All text input is passed through `modules/sanitize.sanitize_html()` before insert/update.

### Role Hierarchy
```
Admin → Bishop → Pastor → Prayer Warrior
```
- `modules/auth.py` — `require_login()`, `require_password_changed()`, `require_role(["admin"])` guards; call these at the top of every page in that order.
- `modules/rbac.py` — account CRUD for higher roles (create pastor, create bishop, reset passwords, delete accounts). Uses admin client exclusively.
- Supabase RLS + `can_view_user()` PostgreSQL function enforce data isolation at the DB layer.

### Views (views/)
All pages live in `views/`. Pages visible to all authenticated users:
`0_Dashboard`, `1_Daily_Entry`, `2_Daily_Log`, `3_Weekly_Assignment`, `4_Streaks_and_Stats`, `6_Sermon_Notes`, `7_Prayer_Journal`, `8_Prayer_Engine`, `Fasting_Tracker`, `Personal_Goals`, `Testimonies`, `5_Settings`, `Profile`

Role-gated (added in `app.py`):
- `Admin_Panel` — admin only
- `Bishop_Dashboard` — admin, bishop
- `Pastor_Dashboard`, `Wizard_Assignment`, `Member_Detail` — admin, bishop, pastor

### Design System (modules/styles.py)
`styles.py` defines `COLORS` (design tokens), `SHARED_CSS` (global overrides, mobile responsive rules, card/badge/button styles), and helper functions like `apply_shared_styles()` and `sidebar_logo()`. Every page must call `apply_shared_styles()` — never add inline CSS that duplicates or overrides these tokens.

### Key Modules
| Module | Purpose |
|---|---|
| `modules/growth_score.py` | Spiritual Growth Score (0-100) — Consistency 40% + Quantity 30% + Diversity 20% + Engagement 10%. Levels: Seed/Sprout/Sapling/Tree/Forest. Uses admin client. |
| `modules/message.py` | `format_whatsapp_message()` — generates the shareable daily report string |
| `modules/bible_data.py` | Static Bible book/chapter data |
| `modules/bible_reader.py` | Bible text reading with font controls |
| `modules/scripture_lookup.py` | Scripture autocomplete and lookup |
| `modules/chapter_splitter.py` | Splits chapter ranges for weekly assignments |
| `modules/seed.py` | Seeds default prayer categories/prayers for new Prayer Warriors |
| `modules/models.py` | `DailyEntry` and `WeeklyAssignment` dataclasses with `from_row()` constructors |
| `modules/sanitize.py` | `sanitize_html()` — strip XSS from all user text before DB writes |

### Prayer Engine (views/8_Prayer_Engine.py)
Distinct subsystem with its own DB tables: `confession_categories`, `confession_templates`, `member_confession_plans`, `confession_completions`, `confession_of_the_week`, `new_believer_track`. Pastors assign confession plans to members; completions are tracked per-day per-plan. The "Confession of the Week" is set by admin/pastor and shown on the dashboard.

### Wizard Assignments (views/Wizard_Assignment.py)
Composite assignments (bible reading + prayer + confession) created by pastors/bishops for specific members. Tables: `wizard_assignments`, `wizard_assignment_targets`, `wizard_components`, `wizard_component_progress`.

## Supabase Setup
- Project ID: `whyvlkkjbxehdbsgohre`
- Schema: run `migrations/001_schema.sql` in Supabase SQL Editor
- Auth: email/password; disable "Confirm email" in Supabase Auth settings (accounts are created with `email_confirm=True` via admin API)
- New tables must be added to `migrations/001_schema.sql` and have appropriate RLS policies

## Role Hierarchy & Default Passwords
```
Admin    Raju@002
Bishop   Bishop@123
Pastor   Pastor@123
Prayer Warrior  Open@123
```
All accounts are created with `must_change_password = True` — users are forced to change on first login.

## BMAD Framework
`bmad-core/` contains the BMAD agent definitions and knowledge base for AI-assisted planning. Church-specific agents: `bmad-core/agents/bishop.md`, `sr-pastor.md`, `pastor.md`. Bible knowledge base: `bmad-core/knowledge/bible-knowledge.md`. Design docs live in `bmad-docs/`.
