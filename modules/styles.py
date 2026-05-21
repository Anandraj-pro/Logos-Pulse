"""
Logos Pulse Design System — Illuminated Codex
Dark parchment night. Gold leaf. Medieval manuscript meets digital devotional.
IM Fell English × Cinzel × Cardo
"""

import streamlit as st

# ==================== DESIGN TOKENS ====================
COLORS = {
    "primary":          "#C48A1C",
    "primary_light":    "#DFA830",
    "primary_dark":     "#8A6018",
    "accent_gold":      "#C48A1C",
    "accent_gold_light":"#DFA830",
    "accent_gold_dark": "#8A6018",
    "accent_gold_pale": "#1A1108",
    "surface":          "#1A1108",
    "surface_warm":     "#1E1510",
    "card_bg":          "#1A1108",
    "card_border":      "rgba(196,138,28,0.18)",
    "text_primary":     "#F5E8C0",
    "text_secondary":   "#C4A870",
    "text_muted":       "#8A7860",
    "success":          "#2A7A4A",
    "success_bg":       "#0A1A0F",
    "warning":          "#B85A30",
    "warning_bg":       "#1A0A04",
    "danger":           "#9C2424",
    "streak_fire":      "#D44A22",
    "streak_gold":      "#C48A1C",
}

# ==================== SHARED CSS ====================
SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Cinzel:wght@400;600;700&family=Cardo:ital,wght@0,400;0,700;1,400&family=Cormorant:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Jost:wght@300;400;500;600;700;800&display=swap');

/* ================================================================
   DESIGN TOKENS — ILLUMINATED CODEX
   ================================================================ */
:root {
    --lp-primary:        #C48A1C;
    --lp-primary-light:  #DFA830;
    --lp-primary-dark:   #8A6018;
    --lp-gold:           #C48A1C;
    --lp-gold-light:     #DFA830;
    --lp-gold-dark:      #8A6018;
    --lp-gold-pale:      rgba(196,138,28,0.08);
    --lp-bg:             #0A0703;
    --lp-surface:        #1A1108;
    --lp-surface-2:      #221608;
    --lp-border:         rgba(196,138,28,0.18);
    --lp-border-strong:  rgba(196,138,28,0.40);
    --lp-text:           #F5E8C0;
    --lp-text-2:         #C4A870;
    --lp-text-3:         #8A7860;
    --lp-success:        #2A7A4A;
    --lp-warning:        #B85A30;
    --lp-danger:         #9C2424;
    --lp-r-sm:  10px;
    --lp-r-md:  16px;
    --lp-r-lg:  22px;
    --lp-shadow-xs: 0 1px 6px rgba(0,0,0,0.3), 0 1px 2px rgba(196,138,28,0.05);
    --lp-shadow-sm: 0 2px 14px rgba(0,0,0,0.4), 0 1px 4px rgba(196,138,28,0.08);
    --lp-shadow-md: 0 6px 28px rgba(0,0,0,0.5), 0 2px 8px rgba(196,138,28,0.10);
    --lp-shadow-lg: 0 14px 50px rgba(0,0,0,0.6), 0 4px 14px rgba(196,138,28,0.12);
    --lp-glow-indigo: 0 6px 28px rgba(196,138,28,0.20);
    --lp-glow-gold:   0 6px 28px rgba(196,138,28,0.28);
    --lp-gold-stripe: linear-gradient(90deg,
        transparent 0%,
        var(--lp-gold) 30%,
        var(--lp-gold-light) 50%,
        var(--lp-gold) 70%,
        transparent 100%
    );
    --lp-font-display: 'IM Fell English', Georgia, serif;
    --lp-font-label:   'Cinzel', Georgia, serif;
    --lp-font-body:    'Cardo', Georgia, serif;
    --lp-font-ui:      'Jost', system-ui, sans-serif;
}

/* ================================================================
   HIDE STREAMLIT NATIVE CHROME
   ================================================================ */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, .stAppToolbar, .stDeployButton { display: none !important; }

#MainMenu { visibility: hidden !important; }

[data-testid="stVerticalBlock"] { width: 100% !important; }

/* ================================================================
   GLOBAL BASE — PARCHMENT NIGHT
   ================================================================ */
.stApp {
    font-family: var(--lp-font-body) !important;
    background:
        radial-gradient(ellipse at 8% 8%,   rgba(196,138,28,0.07) 0%, transparent 38%),
        radial-gradient(ellipse at 92% 92%,  rgba(196,138,28,0.05) 0%, transparent 38%),
        radial-gradient(ellipse at 50% -6%,  rgba(196,138,28,0.04) 0%, transparent 40%),
        #0A0703 !important;
    color: var(--lp-text) !important;
}

h1, h2, h3 {
    font-family: var(--lp-font-display) !important;
    color: var(--lp-text) !important;
    font-weight: 400 !important;
    letter-spacing: 0.02em !important;
}

p, li, td, th, label, span {
    font-family: var(--lp-font-body) !important;
    color: var(--lp-text-2) !important;
}

/* ================================================================
   SIDEBAR — BOOK SPINE
   ================================================================ */
[data-testid="stSidebar"] {
    background:
        radial-gradient(ellipse at 50% 0%, rgba(196,138,28,0.07) 0%, transparent 50%),
        #060401 !important;
    border-right: 1px solid rgba(196,138,28,0.14) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Sidebar section headers (dict navigation sections) */
[data-testid="stSidebarNavSectionHeader"],
[data-testid="stSidebarNavItems"] [data-testid*="Section"] {
    font-family: var(--lp-font-label) !important;
    font-size: 8.5px !important;
    letter-spacing: 2.5px !important;
    color: rgba(196,138,28,0.40) !important;
    text-transform: uppercase !important;
    font-weight: 400 !important;
    padding: 14px 16px 4px !important;
}

/* Nav links */
[data-testid="stSidebarNavLink"] {
    color: var(--lp-text-3) !important;
    font-family: var(--lp-font-body) !important;
    font-size: 14px !important;
    border-radius: 6px !important;
    padding: 7px 14px !important;
    border-left: 2px solid transparent !important;
    margin: 1px 4px !important;
    transition: all 0.22s ease !important;
    background: transparent !important;
}

[data-testid="stSidebarNavLink"]:hover {
    color: var(--lp-gold) !important;
    background: rgba(196,138,28,0.07) !important;
    border-left-color: rgba(196,138,28,0.3) !important;
}

[data-testid="stSidebarNavLink"][aria-current="page"] {
    color: var(--lp-gold) !important;
    background: rgba(196,138,28,0.08) !important;
    border-left-color: var(--lp-gold) !important;
    font-style: italic;
}

[data-testid="stSidebarNavLink"] span,
[data-testid="stSidebarNavLink"] p {
    color: inherit !important;
    font-family: var(--lp-font-body) !important;
}

/* Sidebar text elements */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] span {
    color: var(--lp-text-3) !important;
}

