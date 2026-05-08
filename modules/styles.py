"""
Logos Pulse Design System — Daybreak Final
Warm terra palette with Cormorant display type and Jost UI sans-serif.
"""

import streamlit as st

# ==================== DESIGN TOKENS ====================
COLORS = {
    "primary":          "#B85A30",
    "primary_light":    "#D46A38",
    "primary_dark":     "#8C3E1E",
    "accent_gold":      "#C48A1C",
    "accent_gold_light":"#DFA830",
    "accent_gold_dark": "#8A6018",
    "accent_gold_pale": "#FDF6E3",
    "surface":          "#F9F5EF",
    "surface_warm":     "#FFFFFF",
    "card_bg":          "#FFFFFF",
    "card_border":      "rgba(165, 135, 65, 0.14)",
    "text_primary":     "#1A1208",
    "text_secondary":   "#5A4A32",
    "text_muted":       "#A09080",
    "success":          "#1E5E3E",
    "success_bg":       "#E4F2EB",
    "warning":          "#A84C16",
    "warning_bg":       "#FFF1E4",
    "danger":           "#9C2424",
    "streak_fire":      "#D44A22",
    "streak_gold":      "#C48A1C",
}

# ==================== SHARED CSS ====================
SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500&family=Jost:wght@300;400;500;600;700;800&display=swap');

/* ================================================================
   DESIGN TOKENS
   ================================================================ */
:root {
    --lp-primary:        #B85A30;
    --lp-primary-light:  #D46A38;
    --lp-primary-dark:   #8C3E1E;
    --lp-gold:           #C48A1C;
    --lp-gold-light:     #DFA830;
    --lp-gold-dark:      #8A6018;
    --lp-gold-pale:      #FDF6E3;
    --lp-bg:             #F9F5EF;
    --lp-surface:        #FFFFFF;
    --lp-border:         rgba(165, 135, 65, 0.14);
    --lp-border-strong:  rgba(165, 135, 65, 0.30);
    --lp-text:           #1A1208;
    --lp-text-2:         #5A4A32;
    --lp-text-3:         #A09080;
    --lp-success:        #1E5E3E;
    --lp-warning:        #A84C16;
    --lp-danger:         #9C2424;
    --lp-r-sm:  10px;
    --lp-r-md:  16px;
    --lp-r-lg:  22px;
    --lp-shadow-xs: 0 1px 4px rgba(184,90,48,0.04), 0 1px 2px rgba(26,18,8,0.03);
    --lp-shadow-sm: 0 2px 10px rgba(184,90,48,0.06), 0 1px 4px rgba(26,18,8,0.04);
    --lp-shadow-md: 0 6px 24px rgba(184,90,48,0.09), 0 2px 8px rgba(26,18,8,0.05);
    --lp-shadow-lg: 0 14px 44px rgba(184,90,48,0.12), 0 4px 12px rgba(26,18,8,0.06);
    --lp-glow-indigo: 0 6px 28px rgba(184,90,48,0.22);
    --lp-glow-gold:   0 6px 28px rgba(196,144,42,0.20);
    --lp-gold-stripe: linear-gradient(90deg,
        transparent 0%,
        var(--lp-gold) 30%,
        var(--lp-gold-light) 50%,
        var(--lp-gold) 70%,
        transparent 100%
    );
}

/* ================================================================
   HIDE ALL STREAMLIT NATIVE CHROME
   ================================================================ */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNavItems"],
#MainMenu, .stAppToolbar, .stDeployButton,
button[kind="header"], header { display: none !important; }

#MainMenu { visibility: hidden !important; }

/* ================================================================
   LAYOUT RESET — strip Streamlit's default header spacing
   ================================================================ */

/* The AppViewContainer wraps everything — remove any top offset */
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
    margin-top:  0 !important;
}

/* stMain is the scrollable content area — remove Streamlit's
   built-in header-compensation padding */
[data-testid="stMain"],
.stMain,
.main {
    padding-top: 0 !important;
    overflow-x: hidden !important;
}

/* The actual content block — our fixed nav is 56px, so push
   content down just enough, then cap width and center it */
[data-testid="stMainBlockContainer"],
.main .block-container,
.block-container {
    padding-top:    72px !important;   /* 56px nav + 16px breathing room */
    padding-left:   24px !important;
    padding-right:  24px !important;
    padding-bottom: 80px !important;
    max-width:      1180px !important;
    margin-left:    auto !important;
    margin-right:   auto !important;
}

/* Streamlit sometimes wraps in an extra div — handle it */
[data-testid="stVerticalBlock"] { width: 100% !important; }

/* ================================================================
   GLOBAL BASE
   ================================================================ */
.stApp {
    font-family: 'Jost', -apple-system, sans-serif !important;
    background:
        radial-gradient(ellipse at 6% 6%,   rgba(184,90,48,0.055) 0%, transparent 40%),
        radial-gradient(ellipse at 94% 90%,  rgba(196,144,42,0.05)  0%, transparent 40%),
        radial-gradient(ellipse at 50% -4%,  rgba(212,106,56,0.035) 0%, transparent 45%),
        radial-gradient(ellipse at 50% 108%, rgba(138,96,108,0.025) 0%, transparent 45%),
        #F9F5EF !important;
    color: var(--lp-text) !important;
}

h1, h2, h3 {
    font-family: 'Cormorant', Georgia, serif !important;
    color: var(--lp-text) !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
}

