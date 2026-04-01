# Risks & Limitations — Free Tier Constraints

> **Purpose**: Document all known risks, limitations, and technical debt introduced by operating on zero budget. These items should be addressed once funding is secured.
>
> **Last Updated**: 2026-04-01
> **Status**: Active — review quarterly or upon funding

---

## 1. Supabase Free Tier Limits

### 1.1 Database Storage — 500 MB cap

- **Risk**: At ~1,500 users with daily entries, sermon notes, and prayer journals, storage could approach the limit within 6-9 months.
- **Impact**: Database writes will fail once limit is reached. Users lose ability to log entries.
- **Estimate**: ~0.3 MB per active user/month (entries + notes + prayers). 1,500 users = ~450 MB/month of cumulative data.
- **Fix on funding**: Upgrade to Supabase Pro ($25/month, 8 GB storage) or migrate to dedicated PostgreSQL.

### 1.2 Auth Email Rate Limit — 3 emails/hour

- **Risk**: Supabase free tier limits auth emails (OTP, password reset, confirmation) to 3 per hour.
- **Impact**: If multiple users request password resets simultaneously, they'll be queued or dropped. Poor UX during onboarding spikes.
- **Trigger point**: Becomes a problem with 50+ simultaneous signups or password resets.
- **Fix on funding**: Configure custom SMTP provider (SendGrid free: 100 emails/day, or Resend: 3,000/month free). Supabase Pro also raises the limit.

### 1.3 Project Pausing — 1 week inactivity

- **Risk**: Supabase free projects pause after 7 days of no API requests.
- **Impact**: App goes down until project is manually resumed. All users locked out.
- **Mitigation (free)**: With 100+ active users, this won't trigger. As a safety net, set up a free cron ping (e.g., cron-job.org) to hit the Supabase health endpoint daily.
- **Fix on funding**: Supabase Pro projects never pause.

### 1.4 Bandwidth — 5 GB/month

- **Risk**: API requests and data transfers count toward bandwidth.
- **Impact**: At scale (10,000+ users), could exceed free tier.
- **Fix on funding**: Supabase Pro includes 250 GB bandwidth.

### 1.5 Realtime Connections — 200 concurrent

- **Risk**: Not currently using realtime, but if added later (live dashboards, notifications), 200 concurrent connection limit applies.
- **Fix on funding**: Upgrade tier or use polling instead of websockets.

---

## 2. Streamlit Community Cloud Limitations

### 2.1 No Persistent Filesystem

- **Risk**: Any file written to disk (uploads, generated reports, temp files) is lost on redeploy or restart.
- **Impact**: Cannot store user uploads locally. Bible text cache is lost on restart.
- **Mitigation (free)**: All data in Supabase. Bible API responses can be re-fetched.
- **Fix on funding**: Move to Render/Railway with persistent disk, or use Supabase Storage for file uploads.

### 2.2 Cold Starts & Performance

- **Risk**: Streamlit Community Cloud apps sleep after inactivity. Cold start takes 10-30 seconds.
- **Impact**: First user after idle period sees a loading spinner. Bad first impression for new signups.
- **Mitigation (free)**: Free cron ping to keep the app warm (cron-job.org).
- **Fix on funding**: Deploy on Render/Railway with always-on instances, or Streamlit Teams.

### 2.3 Single Instance — No Horizontal Scaling

- **Risk**: Streamlit Community Cloud runs one instance. All users share the same process.
- **Impact**: At 500+ concurrent users, performance degrades. Streamlit is not designed for high concurrency.
- **Trigger point**: ~100-200 concurrent users will feel sluggish.
- **Fix on funding**: Move to a container-based deployment (Railway, Render, or AWS ECS) with multiple instances behind a load balancer. Long-term: consider migrating frontend to React/Next.js.

### 2.4 No Custom Domain

- **Risk**: App URL is `appname.streamlit.app` — not brandable.
- **Impact**: Looks less professional for user-facing product.
- **Fix on funding**: Streamlit Teams ($250/month) or self-host with custom domain.

### 2.5 Resource Limits — 1 GB RAM

- **Risk**: Community Cloud apps get ~1 GB RAM.
- **Impact**: With many concurrent users loading Bible chapters and sermon data, memory pressure increases.
- **Fix on funding**: Self-host with higher resource allocation.

---

## 3. Security Risks

### 3.1 Default Password `Open@123`

- **Risk**: All new users start with the same known password. If a user doesn't change it immediately, anyone who knows their email can log in.
- **Impact**: Account takeover for users who skip the mandatory password change.
- **Mitigation (free)**: Enforce `must_change_password` flag — block all app access until password is changed. Show prominent warning.
- **Fix on funding**: Switch to email-based invitation flow where each user receives a unique signup link. Or implement email verification before account activation.

### 3.2 No Email Verification on Registration

- **Risk**: On free tier, Supabase email sending is limited. We may skip email verification to reduce email usage.
- **Impact**: Users can register with fake email addresses. Password reset won't work for them.
- **Mitigation (free)**: Admin manually creates accounts (controls who registers).
- **Fix on funding**: Enable Supabase email verification with custom SMTP.