/* Sidebar selectbox and buttons */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(196,138,28,0.05) !important;
    border: 1px solid rgba(196,138,28,0.18) !important;
    color: var(--lp-text-2) !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: rgba(196,138,28,0.08) !important;
    border: 1px solid rgba(196,138,28,0.22) !important;
    color: var(--lp-text-2) !important;
    font-family: var(--lp-font-label) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(196,138,28,0.14) !important;
    border-color: var(--lp-gold) !important;
    color: var(--lp-gold) !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, rgba(196,138,28,0.6), rgba(196,138,28,0.4)) !important;
    border-color: var(--lp-gold) !important;
    color: #1a1108 !important;
}

/* ================================================================
   PAGE TRANSITION — FADE + RISE
   ================================================================ */
@keyframes codexPageEnter {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

[data-testid="stMainBlockContainer"] > div {
    animation: codexPageEnter 0.45s cubic-bezier(0.22, 1, 0.36, 1) both !important;
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
    0%, 100% { box-shadow: 0 4px 20px rgba(196,138,28,0.10); }
    50%       { box-shadow: 0 4px 30px rgba(196,138,28,0.30), 0 0 0 3px rgba(196,138,28,0.10); }
}
@keyframes breathe {
    0%, 100% { box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
    50%       { box-shadow: 0 4px 24px rgba(196,138,28,0.20), 0 0 0 3px rgba(196,138,28,0.08); }
}
@keyframes goldPulse {
    0%, 100% { border-color: rgba(196,138,28,0.22); }
    50%       { border-color: rgba(196,138,28,0.55); }
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(10px); }
    to   { opacity: 1; transform: translateX(0);    }
}
@keyframes candleFlicker {
    0%,100%{ text-shadow: 0 0 8px rgba(196,138,28,0.4); }
    50%    { text-shadow: 0 0 22px rgba(196,138,28,0.8), 0 0 44px rgba(196,138,28,0.3); }
}

/* ================================================================
   HERO SECTION (Dashboard)
   ================================================================ */
.hero-section {
    background:
        radial-gradient(ellipse at 80% 20%, rgba(196,138,28,0.10) 0%, transparent 50%),
        linear-gradient(148deg, rgba(30,21,8,0.98), rgba(22,16,6,0.96));
    border: 1px solid rgba(196,138,28,0.20);
    border-radius: var(--lp-r-lg);
    padding: 46px 38px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 28px 70px rgba(0,0,0,0.5),
        0 6px 18px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(196,138,28,0.12);
    animation: riseUp 0.7s cubic-bezier(0.22,1,0.36,1) both;
    color: var(--lp-text);
}

.hero-section::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        -52deg,
        rgba(196,138,28,0.012) 0px,
        rgba(196,138,28,0.012) 1px,
        transparent 1px,
        transparent 18px
    );
    pointer-events: none;
    border-radius: inherit;
}

.hero-section::after {
    content: '';
    position: absolute;
    top: -80px;
    right: -80px;
    width: 330px;
    height: 330px;
    background: radial-gradient(circle, rgba(196,138,28,0.12) 0%, transparent 66%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-greeting {
    font-family: var(--lp-font-label);
    font-size: 9.5px;
    font-weight: 400;
    color: rgba(196,138,28,0.80);
    letter-spacing: 3.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
    position: relative;
}

.hero-name {
    font-family: var(--lp-font-display);
    font-size: 42px;
    font-weight: 400;
    color: var(--lp-text);
    line-height: 1.12;
    margin-bottom: 5px;
    position: relative;
    letter-spacing: 0.02em;
    font-style: italic;
}

.hero-date {
    font-size: 12px;
    color: var(--lp-text-3);
    position: relative;
    font-weight: 400;
    letter-spacing: 0.6px;
    font-family: var(--lp-font-label);
    font-size: 10px;
    letter-spacing: 2px;
}

.hero-verse {
    margin-top: 24px;
    padding: 20px 22px 20px 36px;
    background: rgba(196,138,28,0.05);
    border-radius: 14px;
    font-family: var(--lp-font-display);
    font-style: italic;
    font-size: 16px;
    color: var(--lp-text-2);
    line-height: 1.82;
    border: 1px solid rgba(196,138,28,0.20);
    position: relative;
}

.hero-verse::before {
    content: '\201C';
    position: absolute;
    top: -4px;
    left: 12px;
    font-size: 60px;
    color: rgba(196,138,28,0.35);
    font-family: var(--lp-font-display);
    line-height: 1;
    font-style: normal;
}

/* ================================================================
   PAGE HEADER
   ================================================================ */
.page-header {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.18);
    border-radius: var(--lp-r-lg);
    padding: 28px 34px 26px 34px;
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 16px 50px rgba(0,0,0,0.4),
        0 2px 10px rgba(0,0,0,0.2),
        inset 0 1px 0 rgba(196,138,28,0.10);
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
    color: var(--lp-text);
}

.page-header::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        -46deg,
        rgba(196,138,28,0.008) 0px,
        rgba(196,138,28,0.008) 1px,
        transparent 1px,
        transparent 20px
    );
    pointer-events: none;
    border-radius: inherit;
}

.page-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: var(--lp-gold-stripe);
    opacity: 0.60;
}

.page-header-title {
    font-family: var(--lp-font-display);
    font-size: 26px;
    font-weight: 400;
    letter-spacing: 0.02em;
    color: var(--lp-text);
    position: relative;
    font-style: italic;
}

.page-header-sub {
    font-size: 10px;
    color: var(--lp-text-3);
    margin-top: 6px;
    font-weight: 400;
    letter-spacing: 2px;
    position: relative;
    font-family: var(--lp-font-label);
    text-transform: uppercase;
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
    background: linear-gradient(90deg, transparent, rgba(196,138,28,0.30), transparent);
}