/* ================================================================
   KEYFRAMES
   ================================================================ */
@keyframes riseUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0);    }
}
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
@keyframes aureate {
    0%, 100% { box-shadow: 0 4px 20px rgba(196,144,42,0.10); }
    50%       { box-shadow: 0 4px 30px rgba(196,144,42,0.24), 0 0 0 3px rgba(196,144,42,0.07); }
}
@keyframes breathe {
    0%, 100% { box-shadow: 0 4px 16px rgba(168,76,22,0.08); }
    50%       { box-shadow: 0 4px 24px rgba(168,76,22,0.18), 0 0 0 3px rgba(196,144,42,0.06); }
}
@keyframes goldPulse {
    0%, 100% { border-color: rgba(196,144,42,0.22); }
    50%       { border-color: rgba(196,144,42,0.55); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(10px); }
    to   { opacity: 1; transform: translateX(0);    }
}
@keyframes ornamentSpin {
    from { transform: rotate(0deg);   }
    to   { transform: rotate(360deg); }
}

/* ================================================================
   HERO SECTION (Dashboard)
   ================================================================ */
.hero-section {
    background: linear-gradient(148deg, rgba(253,250,245,0.97), rgba(247,242,234,0.94));
    border: 1px solid rgba(184,90,48,0.14);
    border-radius: var(--lp-r-lg);
    padding: 46px 38px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 28px 70px rgba(184,90,48,0.12),
        0 6px 18px rgba(184,90,48,0.08),
        inset 0 1px 0 rgba(255,255,255,0.90);
    animation: riseUp 0.7s cubic-bezier(0.22,1,0.36,1) both;
    color: #1A1208;
}

/* Fine diagonal hatching */
.hero-section::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        -52deg,
        rgba(255,255,255,0.014) 0px,
        rgba(255,255,255,0.014) 1px,
        transparent 1px,
        transparent 14px
    );
    pointer-events: none;
    border-radius: inherit;
}

/* Gold orb top-right */
.hero-section::after {
    content: '';
    position: absolute;
    top:   -80px;
    right: -80px;
    width:  330px;
    height: 330px;
    background: radial-gradient(circle, rgba(196,144,42,0.16) 0%, transparent 66%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-greeting {
    font-family: 'Cormorant', serif;
    font-size: 10px;
    font-weight: 600;
    color: rgba(196,138,28,0.92);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 10px;
    position: relative;
}

.hero-name {
    font-family: 'Cormorant', serif;
    font-size: 42px;
    font-weight: 700;
    color: #1A1208;
    line-height: 1.12;
    margin-bottom: 5px;
    position: relative;
    text-shadow: none;
    letter-spacing: 0.02em;
}

.hero-date {
    font-size: 12px;
    color: rgba(26,18,8,0.42);
    position: relative;
    font-weight: 600;
    letter-spacing: 0.6px;
    font-family: 'Jost', sans-serif;
}

.hero-verse {
    margin-top: 24px;
    padding: 20px 22px 20px 36px;
    background: rgba(255,255,255,0.60);
    border-radius: 14px;
    font-family: 'Cormorant', 'Cormorant', Georgia, serif;
    font-style: italic;
    font-size: 16px;
    color: rgba(26,18,8,0.88);
    line-height: 1.82;
    border: 1px solid rgba(196,138,28,0.24);
    position: relative;
    backdrop-filter: blur(6px);
}

.hero-verse::before {
    content: '\201C';
    position: absolute;
    top: -4px;
    left: 12px;
    font-size: 60px;
    color: rgba(196,138,28,0.40);
    font-family: 'Cormorant', Georgia, serif;
    line-height: 1;
    font-style: normal;
}

/* ================================================================
   PAGE HEADER
   ================================================================ */
.page-header {
    background: linear-gradient(148deg, rgba(253,250,245,0.97), rgba(247,242,234,0.94));
    border: 1px solid rgba(184,90,48,0.14);
    border-radius: var(--lp-r-lg);
    padding: 28px 34px 26px 34px;
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 16px 50px rgba(184,90,48,0.10),
        0 2px 10px rgba(184,90,48,0.07),
        inset 0 1px 0 rgba(255,255,255,0.90);
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
    color: #1A1208;
}

.page-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        -46deg,
        rgba(255,255,255,0.010) 0px,
        rgba(255,255,255,0.010) 1px,
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
    background: var(--lp-gold-stripe);
    opacity: 0.85;
}

.page-header-title {
    font-family: 'Cormorant', Georgia, serif;
    font-size: 24px;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: #1A1208;
    position: relative;
    text-shadow: none;
}

.page-header-sub {
    font-size: 12px;
    color: rgba(26,18,8,0.50);
    margin-top: 6px;
    font-weight: 600;
    letter-spacing: 0.4px;
    position: relative;
    font-family: 'Jost', sans-serif;
}

/* ================================================================
   ORNAMENTAL DIVIDER
   ================================================================ */
.lp-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 22px 0;
}

.lp-divider::before,
.lp-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,144,42,0.3), transparent);
}

.lp-divider-ornament {
    width: 8px;
    height: 8px;
    border: 1px solid rgba(196,144,42,0.5);
    transform: rotate(45deg);
    flex-shrink: 0;
}

/* ================================================================
   ANNOUNCEMENT CARD
   ================================================================ */