### 3.3 Supabase Anon Key Exposed in Client

- **Risk**: The Supabase `anon` key is embedded in the Streamlit app. While RLS protects data, the key is technically visible.
- **Impact**: Low risk if RLS policies are correct. But a misconfigured policy could leak data.
- **Mitigation (free)**: Thorough RLS policy testing. Use service_role key only server-side.
- **Fix on funding**: Add a backend API layer between Streamlit and Supabase.

### 3.4 No Rate Limiting on Login

- **Risk**: No brute-force protection beyond Supabase's built-in (which is basic on free tier).
- **Impact**: Automated attacks could guess passwords, especially with the known default `Open@123`.
- **Fix on funding**: Implement account lockout after 5 failed attempts. Add CAPTCHA on login.

---

## 4. Data & Reliability Risks

### 4.1 No Automated Backups

- **Risk**: Supabase free tier has no automated daily backups.
- **Impact**: Data loss if Supabase has an incident or accidental deletion occurs.
- **Mitigation (free)**: Manual weekly export via Supabase dashboard or pg_dump. Keep the existing JSON export feature in Settings page.
- **Fix on funding**: Supabase Pro includes daily backups with point-in-time recovery.

### 4.2 Single Region Deployment

- **Risk**: Supabase free project is in one region. Users far from that region experience latency.
- **Impact**: Bible reader and data loading feel slow for geographically distant users.
- **Fix on funding**: Multi-region or edge deployment. CDN for static assets.

### 4.3 SQLite Migration Data Loss Risk

- **Risk**: Migrating existing SQLite data to Supabase is a one-time manual process. If done incorrectly, existing entries could be lost.
- **Impact**: Current user (Bhargavi) loses historical data.
- **Mitigation (free)**: Run JSON export backup before migration. Keep SQLite file as archive. Test migration on a staging Supabase project first.

---

## 5. Scalability Ceilings

### 5.1 Streamlit Framework Limits

- **Risk**: Streamlit is designed for data apps and dashboards, not production SaaS. It re-runs the entire page script on every interaction.
- **Impact**: At 10,000+ users, the single-threaded model becomes a bottleneck. No WebSocket-based real-time updates.
- **Trigger point**: ~500 concurrent users.
- **Fix on funding**: Phase 1 — optimize with caching (`st.cache_data`, `st.cache_resource`). Phase 2 — migrate frontend to Next.js/React with FastAPI backend.

### 5.2 Bible API Dependency

- **Risk**: Bible text is fetched from an external API on every chapter read. API could rate-limit, go down, or change.
- **Impact**: Bible reader tab fails. Core feature broken.
- **Mitigation (free)**: Cache responses in Supabase (bible_cache table). Serve cached text on API failure.
- **Fix on funding**: License a Bible text database and serve locally. Or use a paid Bible API with SLA.

---

## 6. UX & Product Risks

### 6.1 No Offline Support

- **Risk**: App requires internet. No PWA/offline capability.
- **Impact**: Users in low-connectivity areas (common in some ministry contexts) can't log entries.
- **Fix on funding**: Build a PWA version or native mobile app with offline sync.

### 6.2 No Push Notifications

- **Risk**: No way to remind users to log their daily entry.
- **Impact**: Streaks break, engagement drops.
- **Fix on funding**: Add push notifications via PWA service workers or integrate with WhatsApp Business API for reminders.

### 6.3 WhatsApp Report — Manual Copy

- **Risk**: Users must manually copy the report and paste into WhatsApp.
- **Impact**: Friction in the daily workflow. Some users may skip reporting.
- **Fix on funding**: WhatsApp Business API integration for one-tap send to pastor.

---

## Priority Matrix — What to Fix First on Funding

| Priority | Risk | Cost to Fix | Impact |
|----------|------|-------------|--------|
| P0 | Supabase Pro upgrade (pausing, backups, email) | $25/month | Reliability |
| P0 | Custom SMTP for auth emails | Free (SendGrid) or $20/mo | Onboarding |
| P1 | Email verification on registration | $0 (config change) | Security |
| P1 | Login rate limiting + account lockout | 2-3 days dev | Security |
| P1 | Automated backups | Included in Pro | Data safety |
| P2 | Custom domain | $10/year domain + hosting | Branding |
| P2 | Bible text caching in Supabase | 2-3 days dev | Reliability |
| P2 | Performance optimization (caching) | 3-5 days dev | UX |
| P3 | Move to always-on hosting | $7-25/month | Performance |
| P3 | Push notifications / reminders | 1-2 weeks dev | Engagement |
| P4 | Frontend migration (Next.js) | 2-3 months dev | Scale to 10K+ |
| P4 | Mobile app / PWA | 1-2 months dev | Offline access |

---

## Review Schedule

- **Monthly**: Check Supabase usage dashboard (storage, bandwidth, auth emails)
- **At 500 users**: Evaluate Supabase Pro upgrade
- **At 1,000 users**: Plan Streamlit performance optimization or hosting migration
- **On funding**: Execute P0 and P1 items immediately