.lp-divider-ornament {
    width: 8px;
    height: 8px;
    border: 1px solid rgba(196,138,28,0.45);
    transform: rotate(45deg);
    flex-shrink: 0;
}

/* ================================================================
   ANNOUNCEMENT CARD
   ================================================================ */
.announcement-card {
    background: rgba(196,138,28,0.05);
    border: 1px solid rgba(196,138,28,0.16);
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
    font-weight: 400;
    color: var(--lp-gold);
    font-family: var(--lp-font-display);
    letter-spacing: 0.01em;
    font-style: italic;
}

.announcement-body {
    font-size: 13px;
    color: var(--lp-text-2);
    margin-top: 4px;
    line-height: 1.6;
    font-family: var(--lp-font-body);
}

/* ================================================================
   GROWTH BADGE
   ================================================================ */
.growth-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: var(--lp-font-label);
}

.growth-badge-seed    { background: rgba(138,96,24,0.12);  color: #C4A030; border: 1px solid rgba(138,96,24,0.28); }
.growth-badge-sprout  { background: rgba(42,122,74,0.10);  color: #4AA870; border: 1px solid rgba(42,122,74,0.25); }
.growth-badge-sapling { background: rgba(184,90,48,0.10);  color: #D4703A; border: 1px solid rgba(184,90,48,0.25); }
.growth-badge-tree    { background: rgba(196,138,28,0.12); color: #DFA830; border: 1px solid rgba(196,138,28,0.30); animation: aureate 3.5s ease-in-out infinite; }
.growth-badge-forest  { background: linear-gradient(135deg, rgba(196,138,28,0.12), rgba(184,90,48,0.10)); color: #C48A1C; border: 1px solid rgba(196,138,28,0.35); animation: aureate 3s ease-in-out infinite; }

/* ================================================================
   SECTION LABEL
   ================================================================ */
.section-label {
    font-size: 9px;
    color: rgba(196,138,28,0.50);
    text-transform: uppercase;
    letter-spacing: 3.5px;
    font-weight: 400;
    font-family: var(--lp-font-label);
    margin: 26px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(196,138,28,0.30) 0%, transparent 100%);
}

/* ================================================================
   METRIC CARDS
   ================================================================ */
.metric-card {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.16);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.30;
    transition: opacity 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--lp-glow-gold), var(--lp-shadow-md);
    border-color: rgba(196,138,28,0.35);
}

.metric-card:hover::before { opacity: 0.80; }

.metric-value {
    font-family: var(--lp-font-display);
    font-size: 34px;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 8px;
    letter-spacing: 0.01em;
    color: var(--lp-text);
}

.metric-label {
    font-size: 9px;
    color: rgba(196,138,28,0.55);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 400;
    font-family: var(--lp-font-label);
}

/* ================================================================
   STAT CARDS
   ================================================================ */
.stat-card {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.16);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.30;
    transition: opacity 0.3s;
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--lp-glow-gold);
    border-color: rgba(196,138,28,0.35);
}

.stat-card:hover::before { opacity: 0.80; }

.stat-value {
    font-family: var(--lp-font-display);
    font-size: 30px;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 6px;
    letter-spacing: 0.01em;
    color: var(--lp-text);
}

.stat-label {
    font-size: 9px;
    color: rgba(196,138,28,0.55);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-top: 6px;
    font-weight: 400;
    font-family: var(--lp-font-label);
}

/* ================================================================
   SECTION CARDS
   ================================================================ */
.section-card {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.22;
    transition: opacity 0.3s;
}

.section-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.section-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--lp-shadow-lg), 0 0 0 1px rgba(196,138,28,0.14);
    border-color: rgba(196,138,28,0.35);
}

.section-card:hover::before { opacity: 0.70; }

.section-card:hover::after {
    opacity: 0.50;
    animation: shimmer 2.2s linear infinite;
}

.section-icon { font-size: 28px; margin-bottom: 12px; display: block; }

.section-title {
    font-family: var(--lp-font-display);
    font-size: 18px;
    font-weight: 400;
    color: var(--lp-text);
    margin-bottom: 7px;
    letter-spacing: 0.01em;
    font-style: italic;
}

.section-desc {
    font-size: 13px;
    color: var(--lp-text-3);
    line-height: 1.65;
    font-family: var(--lp-font-body);
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
    background: linear-gradient(135deg, rgba(42,122,74,0.12), rgba(42,122,74,0.06));
    border: 1px solid rgba(42,122,74,0.25);
    box-shadow: 0 4px 18px rgba(0,0,0,0.3), inset 0 1px 0 rgba(42,122,74,0.08);
}

.today-done::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 90px; height: 90px;
    background: radial-gradient(circle at top right, rgba(42,122,74,0.10) 0%, transparent 70%);
    pointer-events: none;
}

.today-pending {
    background: linear-gradient(135deg, rgba(196,138,28,0.10), rgba(196,138,28,0.05));
    border: 1px solid rgba(196,138,28,0.22);
    box-shadow: 0 4px 18px rgba(0,0,0,0.3), inset 0 1px 0 rgba(196,138,28,0.06);
    animation: fadeInUp 0.45s cubic-bezier(0.22,1,0.36,1) both, breathe 4s ease-in-out 1.2s infinite;
}