.announcement-card {
    background: linear-gradient(135deg, rgba(184,90,48,0.055), rgba(212,106,56,0.038));
    border: 1px solid rgba(184,90,48,0.12);
    border-radius: 12px;
    padding: 12px 18px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
}

.announcement-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, var(--lp-primary-light), var(--lp-gold));
    border-radius: 3px 0 0 3px;
}

.announcement-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--lp-primary);
    font-family: 'Cormorant', serif;
    letter-spacing: 0.01em;
}

.announcement-body {
    font-size: 13px;
    color: var(--lp-primary-light);
    margin-top: 4px;
    line-height: 1.6;
}

/* ================================================================
   GROWTH BADGE
   ================================================================ */
.growth-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    font-family: 'Jost', sans-serif;
}

.growth-badge-seed    { background: rgba(138,96,24,0.08);  color: #8A6018; border: 1px solid rgba(138,96,24,0.18); }
.growth-badge-sprout  { background: rgba(30,94,62,0.08);   color: #1E5E3E; border: 1px solid rgba(30,94,62,0.18); }
.growth-badge-sapling { background: rgba(184,90,48,0.07);  color: #B85A30; border: 1px solid rgba(184,90,48,0.16); }
.growth-badge-tree    { background: rgba(196,144,42,0.10); color: #8A6018; border: 1px solid rgba(196,144,42,0.22); animation: aureate 3.5s ease-in-out infinite; }
.growth-badge-forest  { background: linear-gradient(135deg, rgba(184,90,48,0.10), rgba(196,144,42,0.08)); color: #B85A30; border: 1px solid rgba(196,144,42,0.28); animation: aureate 3s ease-in-out infinite; }

/* ================================================================
   SECTION LABEL
   ================================================================ */
.section-label {
    font-size: 10px;
    color: var(--lp-text-3);
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: 800;
    font-family: 'Cormorant', serif;
    margin: 26px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(196,144,42,0.40) 0%, transparent 100%);
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
    transition: all 0.32s cubic-bezier(0.22,1,0.36,1);
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
    opacity: 0.35;
    transition: opacity 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--lp-glow-indigo), var(--lp-shadow-md);
    border-color: rgba(184,90,48,0.18);
}

.metric-card:hover::before { opacity: 1; }

.metric-value {
    font-family: 'Cormorant', Georgia, serif;
    font-size: 34px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: 0.01em;
}

.metric-label {
    font-size: 10px;
    color: var(--lp-text-3);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 800;
    font-family: 'Jost', sans-serif;
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
    transition: all 0.32s cubic-bezier(0.22,1,0.36,1);
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
    opacity: 0.35;
    transition: opacity 0.3s;
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--lp-glow-indigo);
    border-color: rgba(184,90,48,0.16);
}

.stat-card:hover::before { opacity: 1; }

.stat-value {
    font-family: 'Cormorant', Georgia, serif;
    font-size: 30px;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: 0.01em;
}

.stat-label {
    font-size: 10px;
    color: var(--lp-text-3);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 6px;
    font-weight: 800;
    font-family: 'Jost', sans-serif;
}

/* ================================================================
   SECTION CARDS (toolkit / quick-access cards)
   ================================================================ */
.section-card {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 28px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.38s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
}

.section-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0.28;
    transition: opacity 0.3s;
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
    transform: translateY(-6px);
    box-shadow: var(--lp-shadow-lg), 0 0 0 1px rgba(196,144,42,0.10);
    border-color: rgba(196,144,42,0.26);
}

.section-card:hover::before { opacity: 0.7; }

.section-card:hover::after {
    opacity: 1;
    animation: shimmer 2.2s linear infinite;
}

.section-icon { font-size: 30px; margin-bottom: 12px; }

.section-title {
    font-family: 'Cormorant', Georgia, serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--lp-text);
    margin-bottom: 7px;
    letter-spacing: 0.01em;
}

.section-desc {
    font-size: 13px;
    color: var(--lp-text-3);
    line-height: 1.65;
}

/* ================================================================
   TODAY STATUS CARDS
   ================================================================ */
.today-card {
    border-radius: var(--lp-r-md);
    padding: 22px 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.45s cubic-bezier(0.22,1,0.36,1) both;
}

.today-done {
    background: linear-gradient(135deg, #E4F2EB 0%, #F4FAF6 100%);
    border: 1px solid rgba(30,94,62,0.20);
    box-shadow: 0 4px 18px rgba(30,94,62,0.08), inset 0 1px 0 rgba(255,255,255,0.85);
}

.today-done::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 90px; height: 90px;
    background: radial-gradient(circle at top right, rgba(30,94,62,0.09) 0%, transparent 70%);
    pointer-events: none;
}

.today-pending {
    background: linear-gradient(135deg, #FFF1E4 0%, #FFFDF7 100%);
    border: 1px solid rgba(168,76,22,0.22);
    box-shadow: 0 4px 18px rgba(168,76,22,0.07), inset 0 1px 0 rgba(255,255,255,0.85);
    animation: fadeInUp 0.45s cubic-bezier(0.22,1,0.36,1) both, breathe 4s ease-in-out 1.2s infinite;
}

.today-pending::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 90px; height: 90px;
    background: radial-gradient(circle at top right, rgba(196,144,42,0.11) 0%, transparent 70%);
    pointer-events: none;
}

.today-title {
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 9px;
    position: relative;
    font-family: 'Jost', sans-serif;
}

