"""
Logos Pulse Design System v3 — Sacred Lux
Single source of truth for all visual styles across every page.
"""

import streamlit as st

# ==================== DESIGN TOKENS ====================
COLORS = {
    "primary": "#3B2F8E",
    "primary_light": "#5B4FC4",
    "primary_dark": "#261F62",
    "accent_gold": "#C9982A",
    "accent_gold_light": "#E8C560",
    "accent_warm": "#C26B2C",
    "surface": "#F7F5F0",
    "surface_warm": "#FFFDF8",
    "card_bg": "#FFFFFF",
    "card_border": "rgba(175, 150, 90, 0.12)",
    "text_primary": "#1A1628",
    "text_secondary": "#574F6E",
    "text_muted": "#9E96AB",
    "success": "#2D6A4F",
    "success_bg": "#E8F5EE",
    "warning": "#C26B2C",
    "warning_bg": "#FFF4E6",
    "danger": "#B5383C",
    "streak_fire": "#E85D3A",
    "streak_gold": "#C9982A",
}

# ==================== SHARED CSS ====================
SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400&family=Nunito:wght@300;400;500;600;700;800&family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* ================================================================
   DESIGN TOKENS
   ================================================================ */
:root {
    --lp-primary:       #3B2F8E;
    --lp-primary-light: #5B4FC4;
    --lp-primary-dark:  #261F62;
    --lp-gold:          #C9982A;
    --lp-gold-light:    #E8C560;
    --lp-gold-dark:     #9B7420;
    --lp-bg:            #F7F5F0;
    --lp-surface:       #FFFFFF;
    --lp-border:        rgba(175, 150, 90, 0.12);
    --lp-text:          #1A1628;
    --lp-text-2:        #574F6E;
    --lp-text-3:        #9E96AB;
    --lp-success:       #2D6A4F;
    --lp-warning:       #C26B2C;
    --lp-danger:        #B5383C;
    --lp-r-sm:  10px;
    --lp-r-md:  16px;
    --lp-r-lg:  22px;
    --lp-shadow-xs: 0 1px 3px rgba(26,22,40,0.04), 0 1px 6px rgba(26,22,40,0.02);
    --lp-shadow-sm: 0 2px 8px rgba(26,22,40,0.05), 0 1px 3px rgba(26,22,40,0.03);
    --lp-shadow-md: 0 6px 20px rgba(26,22,40,0.07), 0 2px 6px rgba(26,22,40,0.04);
    --lp-shadow-lg: 0 12px 40px rgba(26,22,40,0.09), 0 4px 10px rgba(26,22,40,0.05);
    --lp-glow-indigo: 0 6px 24px rgba(59,47,142,0.18);
    --lp-glow-gold:   0 6px 24px rgba(201,152,42,0.15);
}

/* ================================================================
   GLOBAL BASE
   ================================================================ */
.stApp {
    font-family: 'Nunito', 'DM Sans', -apple-system, sans-serif !important;
    background:
        radial-gradient(ellipse at 8% 8%,   rgba(59,47,142,0.055) 0%, transparent 42%),
        radial-gradient(ellipse at 92% 88%,  rgba(201,152,42,0.045) 0%, transparent 42%),
        radial-gradient(ellipse at 50% -5%,  rgba(91,79,196,0.03)  0%, transparent 50%),
        radial-gradient(ellipse at 50% 105%, rgba(155,95,168,0.02)  0%, transparent 50%),
        #F7F5F0 !important;
    color: var(--lp-text) !important;
}

h1, h2, h3 {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif !important;
    color: var(--lp-text) !important;
    font-weight: 700 !important;
}

/* ================================================================
   KEYFRAMES
   ================================================================ */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position:  200% 0; }
}
@keyframes breathe {
    0%, 100% { box-shadow: 0 4px 16px rgba(194,107,44,0.08); }
    50%       { box-shadow: 0 4px 24px rgba(194,107,44,0.18), 0 0 0 3px rgba(201,152,42,0.06); }
}
@keyframes goldPulse {
    0%, 100% { border-color: rgba(201,152,42,0.2); }
    50%       { border-color: rgba(201,152,42,0.5); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(10px); }
    to   { opacity: 1; transform: translateX(0);    }
}