.today-pending::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 90px; height: 90px;
    background: radial-gradient(circle at top right, rgba(196,138,28,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.today-title {
    font-size: 14px;
    font-weight: 400;
    margin-bottom: 9px;
    position: relative;
    font-family: var(--lp-font-display);
    font-style: italic;
    color: var(--lp-text);
}

.today-detail {
    font-size: 13px;
    color: var(--lp-text-2);
    line-height: 1.65;
    position: relative;
    font-family: var(--lp-font-body);
}

/* ================================================================
   PROGRESS BARS
   ================================================================ */
.progress-section {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.22;
    transition: opacity 0.3s;
}

.progress-section:hover { box-shadow: var(--lp-shadow-sm); }
.progress-section:hover::before { opacity: 0.60; }

.progress-title {
    font-size: 13px;
    font-weight: 400;
    color: var(--lp-text-2);
    margin-bottom: 14px;
    font-family: var(--lp-font-display);
    font-style: italic;
}

.progress-bar-bg {
    background: rgba(196,138,28,0.10);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg,
        var(--lp-primary-dark) 0%,
        var(--lp-gold-light) 50%,
        var(--lp-primary-dark) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
    box-shadow: 0 0 10px rgba(196,138,28,0.35);
    transition: width 0.8s cubic-bezier(0.22,1,0.36,1);
}

.progress-label {
    font-size: 11px;
    color: var(--lp-text-3);
    margin-top: 8px;
    font-weight: 400;
    font-family: var(--lp-font-label);
    letter-spacing: 1px;
}

/* ================================================================
   ENTRY / DATA CARDS
   ================================================================ */
.entry-card {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.18;
    transition: opacity 0.25s;
}

.entry-card:hover {
    box-shadow: var(--lp-shadow-sm), 0 0 0 1px rgba(196,138,28,0.12);
    border-color: rgba(196,138,28,0.30);
    transform: translateY(-1px);
}

.entry-card:hover::before { opacity: 0.60; }

/* ================================================================
   REPORT CARD (parchment / scripture feel)
   ================================================================ */
.report-card {
    background: linear-gradient(135deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.22);
    border-radius: var(--lp-r-md);
    padding: 30px;
    font-family: var(--lp-font-display);
    font-style: italic;
    font-size: 17px;
    line-height: 1.92;
    color: var(--lp-text-2);
    white-space: pre-line;
    box-shadow:
        0 4px 22px rgba(0,0,0,0.4),
        inset 0 1px 0 rgba(196,138,28,0.08);
    position: relative;
    overflow: hidden;
}

.report-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--lp-gold), var(--lp-primary));
    border-radius: 3px 0 0 3px;
}

/* ================================================================
   GOAL / INFO BANNERS
   ================================================================ */
.goal-banner {
    background: rgba(196,138,28,0.07);
    border: 1px solid rgba(196,138,28,0.18);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px 14px 24px;
    font-size: 14px;
    color: var(--lp-gold);
    font-weight: 400;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
    font-family: var(--lp-font-display);
    font-style: italic;
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
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.18;
    transition: opacity 0.25s;
}

.prayer-card:hover {
    box-shadow: var(--lp-shadow-sm);
    border-color: rgba(196,138,28,0.28);
    transform: translateY(-1px);
}

.prayer-card:hover::before { opacity: 0.65; }

.prayer-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
}

.prayer-name {
    font-family: var(--lp-font-display);
    font-size: 17px;
    font-weight: 400;
    color: var(--lp-text);
    letter-spacing: 0.01em;
    font-style: italic;
}

.status-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 400;
    letter-spacing: 1.5px;
    font-family: var(--lp-font-label);
    text-transform: uppercase;
}

/* ================================================================
   SCRIPTURE / CONFESSION / DECLARATION BLOCKS
   ================================================================ */
.scripture-block {
    background: rgba(196,138,28,0.05);
    border-left: 2px solid rgba(196,138,28,0.35);
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 8px;
    font-family: var(--lp-font-display);
    font-style: italic;
    font-size: 15.5px;
    line-height: 1.88;
    color: var(--lp-text-2);
}

.confession-block {
    background: rgba(42,122,74,0.08);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px;
    font-weight: 400;
    color: #4AA870;
    line-height: 1.80;
    border: 1px solid rgba(42,122,74,0.20);
    font-family: var(--lp-font-display);
    font-style: italic;
}

.declaration-block {
    background: rgba(196,138,28,0.07);
    border-radius: var(--lp-r-sm);
    padding: 14px 18px;
    font-weight: 400;
    color: var(--lp-gold);
    line-height: 1.80;
    border: 1px solid rgba(196,138,28,0.18);
    font-family: var(--lp-font-display);
    font-style: italic;
}

/* ================================================================
   SERMON CARDS
   ================================================================ */
.sermon-card {
    background: linear-gradient(135deg, rgba(26,17,8,0.98), rgba(22,15,6,0.96));
    border: 1px solid rgba(196,138,28,0.16);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.25;
    transition: opacity 0.3s;
}

.sermon-card:hover {
    box-shadow: var(--lp-glow-gold);
    border-color: rgba(196,138,28,0.35);
    transform: translateY(-2px);
}

.sermon-card:hover::before { opacity: 0.80; }

/* ================================================================
   CATEGORY CARDS (Prayer Journal pill nav)
   ================================================================ */
.cat-card {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
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
    border-color: rgba(196,138,28,0.25);
}

.cat-card-active {
    border: 2px solid currentColor;
    box-shadow: var(--lp-shadow-sm);
}

.cat-icon  { font-size: 28px; margin-bottom: 7px; display: block; }
.cat-name  { font-size: 12px; font-weight: 400; letter-spacing: 1.5px; font-family: var(--lp-font-label); color: var(--lp-text-2); }
.cat-count { font-size: 11px; opacity: 0.65; margin-top: 3px; font-family: var(--lp-font-body); }

/* ================================================================
   WIZARD STEPS
   ================================================================ */
.wizard-step {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.22;
}

.wizard-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    font-size: 13px;
    font-weight: 400;
    color: var(--lp-text);
    margin-right: 10px;
    border: 1px solid rgba(196,138,28,0.35);
    background: rgba(196,138,28,0.08);
    font-family: var(--lp-font-label);
}

.wizard-step-title {
    font-family: var(--lp-font-display);
    font-size: 16px;
    font-weight: 400;
    color: var(--lp-text);
    display: inline;
    letter-spacing: 0.01em;
    font-style: italic;
}

.wizard-step-desc {
    font-size: 13px;
    color: var(--lp-text-3);
    margin: 6px 0 12px 40px;
    font-weight: 400;
    font-family: var(--lp-font-body);
}

/* ================================================================
   PRAYER PILLS
   ================================================================ */
.prayer-pill {
    display: inline-block;
    padding: 5px 16px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 400;
    margin: 3px 4px;
    transition: transform 0.2s, box-shadow 0.2s;
    font-family: var(--lp-font-label);
    letter-spacing: 1px;
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
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.35;
    display: block;
    animation: candleFlicker 4s ease-in-out infinite;
}

.empty-state-title {
    font-family: var(--lp-font-display);
    font-size: 20px;
    color: var(--lp-text-3);
    font-weight: 400;
    margin-bottom: 6px;
    letter-spacing: 0.02em;
    font-style: italic;
}

