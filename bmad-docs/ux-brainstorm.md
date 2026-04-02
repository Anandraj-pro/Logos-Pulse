# Logos Pulse -- UX Brainstorming Document

**Date:** 2026-03-31
**Context:** Post-launch review after initial deployment at https://logos-pulse.streamlit.app/
**Method:** Role-based gap analysis informed by real church ministry workflows (Bishop oversight of multiple churches in India, Pastor daily member management, Prayer Warrior daily mobile usage, Admin platform operations)

---

## 1. Findings by Role

### 1A. Bishop -- "I oversee 5-10 pastors across multiple churches"

**What works today:**
- Bishop Dashboard shows pastor list with today's logged/total members and engagement percentage
- Progress bars per pastor give a quick visual

**What is missing:**

| Gap | Why it matters |
|-----|----------------|
| **No historical trend data** | The Bishop Dashboard is today-only. A Bishop checking on Saturday has no idea how Monday-Thursday went. There is no weekly or monthly summary view. |
| **No pastor-level streaks or consistency metrics** | The Bishop can see member engagement for today but cannot tell which pastor's group has been declining over weeks. A pastor whose group drops from 80% to 30% over three weeks is invisible. |
| **No communication channel** | A Bishop cannot send a message, encouragement, or notice to all pastors from within the app. They must leave the app entirely and use WhatsApp or phone calls. |
| **No scheduled reports** | There is no weekly email digest or exportable PDF summary. The Bishop must open the app daily to stay informed. |
| **No drill-down into a pastor's group** | The Bishop Dashboard lists pastors but cannot expand to see individual members or their stats. The Bishop must switch to the Pastor Dashboard and select a pastor from the dropdown, which is a separate page and mental context switch. |
| **No alerts or flags** | If a pastor has not logged in for 5 days, or if a group's engagement drops below 40%, there is no automated alert. The Bishop must manually scan every pastor every day. |
| **No regional grouping** | Bishops in India often oversee churches across multiple cities. There is a `region_or_group` field displayed but no way to filter or group pastors by region. |
| **No pastor performance comparison** | No side-by-side chart showing Pastor A vs Pastor B group engagement over time. |

**Bishop's real daily workflow (what the app should support):**
1. Open app, see a summary card: "3 of 7 pastors have groups above 70% engagement this week"
2. See flagged items: "Pastor Ravi's group engagement dropped to 25% -- 3-week decline"
3. Tap a pastor to see their group details inline
4. Send a broadcast encouragement: "Great week, pastors! Keep pressing in."
5. Once a month, export a report for the church board meeting

---

### 1B. Pastor -- "I manage 20-50 prayer warriors daily"

**What works today:**
- Members tab with logged/not-logged filter and today's entry details
- Streak leaderboard with medals
- Group assignment creation with chapter breakdown preview
- Assignment history with cancel functionality

**What is missing:**

| Gap | Why it matters |
|-----|----------------|
| **No member history view** | A pastor can see if a member logged today, but cannot view that member's full history -- their prayer trend, chapters read over time, streak history, or journal entries. The pastor must ask the member directly. |
| **No private pastor notes per member** | Pastors in Indian churches often track pastoral care context: "Priya is going through a difficult season, needs extra encouragement." There is nowhere to store this. |
| **No reminder mechanism** | If 15 members have not logged by 6 PM, the pastor cannot send them a reminder from within the app. They must manually cross-reference with WhatsApp and message each person. |
| **No week-over-week comparison** | The members tab shows today only. A pastor cannot see: "Last week 35 of 40 logged, this week only 20 of 40 by Wednesday." |
| **No spiritual growth indicators** | Prayer minutes and chapters read are quantitative, but a pastor wants qualitative signals: Is prayer time increasing? Is the member reading more diverse books? Are they engaging with sermon notes? A "growth score" or trend arrow would help. |
| **No group announcements** | A pastor cannot post a message to their group within the app ("Tomorrow we fast collectively" or "Please read Psalm 91 this week as preparation for Sunday"). |
| **No prayer request visibility** | Prayer Warriors can create prayer journal entries, but their pastor cannot see them. A Prayer Warrior might want to share a request with their pastor for intercession. |
| **No follow-up tracking** | If a pastor reaches out to a struggling member, there is no way to log that follow-up or track whether the member responded. |
| **Assignment completion tracking is weak** | The pastor can see active vs completed assignments but cannot see which members completed each day's reading and which fell behind. |
| **No batch actions** | Cannot select multiple members to send a group message or tag them for follow-up. |