/* ================================================================
   HERO SECTION (Dashboard)
   ================================================================ */
.hero-section {
    background:
        radial-gradient(ellipse at 18% 15%, rgba(201,152,42,0.20) 0%, transparent 55%),
        radial-gradient(ellipse at 82% 80%, rgba(155,95,168,0.16) 0%, transparent 52%),
        radial-gradient(ellipse at 55%  5%, rgba(91,79,196,0.10)  0%, transparent 40%),
        linear-gradient(135deg, #1F1854 0%, #3B2F8E 28%, #5B3FA0 58%, #7B4FA8 100%);
    border-radius: var(--lp-r-lg);
    padding: 44px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 24px 64px rgba(59,47,142,0.32),
        0 4px 16px rgba(59,47,142,0.20),
        inset 0 1px 0 rgba(255,255,255,0.10),
        inset 0 -1px 0 rgba(0,0,0,0.08);
    animation: fadeInUp 0.65s cubic-bezier(0.22,1,0.36,1) both;
}

/* Diagonal hatching overlay */
.hero-section::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        -55deg,
        rgba(255,255,255,0.012) 0px,
        rgba(255,255,255,0.012) 1px,
        transparent 1px,
        transparent 14px
    );
    pointer-events: none;
    border-radius: inherit;
}

/* Orb top-right */
.hero-section::after {
    content: '';
    position: absolute;
    top:   -70px;
    right: -70px;
    width:  300px;
    height: 300px;
    background: radial-gradient(circle, rgba(201,152,42,0.14) 0%, transparent 68%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-greeting {
    font-family: 'Nunito', sans-serif;
    font-size: 10px;
    font-weight: 800;
    color: rgba(201,152,42,0.9);
    letter-spacing: 3.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
    position: relative;
}

.hero-name {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 40px;
    font-weight: 700;
    color: white;
    line-height: 1.15;
    margin-bottom: 4px;
    position: relative;
    text-shadow: 0 3px 20px rgba(0,0,0,0.30);
}

.hero-date {
    font-size: 13px;
    color: rgba(255,255,255,0.44);
    position: relative;
    font-weight: 600;
    letter-spacing: 0.4px;
}

.hero-verse {
    margin-top: 22px;
    padding: 18px 20px 18px 34px;
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    font-family: 'EB Garamond', 'DM Serif Display', Georgia, serif;
    font-style: italic;
    font-size: 16px;
    color: rgba(255,255,255,0.88);
    line-height: 1.78;
    border: 1px solid rgba(201,152,42,0.22);
    position: relative;
    backdrop-filter: blur(6px);
}

.hero-verse::before {
    content: '\201C';
    position: absolute;
    top: -2px;
    left: 12px;
    font-size: 56px;
    color: rgba(201,152,42,0.38);
    font-family: 'EB Garamond', Georgia, serif;
    line-height: 1;
    font-style: normal;
}

/* ================================================================
   PAGE HEADER
   ================================================================ */
.page-header {
    background:
        radial-gradient(ellipse at 80% 20%, rgba(201,152,42,0.16) 0%, transparent 55%),
        radial-gradient(ellipse at 15% 85%, rgba(155,95,168,0.10) 0%, transparent 48%),
        linear-gradient(135deg, #1F1854 0%, #3B2F8E 38%, #5B4FA0 100%);
    border-radius: var(--lp-r-lg);
    padding: 28px 32px 26px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 14px 44px rgba(59,47,142,0.26),
        0 2px 8px  rgba(59,47,142,0.14),
        inset 0 1px 0 rgba(255,255,255,0.09);
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
}

.page-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        -48deg,
        rgba(255,255,255,0.009) 0px,
        rgba(255,255,255,0.009) 1px,
        transparent 1px,
        transparent 16px
    );
    pointer-events: none;
    border-radius: inherit;
}

/* Bottom gold accent line */
.page-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(201,152,42,0.6) 30%,
        rgba(201,152,42,0.8) 50%,
        rgba(201,152,42,0.6) 70%,
        transparent 100%
    );
}

.page-header-title {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: -0.2px;
    color: white;
    position: relative;
    text-shadow: 0 2px 14px rgba(0,0,0,0.22);
}