.empty-state-sub {
    font-size: 13px;
    color: rgba(138,120,96,0.6);
    margin-top: 8px;
    line-height: 1.58;
    font-family: var(--lp-font-body);
}

/* ================================================================
   STREAK HERO
   ================================================================ */
.streak-hero {
    background: linear-gradient(148deg, rgba(26,17,8,0.99), rgba(14,10,4,0.98));
    border: 1px solid rgba(196,138,28,0.22);
    border-radius: var(--lp-r-lg);
    padding: 38px 28px;
    margin-bottom: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 16px 50px rgba(0,0,0,0.5), 0 0 40px rgba(196,138,28,0.08);
}

.streak-num {
    font-family: var(--lp-font-display);
    font-size: 72px;
    font-weight: 400;
    line-height: 1;
    letter-spacing: 0.02em;
    color: var(--lp-text);
    animation: candleFlicker 6s ease-in-out infinite;
}

.streak-label {
    font-size: 10px;
    color: rgba(196,138,28,0.50);
    text-transform: uppercase;
    letter-spacing: 3.5px;
    margin-top: 10px;
    font-weight: 400;
    font-family: var(--lp-font-label);
}

/* ================================================================
   CALENDAR / HEATMAP
   ================================================================ */
.cal-header, .heatmap-header {
    text-align: center;
    font-size: 9.5px;
    color: var(--lp-text-3);
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 4px;
    font-family: var(--lp-font-label);
}

.cal-day, .heatmap-day {
    text-align: center;
    border-radius: 6px;
    padding: 6px 4px;
    font-size: 13px;
    font-weight: 400;
    margin: 2px;
    font-family: var(--lp-font-body);
    color: var(--lp-text-2);
}

.cal-done, .heatmap-done {
    background: linear-gradient(135deg, rgba(196,138,28,0.35), rgba(196,138,28,0.20));
    color: var(--lp-text);
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(196,138,28,0.20);
    border: 1px solid rgba(196,138,28,0.30);
}

.cal-empty    { color: rgba(138,120,96,0.35); }
.heatmap-missed { background: rgba(184,90,48,0.10); color: rgba(184,90,48,0.60); }
.heatmap-future { color: rgba(138,120,96,0.28); }

/* ================================================================
   DAY ROWS (Weekly Assignment)
   ================================================================ */
.day-row {
    display: flex;
    align-items: center;
    padding: 13px 20px;
    margin: 5px 0;
    border-radius: var(--lp-r-sm);
    font-size: 14px;
    transition: transform 0.2s ease;
}

.day-done {
    background: rgba(42,122,74,0.08);
    border: 1px solid rgba(42,122,74,0.18);
}

.day-pending {
    background: rgba(196,138,28,0.06);
    border: 1px solid rgba(196,138,28,0.14);
}

.day-row:hover  { transform: translateX(3px); }
.day-name       { font-weight: 400; width: 100px; color: var(--lp-text); font-family: var(--lp-font-label); font-size: 11px; letter-spacing: 1px; }
.day-chapters   { flex: 1; color: var(--lp-text-2); font-family: var(--lp-font-body); }
.day-status     { font-size: 16px; }

/* ================================================================
   SETTINGS
   ================================================================ */
.settings-section {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
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
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    opacity: 0.20;
}

/* ================================================================
   FOOTER
   ================================================================ */
.lp-footer {
    text-align: center;
    padding: 30px 20px;
    margin-top: 52px;
    border-top: 1px solid rgba(196,138,28,0.10);
    position: relative;
}

.lp-footer::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,138,28,0.55), transparent);
}

.lp-footer-brand {
    font-family: var(--lp-font-display);
    font-size: 16px;
    font-weight: 400;
    font-style: italic;
    color: var(--lp-gold);
    letter-spacing: 0.04em;
}

.lp-footer-sub {
    font-size: 10px;
    color: var(--lp-text-3);
    margin-top: 4px;
    letter-spacing: 2px;
    font-weight: 400;
    font-family: var(--lp-font-label);
    text-transform: uppercase;
}

/* ================================================================
   TABS
   ================================================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(196,138,28,0.05);
    border-radius: 14px;
    padding: 5px;
    border: 1px solid rgba(196,138,28,0.12);
}

.stTabs [data-baseweb="tab-list"] button {
    border-radius: 10px !important;
    font-weight: 400 !important;
    font-size: 12px !important;
    font-family: var(--lp-font-label) !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1) !important;
    color: var(--lp-text-3) !important;
    padding: 8px 18px !important;
}

.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    background: rgba(196,138,28,0.10) !important;
    border: 1px solid rgba(196,138,28,0.22) !important;
    box-shadow: 0 2px 12px rgba(196,138,28,0.12) !important;
    color: var(--lp-gold) !important;
}

/* ================================================================
   BUTTONS
   ================================================================ */
.stButton > button,
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-tertiary"] {
    border-radius: 8px !important;
    font-weight: 400 !important;
    font-size: 11px !important;
    font-family: var(--lp-font-label) !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    transition: all 0.25s cubic-bezier(0.22,1,0.36,1) !important;
    border: 1px solid rgba(196,138,28,0.22) !important;
    color: var(--lp-text-2) !important;
    background: rgba(196,138,28,0.06) !important;
}

.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(138deg, #6B4C08 0%, #8A6018 50%, #6B4C08 100%) !important;
    border: 1px solid rgba(196,138,28,0.55) !important;
    box-shadow: 0 4px 18px rgba(196,138,28,0.22), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    color: #F5E8C0 !important;
}

.stButton > button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(138deg, #8A6018 0%, #C48A1C 50%, #8A6018 100%) !important;
    box-shadow: 0 8px 28px rgba(196,138,28,0.35), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    transform: translateY(-2px) !important;
    border-color: var(--lp-gold) !important;
    color: #1a1108 !important;
}

.stButton > button[kind="primary"]:active,
button[data-testid="baseButton-primary"]:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px rgba(196,138,28,0.20) !important;
}

.stButton > button[kind="secondary"],
button[data-testid="baseButton-secondary"] {
    border: 1px solid rgba(196,138,28,0.22) !important;
    color: var(--lp-text-2) !important;
    background: transparent !important;
}

.stButton > button[kind="secondary"]:hover,
button[data-testid="baseButton-secondary"]:hover {
    border-color: var(--lp-gold) !important;
    background: rgba(196,138,28,0.08) !important;
    color: var(--lp-gold) !important;
    transform: translateY(-1px) !important;
}