**Pastor's real daily workflow (what the app should support):**
1. **6:00 AM** -- Open app, see yesterday's summary: "32/45 logged, 3 new personal bests"
2. **6:05 AM** -- Check flagged members: "5 members have not logged in 3+ days"
3. **6:10 AM** -- Tap a member to see their 30-day trend, add a private note
4. **12:00 PM** -- Check mid-day: "Who has logged today so far?"
5. **6:00 PM** -- Send gentle reminder to members who haven't logged
6. **Sunday** -- Review weekly group stats, create next week's assignment
7. **Monthly** -- Review growth trends, identify members for recognition

---

### 1C. Prayer Warrior -- "I use this app every day on my phone"

**What works today:**
- Dashboard with daily verse, streaks, weekly progress, toolkit cards
- Daily Entry with Bible reader, entry logging, WhatsApp report
- Prayer Journal with categories, wizard, scripture/confession/declaration support
- Streaks & Stats with heatmap, Plotly charts
- Sermon Notes with search and Bible reference lookup

**What is missing:**

| Gap | Why it matters |
|-----|----------------|
| **Too many taps to log a daily entry** | The Daily Entry page has three tabs (Read Bible, Log Entry, Report). A Prayer Warrior who already read their Bible physically must navigate to the Log Entry tab, fill in prayer minutes, chapters, etc. This is 4-5 interactions minimum. A "Quick Log" button on the Dashboard would help. |
| **No fasting tracker** | Fasting is a core spiritual discipline in Indian churches. Many members fast 1-3 times per week. There is no way to log or track fasting days, types (full, partial, Daniel fast), or fasting streaks. |
| **No personal goals** | The only goal is the prayer benchmark (minutes). Members cannot set goals like "Read through the New Testament in 90 days" or "Pray for 30 minutes every morning this month." |
| **No encouragement or feedback loop** | The app tracks but does not encourage. There are no milestone celebrations beyond `st.balloons()` at exact streak numbers (7, 30, 50, 100, 365). No "You've prayed 100 hours total!" or "Your longest reading streak ever!" moments. |
| **No way to share prayer requests with pastor** | The Prayer Journal is fully private. A member who wants their pastor to pray for them must communicate outside the app. |
| **Group comparison is invisible** | The member cannot see where they stand relative to their group (anonymized). "You're in the top 20% of your group this week" would be motivating without being judgmental. |
| **Bible reader UX on mobile** | The Bible reader fetches from an API and displays in-app. On small screens, selecting book + chapter + scrolling through long chapters can be cumbersome. No bookmark, highlight, or font size control. |
| **WhatsApp report is copy-only** | The report is generated and copied to clipboard. There is no deep link to WhatsApp or option to share directly. On mobile, this requires switching apps and pasting, which is functional but not seamless. |
| **No offline capability** | Streamlit apps require internet. In rural India, connectivity can be intermittent. There is no PWA mode, no service worker, no local caching of the Bible text. |
| **No devotional content** | The daily verse on the dashboard cycles through 7 hardcoded verses. This is static and repetitive. Members who log daily will see the same verses every week. |
| **No community/social features** | No way to see what others are reading, no shared prayer wall, no group devotional discussions. |
| **No testimonies section** | Answered prayers in the Prayer Journal are private. A testimony-sharing feature where members can celebrate answered prayers with their group would build community. |
| **Empty states are functional but not warm** | The empty states use icons and text but could be more encouraging: "Start your first entry today -- your journey begins with one step." |
| **No dark mode** | Many members pray early morning or late night. A dark mode would reduce eye strain. |

**Prayer Warrior's real daily workflow (what the app should support):**
1. **5:30 AM** -- Open app, see today's verse (fresh, not recycled weekly)
2. **5:31 AM** -- Quick-log: "Prayed 45 min, read 3 chapters of John" (two taps max)
3. **5:32 AM** -- See encouragement: "3-day streak! Keep going!"
4. **5:33 AM** -- Open Bible reader, continue from where they left off (bookmark)
5. **6:00 AM** -- Generate WhatsApp report, share with pastor group
6. **Evening** -- Add to prayer journal, mark yesterday's prayer as answered
7. **Sunday** -- Review weekly stats, feel motivated by progress

---

### 1D. Admin -- "I manage the entire platform"