.page-header-sub {
    font-size: 13px;
    color: rgba(255,255,255,0.52);
    margin-top: 5px;
    font-weight: 600;
    letter-spacing: 0.3px;
    position: relative;
}

/* ================================================================
   SECTION LABEL
   ================================================================ */
.section-label {
    font-size: 10px;
    color: var(--lp-text-3);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 800;
    margin: 24px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(201,152,42,0.35) 0%, transparent 100%);
}

/* ================================================================
   METRIC CARDS
   ================================================================ */
.metric-card {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 22px 14px;
    text-align: center;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.3s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0;
    transition: opacity 0.3s;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--lp-glow-indigo), var(--lp-shadow-md);
    border-color: rgba(59,47,142,0.18);
}

.metric-card:hover::before { opacity: 1; }

.metric-value {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 34px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 6px;
}

.metric-label {
    font-size: 10px;
    color: var(--lp-text-3);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 800;
}

/* ================================================================
   STAT CARDS
   ================================================================ */
.stat-card {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 22px 16px;
    text-align: center;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.3s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0;
    transition: opacity 0.3s;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--lp-glow-indigo);
    border-color: rgba(59,47,142,0.15);
}

.stat-card:hover::before { opacity: 1; }

.stat-value {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 30px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 6px;
}

.stat-label {
    font-size: 10px;
    color: var(--lp-text-3);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    font-weight: 800;
}

/* ================================================================
   SECTION CARDS (3-up toolkit cards)
   ================================================================ */
.section-card {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 26px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.35s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
}

.section-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold), var(--lp-primary));
    background-size: 200% 100%;
    opacity: 0;
    transition: opacity 0.3s;
}

.section-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--lp-shadow-lg), 0 0 0 1px rgba(201,152,42,0.08);
    border-color: rgba(201,152,42,0.22);
}

.section-card:hover::after {
    opacity: 1;
    animation: shimmer 2.2s linear infinite;
}

.section-icon { font-size: 30px; margin-bottom: 10px; }

.section-title {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 19px;
    font-weight: 700;
    color: var(--lp-text);
    margin-bottom: 6px;
}

.section-desc {
    font-size: 13px;
    color: var(--lp-text-3);
    line-height: 1.6;
}

/* ================================================================
   TODAY STATUS CARDS
   ================================================================ */
.today-card {
    border-radius: var(--lp-r-md);
    padding: 22px 26px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.45s cubic-bezier(0.22,1,0.36,1) both;
}

.today-done {
    background: linear-gradient(135deg, #E8F5EE 0%, #F4FAF6 100%);
    border: 1px solid rgba(45,106,79,0.20);
    box-shadow: 0 4px 16px rgba(45,106,79,0.08), inset 0 1px 0 rgba(255,255,255,0.8);
}

.today-done::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 90px; height: 90px;
    background: radial-gradient(circle at top right, rgba(45,106,79,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.today-pending {
    background: linear-gradient(135deg, #FFF4E6 0%, #FFFDF7 100%);
    border: 1px solid rgba(194,107,44,0.22);
    box-shadow: 0 4px 16px rgba(194,107,44,0.07), inset 0 1px 0 rgba(255,255,255,0.8);
    animation: fadeInUp 0.45s cubic-bezier(0.22,1,0.36,1) both, breathe 4s ease-in-out 1.2s infinite;
}

.today-pending::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 90px; height: 90px;
    background: radial-gradient(circle at top right, rgba(201,152,42,0.10) 0%, transparent 70%);
    pointer-events: none;
}

.today-title {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 8px;
    position: relative;
}

.today-detail {
    font-size: 14px;
    color: var(--lp-text-2);
    line-height: 1.6;
    position: relative;
}

/* ================================================================
   PROGRESS BARS
   ================================================================ */
.progress-section {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 22px 26px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
    transition: box-shadow 0.3s;
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
}

.progress-section:hover { box-shadow: var(--lp-shadow-sm); }

.progress-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--lp-text-2);
    margin-bottom: 14px;
}

.progress-bar-bg {
    background: linear-gradient(90deg, rgba(59,47,142,0.06), rgba(201,152,42,0.06));
    border-radius: 100px;
    height: 8px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg,
        var(--lp-primary) 0%,
        var(--lp-gold-light) 50%,
        var(--lp-primary) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
    box-shadow: 0 0 10px rgba(59,47,142,0.28);
    transition: width 0.8s cubic-bezier(0.22,1,0.36,1);
}

.progress-label {
    font-size: 12px;
    color: var(--lp-text-3);
    margin-top: 8px;
    font-weight: 700;
}

/* ================================================================
   ENTRY / DATA CARDS
   ================================================================ */
.entry-card {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 18px 22px;
    margin-bottom: 10px;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
}

.entry-card:hover {
    box-shadow: var(--lp-shadow-sm), 0 0 0 1px rgba(59,47,142,0.05);
    border-color: rgba(59,47,142,0.12);
    transform: translateY(-1px);
}

/* ================================================================
   REPORT CARD (parchment/scripture feel)
   ================================================================ */
.report-card {
    background: linear-gradient(135deg, #FFFDF8, #FFF9F0);
    border: 1px solid rgba(201,152,42,0.22);
    border-radius: var(--lp-r-md);
    padding: 28px;
    font-family: 'EB Garamond', 'DM Serif Display', Georgia, serif;
    font-size: 17px;
    line-height: 1.88;
    color: #2C2010;
    white-space: pre-line;
    box-shadow:
        0 4px 20px rgba(201,152,42,0.08),
        inset 0 1px 0 rgba(255,255,255,0.8);
    position: relative;
    overflow: hidden;
}

.report-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--lp-gold), var(--lp-primary));
    border-radius: 4px 0 0 4px;
}

