-- ============================================================
-- Phase 2 Schema Changes
-- Run this in Supabase SQL Editor
-- ============================================================

-- REQ-2: Multi-book assignments — add JSONB reading plan column
ALTER TABLE weekly_assignments ADD COLUMN IF NOT EXISTS reading_plan JSONB DEFAULT NULL;
-- reading_plan format: [{"book": "Hebrews", "start": 7, "end": 13}, {"book": "1 Corinthians", "start": 7, "end": 11}]

-- REQ-4: Prayer topic templates
CREATE TABLE IF NOT EXISTS prayer_templates (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT,
    template_type TEXT NOT NULL DEFAULT 'standard' CHECK (template_type IN ('standard', 'custom')),
    created_by  UUID REFERENCES auth.users(id),
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    confessions TEXT,
    prayers     TEXT,
    declarations TEXT,
    scriptures  JSONB,
    sort_order  INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_prayer_templates_type ON prayer_templates(template_type);

ALTER TABLE prayer_templates ENABLE ROW LEVEL SECURITY;

-- Standard templates: anyone can read, only admin can write
CREATE POLICY "Anyone can read standard templates"
    ON prayer_templates FOR SELECT
    USING (template_type = 'standard' OR created_by = auth.uid());

CREATE POLICY "Admin can manage standard templates"
    ON prayer_templates FOR INSERT
    WITH CHECK (public.is_admin() OR template_type = 'custom');

CREATE POLICY "Admin or owner can update templates"
    ON prayer_templates FOR UPDATE
    USING (public.is_admin() OR created_by = auth.uid());

CREATE POLICY "Admin or owner can delete templates"
    ON prayer_templates FOR DELETE
    USING (public.is_admin() OR created_by = auth.uid());

-- Seed default prayer templates
INSERT INTO prayer_templates (name, description, template_type, confessions, prayers, declarations, sort_order)
VALUES
('Morning Confession', 'Start your day declaring God''s promises', 'standard',
 'I confess that God is my source of strength and provision.\nI confess that I am a new creation in Christ.\nI confess that the Holy Spirit guides my steps daily.\nI confess that no weapon formed against me shall prosper.',
 'Lord, I thank you for this new day. Fill me with your Holy Spirit. Guide my thoughts, words, and actions today. Protect my family and give me wisdom in all I do.',
 'I declare that this is a day of favor and breakthrough.\nI declare that I walk in divine health and prosperity.\nI declare that God''s grace is sufficient for every challenge I face.',
 1),
('Evening Gratitude', 'End your day with thanksgiving', 'standard',
 'I confess that God has been faithful throughout this day.\nI confess that His mercies are new every morning.',
 'Father, thank you for your protection and provision today. Forgive me where I have fallen short. Watch over me and my family through the night.',
 'I declare that I will rest in peace, for God watches over me.\nI declare tomorrow will be filled with new mercies and fresh grace.',
 2),
('Spiritual Warfare', 'Stand firm in the full armor of God', 'standard',
 'I confess that I am more than a conqueror through Christ.\nI confess that greater is He who is in me than he who is in the world.\nI confess that the battle belongs to the Lord.',
 'Lord, clothe me with the full armor of God. Give me the sword of the Spirit to fight every spiritual battle. I take authority over every scheme of the enemy in Jesus'' name.',
 'I declare that every stronghold is broken in Jesus'' name.\nI declare that I have the mind of Christ.\nI declare victory over every area of my life.',
 3),
('Financial Breakthrough', 'Declaring God''s provision', 'standard',
 'I confess that my God shall supply all my needs according to His riches in glory.\nI confess that I am blessed to be a blessing.',
 'Father, I trust you as my provider. Open doors of financial blessing. Give me wisdom to manage resources. Let me be generous and faithful with what you give me.',
 'I declare that I am debt-free and abundantly blessed.\nI declare that wealth and riches are in my house.\nI declare that the windows of heaven are open over my finances.',
 4),
('Healing & Health', 'Praying for divine healing', 'standard',
 'I confess that by His stripes I am healed.\nI confess that God is my healer, Jehovah Rapha.\nI confess that I walk in divine health.',
 'Lord, I present my body to you as a living sacrifice. Heal every sickness and disease. Renew my strength and restore my health completely.',
 'I declare that sickness has no place in my body.\nI declare that I am healed and whole in Jesus'' name.\nI declare long life and good health over myself and my family.',
 5);