**What works today:**
- User CRUD with role filter and search
- Account creation (one at a time)
- Analytics tab (basic platform stats)
- Password reset functionality

**What is missing:**

| Gap | Why it matters |
|-----|----------------|
| **No bulk account creation** | Onboarding a new church with 50 members requires creating 50 accounts one by one. No CSV upload, no batch creation. |
| **No system health dashboard** | No visibility into API response times, Supabase usage, error rates, or active sessions. |
| **No audit log** | No record of who did what -- who reset passwords, who deleted accounts, who changed roles. |
| **No seed data management** | The `seed_user_data` function exists but there is no UI to manage default prayer categories, default settings, or template data. |
| **No church/organization management** | The app assumes a single church. If deployed across multiple churches, there is no multi-tenancy support or church-level configuration. |
| **No backup/restore UI** | Data export exists in Settings for individual users, but there is no platform-wide backup or restore mechanism accessible to the admin. |
| **No email/notification management** | Cannot configure automated emails, reminder schedules, or notification preferences at the platform level. |
| **Role assignment is manual** | Assigning a pastor to a bishop or a member to a pastor requires editing individual profiles. No drag-and-drop org chart or visual hierarchy management. |
| **No usage analytics** | Cannot see daily active users, feature usage (which pages are visited most), or retention metrics. |
| **No announcement system** | Cannot post a platform-wide announcement ("App maintenance Saturday 2 AM" or "New feature: Fasting Tracker is live!"). |

---

### 1E. UX and Design Gaps (Cross-Role)

| Gap | Severity | Details |
|-----|----------|---------|
| **Login experience** | Medium | Functional but plain. No "Remember me" checkbox. No social login. The "Forgot Password" tab exists but its implementation should be verified. |
| **Onboarding for new users** | High | A brand-new Prayer Warrior who registers sees the Dashboard immediately with zeros everywhere. No guided tour, no "Complete your first entry" prompt, no progress steps. |
| **Navigation on mobile** | Medium | Sidebar navigation works but requires hamburger menu tap on mobile. 9+ nav items in the sidebar may overwhelm. No bottom tab bar pattern common in mobile apps. |
| **Empty states** | Medium | Empty states exist (good) but are informational, not actionable. "No entries yet" should have a button: "Log your first entry." |
| **Personalization** | Medium | The dashboard greeting uses `greeting_name` but the overall experience feels one-size-fits-all. No customizable dashboard, no chosen accent color, no avatar. |
| **Notification/reminders** | High | Zero push notifications, zero email reminders, zero in-app nudges. For a daily habit app, this is a critical gap. Habit apps live and die by reminders. |
| **Milestone celebrations** | Low | Only `st.balloons()` at exact streak milestones. No persistent badges, no shareable milestone cards, no "congrats" messages. |
| **Loading states** | Low | Some pages fetch multiple Supabase queries synchronously. No skeleton loaders or progress indicators during multi-query page loads. |
| **Accessibility** | Medium | Heavy use of `unsafe_allow_html` with custom styling. Screen reader support is likely poor. Color contrast should be audited. |
| **Data visualization** | Low | Stats page has good Plotly charts but they are not interactive on mobile (hard to tap data points). |

---

## 2. Quick Wins (Under 1 Day Each)

| # | Feature | Effort | Impact | Role |
|---|---------|--------|--------|------|
| Q1 | **Quick Log button on Dashboard** -- Single button that opens a modal/expander for fast entry (prayer minutes + chapters + submit). Skip the full Daily Entry page for returning users. | 3 hrs | High | Prayer Warrior |
| Q2 | **Expand daily verse pool to 365** -- Replace the 7 hardcoded verses with a JSON file of 365 verses (one per day of year). Many free Bible verse datasets exist. | 2 hrs | Medium | Prayer Warrior |
| Q3 | **Actionable empty states** -- Add "Log your first entry" button to empty Dashboard, "Create your first prayer" to empty Prayer Journal, etc. | 2 hrs | Medium | All |
| Q4 | **"Continue reading" bookmark** -- Store last-read book + chapter in session/DB. Show "Continue: John 4" link on Dashboard and Bible reader. | 3 hrs | High | Prayer Warrior |
| Q5 | **Yesterday's summary on Dashboard** -- Small card below the hero showing "Yesterday: 45 min prayer, 3 chapters, streak +1". Gives instant context. | 2 hrs | Medium | Prayer Warrior |
| Q6 | **Pastor: "Not Logged" count badge** -- Show a red badge on the Pastor Dashboard nav item with the count of members who have not logged today. Uses existing data. | 1 hr | Medium | Pastor |
| Q7 | **Bishop: Inline pastor drill-down** -- Add an expander on each pastor card in Bishop Dashboard to show their members list inline (reuse Pastor Dashboard member query). | 3 hrs | High | Bishop |
| Q8 | **Add fasting checkbox to Daily Entry** -- Simple boolean field: "Did you fast today?" with type dropdown (Full, Partial, Daniel). Minimal schema change. | 3 hrs | High | Prayer Warrior |
| Q9 | **Streak milestone messages** -- Show encouraging messages at milestones beyond just balloons. "7 days! You're building a habit." / "30 days! Your discipline is bearing fruit." | 1 hr | Medium | Prayer Warrior |
| Q10 | **Dark mode toggle** -- Streamlit supports `st.set_page_config(theme=...)` natively. Add toggle in Settings. | 2 hrs | Medium | All |

