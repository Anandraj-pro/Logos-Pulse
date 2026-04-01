-- ============================================================
-- Logos Pulse: Full Supabase Schema
-- Run this in Supabase SQL Editor (Dashboard > SQL Editor > New Query)
-- ============================================================

-- 1. Role Enum
CREATE TYPE user_role AS ENUM ('admin', 'bishop', 'pastor', 'prayer_warrior');

-- ============================================================
-- 2. CREATE ALL TABLES FIRST (before functions that reference them)
-- ============================================================

-- 2a. User Profiles
CREATE TABLE user_profiles (
    id                   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id              UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role                 user_role NOT NULL DEFAULT 'prayer_warrior',
    pastor_id            UUID REFERENCES auth.users(id),
    bishop_id            UUID REFERENCES auth.users(id),
    created_by           UUID REFERENCES auth.users(id),
    membership_card_id   TEXT DEFAULT NULL,
    reporting_pastor     TEXT NOT NULL DEFAULT '',
    prayer_benchmark_min INTEGER NOT NULL DEFAULT 60,
    region_or_group      TEXT DEFAULT '',
    must_change_password BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id)
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_role ON user_profiles(role);
CREATE INDEX idx_user_profiles_pastor_id ON user_profiles(pastor_id);
CREATE INDEX idx_user_profiles_bishop_id ON user_profiles(bishop_id);

-- 2b. Daily Entries
CREATE TABLE daily_entries (
    id               BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id          UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    date             TEXT NOT NULL,
    prayer_minutes   INTEGER NOT NULL DEFAULT 60,
    bible_book       TEXT,
    chapters_read    JSONB,
    chapters_display TEXT,
    sermon_title     TEXT,
    sermon_speaker   TEXT,
    youtube_link     TEXT,
    report_copied    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, date)
);

CREATE INDEX idx_daily_entries_user_date ON daily_entries(user_id, date);

