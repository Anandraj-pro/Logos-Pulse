-- ============================================================
-- Pastor Notes per Member
-- Run this in Supabase SQL Editor
-- ============================================================

CREATE TABLE pastor_notes (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pastor_id   UUID NOT NULL REFERENCES auth.users(id),
    member_id   UUID NOT NULL REFERENCES auth.users(id),
    note_text   TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_pastor_notes_pastor ON pastor_notes(pastor_id);
CREATE INDEX idx_pastor_notes_member ON pastor_notes(pastor_id, member_id);

ALTER TABLE pastor_notes ENABLE ROW LEVEL SECURITY;

-- Only the pastor who wrote the note can see it (+ admin)
CREATE POLICY "Pastor can read own notes"
    ON pastor_notes FOR SELECT
    USING (pastor_id = auth.uid() OR public.is_admin());

CREATE POLICY "Pastor can insert notes"
    ON pastor_notes FOR INSERT
    WITH CHECK (pastor_id = auth.uid() OR public.is_admin());

CREATE POLICY "Pastor can delete own notes"
    ON pastor_notes FOR DELETE
    USING (pastor_id = auth.uid() OR public.is_admin());
