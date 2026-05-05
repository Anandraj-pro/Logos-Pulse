-- ============================================================
-- Sprint 6: system_settings + care_tasks + reading plans + bible annotations
-- Run each section in Supabase SQL Editor
-- ============================================================

-- ── S6 Story 1: System Settings (global feature flags) ──────

CREATE TABLE IF NOT EXISTS system_settings (
    key        TEXT PRIMARY KEY,
    value      TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Default: reminders on
INSERT INTO system_settings (key, value)
VALUES ('reminders_enabled', 'true')
ON CONFLICT (key) DO NOTHING;

ALTER TABLE system_settings ENABLE ROW LEVEL SECURITY;

-- Admins can read and write; Edge Function reads via service role (bypasses RLS)
CREATE POLICY "Admin can read system settings"
    ON system_settings FOR SELECT
    USING (public.is_admin());

CREATE POLICY "Admin can update system settings"
    ON system_settings FOR UPDATE
    USING (public.is_admin())
    WITH CHECK (public.is_admin());

CREATE POLICY "Admin can insert system settings"
    ON system_settings FOR INSERT
    WITH CHECK (public.is_admin());

-- ── S6 Story 2: Care Tasks + Inactivity View ────────────────

CREATE TABLE IF NOT EXISTS care_tasks (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pastor_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    member_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    care_type    TEXT NOT NULL DEFAULT 'Check-In Call'
                   CHECK (care_type IN ('Check-In Call','Prayer Visit','Message','Escalate to Bishop')),
    note         TEXT,
    due_date     TEXT,
    status       TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','done')),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_care_tasks_pastor ON care_tasks(pastor_id, status);
CREATE INDEX IF NOT EXISTS idx_care_tasks_member ON care_tasks(member_id);

ALTER TABLE care_tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Pastor can read own care tasks"
    ON care_tasks FOR SELECT
    USING (pastor_id = auth.uid() OR public.is_admin()
           OR (public.get_my_role() = 'bishop'
               AND pastor_id IN (
                 SELECT user_id FROM user_profiles WHERE bishop_id = auth.uid()
               )));

CREATE POLICY "Pastor can create care tasks"
    ON care_tasks FOR INSERT
    WITH CHECK (pastor_id = auth.uid() OR public.is_admin());

CREATE POLICY "Pastor can update own care tasks"
    ON care_tasks FOR UPDATE
    USING (pastor_id = auth.uid() OR public.is_admin())
    WITH CHECK (pastor_id = auth.uid() OR public.is_admin());

-- View: members who haven't logged in threshold_days days
-- Pastors query this through the admin client (bypasses RLS)
CREATE OR REPLACE VIEW inactive_members_view AS
SELECT
    up.user_id,
    up.pastor_id,
    up.bishop_id,
    COALESCE(MAX(de.date), '2000-01-01') AS last_entry_date,
    CURRENT_DATE - COALESCE(MAX(de.date::date), '2000-01-01'::date) AS days_since_last_entry
FROM user_profiles up
LEFT JOIN daily_entries de ON de.user_id = up.user_id
WHERE up.role = 'prayer_warrior'
GROUP BY up.user_id, up.pastor_id, up.bishop_id;

-- ── S6 Story 3: Bible Reading Plans ─────────────────────────

CREATE TABLE IF NOT EXISTS reading_plans (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    total_days  INTEGER NOT NULL,
    created_by  UUID REFERENCES auth.users(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS reading_plan_days (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    plan_id       BIGINT NOT NULL REFERENCES reading_plans(id) ON DELETE CASCADE,
    day_number    INTEGER NOT NULL,
    book          TEXT NOT NULL,
    chapter_start INTEGER NOT NULL,
    chapter_end   INTEGER NOT NULL,
    UNIQUE (plan_id, day_number)
);

CREATE INDEX IF NOT EXISTS idx_plan_days_plan ON reading_plan_days(plan_id, day_number);

CREATE TABLE IF NOT EXISTS reading_plan_progress (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id      UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    plan_id      BIGINT NOT NULL REFERENCES reading_plans(id) ON DELETE CASCADE,
    enrolled_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    assigned_by  UUID REFERENCES auth.users(id),
    current_day  INTEGER NOT NULL DEFAULT 1,
    last_completed_date TEXT,
    completed_at TIMESTAMPTZ,
    UNIQUE (user_id, plan_id)
);

CREATE INDEX IF NOT EXISTS idx_plan_progress_user ON reading_plan_progress(user_id);

ALTER TABLE reading_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE reading_plan_days ENABLE ROW LEVEL SECURITY;
ALTER TABLE reading_plan_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone authenticated can read plans"
    ON reading_plans FOR SELECT USING (auth.uid() IS NOT NULL);
CREATE POLICY "Admin can manage plans"
    ON reading_plans FOR ALL USING (public.is_admin());

CREATE POLICY "Anyone authenticated can read plan days"
    ON reading_plan_days FOR SELECT USING (auth.uid() IS NOT NULL);
CREATE POLICY "Admin can manage plan days"
    ON reading_plan_days FOR ALL USING (public.is_admin());

CREATE POLICY "Users can read own progress"
    ON reading_plan_progress FOR SELECT
    USING (user_id = auth.uid() OR public.can_view_user(user_id));
CREATE POLICY "Users can enroll themselves"
    ON reading_plan_progress FOR INSERT
    WITH CHECK (user_id = auth.uid() OR public.get_my_role() IN ('admin','pastor','bishop'));
CREATE POLICY "Users can update own progress"
    ON reading_plan_progress FOR UPDATE
    USING (user_id = auth.uid() OR public.is_admin());

-- ── S6 Story 4: Bible Bookmarks & Highlights ────────────────

CREATE TABLE IF NOT EXISTS bible_bookmarks (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id      UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    book         TEXT NOT NULL,
    chapter      INTEGER NOT NULL,
    verse_number INTEGER NOT NULL,
    note         TEXT DEFAULT '',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, book, chapter, verse_number)
);

CREATE INDEX IF NOT EXISTS idx_bible_bookmarks_user ON bible_bookmarks(user_id);
CREATE INDEX IF NOT EXISTS idx_bible_bookmarks_chapter ON bible_bookmarks(user_id, book, chapter);

CREATE TABLE IF NOT EXISTS bible_highlights (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id      UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    book         TEXT NOT NULL,
    chapter      INTEGER NOT NULL,
    verse_number INTEGER NOT NULL,
    color        TEXT NOT NULL DEFAULT 'yellow' CHECK (color IN ('yellow','green')),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, book, chapter, verse_number)
);

CREATE INDEX IF NOT EXISTS idx_bible_highlights_chapter ON bible_highlights(user_id, book, chapter);

ALTER TABLE bible_bookmarks ENABLE ROW LEVEL SECURITY;
ALTER TABLE bible_highlights ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own bookmarks"
    ON bible_bookmarks FOR ALL USING (user_id = auth.uid());
CREATE POLICY "Users can manage own highlights"
    ON bible_highlights FOR ALL USING (user_id = auth.uid());

-- ── pg_cron: Daily Reminder Job ──────────────────────────────
-- Run this AFTER enabling the pg_cron extension in Supabase dashboard:
-- Dashboard > Database > Extensions > pg_cron (enable)
-- Then run in SQL Editor:
--
-- SELECT cron.schedule(
--   'daily-reminders',
--   '30 13 * * *',   -- 7:00 PM IST (13:30 UTC)
--   $$
--     SELECT net.http_post(
--       url := 'https://whyvlkkjbxehdbsgohre.supabase.co/functions/v1/send-daily-reminders',
--       headers := jsonb_build_object(
--         'Content-Type', 'application/json',
--         'Authorization', 'Bearer <service_role_key>'
--       ),
--       body := '{}'::jsonb
--     )
--   $$
-- );
-- Replace <service_role_key> with the key from Supabase > Settings > API.
