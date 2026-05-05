-- ============================================================
-- Sprint 9: Sermon Notes tags + starred
-- Run in Supabase SQL Editor
-- ============================================================

ALTER TABLE sermon_notes ADD COLUMN IF NOT EXISTS tags        TEXT[]  DEFAULT '{}';
ALTER TABLE sermon_notes ADD COLUMN IF NOT EXISTS is_starred  BOOLEAN NOT NULL DEFAULT FALSE;