---

## 3. Medium Features (2-5 Days Each)

| # | Feature | Effort | Impact | Role |
|---|---------|--------|--------|------|
| M1 | **Pastor Notes per Member** -- New `pastor_notes` table. In Pastor Dashboard, each member card gets a "Notes" expander where the pastor can add timestamped private notes. | 3 days | High | Pastor |
| M2 | **Member History View** -- Clicking a member in Pastor Dashboard opens a detail view: 30-day heatmap, prayer trend chart, chapter reading history, current streak, and personal bests. Reuses existing Streaks & Stats components. | 4 days | High | Pastor, Bishop |
| M3 | **Bulk Account Creation** -- CSV upload in Admin Panel. Columns: email, first_name, last_name, role, pastor_email. Validates, creates accounts, assigns to pastors. | 3 days | High | Admin |
| M4 | **Weekly Digest (Bishop + Pastor)** -- Scheduled Supabase Edge Function that runs every Monday at 6 AM. Sends email summary to each Bishop (pastor group stats for the past week) and each Pastor (member engagement summary). | 5 days | High | Bishop, Pastor |
| M5 | **Prayer Request Sharing** -- Add "Share with Pastor" toggle on individual prayers in Prayer Journal. Creates entry in new `shared_prayers` table. Pastor sees shared prayers in a new tab on their dashboard. | 4 days | High | Prayer Warrior, Pastor |
| M6 | **In-App Announcements** -- Admin and Pastor can post announcements. Members see a banner or notification bell on Dashboard. Announcements are dismissable and time-bound. | 3 days | Medium | Admin, Pastor, All |
| M7 | **Fasting Tracker (Full)** -- Dedicated page or section: log fasting days, set fasting goals (e.g., "Fast every Wednesday"), view fasting calendar, fasting streaks. Include in WhatsApp report. | 4 days | High | Prayer Warrior |
| M8 | **Personal Goals** -- Allow users to create custom goals: "Read New Testament in 90 days", "Pray 60 min daily for 30 days". Track progress against goal with visual progress bar on Dashboard. | 5 days | Medium | Prayer Warrior |
| M9 | **Group Engagement Chart (Bishop)** -- Weekly engagement trend chart per pastor's group over the last 12 weeks. Line chart showing percentage of members logging daily. Allows Bishop to spot declining groups. | 3 days | High | Bishop |
| M10 | **Audit Log** -- Log all admin actions (account creation, deletion, role change, password reset) with timestamp, actor, and target. Display in Admin Panel. | 2 days | Medium | Admin |

---

## 4. Large Features (1-2 Weeks Each)