/* ================================================================
   GOAL / INFO BANNERS
   ================================================================ */
.goal-banner {
    background: linear-gradient(135deg, rgba(59,47,142,0.05), rgba(91,79,196,0.04));
    border: 1px solid rgba(59,47,142,0.10);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px 14px 22px;
    font-size: 14px;
    color: var(--lp-primary);
    font-weight: 700;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}

.goal-banner::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--lp-primary), var(--lp-gold));
}

/* ================================================================
   PRAYER CARDS
   ================================================================ */
.prayer-card {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 20px 24px;
    margin-bottom: 12px;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
}

.prayer-card:hover {
    box-shadow: var(--lp-shadow-sm);
    border-color: rgba(59,47,142,0.12);
    transform: translateY(-1px);
}

.prayer-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.prayer-name {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 17px;
    font-weight: 700;
    color: var(--lp-text);
}

.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.4px;
}

/* ================================================================
   SCRIPTURE / CONFESSION / DECLARATION BLOCKS
   ================================================================ */
.scripture-block {
    background: linear-gradient(135deg, #FFFDF8, #FFFAF2);
    border-left: 3px solid;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 6px;
    font-family: 'EB Garamond', 'DM Serif Display', Georgia, serif;
    font-size: 15px;
    line-height: 1.82;
    color: #2C2010;
}

.confession-block {
    background: linear-gradient(135deg, #E8F5EE, #F4FAF6);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px;
    font-weight: 700;
    color: var(--lp-success);
    line-height: 1.78;
    border: 1px solid rgba(45,106,79,0.14);
}

.declaration-block {
    background: linear-gradient(135deg, #FFF4E6, #FFFCF5);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px;
    font-weight: 800;
    color: var(--lp-warning);
    line-height: 1.78;
    border: 1px solid rgba(194,107,44,0.14);
}

/* ================================================================
   SERMON CARDS
   ================================================================ */
.sermon-card {
    background: linear-gradient(135deg, #FEFEFE, #FFFDF8);
    border: 1px solid rgba(201,152,42,0.14);
    border-radius: var(--lp-r-md);
    padding: 20px 24px;
    margin: 10px 0;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.3s cubic-bezier(0.22,1,0.36,1);
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
}

.sermon-card:hover {
    box-shadow: var(--lp-glow-gold);
    border-color: rgba(201,152,42,0.28);
    transform: translateY(-2px);
}

/* ================================================================
   CATEGORY CARDS (Prayer Journal pill nav)
   ================================================================ */
.cat-card {
    border-radius: var(--lp-r-md);
    padding: 18px 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1);
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}

.cat-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--lp-shadow-sm);
}

.cat-card-active {
    border: 2px solid currentColor;
    box-shadow: var(--lp-shadow-sm);
}

.cat-icon  { font-size: 28px; margin-bottom: 6px; }
.cat-name  { font-size: 13px; font-weight: 800; letter-spacing: 0.2px; }
.cat-count { font-size: 11px; opacity: 0.65; margin-top: 2px; }

/* ================================================================
   WIZARD STEPS
   ================================================================ */
.wizard-step {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 22px 26px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
}

.wizard-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    font-size: 13px;
    font-weight: 800;
    color: white;
    margin-right: 10px;
    box-shadow: 0 2px 10px rgba(59,47,142,0.30);
}