.today-detail {
    font-size: 14px;
    color: var(--lp-text-2);
    line-height: 1.65;
    position: relative;
}

/* ================================================================
   PROGRESS BARS
   ================================================================ */
.progress-section {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 22px 28px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
    transition: box-shadow 0.3s;
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
    position: relative;
    overflow: hidden;
}

.progress-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0.28;
    transition: opacity 0.3s;
}

.progress-section:hover { box-shadow: var(--lp-shadow-sm); }
.progress-section:hover::before { opacity: 0.65; }

.progress-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--lp-text-2);
    margin-bottom: 14px;
}

.progress-bar-bg {
    background: linear-gradient(90deg, rgba(184,90,48,0.07), rgba(196,144,42,0.07));
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
    box-shadow: 0 0 12px rgba(184,90,48,0.30);
    transition: width 0.8s cubic-bezier(0.22,1,0.36,1);
}

.progress-label {
    font-size: 12px;
    color: var(--lp-text-3);
    margin-top: 8px;
    font-weight: 700;
    font-family: 'Jost', sans-serif;
}

/* ================================================================
   ENTRY / DATA CARDS
   ================================================================ */
.entry-card {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 18px 24px;
    margin-bottom: 10px;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
}

.entry-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0.22;
    transition: opacity 0.25s;
}

.entry-card:hover {
    box-shadow: var(--lp-shadow-sm), 0 0 0 1px rgba(42,29,126,0.06);
    border-color: rgba(42,29,126,0.12);
    transform: translateY(-1px);
}

.entry-card:hover::before { opacity: 0.7; }

/* ================================================================
   REPORT CARD (parchment / scripture feel)
   ================================================================ */
.report-card {
    background: linear-gradient(135deg, #FFFDF7, #FFF8EC);
    border: 1px solid rgba(196,144,42,0.24);
    border-radius: var(--lp-r-md);
    padding: 30px;
    font-family: 'Cormorant', 'Cormorant', Georgia, serif;
    font-size: 17px;
    line-height: 1.92;
    color: #2A1A08;
    white-space: pre-line;
    box-shadow:
        0 4px 22px rgba(196,144,42,0.09),
        inset 0 1px 0 rgba(255,255,255,0.85);
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
    background: linear-gradient(135deg, rgba(42,29,126,0.055), rgba(75,61,192,0.040));
    border: 1px solid rgba(42,29,126,0.10);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px 14px 24px;
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
    padding: 20px 26px;
    margin-bottom: 12px;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
}

.prayer-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0.22;
    transition: opacity 0.25s;
}

.prayer-card:hover {
    box-shadow: var(--lp-shadow-sm);
    border-color: rgba(42,29,126,0.14);
    transform: translateY(-1px);
}

.prayer-card:hover::before { opacity: 0.75; }

.prayer-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.prayer-name {
    font-family: 'Cormorant', 'Cormorant', Georgia, serif;
    font-size: 17px;
    font-weight: 600;
    color: var(--lp-text);
    letter-spacing: 0.01em;
}

.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
    font-family: 'Jost', sans-serif;
}

/* ================================================================
   SCRIPTURE / CONFESSION / DECLARATION BLOCKS
   ================================================================ */
.scripture-block {
    background: linear-gradient(135deg, #FFFDF7, #FFFAF0);
    border-left: 3px solid;
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 8px;
    font-family: 'Cormorant', 'Cormorant', Georgia, serif;
    font-size: 15.5px;
    line-height: 1.88;
    color: #2A1A08;
}

.confession-block {
    background: linear-gradient(135deg, #E4F2EB, #F4FAF6);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px;
    font-weight: 700;
    color: var(--lp-success);
    line-height: 1.80;
    border: 1px solid rgba(30,94,62,0.15);
}

.declaration-block {
    background: linear-gradient(135deg, #FFF1E4, #FFFCF5);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px;
    font-weight: 800;
    color: var(--lp-warning);
    line-height: 1.80;
    border: 1px solid rgba(168,76,22,0.14);
}

/* ================================================================
   SERMON CARDS
   ================================================================ */
.sermon-card {
    background: linear-gradient(135deg, var(--lp-surface), #FFFDF7);
    border: 1px solid rgba(196,144,42,0.16);
    border-radius: var(--lp-r-md);
    padding: 20px 26px;
    margin: 10px 0;
    box-shadow: var(--lp-shadow-xs);
    transition: all 0.3s cubic-bezier(0.22,1,0.36,1);
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
    position: relative;
    overflow: hidden;
}

.sermon-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-gold), var(--lp-primary), var(--lp-gold));
    opacity: 0.30;
    transition: opacity 0.3s;
}

.sermon-card:hover {
    box-shadow: var(--lp-glow-gold);
    border-color: rgba(196,144,42,0.30);
    transform: translateY(-2px);
}

.sermon-card:hover::before { opacity: 0.9; }

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

.cat-icon  { font-size: 28px; margin-bottom: 7px; }
.cat-name  { font-size: 13px; font-weight: 800; letter-spacing: 0.3px; font-family: 'Jost', sans-serif; }
.cat-count { font-size: 11px; opacity: 0.65; margin-top: 3px; }

/* ================================================================
   WIZARD STEPS
   ================================================================ */
.wizard-step {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 22px 28px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
    animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
    position: relative;
    overflow: hidden;
}

.wizard-step::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0.28;
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
    box-shadow: 0 2px 10px rgba(42,29,126,0.32);
    font-family: 'Jost', sans-serif;
}