| # | Feature | Effort | Impact | Role |
|---|---------|--------|--------|------|
| L1 | **Notification/Reminder System** -- Email and/or WhatsApp reminders. Configurable per user: "Remind me at 7 AM if I haven't logged by then." Pastor can trigger "gentle nudge" to members who haven't logged. Requires external service (SendGrid, Twilio, or Supabase Edge Functions + cron). | 2 weeks | Critical | All |
| L2 | **Guided Onboarding Flow** -- First-time user sees a 4-step wizard: Welcome > Set prayer goal > Make first entry > See your dashboard. Progress dots. Skippable. Stores onboarding completion flag. | 1 week | High | Prayer Warrior |
| L3 | **Testimony / Praise Wall** -- Members can share answered prayers as testimonies (anonymized or named). Group-visible feed. Reactions (pray, amen, hallelujah). Moderated by pastor. Builds community. | 1.5 weeks | Medium | Prayer Warrior, Pastor |
| L4 | **Spiritual Growth Score** -- Composite metric combining: consistency (streak), quantity (prayer minutes, chapters), diversity (different books read, sermon notes created, prayers logged). Displayed as a simple score or level system (Seed > Sprout > Tree > Forest). Non-judgmental framing. | 1.5 weeks | Medium | Prayer Warrior, Pastor |
| L5 | **Multi-Church / Multi-Tenancy** -- Organization-level isolation. Each church has its own pastors, members, and settings. A super-admin can manage multiple churches. Critical for scaling beyond one church. | 2 weeks | High | Admin |
| L6 | **Advanced Bible Reader** -- Font size controls, bookmarks, highlights, note-taking in margins. Reading plans (not just weekly assignments but structured 90-day plans). Offline caching of previously read chapters. | 2 weeks | Medium | Prayer Warrior |
| L7 | **WhatsApp Bot Integration** -- Members can log entries via WhatsApp message ("Prayed 30 min, read John 3"). Bot parses and creates entry. Removes app friction entirely for low-tech users. Extremely valuable in Indian church context where WhatsApp is universal. | 2 weeks | High | Prayer Warrior |
| L8 | **Pastor Care Workflow** -- Full follow-up tracking: Pastor flags a member for care > adds context note > logs outreach attempts > tracks resolution. Dashboard widget: "3 members need follow-up this week." | 1.5 weeks | High | Pastor |

---

## 5. Future Vision (Post-Funding)

These features assume a dedicated team, backend infrastructure budget, and potentially a mobile-native companion app.

1. **Native Mobile App (React Native / Flutter)** -- Push notifications, offline mode, camera for sermon note photos, biometric login. Streamlit web version continues as the admin/pastor portal.

2. **AI-Powered Devotional Content** -- Personalized daily devotionals based on what the member has been reading and praying about. "You've been reading about faith this week -- here's a devotion on Hebrews 11."

3. **Voice Prayer Logging** -- Member taps "Record Prayer" and prays aloud. Transcription captures key themes. Auto-tags prayer categories. Particularly valuable for older members uncomfortable with typing.

4. **Church Service Integration** -- QR code at church service logs attendance. Sermon notes auto-populate with sermon title and scripture references from the church's worship planning tool.

5. **Inter-Church Challenges** -- "30-Day Prayer Challenge" between churches. Aggregate statistics. Friendly competition to drive engagement.

6. **Family Accounts** -- Parent manages children's spiritual tracking. Family prayer goals. Age-appropriate Bible reading plans.

7. **Analytics Dashboard for Church Board** -- Exportable quarterly reports with trends, growth metrics, and engagement data for church leadership meetings.

8. **Multilingual Support** -- Telugu, Hindi, Tamil, and other Indian languages. Bible reader in local languages. UI language switcher.

9. **Integration with YouVersion / Bible Gateway APIs** -- Richer Bible content, reading plans, cross-references.

10. **Donation/Tithe Tracking Module** -- Sensitive but frequently requested by church admins. Private to user + admin only.

---

## 6. Prioritized Backlog

Scoring: Effort (1=easy, 5=hardest) | Impact (1=low, 5=critical) | Priority = Impact / Effort