-- 2c. Weekly Assignments
CREATE TABLE weekly_assignments (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    assigned_by     UUID REFERENCES auth.users(id),
    book            TEXT NOT NULL,
    start_chapter   INTEGER NOT NULL,
    end_chapter     INTEGER NOT NULL,
    total_chapters  INTEGER NOT NULL,
    week_start_date TEXT NOT NULL,
    week_end_date   TEXT NOT NULL,
    daily_breakdown JSONB NOT NULL,
    status          TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_weekly_assignments_user_status ON weekly_assignments(user_id, status);
CREATE INDEX idx_weekly_assignments_dates ON weekly_assignments(week_start_date, week_end_date);

-- 2d. App Settings
CREATE TABLE app_settings (
    id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id  UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    key      TEXT NOT NULL,
    value    TEXT NOT NULL,
    UNIQUE (user_id, key)
);

CREATE INDEX idx_app_settings_user ON app_settings(user_id);

-- 2e. Sermon Notes
CREATE TABLE sermon_notes (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id             UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title               TEXT NOT NULL,
    speaker             TEXT NOT NULL,
    sermon_date         TEXT NOT NULL,
    notes_text          TEXT,
    bible_references    JSONB,
    learnings           TEXT,
    key_takeaways       TEXT,
    additional_thoughts TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_sermon_notes_user_date ON sermon_notes(user_id, sermon_date);

-- 2f. Prayer Categories
CREATE TABLE prayer_categories (
    id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id    UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name       TEXT NOT NULL,
    icon       TEXT DEFAULT '',
    color      TEXT DEFAULT '#5B4FC4',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, name)
);

CREATE INDEX idx_prayer_categories_user ON prayer_categories(user_id);

-- 2g. Prayer Entries
CREATE TABLE prayer_entries (
    id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id      UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    category_id  BIGINT NOT NULL REFERENCES prayer_categories(id) ON DELETE CASCADE,
    title        TEXT NOT NULL,
    prayer_text  TEXT,
    scriptures   JSONB,
    confessions  TEXT,
    declarations TEXT,
    status       TEXT NOT NULL DEFAULT 'ongoing',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_prayer_entries_user ON prayer_entries(user_id);
CREATE INDEX idx_prayer_entries_category ON prayer_entries(category_id);
CREATE INDEX idx_prayer_entries_status ON prayer_entries(status);

-- ============================================================
-- 3. HELPER FUNCTIONS (tables exist now, safe to reference them)
-- ============================================================

CREATE OR REPLACE FUNCTION public.get_my_role()
RETURNS TEXT AS $$
  SELECT role::TEXT FROM public.user_profiles WHERE user_id = auth.uid();
$$ LANGUAGE sql SECURITY DEFINER STABLE;

CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.user_profiles
    WHERE user_id = auth.uid() AND role = 'admin'
  );
$$ LANGUAGE sql SECURITY DEFINER STABLE;

CREATE OR REPLACE FUNCTION public.can_view_user(target_user_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
  my_role TEXT;
  my_id UUID := auth.uid();
BEGIN
  IF target_user_id = my_id THEN
    RETURN TRUE;
  END IF;

  SELECT role::TEXT INTO my_role FROM public.user_profiles WHERE user_id = my_id;

  IF my_role = 'admin' THEN
    RETURN TRUE;
  END IF;

  IF my_role = 'bishop' THEN
    RETURN EXISTS (
      SELECT 1 FROM public.user_profiles
      WHERE user_id = target_user_id
        AND (bishop_id = my_id
             OR pastor_id IN (SELECT p.user_id FROM public.user_profiles p WHERE p.bishop_id = my_id))
    );
  END IF;

  IF my_role = 'pastor' THEN
    RETURN EXISTS (
      SELECT 1 FROM public.user_profiles
      WHERE user_id = target_user_id AND pastor_id = my_id
    );
  END IF;

  RETURN FALSE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION public.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- 4. ROW LEVEL SECURITY POLICIES
-- ============================================================

-- 4a. user_profiles RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON user_profiles FOR SELECT
    USING (public.can_view_user(user_id));

CREATE POLICY "Account creation"
    ON user_profiles FOR INSERT
    WITH CHECK (
        auth.uid() = user_id
        OR public.is_admin()
        OR (public.get_my_role() = 'bishop' AND role::TEXT = 'pastor')
        OR (public.get_my_role() = 'pastor' AND role::TEXT = 'prayer_warrior')
    );

CREATE POLICY "Profile updates"
    ON user_profiles FOR UPDATE
    USING (
        auth.uid() = user_id
        OR public.is_admin()
        OR (public.get_my_role() = 'bishop' AND bishop_id = auth.uid())
        OR (public.get_my_role() = 'pastor' AND pastor_id = auth.uid())
    )
    WITH CHECK (
        auth.uid() = user_id
        OR public.is_admin()
        OR (public.get_my_role() = 'bishop' AND bishop_id = auth.uid())
        OR (public.get_my_role() = 'pastor' AND pastor_id = auth.uid())
    );

-- 4b. daily_entries RLS
ALTER TABLE daily_entries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON daily_entries FOR SELECT
    USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own entries"
    ON daily_entries FOR INSERT
    WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own entries"
    ON daily_entries FOR UPDATE
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own entries"
    ON daily_entries FOR DELETE
    USING (auth.uid() = user_id);

-- 4c. weekly_assignments RLS
ALTER TABLE weekly_assignments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON weekly_assignments FOR SELECT
    USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own assignments"
    ON weekly_assignments FOR INSERT
    WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Pastors can assign to members"
    ON weekly_assignments FOR INSERT
    WITH CHECK (
        public.get_my_role() IN ('admin', 'pastor')
        AND public.can_view_user(user_id)
    );
CREATE POLICY "Users can update own assignments"
    ON weekly_assignments FOR UPDATE
    USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own assignments"
    ON weekly_assignments FOR DELETE
    USING (auth.uid() = user_id);

-- 4d. app_settings RLS (private — own data only)
ALTER TABLE app_settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own settings"
    ON app_settings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own settings"
    ON app_settings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own settings"
    ON app_settings FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own settings"
    ON app_settings FOR DELETE USING (auth.uid() = user_id);

-- 4e. sermon_notes RLS
ALTER TABLE sermon_notes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON sermon_notes FOR SELECT USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own sermon notes"
    ON sermon_notes FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own sermon notes"
    ON sermon_notes FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own sermon notes"
    ON sermon_notes FOR DELETE USING (auth.uid() = user_id);

-- 4f. prayer_categories RLS
ALTER TABLE prayer_categories ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON prayer_categories FOR SELECT USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own categories"
    ON prayer_categories FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own categories"
    ON prayer_categories FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own categories"
    ON prayer_categories FOR DELETE USING (auth.uid() = user_id);

-- 4g. prayer_entries RLS
ALTER TABLE prayer_entries ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Hierarchical read access"
    ON prayer_entries FOR SELECT USING (public.can_view_user(user_id));
CREATE POLICY "Users can insert own prayers"
    ON prayer_entries FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own prayers"
    ON prayer_entries FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own prayers"
    ON prayer_entries FOR DELETE USING (auth.uid() = user_id);

-- ============================================================
-- 5. TRIGGERS
-- ============================================================

CREATE TRIGGER set_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();
CREATE TRIGGER set_updated_at BEFORE UPDATE ON daily_entries
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();
CREATE TRIGGER set_updated_at BEFORE UPDATE ON sermon_notes
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();
CREATE TRIGGER set_updated_at BEFORE UPDATE ON prayer_entries
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at();