.wizard-step-title {
    font-family: 'Cormorant', 'Cormorant', Georgia, serif;
    font-size: 16px;
    font-weight: 600;
    color: var(--lp-text);
    display: inline;
    letter-spacing: 0.01em;
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
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 700;
    margin: 3px 4px;
    transition: transform 0.2s, box-shadow 0.2s;
    font-family: 'Jost', sans-serif;
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
    padding: 56px 24px;
    animation: fadeIn 0.5s ease both;
}

.empty-state-icon {
    font-size: 52px;
    margin-bottom: 16px;
    opacity: 0.40;
    display: block;
}

.empty-state-title {
    font-family: 'Cormorant', Georgia, serif;
    font-size: 18px;
    color: var(--lp-text-3);
    font-weight: 500;
    margin-bottom: 6px;
    letter-spacing: 0.02em;
}

.empty-state-sub {
    font-size: 13px;
    color: rgba(138,133,160,0.7);
    margin-top: 8px;
    line-height: 1.58;
}

/* ================================================================
   STREAK HERO
   ================================================================ */
.streak-hero {
    border-radius: var(--lp-r-lg);
    padding: 38px 28px;
    margin-bottom: 20px;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 16px 50px rgba(42,29,126,0.30);
}

.streak-num {
    font-family: 'Cormorant', 'Cormorant', Georgia, serif;
    font-size: 72px;
    font-weight: 700;
    line-height: 1;
    text-shadow: 0 4px 28px rgba(0,0,0,0.32);
    letter-spacing: 0.02em;
}

.streak-label {
    font-size: 11px;
    color: rgba(255,255,255,0.65);
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-top: 10px;
    font-weight: 800;
    font-family: 'Cormorant', sans-serif;
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
    letter-spacing: 0.6px;
    padding: 4px;
    font-family: 'Jost', sans-serif;
}

.cal-day, .heatmap-day {
    text-align: center;
    border-radius: 8px;
    padding: 6px 4px;
    font-size: 13px;
    font-weight: 600;
    margin: 2px;
    font-family: 'Jost', sans-serif;
}

.cal-done, .heatmap-done {
    background: linear-gradient(135deg, var(--lp-primary), #6B3FA8);
    color: white;
    font-weight: 800;
    box-shadow: 0 2px 8px rgba(42,29,126,0.32);
}

.cal-empty    { color: rgba(138,133,160,0.45); }
.heatmap-missed { background: #FFF0EC; color: #FFA07A; }
.heatmap-future { color: rgba(138,133,160,0.38); }

/* ================================================================
   DAY ROWS (Weekly Assignment)
   ================================================================ */
.day-row {
    display: flex;
    align-items: center;
    padding: 13px 20px;
    margin: 5px 0;
    border-radius: var(--lp-r-sm);
    font-size: 15px;
    transition: transform 0.2s ease;
}

.day-done {
    background: linear-gradient(135deg, #E4F2EB, #F4FAF6);
    border: 1px solid rgba(30,94,62,0.11);
}

.day-pending {
    background: linear-gradient(135deg, #FFF1E4, #FFFDF7);
    border: 1px solid rgba(196,144,42,0.11);
}

.day-row:hover  { transform: translateX(3px); }
.day-name       { font-weight: 800; width: 100px; color: var(--lp-text); font-family: 'Jost', sans-serif; }
.day-chapters   { flex: 1; color: var(--lp-text-2); }
.day-status     { font-size: 18px; }

/* ================================================================
   SETTINGS
   ================================================================ */
.settings-section {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 24px 28px;
    margin-bottom: 16px;
    box-shadow: var(--lp-shadow-xs);
    position: relative;
    overflow: hidden;
}

.settings-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    opacity: 0.22;
}

/* ================================================================
   FOOTER
   ================================================================ */
.lp-footer {
    text-align: center;
    padding: 30px 20px;
    margin-top: 52px;
    border-top: 1px solid rgba(42,29,126,0.07);
    position: relative;
}

.lp-footer::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,144,42,0.70), transparent);
}

.lp-footer-brand {
    font-family: 'Cormorant', 'Cormorant', Georgia, serif;
    font-size: 15px;
    font-weight: 600;
    background: linear-gradient(135deg, var(--lp-primary), var(--lp-gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.04em;
}

.lp-footer-sub {
    font-size: 11px;
    color: var(--lp-text-3);
    margin-top: 4px;
    letter-spacing: 0.5px;
    font-weight: 600;
    font-family: 'Jost', sans-serif;
}

/* ================================================================
   TABS
   ================================================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(42,29,126,0.04);
    border-radius: 14px;
    padding: 5px;
    border: 1px solid rgba(42,29,126,0.07);
}

.stTabs [data-baseweb="tab-list"] button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    font-family: 'Jost', sans-serif !important;
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1) !important;
    color: var(--lp-text-2) !important;
    padding: 8px 18px !important;
}

.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background: var(--lp-surface) !important;
    box-shadow: 0 2px 12px rgba(42,29,126,0.13) !important;
    color: var(--lp-primary) !important;
}

/* ================================================================
   BUTTONS
   ================================================================ */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    font-family: 'Jost', sans-serif !important;
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1) !important;
    letter-spacing: 0.3px !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(138deg, var(--lp-primary) 0%, var(--lp-primary-light) 100%) !important;
    border: none !important;
    box-shadow: 0 4px 18px rgba(42,29,126,0.34), inset 0 1px 0 rgba(255,255,255,0.12) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 28px rgba(42,29,126,0.42), inset 0 1px 0 rgba(255,255,255,0.14) !important;
    transform: translateY(-2px) !important;
}

