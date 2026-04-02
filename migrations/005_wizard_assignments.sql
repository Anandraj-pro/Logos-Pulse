-- ============================================================
-- REQ-5: Custom Wizard Assignments
-- Run this in Supabase SQL Editor
-- ============================================================

-- Wizard assignments (the main assignment entity)
CREATE TABLE wizard_assignments (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title           TEXT NOT NULL,
    description     TEXT,
    created_by      UUID NOT NULL REFERENCES auth.users(id),
    target_type     TEXT NOT NULL DEFAULT 'all' CHECK (target_type IN ('all', 'role', 'specific')),
    target_role     TEXT,
    start_date      TEXT NOT NULL,
    end_date        TEXT NOT NULL,
    is_published     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_wizard_assignments_created_by ON wizard_assignments(created_by);

ALTER TABLE wizard_assignments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Creators and targets can read wizard assignments"
    ON wizard_assignments FOR SELECT
    USING (
        created_by = auth.uid()
        OR public.is_admin()
        OR EXISTS (
            SELECT 1 FROM wizard_assignment_targets
            WHERE wizard_assignment_id = wizard_assignments.id AND user_id = auth.uid()
        )
    );

CREATE POLICY "Bishop/Pastor/Admin can create"
    ON wizard_assignments FOR INSERT
    WITH CHECK (public.get_my_role() IN ('admin', 'bishop', 'pastor'));

CREATE POLICY "Creator can update"
    ON wizard_assignments FOR UPDATE
    USING (created_by = auth.uid() OR public.is_admin());

CREATE POLICY "Creator can delete"
    ON wizard_assignments FOR DELETE
    USING (created_by = auth.uid() OR public.is_admin());

-- Assignment targets (which users are assigned)
CREATE TABLE wizard_assignment_targets (
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    wizard_assignment_id    BIGINT NOT NULL REFERENCES wizard_assignments(id) ON DELETE CASCADE,
    user_id                 UUID NOT NULL REFERENCES auth.users(id),
    UNIQUE (wizard_assignment_id, user_id)
);

CREATE INDEX idx_wizard_targets_user ON wizard_assignment_targets(user_id);
CREATE INDEX idx_wizard_targets_assignment ON wizard_assignment_targets(wizard_assignment_id);

ALTER TABLE wizard_assignment_targets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Targets can read own"
    ON wizard_assignment_targets FOR SELECT
    USING (user_id = auth.uid() OR public.is_admin() OR
           EXISTS (SELECT 1 FROM wizard_assignments WHERE id = wizard_assignment_id AND created_by = auth.uid()));

CREATE POLICY "Creator inserts targets"
    ON wizard_assignment_targets FOR INSERT
    WITH CHECK (public.get_my_role() IN ('admin', 'bishop', 'pastor'));

-- Components of a wizard assignment
CREATE TABLE wizard_components (
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    wizard_assignment_id    BIGINT NOT NULL REFERENCES wizard_assignments(id) ON DELETE CASCADE,
    component_type          TEXT NOT NULL CHECK (component_type IN ('prayer_template', 'sermon_series', 'bible_reading', 'prayer_time')),
    config                  JSONB NOT NULL,
    sort_order              INTEGER DEFAULT 0
);

CREATE INDEX idx_wizard_components_assignment ON wizard_components(wizard_assignment_id);

ALTER TABLE wizard_components ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Readable by assignment participants"
    ON wizard_components FOR SELECT
    USING (
        EXISTS (SELECT 1 FROM wizard_assignments WHERE id = wizard_assignment_id
                AND (created_by = auth.uid() OR public.is_admin()))
        OR EXISTS (SELECT 1 FROM wizard_assignment_targets
                   WHERE wizard_assignment_id = wizard_components.wizard_assignment_id AND user_id = auth.uid())
    );

CREATE POLICY "Creator inserts components"
    ON wizard_components FOR INSERT
    WITH CHECK (public.get_my_role() IN ('admin', 'bishop', 'pastor'));

-- Per-user progress on each component
CREATE TABLE wizard_component_progress (
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    wizard_component_id     BIGINT NOT NULL REFERENCES wizard_components(id) ON DELETE CASCADE,
    user_id                 UUID NOT NULL REFERENCES auth.users(id),
    status                  TEXT NOT NULL DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    progress_data           JSONB,
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (wizard_component_id, user_id)
);

CREATE INDEX idx_wizard_progress_user ON wizard_component_progress(user_id);

ALTER TABLE wizard_component_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own progress"
    ON wizard_component_progress FOR SELECT
    USING (user_id = auth.uid() OR public.is_admin() OR public.can_view_user(user_id));

CREATE POLICY "Users can update own progress"
    ON wizard_component_progress FOR INSERT
    WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can modify own progress"
    ON wizard_component_progress FOR UPDATE
    USING (user_id = auth.uid());

-- Sermon series (for sermon component)
CREATE TABLE sermon_series (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title           TEXT NOT NULL,
    speaker         TEXT NOT NULL DEFAULT 'Bishop Samuel Patta',
    playlist_url    TEXT,
    episode_count   INTEGER NOT NULL DEFAULT 0,
    created_by      UUID REFERENCES auth.users(id),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE sermon_series ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can read sermon series"
    ON sermon_series FOR SELECT USING (true);

CREATE POLICY "Admin/Bishop can manage series"
    ON sermon_series FOR INSERT
    WITH CHECK (public.get_my_role() IN ('admin', 'bishop'));

-- Seed a sample sermon series
INSERT INTO sermon_series (title, speaker, episode_count)
VALUES
('The Power of Prayer', 'Bishop Samuel Patta', 6),
('Walking in Faith', 'Bishop Samuel Patta', 8),
('The Book of Romans', 'Bishop Samuel Patta', 12);