/* Form submit buttons specifically */
button[data-testid="stFormSubmitButton"] > button,
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(138deg, #6B4C08 0%, #8A6018 50%, #6B4C08 100%) !important;
    border: 1px solid rgba(196,138,28,0.55) !important;
    color: #F5E8C0 !important;
    font-family: var(--lp-font-label) !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    font-size: 11px !important;
}

/* ================================================================
   FORM INPUTS
   ================================================================ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
input[data-testid],
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    border-radius: 8px !important;
    border: 1px solid rgba(196,138,28,0.22) !important;
    font-family: var(--lp-font-body) !important;
    font-size: 15px !important;
    transition: all 0.22s ease !important;
    background: rgba(14,10,4,0.90) !important;
    color: #F5E8C0 !important;
    -webkit-text-fill-color: #F5E8C0 !important;
}

[data-baseweb="input"],
[data-baseweb="textarea"] {
    background: rgba(14,10,4,0.90) !important;
    border: 1px solid rgba(196,138,28,0.22) !important;
    border-radius: 8px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
[data-baseweb="input"] input:focus,
[data-baseweb="textarea"] textarea:focus {
    border-color: rgba(196,138,28,0.55) !important;
    box-shadow: 0 0 0 3px rgba(196,138,28,0.12) !important;
    background: rgba(20,14,5,0.95) !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder,
[data-baseweb="input"] input::placeholder {
    color: rgba(138,120,96,0.55) !important;
    font-style: italic;
    font-family: var(--lp-font-body) !important;
    -webkit-text-fill-color: rgba(138,120,96,0.55) !important;
}

/* Input labels */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stMultiSelect label,
[data-testid="stWidgetLabel"] p {
    font-family: var(--lp-font-label) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: rgba(196,138,28,0.55) !important;
    font-weight: 400 !important;
}

/* ================================================================
   SELECT / MULTISELECT
   ================================================================ */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-radius: 8px !important;
    border: 1px solid rgba(196,138,28,0.20) !important;
    font-family: var(--lp-font-body) !important;
    transition: border-color 0.22s !important;
    background: rgba(196,138,28,0.04) !important;
    color: var(--lp-text) !important;
}

.stSelectbox > div > div:hover,
.stMultiSelect > div > div:hover {
    border-color: rgba(196,138,28,0.40) !important;
}

/* ================================================================
   FORMS
   ================================================================ */
[data-testid="stForm"] {
    border: 1px solid rgba(196,138,28,0.14) !important;
    border-radius: var(--lp-r-md) !important;
    padding: 24px !important;
    background: rgba(196,138,28,0.03) !important;
    box-shadow: var(--lp-shadow-xs) !important;
}

/* ================================================================
   EXPANDERS
   ================================================================ */
[data-testid="stExpander"] {
    border: 1px solid rgba(196,138,28,0.14) !important;
    border-radius: 10px !important;
    overflow: hidden;
    background: rgba(196,138,28,0.03) !important;
    transition: border-color 0.22s !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(196,138,28,0.28) !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpanderDetails"] {
    background: transparent !important;
}

/* ================================================================
   ALERT / INFO BOXES
   ================================================================ */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: var(--lp-font-body) !important;
    font-weight: 400 !important;
    background: rgba(196,138,28,0.06) !important;
    border: 1px solid rgba(196,138,28,0.18) !important;
    color: var(--lp-text-2) !important;
}

/* ================================================================
   METRIC (native Streamlit)
   ================================================================ */
[data-testid="stMetric"] {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.14);
    border-radius: var(--lp-r-md);
    padding: 18px;
    box-shadow: var(--lp-shadow-xs);
}

[data-testid="stMetricValue"] {
    font-family: var(--lp-font-display) !important;
    color: var(--lp-text) !important;
}

[data-testid="stMetricLabel"] {
    font-family: var(--lp-font-label) !important;
    color: var(--lp-text-3) !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

/* ================================================================
   DOWNLOAD BUTTON
   ================================================================ */
[data-testid="stDownloadButton"] > button {
    border-radius: 8px !important;
    font-weight: 400 !important;
    font-family: var(--lp-font-label) !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

/* ================================================================
   DAYBREAK SHARED CARD COMPONENTS (db-*)
   Used by dashboard and other pages
   ================================================================ */
.db-card {
    background: linear-gradient(148deg, rgba(26,17,8,0.98), rgba(20,13,5,0.96));
    border: 1px solid rgba(196,138,28,0.16);
    border-radius: 16px;
    padding: 22px;
    box-shadow: var(--lp-shadow-xs);
    transition: box-shadow 0.22s, border-color 0.22s;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}

.db-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(196,138,28,0.40), transparent);
    opacity: 0.50;
}

.db-card:hover {
    box-shadow: var(--lp-shadow-md);
    border-color: rgba(196,138,28,0.28);
}

.db-card-hdr {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 16px; padding-bottom: 13px;
    border-bottom: 1px solid rgba(196,138,28,0.10);
}

.db-card-title {
    font-family: var(--lp-font-display);
    font-size: 18px;
    font-weight: 400;
    font-style: italic;
    color: var(--lp-text);
}

.db-card-sub {
    font-size: 9px;
    color: rgba(196,138,28,0.50);
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-family: var(--lp-font-label);
}

.db-sec-label {
    font-size: 8.5px;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: rgba(196,138,28,0.45);
    margin: 0 0 14px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: var(--lp-font-label);
}

.db-sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(196,138,28,0.25), transparent);
}

.db-stat-val {
    font-family: var(--lp-font-display);
    font-size: 36px;
    font-weight: 400;
    color: var(--lp-text);
    line-height: 1;
    margin-bottom: 5px;
    font-variant-numeric: tabular-nums;
}

.db-stat-lbl {
    font-size: 8.5px;
    color: rgba(196,138,28,0.50);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 400;
    font-family: var(--lp-font-label);
}

.db-stat-sub {
    font-size: 11px;
    font-weight: 400;
    margin-top: 5px;
    color: var(--lp-text-3);
    font-family: var(--lp-font-body);
}