| Rank | Item | Category | Effort | Impact | Priority Score | Rationale |
|------|------|----------|--------|--------|----------------|-----------|
| 1 | Q1: Quick Log on Dashboard | Quick Win | 1 | 5 | 5.0 | Single highest-friction daily interaction. Every user benefits every day. |
| 2 | Q8: Fasting checkbox on Daily Entry | Quick Win | 1 | 4 | 4.0 | Core spiritual discipline completely untracked. Trivial to add. |
| 3 | Q4: Continue reading bookmark | Quick Win | 1 | 4 | 4.0 | Removes "where was I?" friction from every Bible reading session. |
| 4 | Q2: Expand daily verse pool to 365 | Quick Win | 1 | 3 | 3.0 | Prevents staleness for daily users. Zero risk. |
| 5 | Q3: Actionable empty states | Quick Win | 1 | 3 | 3.0 | Improves first-time experience significantly. |
| 6 | Q7: Bishop inline drill-down | Quick Win | 1 | 4 | 4.0 | Biggest gap in Bishop Dashboard. Uses existing data. |
| 7 | Q5: Yesterday's summary card | Quick Win | 1 | 3 | 3.0 | Instant context for returning users. |
| 8 | Q9: Streak milestone messages | Quick Win | 1 | 2 | 2.0 | Small delight, high warmth. |
| 9 | M1: Pastor Notes per Member | Medium | 3 | 5 | 1.7 | Core pastoral care need. Pastors will use this daily. |
| 10 | M2: Member History View | Medium | 3 | 5 | 1.7 | Pastors cannot do their job without seeing member trends. |
| 11 | M3: Bulk Account Creation | Medium | 2 | 4 | 2.0 | Blocks onboarding of new churches. One-time but critical. |
| 12 | M5: Prayer Request Sharing | Medium | 3 | 4 | 1.3 | Bridges private prayer life with pastoral care. |
| 13 | M9: Group Engagement Chart (Bishop) | Medium | 2 | 4 | 2.0 | Bishop's primary need: trends over time, not just today. |
| 14 | L1: Notification/Reminder System | Large | 4 | 5 | 1.25 | The single most impactful large feature. Habit apps need reminders. Without this, engagement will decay. |
| 15 | M4: Weekly Digest Email | Medium | 4 | 4 | 1.0 | Keeps Bishop and Pastor informed without daily app visits. |
| 16 | L2: Guided Onboarding Flow | Large | 3 | 4 | 1.3 | First impressions determine retention. New users are lost currently. |
| 17 | M7: Fasting Tracker (Full) | Medium | 3 | 4 | 1.3 | Builds on Q8 checkbox. Complete spiritual discipline tracking. |
| 18 | M6: In-App Announcements | Medium | 2 | 3 | 1.5 | Enables pastor-to-group communication within the app. |
| 19 | M8: Personal Goals | Medium | 4 | 3 | 0.75 | Nice to have. Drives individual motivation. |
| 20 | L7: WhatsApp Bot Integration | Large | 5 | 5 | 1.0 | Game-changer for adoption in Indian church context. High effort but transformative. |
| 21 | M10: Audit Log | Medium | 2 | 3 | 1.5 | Admin accountability. Low effort. |
| 22 | L4: Spiritual Growth Score | Large | 4 | 3 | 0.75 | Compelling but requires careful design to avoid legalism. |
| 23 | L3: Testimony Wall | Large | 3 | 3 | 1.0 | Community building. Not urgent but high-warmth. |
| 24 | L8: Pastor Care Workflow | Large | 4 | 4 | 1.0 | Professional pastoral care. Differentiates from generic habit trackers. |
| 25 | L5: Multi-Church Tenancy | Large | 5 | 4 | 0.8 | Required for scaling. Not needed for single-church deployment. |
| 26 | L6: Advanced Bible Reader | Large | 5 | 3 | 0.6 | Nice to have. Competes with YouVersion. |
| 27 | Q10: Dark mode toggle | Quick Win | 1 | 2 | 2.0 | User comfort. Low priority but trivial effort. |
| 28 | Q6: "Not Logged" badge on nav | Quick Win | 1 | 2 | 2.0 | Visual nudge for pastors. |

---

## Summary of Recommended Sprints

**Sprint 1 (Week 1): Quick Wins Blitz**
Ship Q1 through Q9. These are all under 3 hours each and collectively transform the daily experience for every role. Total effort: approximately 3 days.

**Sprint 2 (Weeks 2-3): Pastor Empowerment**
Ship M1 (Pastor Notes), M2 (Member History), and M3 (Bulk Account Creation). These unblock the two biggest operational pain points: pastors cannot see member history, and admins cannot onboard churches efficiently.

**Sprint 3 (Weeks 4-5): Bishop Intelligence + Communication**
Ship M9 (Group Engagement Charts), Q7 (Bishop Drill-down, if not done in Sprint 1), M6 (Announcements), and M5 (Prayer Request Sharing). Gives the Bishop actionable intelligence and opens the first communication channel within the app.

**Sprint 4 (Weeks 6-8): Engagement Infrastructure**
Ship L1 (Notifications/Reminders) and L2 (Guided Onboarding). These are the retention multipliers. Without reminders, daily active usage will decay. Without onboarding, new user activation will remain low.

**Sprint 5 (Weeks 9-10): Spiritual Depth**
Ship M7 (Full Fasting Tracker), M8 (Personal Goals), and L4 (Spiritual Growth Score). These differentiate Logos Pulse from a generic habit tracker and make it a true spiritual growth companion.
