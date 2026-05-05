-- ============================================================
-- Sprint 8: Prayer Requests, Notifications, Check-in Requests
-- Run in Supabase SQL Editor
-- ============================================================

-- ── Prayer Requests ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS prayer_requests (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    body        TEXT,
    is_anonymous BOOLEAN NOT NULL DEFAULT FALSE,
    status      TEXT NOT NULL DEFAULT 'active'
                  CHECK (status IN ('active', 'hidden', 'answered')),
    pray_count  INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS prayer_request_prays (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id  UUID NOT NULL REFERENCES prayer_requests(id) ON DELETE CASCADE,
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(request_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_prayer_requests_user   ON prayer_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_prayer_requests_status ON prayer_requests(status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_prays_request          ON prayer_request_prays(request_id);

ALTER TABLE prayer_requests       ENABLE ROW LEVEL SECURITY;
ALTER TABLE prayer_request_prays  ENABLE ROW LEVEL SECURITY;

-- Members/PW see active requests; owner + pastor/admin see all
CREATE POLICY "prayer_requests_select" ON prayer_requests FOR SELECT USING (
    status = 'active'
    OR user_id = auth.uid()
    OR public.is_admin()
    OR public.get_my_role() IN ('pastor', 'bishop')
);
CREATE POLICY "prayer_requests_insert" ON prayer_requests FOR INSERT WITH CHECK (
    user_id = auth.uid()
);
CREATE POLICY "prayer_requests_update" ON prayer_requests FOR UPDATE USING (
    user_id = auth.uid()
    OR public.is_admin()
    OR public.get_my_role() IN ('pastor', 'bishop')
);

CREATE POLICY "prays_select" ON prayer_request_prays FOR SELECT USING (TRUE);
CREATE POLICY "prays_insert" ON prayer_request_prays FOR INSERT WITH CHECK (user_id = auth.uid());
CREATE POLICY "prays_delete" ON prayer_request_prays FOR DELETE USING (user_id = auth.uid());


-- ── Check-in Requests (member → pastor) ──────────────────────
CREATE TABLE IF NOT EXISTS checkin_requests (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_id   UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    pastor_id   UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    message     TEXT,
    status      TEXT NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'acknowledged')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_checkin_member ON checkin_requests(member_id);
CREATE INDEX IF NOT EXISTS idx_checkin_pastor ON checkin_requests(pastor_id, status);

ALTER TABLE checkin_requests ENABLE ROW LEVEL SECURITY;

CREATE POLICY "checkin_select" ON checkin_requests FOR SELECT USING (
    member_id = auth.uid()
    OR pastor_id = auth.uid()
    OR public.is_admin()
);
CREATE POLICY "checkin_insert" ON checkin_requests FOR INSERT WITH CHECK (member_id = auth.uid());
CREATE POLICY "checkin_update" ON checkin_requests FOR UPDATE USING (
    pastor_id = auth.uid() OR public.is_admin()
);


-- ── Notifications ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    type        TEXT NOT NULL DEFAULT 'general',
    title       TEXT NOT NULL,
    body        TEXT,
    is_read     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_notif_user_unread ON notifications(user_id, is_read, created_at DESC);

ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

CREATE POLICY "notifications_own" ON notifications FOR ALL USING (user_id = auth.uid());