.wizard-step-title {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--lp-text);
    display: inline;
}

.wizard-step-desc {
    font-size: 13px;
    color: var(--lp-text-3);
    margin: 6px 0 12px 40px;
    font-weight: 500;
}

/* ================================================================
   PRAYER PILLS
   ================================================================ */
.prayer-pill {
    display: inline-block;
    padding: 6px 15px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 700;
    margin: 3px 4px;
    transition: transform 0.2s, box-shadow 0.2s;
}

.prayer-pill:hover {
    transform: translateY(-1px);
    box-shadow: var(--lp-shadow-xs);
}

/* ================================================================
   EMPTY STATES
   ================================================================ */
.empty-state {
    text-align: center;
    padding: 52px 24px;
    animation: fadeIn 0.5s ease both;
}

.empty-state-icon {
    font-size: 52px;
    margin-bottom: 14px;
    opacity: 0.45;
    display: block;
}

.empty-state-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 18px;
    color: var(--lp-text-3);
    font-weight: 500;
    margin-bottom: 4px;
}

.empty-state-sub {
    font-size: 13px;
    color: rgba(158,150,171,0.7);
    margin-top: 6px;
    line-height: 1.55;
}

/* ================================================================
   STREAK HERO
   ================================================================ */
.streak-hero {
    border-radius: var(--lp-r-lg);
    padding: 36px 28px;
    margin-bottom: 20px;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 14px 44px rgba(59,47,142,0.28);
}

.streak-num {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 72px;
    font-weight: 700;
    line-height: 1;
    text-shadow: 0 4px 24px rgba(0,0,0,0.32);
}

.streak-label {
    font-size: 11px;
    color: rgba(255,255,255,0.68);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-top: 8px;
    font-weight: 800;
}

/* ================================================================
   CALENDAR / HEATMAP
   ================================================================ */
.cal-header, .heatmap-header {
    text-align: center;
    font-size: 10px;
    color: var(--lp-text-3);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 4px;
}

.cal-day, .heatmap-day {
    text-align: center;
    border-radius: 8px;
    padding: 6px 4px;
    font-size: 13px;
    font-weight: 600;
    margin: 2px;
}

