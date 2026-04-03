-- ============================================================
-- L1: Reminder Preferences
-- Run this in Supabase SQL Editor
-- ============================================================

-- User reminder preferences
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS reminder_enabled BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS reminder_hour INTEGER DEFAULT 18;

-- Pastor follow-up log
CREATE TABLE IF NOT EXISTS follow_up_log (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pastor_id   UUID NOT NULL REFERENCES auth.users(id),
    member_id   UUID NOT NULL REFERENCES auth.users(id),
    action      TEXT NOT NULL,
    notes       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_follow_up_pastor ON follow_up_log(pastor_id);

ALTER TABLE follow_up_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Pastor can read own follow-ups"
    ON follow_up_log FOR SELECT
    USING (pastor_id = auth.uid() OR public.is_admin());

CREATE POLICY "Pastor can insert follow-ups"
    ON follow_up_log FOR INSERT
    WITH CHECK (pastor_id = auth.uid() OR public.is_admin());

-- Onboarding flag
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN NOT NULL DEFAULT FALSE;
