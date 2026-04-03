-- ============================================================
-- M4: Shared Prayer Requests
-- Run this in Supabase SQL Editor
-- ============================================================

-- Track which prayers are shared with the pastor
ALTER TABLE prayer_entries ADD COLUMN IF NOT EXISTS shared_with_pastor BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE prayer_entries ADD COLUMN IF NOT EXISTS shared_at TIMESTAMPTZ DEFAULT NULL;