.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px rgba(42,29,126,0.30) !important;
}

.stButton > button[kind="secondary"] {
    border: 1.5px solid rgba(42,29,126,0.16) !important;
    color: var(--lp-primary) !important;
    background: transparent !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--lp-primary) !important;
    background: rgba(42,29,126,0.04) !important;
    transform: translateY(-1px) !important;
}

/* ================================================================
   FORM INPUTS
   ================================================================ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 1.5px solid rgba(42,29,126,0.13) !important;
    font-family: 'Jost', sans-serif !important;
    transition: all 0.22s ease !important;
    background: rgba(254,252,248,0.90) !important;
    color: var(--lp-text) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--lp-primary) !important;
    box-shadow: 0 0 0 3px rgba(42,29,126,0.09) !important;
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
    border: 1.5px solid rgba(42,29,126,0.13) !important;
    font-family: 'Jost', sans-serif !important;
    transition: border-color 0.22s !important;
}

.stSelectbox > div > div:hover,
.stMultiSelect > div > div:hover {
    border-color: rgba(42,29,126,0.26) !important;
}

/* ================================================================
   FORMS
   ================================================================ */
[data-testid="stForm"] {
    border: 1px solid rgba(42,29,126,0.09) !important;
    border-radius: var(--lp-r-md) !important;
    padding: 24px !important;
    background: rgba(254,252,248,0.80) !important;
    box-shadow: var(--lp-shadow-xs) !important;
    backdrop-filter: blur(8px) !important;
}

/* ================================================================
   EXPANDERS
   ================================================================ */
[data-testid="stExpander"] {
    border: 1px solid rgba(42,29,126,0.09) !important;
    border-radius: 12px !important;
    overflow: hidden;
    transition: border-color 0.22s !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(42,29,126,0.16) !important;
}

/* ================================================================
   ALERT / INFO BOXES
   ================================================================ */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Jost', sans-serif !important;
    font-weight: 600 !important;
}

/* ================================================================
   DOWNLOAD BUTTON
   ================================================================ */
[data-testid="stDownloadButton"] > button {
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-family: 'Jost', sans-serif !important;
}

/* ================================================================
   METRIC (native Streamlit)
   ================================================================ */
[data-testid="stMetric"] {
    background: var(--lp-surface);
    border: 1px solid var(--lp-border);
    border-radius: var(--lp-r-md);
    padding: 18px;
    box-shadow: var(--lp-shadow-xs);
}

/* ================================================================
   DAYBREAK SHARED CARD COMPONENTS (used by all pages)
   ================================================================ */