.cal-done, .heatmap-done {
    background: linear-gradient(135deg, var(--lp-primary), #7B4FA8);
    color: white;
    font-weight: 800;
    box-shadow: 0 2px 6px rgba(59,47,142,0.30);
}

.cal-empty    { color: rgba(158,150,171,0.45); }
.heatmap-missed { background: #FFF0EC; color: #FFA07A; }
.heatmap-future { color: rgba(158,150,171,0.38); }

/* ================================================================
   DAY ROWS (Weekly Assignment)
   ================================================================ */
.day-row {
    display: flex;
    align-items: center;
    padding: 13px 18px;
    margin: 5px 0;
    border-radius: var(--lp-r-sm);
    font-size: 15px;
    transition: transform 0.2s ease;
}

.day-done {
    background: linear-gradient(135deg, #E8F5EE, #F4FAF6);
    border: 1px solid rgba(45,106,79,0.10);
}

.day-pending {
    background: linear-gradient(135deg, #FFF4E6, #FFFDF7);
    border: 1px solid rgba(201,152,42,0.10);
}

.day-row:hover  { transform: translateX(3px); }
.day-name       { font-weight: 800; width: 100px; color: var(--lp-text); }
.day-chapters   { flex: 1; color: var(--lp-text-2); }
.day-status     { font-size: 18px; }

/* ================================================================
   SETTINGS
   ================================================================ */
.settings-section {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 22px 26px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
}

/* ================================================================
   FOOTER
   ================================================================ */
.lp-footer {
    text-align: center;
    padding: 28px 20px;
    margin-top: 48px;
    border-top: 1px solid rgba(59,47,142,0.06);
    position: relative;
}

.lp-footer::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 22%; right: 22%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,152,42,0.65), transparent);
}

.lp-footer-brand {
    font-family: 'Playfair Display', 'DM Serif Display', Georgia, serif;
    font-size: 15px;
    font-weight: 700;
    background: linear-gradient(135deg, var(--lp-primary), var(--lp-gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.lp-footer-sub {
    font-size: 11px;
    color: var(--lp-text-3);
    margin-top: 4px;
    letter-spacing: 0.4px;
    font-weight: 600;
}

/* ================================================================
   SIDEBAR
   ================================================================ */
[data-testid="stSidebar"] > div:first-child {
    background:
        radial-gradient(ellipse at 50% 0%,   rgba(59,47,142,0.055) 0%, transparent 52%),
        radial-gradient(ellipse at 50% 100%,  rgba(201,152,42,0.03) 0%, transparent 52%),
        #F2F0EB;
    border-right: 1px solid rgba(59,47,142,0.06) !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
    background: rgba(59,47,142,0.06) !important;
    transform: translateX(3px);
}

[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
    background: rgba(59,47,142,0.08) !important;
    border-left: 3px solid var(--lp-primary) !important;
    color: var(--lp-primary) !important;
}

/* ================================================================
   TABS
   ================================================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(59,47,142,0.04);
    border-radius: 14px;
    padding: 5px;
    border: 1px solid rgba(59,47,142,0.06);
}

.stTabs [data-baseweb="tab-list"] button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    font-family: 'Nunito', sans-serif !important;
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1) !important;
    color: var(--lp-text-2) !important;
    padding: 8px 16px !important;
}

.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background: var(--lp-surface) !important;
    box-shadow: 0 2px 10px rgba(59,47,142,0.12) !important;
    color: var(--lp-primary) !important;
}

/* ================================================================
   BUTTONS
   ================================================================ */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1) !important;
    letter-spacing: 0.2px !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--lp-primary) 0%, var(--lp-primary-light) 100%) !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(59,47,142,0.32) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 24px rgba(59,47,142,0.40) !important;
    transform: translateY(-2px) !important;
}

.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(59,47,142,0.28) !important;
}

.stButton > button[kind="secondary"] {
    border: 1.5px solid rgba(59,47,142,0.14) !important;
    color: var(--lp-primary) !important;
    background: transparent !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--lp-primary) !important;
    background: rgba(59,47,142,0.04) !important;
    transform: translateY(-1px) !important;
}

/* ================================================================
   FORM INPUTS
   ================================================================ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 1.5px solid rgba(59,47,142,0.12) !important;
    font-family: 'Nunito', sans-serif !important;
    transition: all 0.2s ease !important;
    background: rgba(255,255,255,0.85) !important;
    color: var(--lp-text) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--lp-primary) !important;
    box-shadow: 0 0 0 3px rgba(59,47,142,0.09) !important;
    background: white !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: var(--lp-text-3) !important;
    font-style: italic;
}

/* ================================================================
   SELECT / MULTISELECT / SLIDER
   ================================================================ */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-radius: 10px !important;
    border: 1.5px solid rgba(59,47,142,0.12) !important;
    font-family: 'Nunito', sans-serif !important;
    transition: border-color 0.2s !important;
}

.stSelectbox > div > div:hover,
.stMultiSelect > div > div:hover {
    border-color: rgba(59,47,142,0.24) !important;
}

/* ================================================================
   FORMS
   ================================================================ */
[data-testid="stForm"] {
    border: 1px solid rgba(59,47,142,0.08) !important;
    border-radius: var(--lp-r-md) !important;
    padding: 22px !important;
    background: rgba(255,255,255,0.75) !important;
    box-shadow: var(--lp-shadow-xs) !important;
    backdrop-filter: blur(8px) !important;
}

/* ================================================================
   EXPANDERS
   ================================================================ */