.db-streak {
    background:
        radial-gradient(ellipse at 50% 0%, rgba(196,138,28,0.12) 0%, transparent 60%),
        linear-gradient(148deg, rgba(26,17,8,0.99), rgba(14,10,4,0.98));
    border: 1px solid rgba(196,138,28,0.25);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    margin-bottom: 14px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 24px rgba(196,138,28,0.08);
    position: relative;
    overflow: hidden;
    transition: transform 0.28s, box-shadow 0.28s;
}

.db-streak:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 44px rgba(0,0,0,0.5), 0 0 40px rgba(196,138,28,0.14);
}

.db-snum {
    font-family: var(--lp-font-display);
    font-size: 64px;
    font-weight: 400;
    color: var(--lp-text);
    line-height: 1;
    font-variant-numeric: tabular-nums;
    margin-bottom: 3px;
    animation: candleFlicker 6s ease-in-out infinite;
}

.db-slbl {
    font-size: 8.5px;
    text-transform: uppercase;
    letter-spacing: 3.5px;
    font-weight: 400;
    color: rgba(196,138,28,0.50);
    font-family: var(--lp-font-label);
}

.db-sbadge {
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 400;
    background: rgba(196,138,28,0.10);
    color: var(--lp-gold);
    border: 1px solid rgba(196,138,28,0.25);
    font-family: var(--lp-font-label);
    letter-spacing: 1px;
    text-transform: uppercase;
}

.db-day {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 8px 9px;
    border-radius: 8px;
    margin-bottom: 2px;
    transition: background 0.16s;
}

.db-day:hover { background: rgba(196,138,28,0.05); }