.db-card {
    background: #FFFFFF; border: 1px solid rgba(26,18,8,0.09);
    border-radius: 16px; padding: 22px;
    box-shadow: 0 2px 12px rgba(26,18,8,0.06); transition: box-shadow 0.22s;
    margin-bottom: 16px;
}
.db-card:hover { box-shadow: 0 8px 32px rgba(26,18,8,0.09); }
.db-card-hdr {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px; padding-bottom: 13px;
    border-bottom: 1px solid rgba(26,18,8,0.05);
}
.db-card-title { font-family: 'Cormorant', serif; font-size: 18px; font-weight: 600; color: #1A1208; }
.db-card-sub {
    font-size: 9.5px; color: #A09080; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; font-family: 'Jost', sans-serif;
}
.db-sec-label {
    font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 3px;
    color: #A09080; margin: 0 0 14px;
    display: flex; align-items: center; gap: 12px; font-family: 'Jost', sans-serif;
}
.db-sec-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(26,18,8,0.09), transparent);
}
.db-stat-val {
    font-family: 'Jost', sans-serif; font-size: 36px; font-weight: 900;
    color: #1A1208; line-height: 1; margin-bottom: 5px; font-variant-numeric: tabular-nums;
}
.db-stat-lbl {
    font-size: 9px; color: #A09080; text-transform: uppercase;
    letter-spacing: 2px; font-weight: 700; font-family: 'Jost', sans-serif;
}
.db-stat-sub { font-size: 11px; font-weight: 600; margin-top: 5px; color: #A09080; font-family: 'Jost', sans-serif; }
.db-streak {
    background: linear-gradient(148deg, #FFF5EE 0%, #FDEADE 60%, #F8E0D0 100%);
    border: 1.5px solid rgba(184,90,48,0.22); border-radius: 16px;
    padding: 24px 20px; text-align: center; margin-bottom: 14px;
    box-shadow: 0 8px 32px rgba(184,90,48,0.14);
    position: relative; overflow: hidden; transition: transform 0.28s, box-shadow 0.28s;
}
.db-streak:hover { transform: translateY(-3px); box-shadow: 0 14px 44px rgba(184,90,48,0.22); }
.db-snum {
    font-family: 'Jost', sans-serif; font-size: 64px; font-weight: 900;
    color: #B85A30; line-height: 1; font-variant-numeric: tabular-nums; margin-bottom: 3px;
}
.db-slbl { font-size: 8.5px; text-transform: uppercase; letter-spacing: 3px; font-weight: 800; color: #A09080; font-family: 'Jost', sans-serif; }
.db-sbadge { padding: 3px 10px; border-radius: 100px; font-size: 10.5px; font-weight: 700; background: rgba(184,90,48,0.08); color: #B85A30; border: 1px solid rgba(184,90,48,0.20); font-family: 'Jost', sans-serif; }
.db-day { display: flex; align-items: center; gap: 11px; padding: 8px 9px; border-radius: 9px; margin-bottom: 2px; transition: background 0.16s; }
.db-day:hover { background: #F9F5EF; }
.db-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.db-day.done .db-dot { background: #2B5A3E; box-shadow: 0 0 0 2.5px rgba(43,90,62,0.14); }
.db-day.pend .db-dot { background: transparent; border: 1.5px solid #A09080; }
.db-day-name { font-weight: 700; font-size: 13px; width: 76px; color: #1A1208; font-family: 'Jost', sans-serif; }
.db-day-ch { flex: 1; font-size: 13px; color: #5A4A32; font-family: 'Jost', sans-serif; }
.db-day-st { font-size: 14px; font-weight: 700; font-family: 'Jost', sans-serif; }
.db-day.done .db-day-st { color: #2B5A3E; }
.db-day.pend .db-day-st { color: #A09080; }
.db-prog-item { margin-bottom: 14px; }
.db-prog-item:last-child { margin-bottom: 0; }
.db-prog-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
.db-prog-name { font-size: 13px; font-weight: 600; color: #1A1208; font-family: 'Jost', sans-serif; }
.db-prog-pct { font-family: 'Jost', sans-serif; font-size: 15px; font-weight: 800; }
.db-prog-track { height: 5px; background: #EDE8DF; border-radius: 100px; overflow: hidden; }
.db-prog-fill { height: 100%; border-radius: 100px; transition: width 1.2s cubic-bezier(0.22,1,0.36,1); }
.fill-terra { background-image: linear-gradient(90deg,#B85A30 0%,#D46A38 50%,#B85A30 100%); background-size: 200% 100%; animation: shimmer 2.8s linear infinite; box-shadow: 0 0 8px rgba(184,90,48,0.22); }
.fill-gold { background: #C48A1C; }
.fill-ts { background: #B85A30; }
.fill-tw { background: #D46A38; opacity: 0.75; }
.db-pi { display: flex; align-items: center; gap: 10px; padding: 9px 7px; border-radius: 9px; margin-bottom: 2px; transition: background 0.16s; }
.db-pi:hover { background: #F9F5EF; }
.db-pcat { width: 31px; height: 31px; border-radius: 8px; background: #F3EFE7; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; transition: transform 0.22s; }
.db-pi:hover .db-pcat { transform: scale(1.1); }
.db-pname { font-size: 13.5px; font-weight: 600; color: #1A1208; line-height: 1.3; font-family: 'Jost', sans-serif; }
.db-pmeta { font-size: 10.5px; color: #A09080; margin-top: 1px; font-family: 'Jost', sans-serif; }
.db-pbadge { padding: 3px 10px; border-radius: 100px; font-size: 10px; font-weight: 800; flex-shrink: 0; font-family: 'Jost', sans-serif; }
.db-ongoing { background: #FDF0E8; color: #B85A30; border: 1px solid rgba(184,90,48,0.20); }
.db-answered { background: #E8F3ED; color: #2B5A3E; border: 1px solid rgba(43,90,62,0.22); }
.db-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }
.db-abtn { background: #F9F5EF; border: 1.5px solid rgba(26,18,8,0.09); border-radius: 10px; padding: 14px 10px; text-align: center; text-decoration: none; display: block; transition: all 0.22s; }
.db-abtn:hover { border-color: #B85A30; transform: translateY(-3px); box-shadow: 0 6px 18px rgba(184,90,48,0.12); background: #FDF0E8; }
.db-aicon { font-size: 20px; margin-bottom: 6px; display: block; }
.db-albl { font-size: 10px; font-weight: 700; color: #5A4A32; text-transform: uppercase; letter-spacing: 1px; font-family: 'Jost', sans-serif; }
@keyframes fire { 0%,100%{transform:scaleY(1) rotate(-2deg);} 25%{transform:scaleY(1.08) rotate(1deg);} 50%{transform:scaleY(0.95) rotate(-1deg);} 75%{transform:scaleY(1.05) rotate(2deg);} }

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
    .hero-greeting   { font-size: 9px; letter-spacing: 3px; }
    .hero-date       { font-size: 11px; }
    .hero-verse      { font-size: 14px; padding: 14px 16px 14px 28px; margin-top: 16px; }
    .hero-verse::before { font-size: 44px; left: 10px; }

    .page-header         { padding: 20px 20px 18px; border-radius: 18px; margin-bottom: 16px; }
    .page-header-title   { font-size: 19px; }
    .page-header-sub     { font-size: 12px; }

    .metric-card, .stat-card { padding: 14px 10px; border-radius: 12px; }
    .metric-value { font-size: 24px; }
    .stat-value   { font-size: 22px; }
    .metric-label, .stat-label { font-size: 9px; letter-spacing: 1.5px; }

    .section-card  { padding: 18px; border-radius: 12px; }
    .section-icon  { font-size: 26px; }
    .section-title { font-size: 15px; }
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
    .streak-label { font-size: 10px; letter-spacing: 2.5px; }

    .report-card { padding: 18px; font-size: 15px; line-height: 1.80; }
    .goal-banner { font-size: 13px; padding: 12px 16px 12px 22px; }

    .empty-state       { padding: 38px 16px; }
    .empty-state-icon  { font-size: 40px; }
    .empty-state-title { font-size: 15px; }

    .section-label { font-size: 9px; letter-spacing: 2.5px; }
    .prayer-pill   { padding: 5px 12px; font-size: 12px; margin: 2px 3px; }

    .wizard-step         { padding: 16px 18px; }
    .wizard-step-title   { font-size: 14px; }
    .wizard-step-desc    { margin-left: 0; margin-top: 8px; }

    .sermon-card     { padding: 14px 16px; }
    .scripture-block { font-size: 14px; padding: 10px 14px; }

    .announcement-card { padding: 10px 14px; }
    .announcement-title { font-size: 13px; }
    .announcement-body  { font-size: 12px; }
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
    .page-header-title { font-size: 17px; }

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
ENHANCEMENT_CSS = """
<style>
    [data-testid="stForm"] {
        border: 1px solid rgba(42,29,126,0.09) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        background: rgba(254,252,248,0.80) !important;
        box-shadow: 0 2px 10px rgba(42,29,126,0.04) !important;
        backdrop-filter: blur(8px) !important;
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(42,29,126,0.09) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(42,29,126,0.18) !important;
    }
    [data-testid="stCheckbox"] label,
    [data-testid="stToggle"] label {
        font-family: 'Jost', sans-serif !important;
        font-weight: 600 !important;
        color: #3A3255 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderTrack"] {
        background: rgba(42,29,126,0.10) !important;
    }
    .stCaption {
        font-family: 'Jost', sans-serif !important;
        color: #8A85A0 !important;
    }
    [data-baseweb="select"] [data-baseweb="menu"] {
        border-radius: 12px !important;
        border: 1px solid rgba(42,29,126,0.10) !important;
        box-shadow: 0 8px 28px rgba(42,29,126,0.10) !important;
        font-family: 'Jost', sans-serif !important;
    }
    [data-baseweb="tag"] {
        background: rgba(42,29,126,0.09) !important;
        border-radius: 8px !important;
        color: #B85A30 !important;
        font-weight: 700 !important;
        font-family: 'Jost', sans-serif !important;
    }
</style>
"""


def inject_styles():
    """Inject the full Logos Pulse design system into the current page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    st.markdown(ENHANCEMENT_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render the Daybreak warm page header with optional subtitle."""
    st.markdown(
        '<div class="page-header">'
        f'<div class="page-header-title">{icon} {title}</div>'
        + (f'<div class="page-header-sub">{subtitle}</div>' if subtitle else '')
        + '</div>',
        unsafe_allow_html=True
    )


def section_label(text: str):
    """Render a styled section label with trailing gold rule."""
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def empty_state(icon: str, title: str, subtitle: str = ""):
    """Render a centered empty-state placeholder."""
    sub_html = f'<div class="empty-state-sub">{subtitle}</div>' if subtitle else ''
    st.markdown(
        '<div class="empty-state">'
        + f'<div class="empty-state-icon">{icon}</div>'
        + f'<div class="empty-state-title">{title}</div>'
        + sub_html
        + '</div>',
        unsafe_allow_html=True
    )


def spacer(height: int = 16):
    """Render a vertical spacer."""
    st.markdown(f"<div style='height:{height}px'></div>", unsafe_allow_html=True)


def footer():
    """Render the branded footer."""
    st.markdown("""
    <div class="lp-footer">
        <div class="lp-footer-brand">&#9997; Logos Pulse</div>
        <div class="lp-footer-sub">Spiritual Growth Tracker &bull; Built with faith</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Render the sidebar logo block using the SVG brand mark."""
    st.markdown("""
    <div style="text-align:center; padding:10px 0 20px 0;">
        <svg width="44" height="44" viewBox="0 0 100 100" fill="none"
             style="margin-bottom:10px; display:inline-block;"
             xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="lp-sb-glow" cx="50%" cy="50%" r="45%">
                    <stop offset="0%"   stop-color="#C48A1C" stop-opacity="0.14"/>
                    <stop offset="100%" stop-color="#C48A1C" stop-opacity="0"/>
                </radialGradient>
            </defs>
            <rect width="100" height="100" rx="22" fill="#1A1628"/>
            <rect width="100" height="100" rx="22" fill="url(#lp-sb-glow)"/>
            <path d="M 8,40 L 24,40 L 27,35 L 31,48 L 42,12 L 54,40"
                  stroke="#C96A3C" stroke-width="3.2"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="54" y1="40" x2="92" y2="40"
                  stroke="#C96A3C" stroke-width="3.2" stroke-linecap="round"/>
            <rect x="46" y="12" width="8" height="76" rx="2.5" fill="#F0E8D6"/>
        </svg>
        <div style="
            font-family:'Cormorant','Cormorant',Georgia,serif;
            font-size:17px;
            font-weight:600;
            color:#1A1208;
            letter-spacing:0.06em;
            line-height:1.2;
        ">
            Logos Pulse
        </div>
        <div style="
            font-size:8.5px;
            color:#B85A30;
            letter-spacing:2.5px;
            text-transform:uppercase;
            font-weight:700;
            margin-top:3px;
            font-family:'Jost',sans-serif;
            opacity:0.75;
        ">
            Sanctuary
        </div>
    </div>
    """, unsafe_allow_html=True)