[data-testid="stExpander"] {
    border: 1px solid rgba(59,47,142,0.08) !important;
    border-radius: 12px !important;
    overflow: hidden;
    transition: border-color 0.2s !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(59,47,142,0.15) !important;
}

/* ================================================================
   ALERT / INFO BOXES
   ================================================================ */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

/* ================================================================
   DOWNLOAD BUTTON
   ================================================================ */
[data-testid="stDownloadButton"] > button {
    border-radius: 10px !important;
    font-weight: 800 !important;
}

/* ================================================================
   METRIC (native Streamlit)
   ================================================================ */
[data-testid="stMetric"] {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 16px;
    box-shadow: var(--lp-shadow-xs);
}

/* ================================================================
   MOBILE — 768px
   ================================================================ */
@media (max-width: 768px) {
    [data-testid="column"] { padding: 0 4px !important; }

    .stTabs [data-baseweb="tab-list"] button {
        font-size: 12px !important;
        padding: 7px 10px !important;
    }

    [data-testid="stSegmentedControl"] button {
        font-size: 12px !important;
        padding: 6px 10px !important;
    }

    .stTextInput > div, .stSelectbox > div, .stMultiSelect > div {
        font-size: 14px !important;
    }

    .hero-section    { padding: 28px 20px; border-radius: 18px; margin-bottom: 16px; }
    .hero-name       { font-size: 28px; }
    .hero-greeting   { font-size: 10px; letter-spacing: 2.5px; }
    .hero-date       { font-size: 12px; }
    .hero-verse      { font-size: 14px; padding: 14px 16px 14px 26px; margin-top: 16px; }
    .hero-verse::before { font-size: 42px; left: 10px; }

    .page-header         { padding: 20px 20px 18px; border-radius: 18px; margin-bottom: 16px; }
    .page-header-title   { font-size: 20px; }
    .page-header-sub     { font-size: 12px; }

    .metric-card, .stat-card { padding: 14px 10px; border-radius: 12px; }
    .metric-value { font-size: 24px; }
    .stat-value   { font-size: 22px; }
    .metric-label, .stat-label { font-size: 9px; letter-spacing: 1px; }

    .section-card  { padding: 18px; border-radius: 12px; }
    .section-icon  { font-size: 26px; }
    .section-title { font-size: 16px; }
    .section-desc  { font-size: 12px; }

    .entry-card    { padding: 13px 15px; border-radius: 12px; }
    .today-card    { padding: 16px 18px; border-radius: 12px; }
    .today-title   { font-size: 14px; }
    .today-detail  { font-size: 13px; }

    .progress-section { padding: 16px 18px; border-radius: 12px; }

    .prayer-card       { padding: 14px 16px; }
    .prayer-name       { font-size: 15px; }
    .prayer-title-row  { flex-wrap: wrap; gap: 6px; }

    .cat-card  { padding: 12px 8px; border-radius: 12px; }
    .cat-icon  { font-size: 24px; }
    .cat-name  { font-size: 11px; }
    .cat-count { font-size: 10px; }

    .day-row     { padding: 10px 12px; font-size: 13px; }
    .day-name    { width: 72px; font-size: 13px; }
    .day-status  { font-size: 16px; }

    .streak-hero { padding: 24px 20px; border-radius: 18px; }
    .streak-num  { font-size: 52px; }
    .streak-label { font-size: 10px; }

    .report-card { padding: 18px; font-size: 15px; line-height: 1.75; }
    .goal-banner { font-size: 13px; padding: 12px 16px 12px 20px; }

    .empty-state       { padding: 36px 16px; }
    .empty-state-icon  { font-size: 40px; }
    .empty-state-title { font-size: 15px; }

    .section-label { font-size: 10px; letter-spacing: 2px; }
    .prayer-pill   { padding: 5px 12px; font-size: 12px; margin: 2px 3px; }

    .wizard-step         { padding: 16px 18px; }
    .wizard-step-title   { font-size: 15px; }
    .wizard-step-desc    { margin-left: 0; margin-top: 8px; }

    .sermon-card     { padding: 14px 16px; }
    .scripture-block { font-size: 14px; padding: 10px 12px; }
}

/* ================================================================
   MOBILE — 480px
   ================================================================ */
