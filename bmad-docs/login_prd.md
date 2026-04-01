# PRD: Login, Registration & Role-Based Access Control -- Logos Pulse Spiritual Growth Tracker (Supabase Edition)

**Document Version:** 3.0
**Date:** 2026-03-31
**Author:** Product Manager (BMAD)
**Status:** Draft
**Stakeholder:** Bhargavi Gunnam

---

## Table of Contents

1. [Overview & Objectives](#1-overview--objectives)
2. [Role-Based Access Control (RBAC) System](#2-role-based-access-control-rbac-system)
3. [Architecture Change: SQLite to Supabase](#3-architecture-change-sqlite-to-supabase)
4. [Supabase Setup & Configuration](#4-supabase-setup--configuration)
5. [Registration Flows](#5-registration-flows)
6. [Default Passwords & First-Login Policy](#6-default-passwords--first-login-policy)
7. [Login Flow](#7-login-flow)
8. [Password Reset via Supabase OTP](#8-password-reset-via-supabase-otp)
9. [Default Seed Data on Registration](#9-default-seed-data-on-registration)
10. [Multi-User Data Isolation (Hierarchical Row Level Security)](#10-multi-user-data-isolation-hierarchical-row-level-security)
11. [Database Schema](#11-database-schema)
12. [Migration Plan: SQLite to Supabase](#12-migration-plan-sqlite-to-supabase)
13. [Supabase Python Client Integration](#13-supabase-python-client-integration)
14. [New & Modified Files](#14-new--modified-files)
15. [Environment & Secrets Configuration](#15-environment--secrets-configuration)
16. [Functional Requirements](#16-functional-requirements)
17. [Non-Functional Requirements](#17-non-functional-requirements)
18. [UI/UX Considerations](#18-uiux-considerations)
19. [Supabase Free Tier Limits](#19-supabase-free-tier-limits)
20. [Out of Scope / Future Considerations](#20-out-of-scope--future-considerations)
21. [Success Metrics](#21-success-metrics)
22. [Implementation Phases](#22-implementation-phases)

---

## 1. Overview & Objectives

### 1.1 Background

Logos Pulse is a Streamlit-based web application for tracking daily spiritual disciplines including prayer time, Bible reading, sermon notes, weekly Bible reading assignments, streak tracking, WhatsApp report generation, and a prayer journal with categories. The application currently operates as a **single-user system with no authentication**. All data is stored in a local SQLite database (`data/tracker.db`) with no concept of user ownership.

### 1.2 Problem Statement

The application cannot serve multiple users. There is no way to identify who is logging an entry, no data separation between users, and no way for a pastor or leader to oversee the progress of individuals they are mentoring. The local SQLite database cannot be shared across deployments. Adding authentication, a cloud database, multi-user support, and a role-based hierarchy is the critical next step to make the application usable in a church or small-group context with proper oversight and accountability structures.

### 1.3 Objectives

| #  | Objective                                              | Measurable Outcome                                                                 |
|----|--------------------------------------------------------|------------------------------------------------------------------------------------|
| O1 | Migrate from SQLite to Supabase PostgreSQL             | All data persists in a cloud database accessible from any deployment               |
| O2 | Enable user registration with profile information      | Users can self-register as Prayer Warriors via Supabase Auth                       |
| O3 | Secure login with session management                   | Only authenticated users can access the app; sessions persist across page nav      |
| O4 | Isolate user data via hierarchical RLS                 | Each role sees only the data they are permitted to access, enforced at DB level    |
| O5 | Provide password reset via Supabase built-in OTP email | Users who forget their password can reset it without custom SMTP infrastructure    |
| O6 | Seed new accounts with default spiritual content       | Every new Prayer Warrior starts with default prayers, confessions, and declarations|
| O7 | Implement Role-Based Access Control (RBAC)             | Four roles (Admin, Bishop, Pastor, Prayer Warrior) with hierarchical oversight     |
| O8 | Provide role-specific dashboards                       | Admin Panel, Bishop Dashboard, Pastor Dashboard for oversight and management       |
| O9 | Support growth from 100 to 10,000+ users               | Architecture supports scaling without re-architecture                              |

### 1.4 Tech Stack (Current vs. Updated)

| Component          | Current                    | Updated                                      |
|--------------------|----------------------------|----------------------------------------------|
| Framework          | Streamlit (Python 3.13)    | Streamlit (Python 3.13) -- no change         |
| Database           | SQLite3 (WAL mode, local)  | Supabase PostgreSQL (cloud)                  |
| Authentication     | None                       | Supabase Auth (email/password)               |
| Authorization      | None                       | RBAC with hierarchical RLS policies          |
| OTP / Email        | None                       | Supabase built-in email OTP                  |
| Hosting            | Streamlit Community Cloud  | Streamlit Community Cloud -- no change       |
| Python DB client   | `sqlite3` (stdlib)         | `supabase-py` (Supabase Python SDK)          |
| Password hashing   | N/A                        | Supabase Auth (bcrypt, managed internally)   |
| Budget             | $0                         | $0 (Supabase free tier)                      |

### 1.5 Growth Plan

| Phase              | Timeline          | User Count | Tier Required      |
|--------------------|--------------------|------------|---------------------|
| Early adoption     | Now                | ~100       | Supabase Free       |
| Church network     | +3 months          | ~1,500     | Supabase Free/Pro   |
| Post-funding scale | +6-12 months       | 10,000+    | Supabase Pro         |

---

## 2. Role-Based Access Control (RBAC) System

### 2.1 Role Hierarchy

```
                    +------------------+
                    |     ADMIN        |
                    | (System Owner)   |
                    +--------+---------+
                             |
              +--------------+--------------+
              |                             |
     +--------+---------+         +--------+---------+
     |     BISHOP       |         |     BISHOP       |
     | (Regional Lead)  |         | (Regional Lead)  |
     +--------+---------+         +--------+---------+
              |                             |
     +--------+--------+          +--------+--------+
     |                  |          |                  |
+----+-----+     +-----+----+ +---+------+    +-----+----+
|  PASTOR  |     |  PASTOR  | |  PASTOR  |    |  PASTOR  |
| (Group)  |     | (Group)  | | (Group)  |    | (Group)  |
+----+-----+     +-----+----+ +---+------+    +-----+----+
     |                  |          |                  |
 +---+---+          +---+---+  +---+---+         +---+---+
 |  PW   |          |  PW   |  |  PW   |         |  PW   |
 |  PW   |          |  PW   |  |  PW   |         |  PW   |
 |  PW   |          |  PW   |  |  PW   |         |  PW   |
 +-------+          +-------+  +-------+         +-------+

 PW = Prayer Warrior (End User)
```

### 2.2 Role Definitions

| Role             | Created By                  | Default Password | Can Also Use App as User |
|------------------|-----------------------------|------------------|--------------------------|
| Admin            | Manually seeded in Supabase | `Raju@002`       | Yes                      |
| Bishop           | Admin only                  | `Bishop@123`     | Yes                      |
| Pastor           | Admin or Bishop             | `Pastor@123`     | Yes                      |
| Prayer Warrior   | Self-registration or Pastor | `Open@123`       | Yes (primary use case)   |

### 2.3 Role Permissions Matrix

| Permission                                    | Admin | Bishop | Pastor | Prayer Warrior |
|-----------------------------------------------|:-----:|:------:|:------:|:--------------:|
| Log own daily entries (prayer, Bible, sermons) |  Yes  |  Yes   |  Yes   |      Yes       |
| Manage own prayer journal / sermon notes       |  Yes  |  Yes   |  Yes   |      Yes       |
| View own streaks and stats                     |  Yes  |  Yes   |  Yes   |      Yes       |
| Generate WhatsApp report                       |  Yes  |  Yes   |  Yes   |      Yes       |
| View assigned members' data                    |  --   |  --    |  Yes   |      No        |
| Create/manage Prayer Warrior accounts          |  Yes  |  --    |  Yes   |      No        |
| Create weekly Bible reading assignments (group)|  Yes  |  --    |  Yes   |      No        |
| View group stats and streak leaderboard        |  --   |  --    |  Yes   |      No        |
| View all Pastors and PWs under them            |  --   |  Yes   |  --    |      No        |
| Create/manage Pastor accounts                  |  Yes  |  Yes   |  --    |      No        |
| View aggregated stats for their group          |  --   |  Yes   |  --    |      No        |
| Create/manage Bishop accounts                  |  Yes  |  --    |  --    |      No        |
| View ALL users' data and reports               |  Yes  |  --    |  --    |      No        |
| Manage system-wide settings and seed data      |  Yes  |  --    |  --    |      No        |
| View platform-wide analytics                   |  Yes  |  --    |  --    |      No        |
| Assign Bishops to regions/groups               |  Yes  |  --    |  --    |      No        |

### 2.4 Hierarchy Linkage Rules

- A **Prayer Warrior** is always linked to exactly one Pastor (via `pastor_id` in `user_profiles`).
- A **Pastor** is always linked to exactly one Bishop (via `bishop_id` in `user_profiles`).
- A **Bishop** is linked to the Admin (or operates independently under Admin oversight).
- Every role can also function as a regular user -- Admins, Bishops, and Pastors can log their own spiritual entries.
- `must_change_password` flag applies to ALL roles on first login.

### 2.5 Data Visibility Rules (Enforced via RLS)

| Role             | Can See                                                                      |
|------------------|-----------------------------------------------------------------------------|
| Admin            | All data across the entire system (all users, all roles)                    |
| Bishop           | Their own data + all Pastors under them + all Prayer Warriors under those Pastors |
| Pastor           | Their own data + all Prayer Warriors assigned to them                       |
| Prayer Warrior   | Only their own data                                                         |

A Bishop **cannot** see another Bishop's group. A Pastor **cannot** see another Pastor's members.

---

## 3. Architecture Change: SQLite to Supabase

### 3.1 Why Supabase

| Concern                    | SQLite Limitation                              | Supabase Solution                                     |
|----------------------------|------------------------------------------------|-------------------------------------------------------|
| Multi-user access          | Single-file, no concurrent multi-user writes   | PostgreSQL handles concurrent connections              |
| Authentication             | Must build from scratch (bcrypt, sessions)      | Built-in Auth with email/password, OTP, JWT            |
| Data isolation             | Must enforce in application code only           | Row Level Security (RLS) enforced at database level    |
| Role-based access          | No built-in support                            | Hierarchical RLS policies with role-aware functions    |
| Password reset / OTP       | Must build SMTP integration, OTP storage        | Built-in email templates, OTP flow, rate limiting      |
| Cloud deployment           | SQLite file is ephemeral on Streamlit Cloud     | Persistent cloud database, accessible from anywhere    |
| Scalability                | Single-file bottleneck                          | PostgreSQL scales to millions of rows                  |
| Cost                       | Free                                            | Free tier: 500 MB DB, 50,000 auth users, 2 GB bandwidth |

### 3.2 What Changes

| Layer                  | Before                                           | After                                                  |
|------------------------|--------------------------------------------------|--------------------------------------------------------|
| Database connection    | `sqlite3.connect("data/tracker.db")`             | `create_client(url, key)` via `supabase-py`            |
| Schema management      | `CREATE TABLE` in `db.py` SCHEMA_SQL             | SQL migrations in Supabase Dashboard / SQL Editor       |
| Auth                   | None                                             | `supabase.auth.sign_up()`, `supabase.auth.sign_in_with_password()` |
| Authorization          | None                                             | Role column in `user_profiles` + hierarchical RLS      |
| Data queries           | `conn.execute("SELECT ... WHERE ...")`           | `supabase.table("x").select("*").eq("col", val).execute()` |
| Data isolation         | None                                             | Hierarchical RLS: role-based visibility                |
| Password hashing       | Would need `bcrypt` library                      | Handled by Supabase Auth internally                    |
| OTP / password reset   | Would need `smtplib` + custom logic              | `supabase.auth.reset_password_email(email)`            |
| Session management     | `st.session_state` only                          | Supabase JWT session + `st.session_state` + role info  |

### 3.3 Architecture Diagram

```
+-------------------+        HTTPS        +------------------------+
|  Streamlit App    | <=================> |  Supabase Project      |
|  (Community Cloud)|                     |                        |
|                   |                     |  +------------------+  |
|  Home.py          |--- Auth API ------->|  | Supabase Auth    |  |
|  pages/*.py       |                     |  | (email/password) |  |
|                   |                     |  | (OTP email)      |  |
|  modules/auth.py  |--- Data API ------->|  +------------------+  |
|  modules/db.py    |  (PostgREST)        |                        |
|  modules/rbac.py  |                     |  +------------------+  |
|                   |                     |  | PostgreSQL DB    |  |
|  st.session_state |                     |  | + RLS Policies   |  |
|  (JWT token,      |                     |  | + Role Hierarchy |  |
|   user info,      |                     |  | + Helper Funcs   |  |
|   role)           |                     |  +------------------+  |
+-------------------+                     +------------------------+

Role-Specific Pages:
  - Admin Panel (pages/Admin_Panel.py)
  - Bishop Dashboard (pages/Bishop_Dashboard.py)
  - Pastor Dashboard (pages/Pastor_Dashboard.py)
  - Prayer Warrior pages (existing pages/*.py)
```

---

## 4. Supabase Setup & Configuration

### 4.1 Project Creation

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Project name: `logos-pulse` (or similar)
3. Region: Choose closest to primary user base
4. Note down: Project URL, `anon` public key, `service_role` secret key

### 4.2 Auth Configuration

In Supabase Dashboard > Authentication > Settings:

| Setting                        | Value                                               |
|--------------------------------|-----------------------------------------------------|
| Enable email provider          | Yes                                                 |
| Confirm email                  | Disabled (church context, simplicity)               |
| Enable email OTP               | Yes                                                 |
| Minimum password length        | 8                                                   |
| Password requirements          | Custom validation in application layer              |
| Mailer OTP expiration          | 600 seconds (10 minutes)                            |
| Rate limit (emails per hour)   | 3 (free tier limit -- sufficient for early stage)   |
| Site URL                       | Streamlit Cloud app URL                             |
| Redirect URLs                  | Streamlit Cloud app URL                             |

### 4.3 Email Templates

Customize in Supabase Dashboard > Authentication > Email Templates:

**Password Reset Email:**
```
Subject: Logos Pulse - Reset Your Password

Dear User,

Your one-time password (OTP) for resetting your Logos Pulse account is:

    {{ .Token }}

This code expires in 10 minutes. If you did not request this, please ignore this email.

Grace and peace,
Logos Pulse Team
```

### 4.4 Database Setup

Execute all table creation, RLS policy SQL, and helper functions (see Section 11) in the Supabase SQL Editor (Dashboard > SQL Editor > New Query).

### 4.5 Admin Account Seeding

On fresh system setup, manually create the Admin account in Supabase:

1. Create the Auth user via Supabase Admin API or Dashboard with the provided admin email and password `Raju@002`.
2. Insert a `user_profiles` row with `role = 'admin'` and `must_change_password = true` in user_metadata.
3. This is a one-time manual step -- no self-registration path for Admin.

```python
# One-time admin seed script (run locally with service_role key)
admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

user = admin_client.auth.admin.create_user({
    "email": "admin@logospulse.com",  # Provided during setup
    "password": "Raju@002",
    "email_confirm": True,
    "user_metadata": {
        "first_name": "System",
        "last_name": "Admin",
        "preferred_name": "Admin",
        "must_change_password": True
    }
})

admin_client.table("user_profiles").insert({
    "user_id": user.user.id,
    "role": "admin",
    "reporting_pastor": "",
    "prayer_benchmark_min": 60,
}).execute()
```

---

## 5. Registration Flows

The system has two distinct registration flows depending on the role being created.

### 5.1 Self-Registration (Prayer Warrior Only)

This is the public-facing registration form. It creates **only Prayer Warrior** accounts.

#### 5.1.1 Registration Fields

| Field                          | Type         | Required | Validation                       | Storage Location                |
|--------------------------------|--------------|----------|----------------------------------|---------------------------------|
| Email                          | Text input   | Yes      | Valid email format; unique       | Supabase Auth (email)           |
| Password                       | Password     | Yes      | Pre-filled "Open@123", hidden   | Supabase Auth (password hash)   |
| First Name                     | Text input   | Yes      | 1-50 chars, alphabetic          | Supabase Auth user_metadata     |
| Last Name                      | Text input   | Yes      | 1-50 chars, alphabetic          | Supabase Auth user_metadata     |
| Preferred Name                 | Text input   | No       | 1-30 chars                      | Supabase Auth user_metadata     |
| Select Your Pastor             | Dropdown     | Yes      | Must select from list of Pastors| `user_profiles.pastor_id`       |
| Church Membership Card ID      | Text input   | No       | e.g. TKT1694, alphanumeric      | `user_profiles.membership_card_id` |
| Prayer Time Benchmark (min)    | Number input | Yes      | 1-480, default 60               | `user_profiles` table           |

The "Select Your Pastor" dropdown is populated from the `user_profiles` table where `role = 'pastor'`, showing each Pastor's display name. The selected Pastor's `user_id` is stored as `pastor_id` on the Prayer Warrior's profile.

#### 5.1.2 Self-Registration Flow

```
[Landing Page] --> [Register Tab]
  1. User fills in all required fields (including selecting their Pastor)
  2. Client-side validation (email format, required fields, Pastor selected)
  3. Call Supabase Auth sign_up:
     supabase.auth.sign_up({
       "email": email,
       "password": "Open@123",
       "options": {
         "data": {
           "first_name": first_name,
           "last_name": last_name,
           "preferred_name": preferred_name or first_name,
           "must_change_password": True
         }
       }
     })
  4. On success (user created in Supabase Auth):
     a. Insert row into user_profiles table:
        (user_id, role='prayer_warrior', pastor_id, prayer_benchmark_min)
     b. Seed default prayer data (see Section 9)
     c. Show success message:
        "Account created! Please log in with your email and
         the temporary password: Open@123"
  5. Redirect to Login tab
```

### 5.2 Admin-Created Accounts (Bishop, Pastor, Prayer Warrior)

Admins, Bishops, and Pastors can create accounts for roles beneath them in the hierarchy. These accounts are created through the Admin Panel, Bishop Dashboard, or Pastor Dashboard -- never through self-registration.

#### 5.2.1 Who Can Create Whom

| Creator Role    | Can Create               | Via                     |
|-----------------|--------------------------|-------------------------|
| Admin           | Bishop, Pastor, PW       | Admin Panel             |
| Bishop          | Pastor                   | Bishop Dashboard        |
| Pastor          | Prayer Warrior           | Pastor Dashboard        |

#### 5.2.2 Admin-Created Account Fields

| Field                          | Type         | Required | Notes                                  |
|--------------------------------|--------------|----------|----------------------------------------|
| Email                          | Text input   | Yes      | Unique email for the new user          |
| First Name                     | Text input   | Yes      | 1-50 chars                             |
| Last Name                      | Text input   | Yes      | 1-50 chars                             |
| Role                           | Dropdown     | Yes      | Restricted to roles below the creator  |
| Assign to Bishop (for Pastors) | Dropdown     | Yes*     | Only when creating a Pastor            |
| Assign to Pastor (for PWs)     | Dropdown     | Yes*     | Only when creating a Prayer Warrior    |

*Conditional based on role being created.

#### 5.2.3 Admin-Created Account Flow

```
[Admin Panel / Bishop Dashboard / Pastor Dashboard]
  1. Creator fills in new user details
  2. System uses service_role key to create account:
     admin_client.auth.admin.create_user({
       "email": email,
       "password": <role-specific default password>,
       "email_confirm": True,
       "user_metadata": {
         "first_name": first_name,
         "last_name": last_name,
         "preferred_name": first_name,
         "must_change_password": True
       }
     })
  3. Insert user_profiles row:
     (user_id, role, pastor_id or bishop_id as applicable, created_by)
  4. Success message with role-specific default password
```

#### 5.2.4 Default Passwords by Role

| Role             | Default Password | Set By                                |
|------------------|------------------|---------------------------------------|
| Admin            | `Raju@002`       | Manual seed script                    |
| Bishop           | `Bishop@123`     | Admin Panel when creating Bishop      |
| Pastor           | `Pastor@123`     | Admin Panel / Bishop Dashboard        |
| Prayer Warrior   | `Open@123`       | Self-registration or Pastor Dashboard |

### 5.3 Registration Constraints

- No duplicate email addresses (enforced by Supabase Auth).
- Email is case-insensitive (Supabase Auth stores lowercase).
- All text inputs are stripped of leading/trailing whitespace.
- No email verification on registration (`confirm_email` disabled in Supabase Auth settings).
- Self-registration always creates role `prayer_warrior`.
- Admin, Bishop, and Pastor roles cannot be created via self-registration.

---

## 6. Default Passwords & First-Login Policy

### 6.1 Default Passwords

Each role has a specific default password (see Section 5.2.4). These passwords are hashed by Supabase Auth internally (bcrypt). The application never handles raw password hashing.

### 6.2 First-Login Mandatory Password Change

| Aspect            | Detail                                                                      |
|-------------------|-----------------------------------------------------------------------------|
| Trigger           | `must_change_password` flag is `True` in Supabase Auth `user_metadata`      |
| Applies to        | ALL roles (Admin, Bishop, Pastor, Prayer Warrior)                           |
| Flow              | After successful login, check `user_metadata.must_change_password`          |
|                   | If `True`, redirect to Change Password screen before any app access         |
| New Password Rules| Min 8 chars; at least one uppercase, one lowercase, one digit, one special  |
| Confirmation      | User must type new password twice; both must match                          |
| After Change      | Call `supabase.auth.update_user({"data": {"must_change_password": False}})` |
|                   | Then call `supabase.auth.update_user({"password": new_password})`           |
| Skip Prevention   | No navigation to any other page while `must_change_password` is `True`      |

### 6.3 Password Storage

- Supabase Auth handles all password hashing internally using bcrypt.
- The application never stores, logs, or accesses password hashes directly.
- Password updates go through `supabase.auth.update_user({"password": new_pw})`.

---

## 7. Login Flow

### 7.1 Authentication Flow

```
[App Entry Point (Home.py)]
  |
  +--> Is user authenticated in st.session_state?
       |
       YES --> Is Supabase session still valid?
       |       |
       |       YES --> Route to role-appropriate page
       |       NO  --> Clear session, show Login
       |
       NO --> Show Login/Register page
              |
              [Login Tab]
                1. Email + Password fields
                2. Call supabase.auth.sign_in_with_password({
                     "email": email,
                     "password": password
                   })
                3. On success:
                   a. Fetch user_profiles row to get role and hierarchy info
                   b. Store in st.session_state:
                      - session (Supabase session object)
                      - user_id (auth.uid())
                      - user_email
                      - preferred_name (from user_metadata)
                      - must_change_password (from user_metadata)
                      - role (from user_profiles: admin/bishop/pastor/prayer_warrior)
                      - access_token
                      - refresh_token
                      - login_time
                   c. Check must_change_password flag
                   d. If True  --> redirect to Change Password screen
                   e. If False --> redirect to role-appropriate landing page:
                      - Admin    --> Admin Panel
                      - Bishop   --> Bishop Dashboard
                      - Pastor   --> Pastor Dashboard
                      - PW       --> Dashboard (existing)
                4. On failure:
                   a. Show error: "Invalid email or password"
                   b. Supabase Auth handles rate limiting internally
```

### 7.2 Session State Keys

| Key                      | Type   | Description                                        |
|--------------------------|--------|----------------------------------------------------|
| `authenticated`          | bool   | Whether the user is logged in                      |
| `user_id`                | str    | Supabase Auth UUID (`auth.uid()`)                  |
| `user_email`             | str    | The logged-in user's email                         |
| `preferred_name`         | str    | Display name for greetings (from user_metadata)    |
| `must_change_password`   | bool   | Whether password change is required                |
| `role`                   | str    | User role: admin, bishop, pastor, prayer_warrior   |
| `access_token`           | str    | Supabase JWT access token                          |
| `refresh_token`          | str    | Supabase JWT refresh token                         |
| `login_time`             | str    | ISO timestamp of login                             |
| `supabase_client`        | object | Authenticated Supabase client instance             |

### 7.3 Session Persistence & Refresh

- Streamlit session state persists for the duration of a browser session.
- Supabase access tokens expire after 1 hour (default). On expiry, use the refresh token to get a new access token.
- Application-level session timeout: 24 hours. After that, `authenticated` is cleared and the user must log in again.
- Logout button available on all pages (in sidebar) that:
  1. Calls `supabase.auth.sign_out()`
  2. Clears all `st.session_state` keys

### 7.4 Auth Guard Pattern (Role-Aware)

Every page must include an authentication and authorization check at the top:

```python
# modules/auth.py
import streamlit as st
from datetime import datetime, timedelta

def require_login():
    """Auth guard -- call at the top of every page before any rendering."""
    if not st.session_state.get("authenticated"):
        st.switch_page("Home.py")
        st.stop()

    # Check session timeout (24 hours)
    login_time = st.session_state.get("login_time")
    if login_time:
        elapsed = datetime.now() - datetime.fromisoformat(login_time)
        if elapsed > timedelta(hours=24):
            _clear_session()
            st.switch_page("Home.py")
            st.stop()

    # Check mandatory password change
    if st.session_state.get("must_change_password"):
        st.switch_page("pages/Change_Password.py")
        st.stop()

def require_role(allowed_roles: list[str]):
    """Role-based access guard -- call after require_login()."""
    require_login()
    user_role = st.session_state.get("role", "")
    if user_role not in allowed_roles:
        st.error("You do not have permission to access this page.")
        st.stop()

def _clear_session():
    """Clear all auth-related session state."""
    auth_keys = [
        "authenticated", "user_id", "user_email", "preferred_name",
        "must_change_password", "role", "access_token", "refresh_token",
        "login_time", "supabase_client"
    ]
    for key in auth_keys:
        st.session_state.pop(key, None)
```

Usage in pages:

```python
# pages/0_Dashboard.py (all roles can access)
from modules.auth import require_login
require_login()

# pages/Admin_Panel.py (admin only)
from modules.auth import require_role
require_role(["admin"])

# pages/Bishop_Dashboard.py (admin and bishop)
from modules.auth import require_role
require_role(["admin", "bishop"])

# pages/Pastor_Dashboard.py (admin, bishop, and pastor)
from modules.auth import require_role
require_role(["admin", "bishop", "pastor"])
```

---

## 8. Password Reset via Supabase OTP

### 8.1 Flow

Supabase Auth provides built-in password reset via email OTP. No custom SMTP or OTP storage needed. This flow is identical for all roles.

```
[Login Page] --> [Forgot Password link]
  1. User enters their registered email
  2. Call supabase.auth.reset_password_email(email)
     - Supabase sends a 6-digit OTP to the email
     - OTP valid for 10 minutes (configured in Auth settings)
  3. User enters OTP on verification screen
  4. Call supabase.auth.verify_otp({
       "email": email,
       "token": otp_code,
       "type": "email"
     })
  5. On valid OTP:
     a. Supabase returns a valid session
     b. Fetch user role from user_profiles
     c. Reset password to role-specific default:
        - Admin: "Raju@002"
        - Bishop: "Bishop@123"
        - Pastor: "Pastor@123"
        - Prayer Warrior: "Open@123"
     d. Set must_change_password = True in user_metadata
     e. Show message: "Password has been reset. Please log in with your temporary password."
  6. On invalid/expired OTP:
     a. Show error, allow retry
     b. Supabase handles rate limiting (3 emails/hr on free tier)
```

### 8.2 OTP Details

| Aspect                | Detail                                                     |
|-----------------------|------------------------------------------------------------|
| Format                | 6-digit numeric (Supabase default)                         |
| Expiry                | 10 minutes (configured in Supabase Auth settings)          |
| Rate limiting         | 3 emails per hour (Supabase free tier)                     |
| Storage               | Managed entirely by Supabase (no app-side OTP table)       |
| Delivery              | Supabase built-in email (no custom SMTP required)          |
| Custom SMTP (future)  | Can configure custom SMTP in Supabase for higher limits    |

### 8.3 Advantages over Custom OTP

| Aspect                | Custom (v1.0 PRD)                    | Supabase Built-in (v3.0)             |
|-----------------------|--------------------------------------|---------------------------------------|
| OTP storage           | Custom `otp_requests` table          | Managed by Supabase                   |
| OTP hashing           | SHA-256, manual                      | Handled by Supabase                   |
| Email delivery        | Custom SMTP via `smtplib`            | Supabase built-in mailer              |
| Rate limiting         | Custom implementation                | Built into Supabase Auth              |
| SMTP credentials      | Must configure and secure            | Not needed (free tier)                |
| Code to maintain      | ~200 lines (otp.py)                  | ~10 lines (API calls)                |

---

## 9. Default Seed Data on Registration

Seed data behavior varies by role.

### 9.1 Seed Data by Role

| Role             | Seed Prayer Categories | Seed Prayers/Confessions/Declarations | Seed Settings |
|------------------|:---------------------:|:------------------------------------:|:-------------:|
| Admin            | No*                   | No*                                  | Yes           |
| Bishop           | No*                   | No*                                  | Yes           |
| Pastor           | No*                   | No*                                  | Yes           |
| Prayer Warrior   | Yes                   | Yes                                  | Yes           |

*Bishops, Pastors, and the Admin receive seed prayer data when they first access the app as a user (on first navigation to Prayer Journal). This is lazy-loaded rather than created at account creation time.

### 9.2 Default Prayer Categories (Prayer Warrior Registration)

| Category               | Icon  | Color   |
|------------------------|-------|---------|
| Personal               | (prayer hands) | #7B68EE |
| Finance & Breakthroughs| (money bag)    | #4CAF50 |
| Spouse                 | (heart)        | #E91E63 |
| Job & Career           | (briefcase)    | #FF9800 |

### 9.3 Default Prayer Entry

Seed one prayer entry in the "Personal" category:

| Field            | Content                                                                                     |
|------------------|---------------------------------------------------------------------------------------------|
| Title            | Daily Consecration                                                                          |
| Prayer Text      | Lord, I surrender this day to You. Guide my steps, guard my heart, and use me for Your glory. |
| Status           | ongoing                                                                                     |

### 9.4 Default Confessions

Seed as the `confessions` field on the default prayer entry:

> I am the righteousness of God in Christ Jesus (2 Cor 5:21). I am blessed and highly favored. No weapon formed against me shall prosper (Isaiah 54:17). I am the head and not the tail, above only and not beneath (Deut 28:13).

### 9.5 Default Declarations

Seed as the `declarations` field on the default prayer entry:

> I declare that this is the best season of my life. I declare that God's favor surrounds me like a shield. I declare that every plan of the enemy over my life is cancelled. I declare divine health, supernatural provision, and kingdom advancement in every area of my life.

### 9.6 Default Settings (All Roles)

| Setting Key             | Default Value                        | Source              |
|-------------------------|--------------------------------------|---------------------|
| greeting_name           | `preferred_name` or `first_name`     | Registration/creation form |
| pastor_name             | Assigned pastor name (PW only)       | Registration form   |
| default_prayer_minutes  | Value from form or 60                | Registration form   |
| omit_empty_sermon       | false                                | System default      |

These are stored in the `user_profiles` table and `app_settings` table (with `user_id` column).

### 9.7 Seed Data Implementation

```python
def seed_default_data(supabase_client, user_id: str, role: str, profile_data: dict):
    """Seed default data for a new user based on their role."""

    # 1. Insert default settings (all roles)
    preferred = profile_data.get("preferred_name") or profile_data["first_name"]
    settings = [
        {"user_id": user_id, "key": "greeting_name",          "value": preferred},
        {"user_id": user_id, "key": "default_prayer_minutes", "value": str(profile_data.get("prayer_benchmark_min", 60))},
        {"user_id": user_id, "key": "omit_empty_sermon",      "value": "false"},
    ]

    # Only Prayer Warriors have a pastor_name setting
    if role == "prayer_warrior" and profile_data.get("pastor_name"):
        settings.append({"user_id": user_id, "key": "pastor_name", "value": profile_data["pastor_name"]})

    supabase_client.table("app_settings").insert(settings).execute()

    # 2. Only seed prayer data for Prayer Warriors
    if role != "prayer_warrior":
        return

    # 3. Insert default prayer categories
    categories = [
        {"user_id": user_id, "name": "Personal",                "icon": "\U0001f64f", "color": "#7B68EE"},
        {"user_id": user_id, "name": "Finance & Breakthroughs", "icon": "\U0001f4b0", "color": "#4CAF50"},
        {"user_id": user_id, "name": "Spouse",                  "icon": "\u2764\ufe0f",  "color": "#E91E63"},
        {"user_id": user_id, "name": "Job & Career",            "icon": "\U0001f4bc", "color": "#FF9800"},
    ]
    result = supabase_client.table("prayer_categories").insert(categories).execute()

    # 4. Find the "Personal" category ID
    personal_cat = next(c for c in result.data if c["name"] == "Personal")

    # 5. Insert default prayer entry
    supabase_client.table("prayer_entries").insert({
        "user_id": user_id,
        "category_id": personal_cat["id"],
        "title": "Daily Consecration",
        "prayer_text": "Lord, I surrender this day to You. Guide my steps, guard my heart, and use me for Your glory.",
        "confessions": "I am the righteousness of God in Christ Jesus (2 Cor 5:21). I am blessed and highly favored. No weapon formed against me shall prosper (Isaiah 54:17). I am the head and not the tail, above only and not beneath (Deut 28:13).",
        "declarations": "I declare that this is the best season of my life. I declare that God's favor surrounds me like a shield. I declare that every plan of the enemy over my life is cancelled. I declare divine health, supernatural provision, and kingdom advancement in every area of my life.",
        "status": "ongoing",
    }).execute()
```

---

## 10. Multi-User Data Isolation (Hierarchical Row Level Security)

### 10.1 Strategy

All data tables include a `user_id` column (UUID) referencing `auth.users.id`. PostgreSQL Row Level Security (RLS) policies enforce **hierarchical** access: Admin sees all, Bishop sees their tree, Pastor sees their members, Prayer Warrior sees only self. This is enforced at the database level -- even if application code has a bug, RLS prevents unauthorized data access.

### 10.2 Helper Functions for RLS

These PostgreSQL functions are created in Supabase to support hierarchical RLS policies:

```sql
-- Get the role of the current authenticated user
CREATE OR REPLACE FUNCTION public.get_my_role()
RETURNS TEXT AS $$
  SELECT role FROM public.user_profiles WHERE user_id = auth.uid();
$$ LANGUAGE sql SECURITY DEFINER STABLE;

-- Check if the current user is an admin
CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.user_profiles
    WHERE user_id = auth.uid() AND role = 'admin'
  );
$$ LANGUAGE sql SECURITY DEFINER STABLE;

-- Check if target_user_id is in the current user's oversight tree
CREATE OR REPLACE FUNCTION public.can_view_user(target_user_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
  my_role TEXT;
  my_id UUID := auth.uid();
BEGIN
  -- Users can always see their own data
  IF target_user_id = my_id THEN
    RETURN TRUE;
  END IF;

  SELECT role INTO my_role FROM public.user_profiles WHERE user_id = my_id;

  -- Admin sees all
  IF my_role = 'admin' THEN
    RETURN TRUE;
  END IF;

  -- Bishop sees pastors under them and prayer warriors under those pastors
  IF my_role = 'bishop' THEN
    RETURN EXISTS (
      SELECT 1 FROM public.user_profiles
      WHERE user_id = target_user_id
        AND (bishop_id = my_id
             OR pastor_id IN (SELECT user_id FROM public.user_profiles WHERE bishop_id = my_id))
    );
  END IF;

  -- Pastor sees prayer warriors assigned to them
  IF my_role = 'pastor' THEN
    RETURN EXISTS (
      SELECT 1 FROM public.user_profiles
      WHERE user_id = target_user_id AND pastor_id = my_id
    );
  END IF;

  -- Prayer Warrior sees only self (handled above)
  RETURN FALSE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;
```

### 10.3 Hierarchical RLS Policy Pattern

Every data table uses this hierarchical pattern instead of the simple `auth.uid() = user_id` pattern:

```sql
-- Enable RLS on the table
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Users can see data based on role hierarchy
CREATE POLICY "Hierarchical read access"
    ON table_name FOR SELECT
    USING (public.can_view_user(user_id));

-- Users can only insert their own rows
CREATE POLICY "Users can insert own data"
    ON table_name FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can only update their own rows
CREATE POLICY "Users can update own data"
    ON table_name FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can only delete their own rows
CREATE POLICY "Users can delete own data"
    ON table_name FOR DELETE
    USING (auth.uid() = user_id);
```

### 10.4 Tables with Hierarchical RLS

| Table                | RLS Enabled | SELECT Policy                          | INSERT/UPDATE/DELETE Policy   |
|----------------------|-------------|----------------------------------------|-------------------------------|
| `user_profiles`      | Yes         | `can_view_user(user_id)` + special*    | Own data only                 |
| `daily_entries`      | Yes         | `can_view_user(user_id)`               | Own data only                 |
| `weekly_assignments` | Yes         | `can_view_user(user_id)`               | Own data only                 |
| `app_settings`       | Yes         | `auth.uid() = user_id`                 | Own data only                 |
| `sermon_notes`       | Yes         | `can_view_user(user_id)`               | Own data only                 |
| `prayer_categories`  | Yes         | `can_view_user(user_id)`               | Own data only                 |
| `prayer_entries`     | Yes         | `can_view_user(user_id)`               | Own data only                 |

*`user_profiles` has additional policies: Admin can INSERT for any user (account creation), Bishops can INSERT for Pastors under them, Pastors can INSERT for Prayer Warriors.

### 10.5 Special RLS for user_profiles (Account Management)

```sql
-- Admin can create profiles for any role
CREATE POLICY "Admin can insert any profile"
    ON user_profiles FOR INSERT
    WITH CHECK (
        public.is_admin()
        OR auth.uid() = user_id  -- Self-registration
    );

-- Bishops can update pastors under them (for assignment changes)
-- Pastors can update prayer warriors under them
CREATE POLICY "Hierarchical profile updates"
    ON user_profiles FOR UPDATE
    USING (
        auth.uid() = user_id  -- Own profile
        OR public.is_admin()   -- Admin can update anyone
        OR (public.get_my_role() = 'bishop' AND bishop_id = auth.uid())
        OR (public.get_my_role() = 'pastor' AND pastor_id = auth.uid())
    );
```

### 10.6 Query Pattern Change

With hierarchical RLS enabled, queries automatically return only the data the current user is permitted to see.

**Prayer Warrior querying their own entries:**
```python
# RLS automatically returns only their own rows
result = get_supabase_client() \
    .table("daily_entries") \
    .select("*") \
    .eq("date", entry_date) \
    .execute()
```

**Pastor querying their members' entries (for Pastor Dashboard):**
```python
# RLS automatically includes prayer warriors under this pastor
# The pastor sees their own entries + all their members' entries
result = get_supabase_client() \
    .table("daily_entries") \
    .select("*, user_profiles!inner(preferred_name, role)") \
    .eq("date", today) \
    .execute()
# Filter in application to show only members (exclude self if needed)
```

---

## 11. Database Schema

### 11.1 Role Enum Type

```sql
CREATE TYPE user_role AS ENUM ('admin', 'bishop', 'pastor', 'prayer_warrior');
```

### 11.2 User Profiles Table

```sql
CREATE TABLE user_profiles (
    id                   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id              UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role                 user_role NOT NULL DEFAULT 'prayer_warrior',
    pastor_id            UUID REFERENCES auth.users(id),  -- FK: prayer warriors -> their pastor
    bishop_id            UUID REFERENCES auth.users(id),  -- FK: pastors -> their bishop
    created_by           UUID REFERENCES auth.users(id),  -- Who created this account
    membership_card_id   TEXT DEFAULT NULL,                  -- Church membership card (e.g. TKT1694), optional, for future data import
    reporting_pastor     TEXT NOT NULL DEFAULT '',          -- Legacy: display name (kept for backward compat)
    prayer_benchmark_min INTEGER NOT NULL DEFAULT 60,
    region_or_group      TEXT DEFAULT '',                   -- For Bishop: region/group assignment
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id)
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_role ON user_profiles(role);
CREATE INDEX idx_user_profiles_pastor_id ON user_profiles(pastor_id);
CREATE INDEX idx_user_profiles_bishop_id ON user_profiles(bishop_id);

ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- SELECT: hierarchical visibility
CREATE POLICY "Hierarchical read access"
    ON user_profiles FOR SELECT
    USING (public.can_view_user(user_id));

-- INSERT: self-registration OR admin/bishop/pastor creating accounts
CREATE POLICY "Account creation"
    ON user_profiles FOR INSERT
    WITH CHECK (
        auth.uid() = user_id                    -- Self-registration
        OR public.is_admin()                     -- Admin creates any
        OR (public.get_my_role() = 'bishop'      -- Bishop creates pastors
            AND role = 'pastor')
        OR (public.get_my_role() = 'pastor'      -- Pastor creates prayer warriors
            AND role = 'prayer_warrior')
    );

-- UPDATE: own profile or hierarchical management
CREATE POLICY "Profile updates"
    ON user_profiles FOR UPDATE
    USING (
        auth.uid() = user_id
        OR public.is_admin()
        OR (public.get_my_role() = 'bishop' AND bishop_id = auth.uid())
        OR (public.get_my_role() = 'pastor' AND pastor_id = auth.uid())
    )
    WITH CHECK (
        auth.uid() = user_id
        OR public.is_admin()
        OR (public.get_my_role() = 'bishop' AND bishop_id = auth.uid())
        OR (public.get_my_role() = 'pastor' AND pastor_id = auth.uid())
    );
```

### 11.3 Daily Entries Table

```sql
CREATE TABLE daily_entries (
    id               BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id          UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    date             TEXT NOT NULL,
    prayer_minutes   INTEGER NOT NULL DEFAULT 60,
    bible_book       TEXT,
    chapters_read    JSONB,
    chapters_display TEXT,
    sermon_title     TEXT,
    sermon_speaker   TEXT,
    youtube_link     TEXT,
    report_copied    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, date)
);

CREATE INDEX idx_daily_entries_user_date ON daily_entries(user_id, date);

ALTER TABLE daily_entries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON daily_entries FOR SELECT
    USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own entries"
    ON daily_entries FOR INSERT
    WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own entries"
    ON daily_entries FOR UPDATE
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own entries"
    ON daily_entries FOR DELETE
    USING (auth.uid() = user_id);
```

### 11.4 Weekly Assignments Table

```sql
CREATE TABLE weekly_assignments (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    assigned_by     UUID REFERENCES auth.users(id),  -- Pastor who assigned (for group assignments)
    book            TEXT NOT NULL,
    start_chapter   INTEGER NOT NULL,
    end_chapter     INTEGER NOT NULL,
    total_chapters  INTEGER NOT NULL,
    week_start_date TEXT NOT NULL,
    week_end_date   TEXT NOT NULL,
    daily_breakdown JSONB NOT NULL,
    status          TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_weekly_assignments_user_status ON weekly_assignments(user_id, status);
CREATE INDEX idx_weekly_assignments_dates ON weekly_assignments(week_start_date, week_end_date);

ALTER TABLE weekly_assignments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON weekly_assignments FOR SELECT
    USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own assignments"
    ON weekly_assignments FOR INSERT
    WITH CHECK (auth.uid() = user_id);
-- Pastors can also insert assignments for their members
CREATE POLICY "Pastors can assign to members"
    ON weekly_assignments FOR INSERT
    WITH CHECK (
        public.get_my_role() IN ('admin', 'pastor')
        AND public.can_view_user(user_id)
    );
CREATE POLICY "Users can update own assignments"
    ON weekly_assignments FOR UPDATE
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own assignments"
    ON weekly_assignments FOR DELETE
    USING (auth.uid() = user_id);
```

### 11.5 App Settings Table

```sql
CREATE TABLE app_settings (
    id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id  UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    key      TEXT NOT NULL,
    value    TEXT NOT NULL,
    UNIQUE (user_id, key)
);

CREATE INDEX idx_app_settings_user ON app_settings(user_id);

ALTER TABLE app_settings ENABLE ROW LEVEL SECURITY;

-- Settings are private -- only the user can see their own settings
CREATE POLICY "Users can view own settings"
    ON app_settings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own settings"
    ON app_settings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own settings"
    ON app_settings FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own settings"
    ON app_settings FOR DELETE USING (auth.uid() = user_id);
```

### 11.6 Sermon Notes Table

```sql
CREATE TABLE sermon_notes (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id             UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title               TEXT NOT NULL,
    speaker             TEXT NOT NULL,
    sermon_date         TEXT NOT NULL,
    notes_text          TEXT,
    bible_references    JSONB,
    learnings           TEXT,
    key_takeaways       TEXT,
    additional_thoughts TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_sermon_notes_user_date ON sermon_notes(user_id, sermon_date);

ALTER TABLE sermon_notes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON sermon_notes FOR SELECT USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own sermon notes"
    ON sermon_notes FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own sermon notes"
    ON sermon_notes FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own sermon notes"
    ON sermon_notes FOR DELETE USING (auth.uid() = user_id);
```

### 11.7 Prayer Categories Table

```sql
CREATE TABLE prayer_categories (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name       TEXT NOT NULL,
    icon       TEXT DEFAULT '',
    color      TEXT DEFAULT '#7B68EE',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, name)
);

CREATE INDEX idx_prayer_categories_user ON prayer_categories(user_id);

ALTER TABLE prayer_categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON prayer_categories FOR SELECT USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own categories"
    ON prayer_categories FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own categories"
    ON prayer_categories FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own categories"
    ON prayer_categories FOR DELETE USING (auth.uid() = user_id);
```

### 11.8 Prayer Entries Table

```sql
CREATE TABLE prayer_entries (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id      UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    category_id  BIGINT NOT NULL REFERENCES prayer_categories(id) ON DELETE CASCADE,
    title        TEXT NOT NULL,
    prayer_text  TEXT,
    scriptures   JSONB,
    confessions  TEXT,
    declarations TEXT,
    status       TEXT NOT NULL DEFAULT 'ongoing',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_prayer_entries_user ON prayer_entries(user_id);
CREATE INDEX idx_prayer_entries_category ON prayer_entries(category_id);
CREATE INDEX idx_prayer_entries_status ON prayer_entries(status);

ALTER TABLE prayer_entries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON prayer_entries FOR SELECT USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own prayers"
    ON prayer_entries FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own prayers"
    ON prayer_entries FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own prayers"
    ON prayer_entries FOR DELETE USING (auth.uid() = user_id);
```

### 11.9 Entity Relationship Summary

```
auth.users (Supabase managed)
    |
    +--< user_profiles (1:1)
    |       - role (admin | bishop | pastor | prayer_warrior)
    |       - pastor_id --> auth.users (prayer_warrior -> pastor)
    |       - bishop_id --> auth.users (pastor -> bishop)
    |       - created_by --> auth.users (who created this account)
    |
    +--< daily_entries (1:many)
    |
    +--< weekly_assignments (1:many)
    |       - assigned_by --> auth.users (pastor who assigned)
    |
    +--< app_settings (1:many, keyed by user_id + key)
    |
    +--< sermon_notes (1:many)
    |
    +--< prayer_categories (1:many)
            |
            +--< prayer_entries (1:many)


Hierarchy Linkage:
    Admin
      +-- Bishop (bishop.created_by = admin.user_id)
            +-- Pastor (pastor.bishop_id = bishop.user_id)
                  +-- Prayer Warrior (pw.pastor_id = pastor.user_id)
```

---

## 12. Migration Plan: SQLite to Supabase

### 12.1 Migration Strategy

Since the app is pre-launch with minimal data, perform a **clean migration** (Option A).

### 12.2 Migration Steps

| Step | Action                                                                    | Tool                  |
|------|---------------------------------------------------------------------------|-----------------------|
| 1    | Export existing SQLite data to JSON backup                                | Existing `export_all_data()` |
| 2    | Create Supabase project and run role enum, helper functions, all CREATE TABLE + RLS SQL | Supabase SQL Editor   |
| 3    | Seed the Admin account (one-time script)                                 | Python script with service_role key |
| 4    | Create initial Bishop and Pastor accounts via Admin Panel                | Admin Panel UI        |
| 5    | Create a Supabase Auth user for the existing single user (if migrating data) | Supabase Admin API    |
| 6    | Import existing data into Supabase tables with the new user's UUID       | Python migration script |
| 7    | Replace `modules/db.py` with Supabase-backed implementation             | Code change           |
| 8    | Add `modules/auth.py` and `modules/rbac.py`                             | New files             |
| 9    | Update all pages with auth guard + role checks                           | Code change           |
| 10   | Test all functionality end-to-end with multiple roles                    | Manual + automated    |
| 11   | Remove SQLite file and `sqlite3` imports                                 | Cleanup               |

### 12.3 Data Migration Script (One-Time)

```python
"""
One-time migration script: SQLite -> Supabase
Run locally with service_role key.
"""
import json
import sqlite3
from supabase import create_client

SUPABASE_URL = "https://your-project.supabase.co"
SERVICE_ROLE_KEY = "your-service-role-key"
SQLITE_PATH = "data/tracker.db"
MIGRATION_USER_EMAIL = "existing-user@example.com"

def migrate():
    # 1. Connect to both databases
    admin = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row

    # 2. Create auth user for existing data owner (as Prayer Warrior)
    user = admin.auth.admin.create_user({
        "email": MIGRATION_USER_EMAIL,
        "password": "Open@123",
        "email_confirm": True,
        "user_metadata": {
            "first_name": "Existing",
            "last_name": "User",
            "preferred_name": "User",
            "must_change_password": True
        }
    })
    uid = user.user.id

    # 3. Create user_profiles row with role
    # Note: pastor_id should be set to an existing Pastor's user_id
    admin.table("user_profiles").insert({
        "user_id": uid,
        "role": "prayer_warrior",
        "pastor_id": "<pastor-user-id>",  # Set to their pastor
        "reporting_pastor": "Pastor Name",
        "prayer_benchmark_min": 60,
    }).execute()

    # 4. Migrate each table (add user_id = uid to every row)
    # ... (table-specific INSERT logic)

    conn.close()
    print(f"Migration complete. User ID: {uid}")
```

---

## 13. Supabase Python Client Integration

### 13.1 Client Initialization

```python
# modules/supabase_client.py
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_admin_client() -> Client:
    """Get a Supabase client with service_role key (for admin operations like creating accounts)."""
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["service_role_key"]
    )

def get_supabase_client() -> Client:
    """Get a Supabase client with the current user's session (for data operations)."""
    client = create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["anon_key"]
    )
    # Set the user's access token for RLS
    access_token = st.session_state.get("access_token")
    if access_token:
        client.postgrest.auth(access_token)
    return client
```

### 13.2 Role-Aware Data Access Module

```python
# modules/rbac.py
import streamlit as st
from modules.supabase_client import get_supabase_client, get_supabase_admin_client

def get_current_role() -> str:
    """Get the current user's role from session state."""
    return st.session_state.get("role", "prayer_warrior")

def create_user_account(email: str, first_name: str, last_name: str,
                        role: str, pastor_id: str = None, bishop_id: str = None):
    """Create a new user account (admin/bishop/pastor operation)."""
    default_passwords = {
        "admin": "Raju@002",
        "bishop": "Bishop@123",
        "pastor": "Pastor@123",
        "prayer_warrior": "Open@123",
    }

    admin_client = get_supabase_admin_client()

    # Create auth user
    user = admin_client.auth.admin.create_user({
        "email": email,
        "password": default_passwords[role],
        "email_confirm": True,
        "user_metadata": {
            "first_name": first_name,
            "last_name": last_name,
            "preferred_name": first_name,
            "must_change_password": True
        }
    })

    # Create profile
    profile = {
        "user_id": user.user.id,
        "role": role,
        "created_by": st.session_state.get("user_id"),
        "prayer_benchmark_min": 60,
        "reporting_pastor": "",
    }
    if pastor_id:
        profile["pastor_id"] = pastor_id
    if bishop_id:
        profile["bishop_id"] = bishop_id

    admin_client.table("user_profiles").insert(profile).execute()
    return user.user

def get_members_for_pastor(pastor_id: str = None):
    """Get all Prayer Warriors assigned to a pastor."""
    pid = pastor_id or st.session_state.get("user_id")
    client = get_supabase_client()
    result = client.table("user_profiles") \
        .select("*, auth_users:user_id(email)") \
        .eq("pastor_id", pid) \
        .eq("role", "prayer_warrior") \
        .execute()
    return result.data

def get_pastors_for_bishop(bishop_id: str = None):
    """Get all Pastors assigned to a bishop."""
    bid = bishop_id or st.session_state.get("user_id")
    client = get_supabase_client()
    result = client.table("user_profiles") \
        .select("*") \
        .eq("bishop_id", bid) \
        .eq("role", "pastor") \
        .execute()
    return result.data

def get_all_pastors():
    """Get list of all pastors (for registration dropdown)."""
    # Uses service_role to bypass RLS for public registration form
    admin_client = get_supabase_admin_client()
    result = admin_client.table("user_profiles") \
        .select("user_id, reporting_pastor") \
        .eq("role", "pastor") \
        .execute()
    return result.data
```

### 13.3 Replacing db.py Patterns

**Old pattern (SQLite):**
```python
def get_entry_by_date(entry_date: str) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM daily_entries WHERE date = ?", (entry_date,)
        ).fetchone()
        return dict(row) if row else None
```

**New pattern (Supabase with hierarchical RLS):**
```python
def get_entry_by_date(entry_date: str) -> Optional[dict]:
    result = get_supabase_client() \
        .table("daily_entries") \
        .select("*") \
        .eq("date", entry_date) \
        .execute()
    return result.data[0] if result.data else None
# RLS automatically scopes: PW sees own, Pastor sees own + members, etc.
```

### 13.4 Key API Mappings

| SQLite Operation                          | Supabase Equivalent                                                    |
|-------------------------------------------|------------------------------------------------------------------------|
| `conn.execute("SELECT ... WHERE ...")`    | `.table("x").select("*").eq("col", val).execute()`                     |
| `conn.execute("INSERT INTO ...")`         | `.table("x").insert({...}).execute()`                                  |
| `conn.execute("UPDATE ... WHERE ...")`    | `.table("x").update({...}).eq("id", val).execute()`                    |
| `conn.execute("DELETE ... WHERE ...")`    | `.table("x").delete().eq("id", val).execute()`                         |
| `INSERT OR REPLACE`                       | `.table("x").upsert({...}).execute()`                                  |
| `WHERE date BETWEEN ? AND ?`             | `.gte("date", start).lte("date", end)`                                 |
| `ORDER BY date DESC`                      | `.order("date", desc=True)`                                            |
| `LIMIT 1`                                | `.limit(1).single()`                                                    |

---

## 14. New & Modified Files

### 14.1 New Files

| File                                  | Purpose                                                              |
|---------------------------------------|----------------------------------------------------------------------|
| `modules/supabase_client.py`          | Supabase client initialization (admin + user-scoped)                 |
| `modules/auth.py`                     | `require_login()`, `require_role()`, `sign_in()`, `sign_up()`, `sign_out()`, `reset_password()` |
| `modules/rbac.py`                     | Role-based helper functions: `create_user_account()`, `get_members_for_pastor()`, `get_pastors_for_bishop()`, `get_all_pastors()` |
| `pages/Change_Password.py`            | Mandatory and voluntary password change page                         |
| `pages/Profile.py`                    | User profile view and edit page                                      |
| `pages/Admin_Panel.py`                | Admin: user CRUD (all roles), system settings, platform analytics    |
| `pages/Bishop_Dashboard.py`           | Bishop: pastor list, aggregate group stats, pastor creation          |
| `pages/Pastor_Dashboard.py`           | Pastor: member list, who logged today, streak leaderboard, assignments, member creation |
| `migrations/migrate_sqlite_to_supabase.py` | One-time migration script                                       |
| `migrations/seed_admin.py`            | One-time admin account seed script                                   |
| `supabase/schema.sql`                 | Full SQL schema including role enum, helper functions, tables, RLS    |

### 14.2 Files to Modify

| File                         | Changes                                                                  |
|------------------------------|--------------------------------------------------------------------------|
| `Home.py`                    | Add Login/Register UI with Supabase Auth; auth gate; role-based routing  |
| `modules/db.py`              | Complete rewrite: replace `sqlite3` with `supabase-py` calls             |
| `pages/0_Dashboard.py`       | Add `require_login()`; use `st.session_state` for greeting; role-aware sidebar |
| `pages/1_Daily_Entry.py`     | Add `require_login()`; pass `user_id` on inserts                         |
| `pages/2_Daily_Log.py`       | Add `require_login()`                                                    |
| `pages/3_Weekly_Assignment.py` | Add `require_login()`; Pastors can assign to members                   |
| `pages/4_Streaks_Stats.py`   | Add `require_login()`                                                    |
| `pages/5_Settings.py`        | Add `require_login()`; read/write settings via Supabase                  |
| `pages/6_Sermon_Notes.py`    | Add `require_login()`                                                    |
| `pages/7_Prayer_Journal.py`  | Add `require_login()`; lazy-load seed data for non-PW roles             |
| `modules/styles.py`          | Add login/register page styles; role-dashboard styles                    |
| `requirements.txt`           | Add `supabase` package; remove `bcrypt` (not needed)                     |

### 14.3 Files to Remove

| File                         | Reason                                                                   |
|------------------------------|--------------------------------------------------------------------------|
| `data/tracker.db`            | SQLite database no longer used (after migration)                         |
| `modules/otp.py` (if exists) | OTP handled by Supabase, no custom module needed                         |

---

## 15. Environment & Secrets Configuration

### 15.1 Streamlit Secrets

Store in `.streamlit/secrets.toml` (local) or Streamlit Cloud Secrets Manager (production):

```toml
[supabase]
url = "https://your-project-ref.supabase.co"
anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 15.2 Key Types and Usage

| Key                | Access Level       | Used For                                             | Exposed to Client? |
|--------------------|--------------------|------------------------------------------------------|---------------------|
| `anon_key`         | Public (row-level) | All authenticated data operations, auth sign-in      | Yes (safe with RLS) |
| `service_role_key` | Admin (bypass RLS) | Account creation (Admin/Bishop/Pastor), migration    | Never               |

### 15.3 Security Rules

- **Never** commit `.streamlit/secrets.toml` to version control.
- Add `.streamlit/secrets.toml` to `.gitignore`.
- The `service_role_key` bypasses RLS -- use only server-side for admin operations (account creation).
- The `anon_key` is safe to use client-side because hierarchical RLS policies protect data.
- Role information in `st.session_state` is for UI routing only; actual access control is enforced by RLS at the database level.

---

## 16. Functional Requirements

### FR-1: Self-Registration (Prayer Warrior)

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-1.1 | System shall provide a public registration form with fields: email, first name, last name, preferred name, select pastor (dropdown), church membership card ID (optional), prayer time benchmark | Must Have |
| FR-1.2 | Self-registration shall ONLY create accounts with role `prayer_warrior`                              | Must Have |
| FR-1.3 | System shall populate the Pastor dropdown from `user_profiles` where `role = 'pastor'`              | Must Have |
| FR-1.4 | System shall validate email uniqueness via Supabase Auth (case-insensitive)                          | Must Have |
| FR-1.5 | System shall validate email format using standard regex before API call                              | Must Have |
| FR-1.6 | System shall create the user via `supabase.auth.sign_up()` with password "Open@123"                  | Must Have |
| FR-1.7 | System shall set `must_change_password: true` in Supabase Auth `user_metadata`                       | Must Have |
| FR-1.8 | System shall store first_name, last_name, preferred_name in Supabase Auth `user_metadata`            | Must Have |
| FR-1.9 | System shall create a `user_profiles` row with role, pastor_id, membership_card_id, and prayer_benchmark_min | Must Have |
| FR-1.10 | Church Membership Card ID shall be optional, alphanumeric (e.g. TKT1694), for future cross-system data import | Should Have |
| FR-1.10| System shall seed default prayer categories, prayers, confessions, and declarations (Section 9)      | Must Have |
| FR-1.11| System shall display a success message with the default password after registration                  | Must Have |

### FR-2: Admin-Created Accounts

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-2.1 | Admin shall be able to create Bishop, Pastor, and Prayer Warrior accounts via the Admin Panel        | Must Have |
| FR-2.2 | Bishop shall be able to create Pastor accounts via the Bishop Dashboard                              | Must Have |
| FR-2.3 | Pastor shall be able to create Prayer Warrior accounts via the Pastor Dashboard                      | Must Have |
| FR-2.4 | Account creation shall use the service_role key via Admin API                                        | Must Have |
| FR-2.5 | Each created account shall have `must_change_password: true` and a role-specific default password    | Must Have |
| FR-2.6 | `created_by` field shall record who created each account                                             | Must Have |
| FR-2.7 | When creating a Pastor, the creator must assign them to a Bishop (dropdown)                          | Must Have |
| FR-2.8 | When creating a Prayer Warrior (admin-created), the creator must assign them to a Pastor (dropdown)  | Must Have |

### FR-3: Login

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-3.1 | System shall provide a login form with email and password fields                                     | Must Have |
| FR-3.2 | System shall authenticate via `supabase.auth.sign_in_with_password()`                                | Must Have |
| FR-3.3 | On login, system shall fetch user role from `user_profiles` and store in `st.session_state`          | Must Have |
| FR-3.4 | System shall store Supabase session (access_token, refresh_token, user info, role) in `st.session_state` | Must Have |
| FR-3.5 | System shall redirect to mandatory password change if `user_metadata.must_change_password` is true   | Must Have |
| FR-3.6 | After password change, system shall redirect to role-appropriate landing page                        | Must Have |
| FR-3.7 | System shall display a generic error message on invalid credentials                                  | Must Have |
| FR-3.8 | System shall provide a Logout button in the sidebar on all authenticated pages                       | Must Have |
| FR-3.9 | System shall call `supabase.auth.sign_out()` on logout and clear `st.session_state`                  | Must Have |
| FR-3.10| System shall expire application sessions after 24 hours                                              | Should Have |

### FR-4: Password Management

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-4.1 | System shall force password change on first login for ALL roles when `must_change_password` is true  | Must Have |
| FR-4.2 | New passwords must be min 8 chars with uppercase, lowercase, digit, and special character             | Must Have |
| FR-4.3 | System shall require password confirmation (enter twice, must match)                                 | Must Have |
| FR-4.4 | System shall update password via `supabase.auth.update_user({"password": new_pw})`                   | Must Have |
| FR-4.5 | System shall set `must_change_password: false` in user_metadata after successful change              | Must Have |
| FR-4.6 | System shall allow password change from the Profile page                                             | Should Have |

### FR-5: Password Reset (Supabase OTP)

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-5.1 | System shall provide a "Forgot Password" link on the login page                                      | Must Have |
| FR-5.2 | System shall call `supabase.auth.reset_password_email(email)` to send OTP                            | Must Have |
| FR-5.3 | System shall provide an OTP input form for verification                                              | Must Have |
| FR-5.4 | System shall verify OTP via `supabase.auth.verify_otp()`                                             | Must Have |
| FR-5.5 | On valid OTP, system shall reset password to the role-specific default and set `must_change_password: true` | Must Have |
| FR-5.6 | System shall show a user-friendly message if OTP is expired or invalid                               | Must Have |
| FR-5.7 | System shall display rate limit info: "OTP emails limited to 3 per hour"                             | Should Have |

### FR-6: Auth Guard & Role Guard

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-6.1 | Every page except Login/Register shall call `require_login()` before rendering                       | Must Have |
| FR-6.2 | Unauthenticated access to any page shall redirect to the login screen                                | Must Have |
| FR-6.3 | Auth guard shall validate session timeout (24 hours)                                                 | Must Have |
| FR-6.4 | Auth guard shall check `must_change_password` and redirect to Change Password if true                | Must Have |
| FR-6.5 | Role-restricted pages shall call `require_role(allowed_roles)` to enforce access                     | Must Have |
| FR-6.6 | Unauthorized role access shall show an error message and stop page rendering                         | Must Have |

### FR-7: Hierarchical Data Isolation

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-7.1 | All data tables shall include a `user_id` UUID column referencing `auth.users(id)`                   | Must Have |
| FR-7.2 | All data tables shall have hierarchical RLS policies using `can_view_user()` for SELECT              | Must Have |
| FR-7.3 | INSERT/UPDATE/DELETE operations shall be restricted to own data only (except admin operations)        | Must Have |
| FR-7.4 | Admin shall see all users' data across the entire system                                             | Must Have |
| FR-7.5 | Bishop shall see data for all Pastors and Prayer Warriors in their tree                              | Must Have |
| FR-7.6 | Pastor shall see data for all Prayer Warriors assigned to them                                       | Must Have |
| FR-7.7 | Prayer Warrior shall see only their own data                                                         | Must Have |
| FR-7.8 | A Bishop shall NOT see another Bishop's group                                                        | Must Have |
| FR-7.9 | A Pastor shall NOT see another Pastor's members                                                      | Must Have |
| FR-7.10| Export/import functionality shall operate on the authenticated user's visible data only               | Must Have |

### FR-8: Admin Panel

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-8.1 | Admin Panel shall be accessible only to users with role `admin`                                      | Must Have |
| FR-8.2 | Admin shall be able to create Bishop, Pastor, and Prayer Warrior accounts                            | Must Have |
| FR-8.3 | Admin shall be able to view and search all users across the system                                   | Must Have |
| FR-8.4 | Admin shall be able to edit user profiles (role, assignments, status)                                | Must Have |
| FR-8.5 | Admin shall see platform-wide analytics: total users, active streaks, engagement metrics             | Must Have |
| FR-8.6 | Admin shall be able to assign Bishops to regions/groups                                              | Should Have |
| FR-8.7 | Admin shall be able to manage system-wide default seed data (prayers, confessions, declarations)     | Should Have |
| FR-8.8 | Admin shall be able to reset any user's password to their role-specific default                      | Must Have |

### FR-9: Bishop Dashboard

| ID     | Requirement                                                                                          | Priority  |
|--------|------------------------------------------------------------------------------------------------------|-----------|
| FR-9.1 | Bishop Dashboard shall be accessible to users with role `admin` or `bishop`                          | Must Have |
| FR-9.2 | Bishop shall see a list of all Pastors assigned to them                                              | Must Have |
| FR-9.3 | Bishop shall see aggregated stats for their group (total members, active today, avg streaks)         | Must Have |
| FR-9.4 | Bishop shall be able to drill down into any Pastor's member list                                     | Should Have |
| FR-9.5 | Bishop shall be able to create new Pastor accounts under their oversight                             | Must Have |
| FR-9.6 | Bishop shall NOT see data from other Bishops' groups                                                 | Must Have |

### FR-10: Pastor Dashboard

| ID      | Requirement                                                                                         | Priority  |
|---------|-----------------------------------------------------------------------------------------------------|-----------|
| FR-10.1 | Pastor Dashboard shall be accessible to users with role `admin`, `bishop`, or `pastor`              | Must Have |
| FR-10.2 | Pastor shall see a list of all Prayer Warriors assigned to them                                     | Must Have |
| FR-10.3 | Pastor shall see who logged today (daily entry status for each member)                              | Must Have |
| FR-10.4 | Pastor shall see a streak leaderboard for their members                                             | Must Have |
| FR-10.5 | Pastor shall be able to create weekly Bible reading assignments for their entire group               | Must Have |
| FR-10.6 | Pastor shall be able to register new Prayer Warrior accounts                                        | Must Have |
| FR-10.7 | Pastor shall NOT see data from other Pastors' members                                               | Must Have |
| FR-10.8 | Pastor shall see which members have copied their WhatsApp report today                              | Should Have |

### FR-11: User Profile

| ID      | Requirement                                                                                         | Priority  |
|---------|-----------------------------------------------------------------------------------------------------|-----------|
| FR-11.1 | System shall provide a Profile page showing user information including their role                    | Must Have |
| FR-11.2 | Users shall be able to edit: first name, last name, preferred name (via `update_user` metadata)     | Must Have |
| FR-11.3 | Users shall be able to edit: prayer benchmark, membership card ID (via `user_profiles` table)         | Must Have |
| FR-11.4 | Email and role shall be displayed but not editable                                                   | Must Have |
| FR-11.5 | Prayer Warriors shall see their assigned Pastor's name                                              | Must Have |
| FR-11.6 | Pastors shall see their assigned Bishop's name                                                      | Should Have |
| FR-11.7 | Changes to preferred name shall immediately update `st.session_state["preferred_name"]`             | Must Have |

### FR-12: App Usage for All Roles

| ID      | Requirement                                                                                         | Priority  |
|---------|-----------------------------------------------------------------------------------------------------|-----------|
| FR-12.1 | All roles (Admin, Bishop, Pastor, PW) shall be able to log daily entries                            | Must Have |
| FR-12.2 | All roles shall be able to manage their own prayer journal and sermon notes                         | Must Have |
| FR-12.3 | All roles shall be able to view their own streaks and statistics                                    | Must Have |
| FR-12.4 | All roles shall be able to generate and copy their own WhatsApp report                              | Must Have |
| FR-12.5 | Sidebar navigation shall show role-appropriate pages (e.g., Admin Panel only for admin)             | Must Have |

---

## 17. Non-Functional Requirements

### NFR-1: Security

| ID      | Requirement                                                                            | Priority  |
|---------|----------------------------------------------------------------------------------------|-----------|
| NFR-1.1 | Passwords shall be hashed by Supabase Auth (bcrypt, managed internally)                | Must Have |
| NFR-1.2 | All data access shall be protected by hierarchical PostgreSQL RLS policies             | Must Have |
| NFR-1.3 | Supabase keys shall be stored in Streamlit secrets, never in source code               | Must Have |
| NFR-1.4 | The `service_role_key` shall never be exposed to the client or logged                  | Must Have |
| NFR-1.5 | All Supabase API calls use HTTPS (enforced by Supabase)                                | Must Have |
| NFR-1.6 | Error messages shall not reveal whether an email exists (use generic messages)          | Should Have |
| NFR-1.7 | `.streamlit/secrets.toml` shall be in `.gitignore`                                      | Must Have |
| NFR-1.8 | Role-based access control shall be enforced at both UI (guards) and DB (RLS) levels    | Must Have |
| NFR-1.9 | UI role checks are for convenience only; RLS is the authoritative access control       | Must Have |

### NFR-2: Performance

| ID      | Requirement                                                                            | Priority  |
|---------|----------------------------------------------------------------------------------------|-----------|
| NFR-2.1 | Login/registration API calls shall complete in under 3 seconds                         | Should Have |
| NFR-2.2 | Database queries shall use indexed columns (`user_id`, `date`, `role`, `pastor_id`, `bishop_id`) | Must Have |
| NFR-2.3 | Auth guard + role guard check shall add less than 100ms overhead per page load          | Should Have |
| NFR-2.4 | Supabase client shall be cached using `@st.cache_resource` where appropriate           | Should Have |
| NFR-2.5 | `can_view_user()` RLS function shall be optimized with proper indexing                 | Must Have |

### NFR-3: Scalability

| ID      | Requirement                                                                            | Priority  |
|---------|----------------------------------------------------------------------------------------|-----------|
| NFR-3.1 | Architecture shall support 100 concurrent users on Supabase free tier                  | Must Have |
| NFR-3.2 | Architecture shall scale to 10,000+ users with Supabase Pro tier (no code changes)     | Should Have |
| NFR-3.3 | No application-level caching of user data that would prevent scaling                   | Must Have |
| NFR-3.4 | Role hierarchy queries shall remain performant with 100+ bishops/pastors               | Should Have |

### NFR-4: Reliability

| ID      | Requirement                                                                            | Priority  |
|---------|----------------------------------------------------------------------------------------|-----------|
| NFR-4.1 | Failed Supabase API calls shall show clear error messages to the user                  | Must Have |
| NFR-4.2 | Network errors shall be caught with try/except and display retry options                | Must Have |
| NFR-4.3 | Session state loss (Streamlit rerun) shall gracefully redirect to login                | Must Have |

### NFR-5: Maintainability

| ID      | Requirement                                                                            | Priority  |
|---------|----------------------------------------------------------------------------------------|-----------|
| NFR-5.1 | Authentication logic shall be isolated in `modules/auth.py`                            | Must Have |
| NFR-5.2 | Role-based logic shall be isolated in `modules/rbac.py`                                | Must Have |
| NFR-5.3 | Supabase client init shall be isolated in `modules/supabase_client.py`                 | Must Have |
| NFR-5.4 | Database operations shall remain in `modules/db.py` (rewritten for Supabase)           | Must Have |
| NFR-5.5 | SQL schema (including RLS and helper functions) shall be version-controlled in `supabase/schema.sql` | Should Have |

---

## 18. UI/UX Considerations

### 18.1 Login/Register Page Layout

- Use `st.tabs(["Login", "Register"])` for a clean two-tab interface on the landing page.
- The Login tab shows: email input, password input, "Log In" button, "Forgot Password?" link.
- The Register tab shows: all self-registration fields (Prayer Warrior only) including the Pastor dropdown.
- A note on the Register tab: "This form creates a Prayer Warrior account. For Bishop or Pastor accounts, contact your administrator."
- Use `st.form()` for both login and registration to prevent premature reruns.
- Center the form with the Logos Pulse branding above it.

### 18.2 Mandatory Password Change Screen

- Full-page takeover (no sidebar navigation).
- Clear messaging: "Welcome! For your security, please set a new password."
- Password strength indicator (real-time feedback using `st.caption`).
- Two password fields + "Update Password" button inside `st.form()`.
- Applies to ALL roles on first login.

### 18.3 Forgot Password Flow

- Step 1: Email input form with "Send OTP" button.
- Step 2: OTP input form with note: "Check your email for a 6-digit code. It expires in 10 minutes."
- Step 3: Success message with redirect back to login.
- Use `st.session_state` to track the current step of the flow.
- Display rate limit notice: "Note: OTP emails are limited to 3 per hour."

### 18.4 Role-Aware Sidebar Navigation

**All Roles (common pages):**
- Dashboard (personal)
- Daily Entry
- Daily Log
- Weekly Assignment
- Streaks & Stats
- Sermon Notes
- Prayer Journal
- Settings
- Profile
- Logout

**Additional for Pastor:**
- Pastor Dashboard (with member management)

**Additional for Bishop:**
- Bishop Dashboard (with pastor management)

**Additional for Admin:**
- Admin Panel (with full user management and analytics)

The sidebar dynamically shows/hides role-specific links based on `st.session_state["role"]`.

### 18.5 Admin Panel UI

The Admin Panel (`pages/Admin_Panel.py`) layout:

```
+-------------------------------------------------+
|  Admin Panel                                    |
+-------------------------------------------------+
|  [User Management] [Analytics] [Settings]       |  (tabs)
|                                                 |
|  User Management Tab:                           |
|  +---------------------------------------------+
|  | [Create User] button                         |
|  | Search: [___________] Filter by Role: [___]  |
|  |                                              |
|  | User List (sortable table):                  |
|  | Name | Email | Role | Assigned To | Created  |
|  | ---- | ----- | ---- | ----------- | -------  |
|  | ...  | ...   | ...  | ...         | ...      |
|  +---------------------------------------------+
|                                                 |
|  Analytics Tab:                                 |
|  +---------------------------------------------+
|  | Total Users: XX  | Active Today: XX          |
|  | Bishops: XX | Pastors: XX | PWs: XX          |
|  | Avg Streak: XX days | Longest Streak: XX     |
|  | [Charts: daily active users over time]        |
|  +---------------------------------------------+
+-------------------------------------------------+
```

### 18.6 Bishop Dashboard UI

The Bishop Dashboard (`pages/Bishop_Dashboard.py`) layout:

```
+-------------------------------------------------+
|  Bishop Dashboard                               |
+-------------------------------------------------+
|  My Pastors (X total):                          |
|  +---------------------------------------------+
|  | Pastor Name | Members | Active Today | Avg   |
|  | ----------- | ------- | ------------ | Streak|
|  | Pastor A    | 15      | 12           | 8.2   |
|  | Pastor B    | 22      | 18           | 12.1  |
|  | [+ Create New Pastor]                        |
|  +---------------------------------------------+
|                                                 |
|  Group Summary:                                 |
|  Total Members: XX | Active Today: XX (XX%)     |
|  Top Streakers: [list]                          |
+-------------------------------------------------+
```

### 18.7 Pastor Dashboard UI

The Pastor Dashboard (`pages/Pastor_Dashboard.py`) layout:

```
+-------------------------------------------------+
|  Pastor Dashboard                               |
+-------------------------------------------------+
|  My Members (X total):                          |
|  [+ Register New Member]                        |
|  +---------------------------------------------+
|  | Name | Today | Streak | Last Entry | Report  |
|  | ---- | ----- | ------ | ---------- | ------  |
|  | John | Yes   | 15     | 2026-03-31 | Copied  |
|  | Mary | No    | 8      | 2026-03-30 | --      |
|  | ...                                           |
|  +---------------------------------------------+
|                                                 |
|  Streak Leaderboard:                            |
|  1. John - 15 days                              |
|  2. Sarah - 12 days                             |
|  3. Mary - 8 days                               |
|                                                 |
|  [Create Group Assignment] (Bible reading)      |
+-------------------------------------------------+
```

### 18.8 Dashboard Greeting Update

The personal dashboard reads `preferred_name` from `st.session_state["preferred_name"]` and shows a role badge:

```
Good morning, Pastor John!  [Pastor badge]
```

### 18.9 Styling

- Reuse existing `modules/styles.py` patterns (inject_styles, section_label, page_header).
- Login form should be centered on the page with the Logos Pulse branding above it.
- Use the existing color palette (purples, spiritually calming tones).
- Role badges use subtle color coding: Admin (red), Bishop (blue), Pastor (green), PW (purple).
- Dashboard pages for oversight roles use card-based layouts with metrics.

---

## 19. Supabase Free Tier Limits

### 19.1 Current Limits (as of 2026)

| Resource                    | Free Tier Limit         | Impact on Logos Pulse                          |
|-----------------------------|-------------------------|------------------------------------------------|
| Database size               | 500 MB                  | Sufficient for 10,000+ users with text data    |
| Auth users                  | 50,000 MAUs             | Well beyond growth plan                        |
| Auth emails (OTP/reset)     | 3 per hour              | Sufficient for early stage; monitor as grows   |
| API requests                | Unlimited (fair use)    | No concern for current scale                   |
| Bandwidth                   | 2 GB per month          | Sufficient for text-only API calls             |
| Edge functions              | 500,000 invocations     | Not used currently                             |
| Storage                     | 1 GB                    | Not used currently (no file uploads)           |
| Realtime connections        | 200 concurrent          | Not used currently                             |
| Projects                    | 2 active                | 1 project needed                               |
| Paused after inactivity     | 7 days                  | Must have regular usage or ping                |

### 19.2 When to Upgrade to Pro ($25/month)

| Trigger                                  | Action                                        |
|------------------------------------------|-----------------------------------------------|
| More than 3 password resets per hour     | Upgrade or configure custom SMTP              |
| Database exceeds 500 MB                  | Upgrade to Pro (8 GB)                         |
| Need daily backups                       | Upgrade to Pro (includes daily backups)       |
| Project pauses due to inactivity         | Upgrade to Pro (no auto-pause)                |
| More than 200 concurrent connections     | Upgrade to Pro                                |
| Hierarchical RLS functions cause perf issues | Upgrade to Pro (better compute)            |

### 19.3 Mitigation for Free Tier Email Limit

The 3 emails/hour limit applies to password reset OTPs. Mitigations:

1. Display clear messaging: "If you do not receive an email within a few minutes, please wait and try again."
2. Configure custom SMTP in Supabase (free) to bypass the 3/hr limit (e.g., Gmail app password, SendGrid free tier).
3. Track OTP request frequency in the app to pre-empt rate limit errors.

---

## 20. Out of Scope / Future Considerations

| Item                                     | Rationale                                                          |
|------------------------------------------|--------------------------------------------------------------------|
| OAuth/social login (Google, Facebook)    | Can be added via Supabase Auth providers later                     |
| Two-factor authentication (2FA)          | Overkill for current scale; Supabase supports TOTP if needed later |
| Email verification on registration       | Disabled for simplicity in church context; can enable in settings   |
| User avatar / profile picture            | Nice-to-have; would use Supabase Storage                          |
| Account deletion / GDPR compliance       | Address when app grows beyond personal/church use                  |
| Invitation-based registration            | Useful for closed groups; future feature                           |
| Push notifications / email reminders     | Separate feature; could use Supabase Edge Functions                |
| Supabase Realtime subscriptions          | Not needed for current use case; future for live updates           |
| Custom domain for Supabase               | Pro tier feature; not needed initially                             |
| Multi-church / tenant isolation           | Future: each church as a separate tenant with its own Admin        |
| Transferring members between Pastors     | V2 feature: UI for reassignment with data continuity               |
| Audit log for admin actions              | V2 feature: track who created/modified/deleted accounts            |
| Bulk user import (CSV)                   | V2 feature: import members from spreadsheet                       |

---

## 21. Success Metrics

| Metric                                   | Target                   | Measurement                                              |
|------------------------------------------|--------------------------|----------------------------------------------------------|
| Registration completion rate             | > 90%                    | Completed registrations / registration page views        |
| Login success rate                       | > 95% on first attempt   | Successful Supabase auth / total login attempts          |
| Password reset completion                | > 80%                    | Completed resets / OTP requests                          |
| Time to first entry after registration   | < 5 minutes              | First daily_entry timestamp - account creation timestamp |
| Data isolation (zero cross-user leaks)   | 0 incidents              | RLS policies + automated test suite                      |
| Role enforcement (zero unauthorized access) | 0 incidents           | RLS + role guard testing                                 |
| Pastor Dashboard daily usage             | > 70% of pastors         | Daily active pastors viewing dashboard / total pastors   |
| Session stability                        | < 1% unexpected drops    | User complaints / support requests                       |
| Supabase API error rate                  | < 0.1%                   | Error logs in application                                |
| Page load time with auth + role guard    | < 500ms added overhead   | Performance monitoring                                   |

---

## 22. Implementation Phases

### Phase 1: Supabase Setup + Auth Foundation + RBAC Schema

**Duration:** 1-2 weeks

| Task                                                      | Details                                          |
|-----------------------------------------------------------|--------------------------------------------------|
| Create Supabase project                                   | Project creation, note URL and keys              |
| Configure Supabase Auth settings                          | Email provider, disable confirm, set password rules |
| Create role enum type and helper functions                | `user_role` enum, `get_my_role()`, `is_admin()`, `can_view_user()` |
| Run full schema SQL in Supabase SQL Editor                | All CREATE TABLE + hierarchical RLS policies (Section 11) |
| Seed Admin account                                        | One-time script with `Raju@002` default password |
| Create `modules/supabase_client.py`                       | Client init with caching                         |
| Create `modules/auth.py`                                  | `require_login()`, `require_role()`, `sign_in()`, `sign_out()` |
| Create `modules/rbac.py`                                  | Role helpers, account creation, hierarchy queries |
| Configure Streamlit secrets                               | `.streamlit/secrets.toml` + Cloud secrets        |
| Add `supabase` to `requirements.txt`                      | Package dependency                               |

### Phase 2: Login, Self-Registration, Password Management

**Duration:** 1 week

| Task                                                      | Details                                          |
|-----------------------------------------------------------|--------------------------------------------------|
| Add Login/Register UI to `Home.py`                        | Tabs, forms, Supabase Auth calls                 |
| Build self-registration form (Prayer Warrior only)        | All fields per Section 5.1 including Pastor dropdown |
| Implement `sign_up()` with user_metadata and role         | Supabase Auth + user_profiles insert (role=prayer_warrior) |
| Implement seed data function (role-aware)                 | Default categories, prayers, settings (Section 9)|
| Build mandatory password change page                      | `pages/Change_Password.py` (all roles)           |
| Build forgot password flow                                | OTP request + verification + role-specific reset |
| Customize Supabase email templates                        | Password reset email (Section 4.3)               |
| Add auth guard to all existing pages                      | `require_login()` at top of every page           |
| Add role-aware sidebar navigation                         | Dynamic links based on user role                 |

### Phase 3: Admin Panel + Account Management

**Duration:** 1-2 weeks

| Task                                                      | Details                                          |
|-----------------------------------------------------------|--------------------------------------------------|
| Build Admin Panel page                                    | `pages/Admin_Panel.py` with user CRUD            |
| Implement Bishop account creation (Admin only)            | Default password `Bishop@123`, `must_change_password` |
| Implement Pastor account creation (Admin or Bishop)       | Default password `Pastor@123`, assign to Bishop   |
| Implement PW account creation (Admin or Pastor)           | Default password `Open@123`, assign to Pastor     |
| Build user search and filter in Admin Panel               | Search by name/email, filter by role              |
| Build platform analytics tab in Admin Panel               | Total users, active today, engagement metrics     |
| Implement admin password reset for any user               | Reset to role-specific default                   |

### Phase 4: Pastor Dashboard + Bishop Dashboard

**Duration:** 1-2 weeks

| Task                                                      | Details                                          |
|-----------------------------------------------------------|--------------------------------------------------|
| Build Pastor Dashboard page                               | `pages/Pastor_Dashboard.py`                      |
| Implement member list with today's status                 | Who logged today, streak info                    |
| Implement streak leaderboard for pastor's group           | Ranked list of members by streak                 |
| Implement group Bible reading assignment                  | Create assignments pushed to all members         |
| Implement WhatsApp report status tracking                 | Which members copied their report today          |
| Build Bishop Dashboard page                               | `pages/Bishop_Dashboard.py`                      |
| Implement pastor list with aggregate stats                | Members per pastor, active today, avg streak     |
| Implement drill-down from Bishop to Pastor view           | Click pastor to see their member details         |

### Phase 5: DB Rewrite + Profile + Integration

**Duration:** 1-2 weeks

| Task                                                      | Details                                          |
|-----------------------------------------------------------|--------------------------------------------------|
| Rewrite `modules/db.py` for Supabase                     | Replace all `sqlite3` calls with `supabase-py`   |
| Update all pages to use new `db.py` functions             | Pass `user_id` on inserts, rely on RLS for reads |
| Build Profile page (role-aware)                           | `pages/Profile.py` with role display, hierarchy info |
| Update Settings page                                      | Per-user settings via Supabase                   |
| Update sidebar with user info + role badge + logout       | Preferred name, role badge, role-specific links   |
| Implement lazy-load seed data for non-PW roles            | Seed prayer data on first Prayer Journal visit   |
| Remove SQLite dependencies                                | Delete `data/tracker.db`, clean imports           |
| Migrate existing SQLite data (if any)                     | One-time migration script                        |

### Phase 6: Hardening + Testing + Launch

**Duration:** 1 week

| Task                                                      | Details                                          |
|-----------------------------------------------------------|--------------------------------------------------|
| Error handling for all Supabase API calls                 | try/except with user-friendly messages           |
| Session refresh logic                                     | Handle expired JWT tokens                        |
| Rate limit messaging for OTP                              | Inform users of 3/hr limit                       |
| Security audit                                            | Verify hierarchical RLS, check for key exposure  |
| Multi-role testing                                        | Test all 4 roles end-to-end, cross-role isolation|
| Test hierarchy enforcement                                | Bishop cannot see other Bishop's data, etc.      |
| Performance testing                                       | Load test hierarchical RLS with realistic data   |
| Deploy to Streamlit Community Cloud                       | Configure Cloud secrets, verify production       |

---

## Appendix A: Dependencies

| Package    | Version   | Purpose                          | Replaces       |
|------------|-----------|----------------------------------|----------------|
| `supabase` | >= 2.0    | Supabase Python SDK (auth + DB)  | `sqlite3`      |

Removed dependencies (no longer needed):
- `bcrypt` -- password hashing handled by Supabase Auth internally
- `smtplib` config -- OTP email handled by Supabase built-in mailer

## Appendix B: Complete Supabase SQL Schema

The full SQL schema (role enum, helper functions, all tables, hierarchical RLS policies) is provided in Sections 10-11. To apply:

1. Open Supabase Dashboard > SQL Editor > New Query
2. Create the `user_role` enum type (Section 11.1)
3. Create the helper functions: `get_my_role()`, `is_admin()`, `can_view_user()` (Section 10.2)
4. Paste all CREATE TABLE statements from Sections 11.2 through 11.8
5. Run the query
6. Verify tables in Table Editor
7. Verify RLS policies in Authentication > Policies
8. Run the Admin seed script (Section 4.5)

## Appendix C: Supabase Auth User Metadata Schema

```json
{
  "first_name": "string",
  "last_name": "string",
  "preferred_name": "string",
  "must_change_password": "boolean"
}
```

This metadata is stored in `auth.users.raw_user_meta_data` (JSONB) and accessible via `supabase.auth.get_user()`.

Note: The `role` is stored in the `user_profiles` table (not in auth metadata) to allow RLS policies to reference it via SQL functions. This avoids the security risk of users modifying their own metadata to escalate privileges.

## Appendix D: Default Passwords Reference

| Role             | Default Password | When Used                                            |
|------------------|------------------|------------------------------------------------------|
| Admin            | `Raju@002`       | Initial seed, password reset                         |
| Bishop           | `Bishop@123`     | Account creation by Admin, password reset            |
| Pastor           | `Pastor@123`     | Account creation by Admin/Bishop, password reset     |
| Prayer Warrior   | `Open@123`       | Self-registration, account creation by Pastor, reset |

All default passwords require mandatory change on first login (`must_change_password: true`).

---

**END OF PRD**