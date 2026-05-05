-- ============================================================
-- Sprint 7 Schema
-- Run in Supabase SQL Editor
-- ============================================================

-- S7-01: Add status to reading_plan_progress
ALTER TABLE reading_plan_progress
    ADD COLUMN IF NOT EXISTS status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'completed', 'abandoned'));

-- S7-05: Add auto-tracking columns to personal_goals
ALTER TABLE personal_goals
    ADD COLUMN IF NOT EXISTS tracking_mode TEXT NOT NULL DEFAULT 'manual'
        CHECK (tracking_mode IN ('manual', 'auto_prayer', 'auto_reading', 'auto_fasting'));

ALTER TABLE personal_goals
    ADD COLUMN IF NOT EXISTS last_tracked_date TEXT DEFAULT NULL;

ALTER TABLE personal_goals
    ADD COLUMN IF NOT EXISTS unit TEXT DEFAULT NULL;