@media (max-width: 480px) {
    .hero-section    { padding: 22px 16px; border-radius: 14px; }
    .hero-name       { font-size: 24px; }
    .hero-verse      { font-size: 13px; padding: 12px 14px 12px 24px; }
    .hero-verse::before { font-size: 36px; }

    .page-header       { padding: 16px; border-radius: 14px; }
    .page-header-title { font-size: 18px; }

    .metric-value { font-size: 20px; }
    .stat-value   { font-size: 18px; }
    .streak-num   { font-size: 42px; }

    .day-name  { width: 60px; font-size: 12px; }
    .day-row   { padding: 8px 10px; font-size: 12px; }

    .stTabs [data-baseweb="tab-list"] button {
        font-size: 11px !important;
        padding: 6px 8px !important;
    }
}
</style>
"""

# ==================== ENHANCEMENT CSS ====================
# Extra Streamlit-internal overrides injected separately
ENHANCEMENT_CSS = """
<style>
    [data-testid="stForm"] {
        border: 1px solid rgba(59,47,142,0.08) !important;
        border-radius: 16px !important;
        padding: 22px !important;
        background: rgba(255,255,255,0.75) !important;
        box-shadow: 0 2px 8px rgba(26,22,40,0.04) !important;
        backdrop-filter: blur(8px) !important;
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(59,47,142,0.08) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(59,47,142,0.16) !important;
    }
    /* Checkbox and toggle refinements */
    [data-testid="stCheckbox"] label,
    [data-testid="stToggle"] label {
        font-family: 'Nunito', sans-serif !important;
        font-weight: 600 !important;
        color: #574F6E !important;
    }
    /* Slider track */
    [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderTrack"] {
        background: rgba(59,47,142,0.10) !important;
    }
    /* Caption */
    .stCaption {
        font-family: 'Nunito', sans-serif !important;
        color: #9E96AB !important;
    }
    /* Selectbox dropdown font */
    [data-baseweb="select"] [data-baseweb="menu"] {
        border-radius: 12px !important;
        border: 1px solid rgba(59,47,142,0.10) !important;
        box-shadow: 0 8px 24px rgba(26,22,40,0.10) !important;
        font-family: 'Nunito', sans-serif !important;
    }
    /* Multi-select tags */
    [data-baseweb="tag"] {
        background: rgba(59,47,142,0.10) !important;
        border-radius: 8px !important;
        color: #3B2F8E !important;
        font-weight: 700 !important;
        font-family: 'Nunito', sans-serif !important;
    }
</style>
"""


def inject_styles():
    """Inject the full Logos Pulse design system into the current page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    st.markdown(ENHANCEMENT_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render the gradient page header with optional subtitle."""
    sub_html = f'<div class="page-header-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-title">{icon} {title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def section_label(text: str):
    """Render a styled section label with trailing gold rule."""
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def empty_state(icon: str, title: str, subtitle: str = ""):
    """Render a centered empty-state placeholder."""
    sub_html = f'<div class="empty-state-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def spacer(height: int = 16):
    """Render a vertical spacer."""
    st.markdown(f"<div style='height:{height}px'></div>", unsafe_allow_html=True)


def footer():
    """Render the branded footer."""
    st.markdown("""
    <div class="lp-footer">
        <div class="lp-footer-brand">🙏 Logos Pulse</div>
        <div class="lp-footer-sub">Spiritual Growth Tracker &bull; Built with faith</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Render the sidebar logo block."""
    st.markdown("""
    <div style="text-align:center; padding:10px 0 18px 0;">
        <div style="font-size:34px; margin-bottom:6px;">🙏</div>
        <div style="
            font-family:'Playfair Display','DM Serif Display',Georgia,serif;
            font-size:19px;
            font-weight:700;
            background: linear-gradient(135deg, #3B2F8E, #C9982A);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.3px;
        ">
            Logos Pulse
        </div>
        <div style="
            font-size:10px;
            color:#9E96AB;
            letter-spacing:2px;
            text-transform:uppercase;
            font-weight:700;
            margin-top:2px;
            font-family:'Nunito',sans-serif;
        ">
            Spiritual Tracker
        </div>
    </div>
    """, unsafe_allow_html=True)
