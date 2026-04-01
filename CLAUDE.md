# Logos Pulse — Spiritual Growth Tracker

## Project Overview
A Streamlit-based multi-user web app for tracking daily spiritual disciplines (prayer, Bible reading, sermon listening) with WhatsApp report generation, sermon notes journaling, and a categorized prayer journal. Supports role-based access for Admins, Bishops, Pastors, and Prayer Warriors.

## Tech Stack
- **Framework**: Streamlit (Python 3.13)
- **Database**: Supabase (PostgreSQL) with Row Level Security
- **Auth**: Supabase Auth (email/password, OTP password reset)
- **Styling**: Custom CSS via `modules/styles.py` (shared design system)
- **Hosting**: Streamlit Community Cloud
- **Fonts**: DM Serif Display + DM Sans

## Project Structure
```
app.py                      # Entry point — auth-aware navigation + role-based sidebar
pages/
  Login.py                  # Login, self-registration, forgot password
  Change_Password.py        # Mandatory password change on first login
  0_Dashboard.py            # Personal dashboard with streaks, verse, status
  1_Daily_Entry.py          # Log prayer, Bible reading, sermons + generate report
  2_Daily_Log.py            # Calendar/list view of past entries
  3_Weekly_Assignment.py    # Bible reading goals with daily breakdown
  4_Streaks_and_Stats.py    # Heatmap, monthly stats
  5_Settings.py             # User preferences, data export/import
  6_Sermon_Notes.py         # Sermon notes with scripture lookup
  7_Prayer_Journal.py       # Categorized prayers with wizard
  Admin_Panel.py            # Admin: user CRUD, analytics (admin only)
  Bishop_Dashboard.py       # Bishop: pastor oversight (admin, bishop)
  Pastor_Dashboard.py       # Pastor: member tracking (admin, bishop, pastor)
modules/
  auth.py                   # Login, signup, session, auth guards (require_login, require_role)
  rbac.py                   # Role-based account CRUD, hierarchy queries
  supabase_client.py        # Cached Supabase clients (anon + admin)
  seed.py                   # Default prayer categories/prayers for new users
  db.py                     # Data layer — all Supabase queries (replaces SQLite)
  styles.py                 # Shared CSS design system
  bible_data.py / bible_reader.py / scripture_lookup.py
  chapter_splitter.py / clipboard.py / message.py / utils.py
migrations/
  001_schema.sql            # Full Supabase schema (run in SQL Editor)
  seed_admin.py             # One-time admin account seeder
.streamlit/secrets.toml     # Supabase URL + keys (gitignored)
bmad-core/                  # BMAD framework agents, tasks, templates
bmad-docs/                  # PRD, architecture, user stories, risks
```

## Role Hierarchy
```
Admin (Raju@002) → Bishop (Bishop@123) → Pastor (Pastor@123) → Prayer Warrior (Open@123)
```
- All roles can log their own spiritual entries
- Higher roles can view data of users in their oversight tree via RLS
- `must_change_password` flag enforced on first login for all roles

## Key Conventions
- All pages use `modules/styles.py` — never duplicate inline CSS
- Auth guards: `require_login()` + `require_password_changed()` at top of every page
- Role guards: `require_role(["admin"])` for admin-only pages
- Database: all queries go through `modules/db.py`, which uses `_client()` with session tokens
- RLS handles data isolation — `can_view_user()` PostgreSQL function for hierarchical access
- Run with: `streamlit run app.py`

## Supabase Setup
- Project: logos-pulse (whyvlkkjbxehdbsgohre)
- Schema: `migrations/001_schema.sql` (run in Supabase SQL Editor)
- Auth: email/password, admin API for account creation
- Important: disable "Confirm email" in Supabase Auth settings (we use admin.create_user with email_confirm=True)