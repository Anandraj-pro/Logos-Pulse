-- ============================================
-- 011: Complete New Believer Track — Days 6 & 7
-- Run this if 010_prayer_engine.sql was already applied.
-- Safe to run multiple times (INSERT … WHERE NOT EXISTS).
-- ============================================

-- Day 6: I Have Purpose (category 4 — Identity in Christ)
INSERT INTO confession_templates
    (category_id, name, description, short_form_text, confessions, declarations, prayers, scriptures,
     tier, difficulty_level, recommended_duration, time_of_day, is_published, review_status, sort_order)
SELECT
    4,
    'Day 6: I Have Purpose',
    'Discovering your God-given purpose and calling',
    'God has plans to prosper me — Jeremiah 29:11
I am created for good works — Ephesians 2:10
I am called according to His purpose — Romans 8:28',
    '[{"text":"I confess that God has plans to prosper me and not to harm me, to give me hope and a future","scripture_ref":"Jeremiah 29:11"},{"text":"I confess that I was created in Christ Jesus for good works, which God prepared in advance for me to do","scripture_ref":"Ephesians 2:10"},{"text":"I confess that all things work together for good because I am called according to His purpose","scripture_ref":"Romans 8:28"},{"text":"I confess that the One who began a good work in me will carry it on to completion","scripture_ref":"Philippians 1:6"}]',
    '[{"text":"I declare that my life has meaning, direction, and divine purpose","scripture_ref":"Proverbs 19:21"},{"text":"I declare that God''s gifts and calling in my life are irrevocable","scripture_ref":"Romans 11:29"},{"text":"I declare that I am exactly where God needs me to be, and He is working through me","scripture_ref":"Esther 4:14"}]',
    '[{"text":"Father, reveal Your purpose for my life. Give me clarity on my calling and courage to pursue it. I surrender my own plans and choose Yours. Use me for Your glory in this generation. In Jesus'' name, Amen."}]',
    '["Jeremiah 29:11","Ephesians 2:10","Romans 8:28","Philippians 1:6","Proverbs 19:21","Romans 11:29","Esther 4:14"]',
    1, 'beginner', '7_days', 'morning', true, 'approved', 105
WHERE NOT EXISTS (
    SELECT 1 FROM confession_templates WHERE sort_order = 105 AND name LIKE 'Day 6:%'
);

-- Day 7: I Live by the Spirit (category 3 — Faith, Favor & Declarations)
INSERT INTO confession_templates
    (category_id, name, description, short_form_text, confessions, declarations, prayers, scriptures,
     tier, difficulty_level, recommended_duration, time_of_day, is_published, review_status, sort_order)
SELECT
    3,
    'Day 7: I Live by the Spirit',
    'Walking in the power and fruit of the Holy Spirit',
    'I am filled with the Holy Spirit — Ephesians 5:18
The Spirit helps me in my weakness — Romans 8:26
The fruit of the Spirit is mine — Galatians 5:22',
    '[{"text":"I confess that I am filled with the Holy Spirit and walk in His power daily","scripture_ref":"Ephesians 5:18"},{"text":"I confess that the Spirit helps me in my weakness and intercedes for me with groanings too deep for words","scripture_ref":"Romans 8:26"},{"text":"I confess that the fruit of the Spirit — love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, and self-control — is being produced in my life","scripture_ref":"Galatians 5:22-23"},{"text":"I confess that I do not walk by the flesh but by the Spirit of the living God","scripture_ref":"Romans 8:4"}]',
    '[{"text":"I declare that the Holy Spirit guides me into all truth and reminds me of God''s Word","scripture_ref":"John 16:13"},{"text":"I declare that I am sensitive to the voice of the Holy Spirit and I obey His promptings","scripture_ref":"John 10:27"},{"text":"I declare that the same power that raised Jesus from the dead lives in me","scripture_ref":"Romans 8:11"}]',
    '[{"text":"Holy Spirit, I welcome You into every area of my life. Lead me, fill me, and empower me. I choose to walk in step with You every day. Produce Your fruit in me and use me for Your glory. In Jesus'' name, Amen."}]',
    '["Ephesians 5:18","Romans 8:26","Galatians 5:22-23","Romans 8:4","John 16:13","John 10:27","Romans 8:11"]',
    1, 'beginner', '7_days', 'morning', true, 'approved', 106
WHERE NOT EXISTS (
    SELECT 1 FROM confession_templates WHERE sort_order = 106 AND name LIKE 'Day 7:%'
);

-- Wire into new_believer_track
INSERT INTO new_believer_track (day_number, template_id, is_active)
SELECT 6, id, true FROM confession_templates
WHERE sort_order = 105 AND name LIKE 'Day 6:%' LIMIT 1
ON CONFLICT DO NOTHING;

INSERT INTO new_believer_track (day_number, template_id, is_active)
SELECT 7, id, true FROM confession_templates
WHERE sort_order = 106 AND name LIKE 'Day 7:%' LIMIT 1
ON CONFLICT DO NOTHING;
