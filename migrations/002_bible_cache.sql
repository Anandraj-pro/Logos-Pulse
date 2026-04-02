-- ============================================================
-- Bible Reader Cache Table
-- Run this in Supabase SQL Editor after 001_schema.sql
-- ============================================================

CREATE TABLE bible_cache (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book        TEXT NOT NULL,
    chapter     INTEGER NOT NULL,
    content     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (book, chapter)
);

CREATE INDEX idx_bible_cache_book_chapter ON bible_cache(book, chapter);

-- No RLS — Bible text is public/shared across all users
ALTER TABLE bible_cache ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can read bible cache"
    ON bible_cache FOR SELECT
    USING (true);

-- Only service role can insert (done server-side)
CREATE POLICY "Service role can insert cache"
    ON bible_cache FOR INSERT
    WITH CHECK (true);
