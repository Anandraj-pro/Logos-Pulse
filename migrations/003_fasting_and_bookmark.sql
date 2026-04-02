-- ============================================================
-- Add fasting tracking and reading bookmark columns
-- Run this in Supabase SQL Editor
-- ============================================================

-- Fasting fields on daily_entries
ALTER TABLE daily_entries ADD COLUMN IF NOT EXISTS fasted BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE daily_entries ADD COLUMN IF NOT EXISTS fast_type TEXT DEFAULT NULL;

-- Reading bookmark on user_profiles
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_read_book TEXT DEFAULT NULL;
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS last_read_chapter INTEGER DEFAULT NULL;