.db-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.db-day.done .db-dot { background: #4AA870; box-shadow: 0 0 0 2.5px rgba(74,168,112,0.18); }
.db-day.pend .db-dot { background: transparent; border: 1.5px solid rgba(196,138,28,0.30); }

.db-day-name {
    font-weight: 400;
    font-size: 11px;
    width: 76px;
    color: var(--lp-text);
    font-family: var(--lp-font-label);
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.db-day-ch { flex: 1; font-size: 13px; color: var(--lp-text-2); font-family: var(--lp-font-body); }
.db-day-st { font-size: 14px; font-weight: 400; font-family: var(--lp-font-body); }
.db-day.done .db-day-st { color: #4AA870; }
.db-day.pend .db-day-st { color: var(--lp-text-3); }

.db-prog-item { margin-bottom: 14px; }
.db-prog-item:last-child { margin-bottom: 0; }
.db-prog-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 5px; }
.db-prog-name { font-size: 13px; font-weight: 400; color: var(--lp-text-2); font-family: var(--lp-font-body); }
.db-prog-pct { font-family: var(--lp-font-display); font-size: 16px; font-weight: 400; color: var(--lp-gold); }
.db-prog-track { height: 4px; background: rgba(196,138,28,0.10); border-radius: 100px; overflow: hidden; }
.db-prog-fill { height: 100%; border-radius: 100px; transition: width 1.2s cubic-bezier(0.22,1,0.36,1); }
.fill-terra { background-image: linear-gradient(90deg, rgba(196,138,28,0.8) 0%, var(--lp-gold-light) 50%, rgba(196,138,28,0.8) 100%); background-size: 200% 100%; animation: shimmer 2.8s linear infinite; box-shadow: 0 0 8px rgba(196,138,28,0.25); }
.fill-gold  { background: var(--lp-gold); }
.fill-ts    { background: rgba(196,138,28,0.7); }
.fill-tw    { background: rgba(196,138,28,0.5); }

.db-pi { display: flex; align-items: center; gap: 10px; padding: 9px 7px; border-radius: 8px; margin-bottom: 2px; transition: background 0.16s; }
.db-pi:hover { background: rgba(196,138,28,0.05); }

.db-pcat {
    width: 31px; height: 31px; border-radius: 8px;
    background: rgba(196,138,28,0.08);
    border: 1px solid rgba(196,138,28,0.14);
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0;
    transition: transform 0.22s;
}

.db-pi:hover .db-pcat { transform: scale(1.1); }

.db-pname {
    font-size: 13.5px;
    font-weight: 400;
    color: var(--lp-text-2);
    line-height: 1.3;
    font-family: var(--lp-font-body);
    font-style: italic;
}

.db-pmeta { font-size: 10.5px; color: var(--lp-text-3); margin-top: 1px; font-family: var(--lp-font-label); letter-spacing: 1px; }

.db-pbadge {
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 9.5px;
    font-weight: 400;
    flex-shrink: 0;
    font-family: var(--lp-font-label);
    letter-spacing: 1px;
    text-transform: uppercase;
}

.db-ongoing  { background: rgba(196,138,28,0.10); color: var(--lp-gold); border: 1px solid rgba(196,138,28,0.22); }
.db-answered { background: rgba(42,122,74,0.10); color: #4AA870; border: 1px solid rgba(42,122,74,0.22); }

.db-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 9px; }

.db-abtn {
    background: rgba(196,138,28,0.05);
    border: 1px solid rgba(196,138,28,0.14);
    border-radius: 10px;
    padding: 14px 10px;
    text-align: center;
    text-decoration: none;
    display: block;
    transition: all 0.22s;
}

.db-abtn:hover {
    border-color: var(--lp-gold);
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(196,138,28,0.14);
    background: rgba(196,138,28,0.08);
}

.db-aicon { font-size: 20px; margin-bottom: 6px; display: block; }

.db-albl {
    font-size: 9.5px;
    font-weight: 400;
    color: var(--lp-text-2);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-family: var(--lp-font-label);
}

@keyframes fire {
    0%,100%{ transform:scaleY(1) rotate(-2deg); }
    25%    { transform:scaleY(1.08) rotate(1deg); }
    50%    { transform:scaleY(0.95) rotate(-1deg); }
    75%    { transform:scaleY(1.05) rotate(2deg); }
}

/* ================================================================
   MOBILE — 768px
   ================================================================ */
@media (max-width: 768px) {
    [data-testid="column"] { padding: 0 4px !important; }

    .stTabs [data-baseweb="tab-list"] button {
        font-size: 10px !important;
        padding: 7px 10px !important;
    }

    [data-testid="stSegmentedControl"] button {
        font-size: 10px !important;
        padding: 6px 10px !important;
    }

    .hero-section    { padding: 28px 20px; border-radius: 18px; margin-bottom: 16px; }
    .hero-name       { font-size: 28px; }
    .hero-verse      { font-size: 14px; padding: 14px 16px 14px 28px; margin-top: 16px; }
    .hero-verse::before { font-size: 44px; left: 10px; }

    .page-header         { padding: 20px 20px 18px; border-radius: 18px; margin-bottom: 16px; }
    .page-header-title   { font-size: 20px; }
    .page-header-sub     { font-size: 9px; }

    .metric-card, .stat-card { padding: 14px 10px; border-radius: 12px; }
    .metric-value { font-size: 24px; }
    .stat-value   { font-size: 22px; }

    .section-card  { padding: 18px; border-radius: 12px; }
    .section-icon  { font-size: 24px; }
    .section-title { font-size: 15px; }
    .section-desc  { font-size: 12px; }

    .entry-card    { padding: 13px 15px; border-radius: 12px; }
    .today-card    { padding: 16px 18px; border-radius: 12px; }

    .prayer-card       { padding: 14px 16px; }
    .prayer-name       { font-size: 15px; }
    .prayer-title-row  { flex-wrap: wrap; gap: 6px; }

    .cat-card  { padding: 12px 8px; border-radius: 12px; }
    .cat-icon  { font-size: 22px; }
    .cat-name  { font-size: 10px; }

    .day-row     { padding: 10px 12px; font-size: 13px; }
    .day-name    { width: 72px; }
    .day-status  { font-size: 14px; }

    .streak-hero { padding: 24px 20px; border-radius: 18px; }
    .streak-num  { font-size: 52px; }

    .report-card { padding: 18px; font-size: 15px; line-height: 1.80; }

    .empty-state       { padding: 38px 16px; }
    .empty-state-icon  { font-size: 38px; }
    .empty-state-title { font-size: 16px; }

    .wizard-step         { padding: 16px 18px; }
    .wizard-step-title   { font-size: 14px; }
    .wizard-step-desc    { margin-left: 0; margin-top: 8px; }

    .sermon-card     { padding: 14px 16px; }
    .scripture-block { font-size: 14px; padding: 10px 14px; }
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
    .db-snum      { font-size: 48px; }

    .day-name  { width: 60px; }
    .day-row   { padding: 8px 10px; font-size: 12px; }

    .stTabs [data-baseweb="tab-list"] button {
        font-size: 9px !important;
        padding: 6px 8px !important;
    }
}
</style>
"""

# ==================== ENHANCEMENT CSS ====================
ENHANCEMENT_CSS = """
<style>
    [data-testid="stCheckbox"] label,
    [data-testid="stToggle"] label {
        font-family: 'Cardo', serif !important;
        font-size: 14px !important;
        color: var(--lp-text-2) !important;
    }

    .stCaption {
        font-family: 'Cinzel', serif !important;
        font-size: 10px !important;
        letter-spacing: 1.5px !important;
        color: var(--lp-text-3) !important;
    }

    [data-baseweb="select"] [data-baseweb="menu"] {
        border-radius: 10px !important;
        border: 1px solid rgba(196,138,28,0.18) !important;
        box-shadow: 0 8px 28px rgba(0,0,0,0.4) !important;
        background: #1A1108 !important;
        font-family: 'Cardo', serif !important;
    }

    [data-baseweb="select"] [data-baseweb="option"] {
        background: transparent !important;
        color: var(--lp-text-2) !important;
        font-family: 'Cardo', serif !important;
    }

    [data-baseweb="select"] [data-baseweb="option"]:hover,
    [data-baseweb="select"] [data-baseweb="option"][aria-selected="true"] {
        background: rgba(196,138,28,0.08) !important;
        color: var(--lp-gold) !important;
    }

    [data-baseweb="tag"] {
        background: rgba(196,138,28,0.10) !important;
        border-radius: 6px !important;
        border: 1px solid rgba(196,138,28,0.22) !important;
        color: var(--lp-gold) !important;
        font-weight: 400 !important;
        font-family: 'Cinzel', serif !important;
        font-size: 9px !important;
        letter-spacing: 1px !important;
    }

    /* Date/number inputs */
    input[type="date"], input[type="number"], input[type="time"] {
        color-scheme: dark !important;
        background: rgba(196,138,28,0.04) !important;
        color: var(--lp-text) !important;
        border: 1px solid rgba(196,138,28,0.18) !important;
    }

    /* Slider */
    [data-testid="stSlider"] [data-testid="stSliderTrack"] {
        background: rgba(196,138,28,0.12) !important;
    }
    [data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
        color: var(--lp-gold) !important;
        font-family: 'Cinzel', serif !important;
    }
</style>
"""


def inject_styles():
    """Inject the full Logos Pulse Illuminated Codex design system into the current page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    st.markdown(ENHANCEMENT_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render the Illuminated Codex page header with optional subtitle."""
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
        <div style="font-family:'Cinzel',serif;font-size:9px;letter-spacing:3px;color:rgba(196,138,28,0.30);text-transform:uppercase;margin-bottom:8px;">✦ &nbsp; ✦ &nbsp; ✦</div>
        <div class="lp-footer-brand">Logos Pulse</div>
        <div class="lp-footer-sub">Spiritual Chronicle &bull; Built with faith</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Render the Illuminated Codex sidebar logo."""
    st.markdown("""
    <div style="text-align:center; padding:16px 0 20px 0;">
        <div style="
            display:inline-flex;
            align-items:center;
            justify-content:center;
            width:48px; height:48px;
            border-radius:50%;
            border:1px solid rgba(196,138,28,0.30);
            background:radial-gradient(circle, rgba(196,138,28,0.12) 0%, transparent 70%);
            font-size:22px;
            margin-bottom:12px;
            box-shadow:0 0 20px rgba(196,138,28,0.15);
            animation:candleFlicker 6s ease-in-out infinite;
        ">✟</div>
        <div style="
            font-family:'IM Fell English','Cormorant',Georgia,serif;
            font-size:17px;
            font-weight:400;
            font-style:italic;
            color:#F5E8C0;
            letter-spacing:0.06em;
            line-height:1.2;
        ">
            Logos Pulse
        </div>
        <div style="
            font-family:'Cinzel',serif;
            font-size:7.5px;
            color:rgba(196,138,28,0.45);
            letter-spacing:3px;
            text-transform:uppercase;
            font-weight:400;
            margin-top:4px;
        ">
            Spiritual Chronicle
        </div>
    </div>
    """, unsafe_allow_html=True)