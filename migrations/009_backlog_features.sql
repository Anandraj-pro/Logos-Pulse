-- ============================================================
-- Remaining Backlog Features
-- Run this in Supabase SQL Editor
-- ============================================================

-- 1. Testimony / Praise Wall
CREATE TABLE testimonies (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    testimony   TEXT NOT NULL,
    is_anonymous BOOLEAN NOT NULL DEFAULT FALSE,
    is_approved  BOOLEAN NOT NULL DEFAULT FALSE,
    approved_by  UUID REFERENCES auth.users(id),
    reactions    JSONB DEFAULT '{"pray": 0, "amen": 0, "hallelujah": 0}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_testimonies_user ON testimonies(user_id);

ALTER TABLE testimonies ENABLE ROW LEVEL SECURITY;

-- Approved testimonies visible to all in the same pastor group
CREATE POLICY "Read approved testimonies"
    ON testimonies FOR SELECT
    USING (is_approved = true OR user_id = auth.uid() OR public.is_admin()
           OR public.get_my_role() IN ('pastor', 'bishop'));

CREATE POLICY "Users can insert own testimonies"
    ON testimonies FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own testimonies"
    ON testimonies FOR UPDATE
    USING (auth.uid() = user_id OR public.is_admin() OR public.get_my_role() IN ('pastor', 'bishop'));

CREATE POLICY "Users can delete own testimonies"
    ON testimonies FOR DELETE
    USING (auth.uid() = user_id OR public.is_admin());

-- 2. Personal Goals
CREATE TABLE personal_goals (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    description TEXT,
    goal_type   TEXT NOT NULL DEFAULT 'custom' CHECK (goal_type IN ('reading', 'prayer', 'fasting', 'custom')),
    target_value INTEGER,
    current_value INTEGER NOT NULL DEFAULT 0,
    target_date TEXT,
    status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'abandoned')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_personal_goals_user ON personal_goals(user_id);

ALTER TABLE personal_goals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own goals"
    ON personal_goals FOR SELECT
    USING (auth.uid() = user_id OR public.can_view_user(user_id));
CREATE POLICY "Users can insert own goals"
    ON personal_goals FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own goals"
    ON personal_goals FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own goals"
    ON personal_goals FOR DELETE USING (auth.uid() = user_id);

-- 3. Fasting Log (dedicated table for full tracking)
CREATE TABLE fasting_log (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    date        TEXT NOT NULL,
    fast_type   TEXT NOT NULL DEFAULT 'Full Day' CHECK (fast_type IN ('Full Day', 'Partial', 'Daniel Fast')),
    notes       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, date)
);

CREATE INDEX idx_fasting_log_user ON fasting_log(user_id, date);

ALTER TABLE fasting_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own fasting"
    ON fasting_log FOR SELECT
    USING (auth.uid() = user_id OR public.can_view_user(user_id));
CREATE POLICY "Users can insert own fasting"
    ON fasting_log FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own fasting"
    ON fasting_log FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own fasting"
    ON fasting_log FOR DELETE USING (auth.uid() = user_id);

-- 4. Audit Log
CREATE TABLE audit_log (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    actor_id    UUID NOT NULL REFERENCES auth.users(id),
    action      TEXT NOT NULL,
    target_type TEXT,
    target_id   TEXT,
    details     JSONB,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_log_actor ON audit_log(actor_id);
CREATE INDEX idx_audit_log_action ON audit_log(action);

ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admin can read audit log"
    ON audit_log FOR SELECT
    USING (public.is_admin());
CREATE POLICY "System can insert audit log"
    ON audit_log FOR INSERT
    WITH CHECK (true);

-- 5. Announcements
CREATE TABLE announcements (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_by  UUID NOT NULL REFERENCES auth.users(id),
    title       TEXT NOT NULL,
    message     TEXT NOT NULL,
    target_role TEXT DEFAULT 'all',
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    expires_at  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can read active announcements"
    ON announcements FOR SELECT
    USING (is_active = true OR created_by = auth.uid() OR public.is_admin());

CREATE POLICY "Admin/Pastor/Bishop can create announcements"
    ON announcements FOR INSERT
    WITH CHECK (public.get_my_role() IN ('admin', 'bishop', 'pastor'));

CREATE POLICY "Creator can update announcements"
    ON announcements FOR UPDATE
    USING (created_by = auth.uid() OR public.is_admin());

CREATE POLICY "Creator can delete announcements"
    ON announcements FOR DELETE
    USING (created_by = auth.uid() OR public.is_admin());

-- 6. Announcement dismissals (track who dismissed what)
CREATE TABLE announcement_dismissals (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    announcement_id BIGINT NOT NULL REFERENCES announcements(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES auth.users(id),
    dismissed_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (announcement_id, user_id)
);

ALTER TABLE announcement_dismissals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own dismissals"
    ON announcement_dismissals FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own dismissals"
    ON announcement_dismissals FOR INSERT WITH CHECK (auth.uid() = user_id);
