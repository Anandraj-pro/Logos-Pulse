"""
Logos Pulse Design System v4 — Sacred Codex
Elevates every screen with Cinzel display type, richer depth, and refined warmth.
"""

import streamlit as st

# ==================== DESIGN TOKENS ====================
COLORS = {
    "primary":          "#2A1D7E",
    "primary_light":    "#4B3DC0",
    "primary_dark":     "#170F4A",
    "accent_gold":      "#C4902A",
    "accent_gold_light":"#E8C050",
    "accent_gold_dark": "#8A6018",
    "accent_gold_pale": "#FAF0D8",
    "surface":          "#F3F0E8",
    "surface_warm":     "#FEFCF8",
    "card_bg":          "#FEFCF8",
    "card_border":      "rgba(165, 135, 65, 0.14)",
    "text_primary":     "#140F1A",
    "text_secondary":   "#3A3255",
    "text_muted":       "#8A85A0",
    "success":          "#1E5E3E",
    "success_bg":       "#E4F2EB",
    "warning":          "#A84C16",
    "warning_bg":       "#FFF1E4",
    "danger":           "#9C2424",
    "streak_fire":      "#D44A22",
    "streak_gold":      "#C4902A",
}

# ==================== SHARED CSS ====================
SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Spectral:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Nunito:wght@300;400;500;600;700;800&display=swap');

/* ================================================================
   DESIGN TOKENS
   ================================================================ */
:root {
    --lp-primary:        #2A1D7E;
    --lp-primary-light:  #4B3DC0;
    --lp-primary-dark:   #170F4A;
    --lp-gold:           #C4902A;
    --lp-gold-light:     #E8C050;
    --lp-gold-dark:      #8A6018;
    --lp-gold-pale:      #FAF0D8;
    --lp-bg:             #F3F0E8;
    --lp-surface:        #FEFCF8;
    --lp-border:         rgba(165, 135, 65, 0.14);
    --lp-border-strong:  rgba(165, 135, 65, 0.30);
    --lp-text:           #140F1A;
    --lp-text-2:         #3A3255;
    --lp-text-3:         #8A85A0;
    --lp-success:        #1E5E3E;
    --lp-warning:        #A84C16;
    --lp-danger:         #9C2424;
    --lp-r-sm:  10px;
    --lp-r-md:  16px;
    --lp-r-lg:  22px;
    --lp-shadow-xs: 0 1px 4px rgba(42,29,126,0.04), 0 1px 2px rgba(20,15,26,0.03);
    --lp-shadow-sm: 0 2px 10px rgba(42,29,126,0.06), 0 1px 4px rgba(20,15,26,0.04);
    --lp-shadow-md: 0 6px 24px rgba(42,29,126,0.09), 0 2px 8px rgba(20,15,26,0.05);
    --lp-shadow-lg: 0 14px 44px rgba(42,29,126,0.12), 0 4px 12px rgba(20,15,26,0.06);
    --lp-glow-indigo: 0 6px 28px rgba(42,29,126,0.22);
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
   GLOBAL BASE
   ================================================================ */
.stApp {
    font-family: 'Nunito', -apple-system, sans-serif !important;
    background:
        radial-gradient(ellipse at 6% 6%,   rgba(42,29,126,0.055) 0%, transparent 40%),
        radial-gradient(ellipse at 94% 90%,  rgba(196,144,42,0.05)  0%, transparent 40%),
        radial-gradient(ellipse at 50% -4%,  rgba(75,61,192,0.035) 0%, transparent 45%),
        radial-gradient(ellipse at 50% 108%, rgba(138,96,168,0.025) 0%, transparent 45%),
        #F3F0E8 !important;
    color: var(--lp-text) !important;
}

h1, h2, h3 {
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif !important;
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
    background:
        radial-gradient(ellipse at 15% 12%, rgba(196,144,42,0.22) 0%, transparent 52%),
        radial-gradient(ellipse at 84% 82%, rgba(138,96,168,0.18) 0%, transparent 50%),
        radial-gradient(ellipse at 52%  3%, rgba(75,61,192,0.12)  0%, transparent 38%),
        linear-gradient(142deg, #170F4A 0%, #2A1D7E 28%, #4B3DA8 60%, #6B3FA8 100%);
    border-radius: var(--lp-r-lg);
    padding: 46px 38px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 28px 70px rgba(42,29,126,0.35),
        0 6px 18px rgba(42,29,126,0.22),
        inset 0 1px 0 rgba(255,255,255,0.11),
        inset 0 -1px 0 rgba(0,0,0,0.08);
    animation: riseUp 0.7s cubic-bezier(0.22,1,0.36,1) both;
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
    font-family: 'Cinzel', serif;
    font-size: 10px;
    font-weight: 600;
    color: rgba(196,144,42,0.92);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 10px;
    position: relative;
}

.hero-name {
    font-family: 'Cinzel', serif;
    font-size: 42px;
    font-weight: 700;
    color: white;
    line-height: 1.12;
    margin-bottom: 5px;
    position: relative;
    text-shadow: 0 3px 22px rgba(0,0,0,0.32);
    letter-spacing: 0.02em;
}

.hero-date {
    font-size: 12px;
    color: rgba(255,255,255,0.42);
    position: relative;
    font-weight: 600;
    letter-spacing: 0.6px;
    font-family: 'Nunito', sans-serif;
}

.hero-verse {
    margin-top: 24px;
    padding: 20px 22px 20px 36px;
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    font-family: 'Spectral', 'EB Garamond', Georgia, serif;
    font-style: italic;
    font-size: 16px;
    color: rgba(255,255,255,0.88);
    line-height: 1.82;
    border: 1px solid rgba(196,144,42,0.24);
    position: relative;
    backdrop-filter: blur(6px);
}

.hero-verse::before {
    content: '\201C';
    position: absolute;
    top: -4px;
    left: 12px;
    font-size: 60px;
    color: rgba(196,144,42,0.40);
    font-family: 'Spectral', Georgia, serif;
    line-height: 1;
    font-style: normal;
}

/* ================================================================
   PAGE HEADER
   ================================================================ */
.page-header {
    background:
        radial-gradient(ellipse at 82% 18%, rgba(196,144,42,0.18) 0%, transparent 52%),
        radial-gradient(ellipse at 14% 86%, rgba(138,96,168,0.12) 0%, transparent 46%),
        linear-gradient(142deg, #170F4A 0%, #2A1D7E 38%, #4B3DA8 100%);
    border-radius: var(--lp-r-lg);
    padding: 28px 34px 26px 34px;
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 16px 50px rgba(42,29,126,0.28),
        0 2px 10px rgba(42,29,126,0.16),
        inset 0 1px 0 rgba(255,255,255,0.10);
    animation: fadeInUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
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
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
    font-size: 24px;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: white;
    position: relative;
    text-shadow: 0 2px 16px rgba(0,0,0,0.24);
}

.page-header-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.50);
    margin-top: 6px;
    font-weight: 600;
    letter-spacing: 0.4px;
    position: relative;
    font-family: 'Nunito', sans-serif;
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
    background: linear-gradient(135deg, rgba(42,29,126,0.055), rgba(75,61,192,0.038));
    border: 1px solid rgba(42,29,126,0.12);
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
    font-family: 'Cinzel', serif;
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
    font-family: 'Nunito', sans-serif;
}

.growth-badge-seed    { background: rgba(138,96,24,0.08);  color: #8A6018; border: 1px solid rgba(138,96,24,0.18); }
.growth-badge-sprout  { background: rgba(30,94,62,0.08);   color: #1E5E3E; border: 1px solid rgba(30,94,62,0.18); }
.growth-badge-sapling { background: rgba(42,29,126,0.07);  color: #2A1D7E; border: 1px solid rgba(42,29,126,0.16); }
.growth-badge-tree    { background: rgba(196,144,42,0.10); color: #8A6018; border: 1px solid rgba(196,144,42,0.22); animation: aureate 3.5s ease-in-out infinite; }
.growth-badge-forest  { background: linear-gradient(135deg, rgba(42,29,126,0.10), rgba(196,144,42,0.08)); color: #2A1D7E; border: 1px solid rgba(196,144,42,0.28); animation: aureate 3s ease-in-out infinite; }

/* ================================================================
   SECTION LABEL
   ================================================================ */
.section-label {
    font-size: 10px;
    color: var(--lp-text-3);
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: 800;
    font-family: 'Cinzel', serif;
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
    border-color: rgba(42,29,126,0.18);
}

.metric-card:hover::before { opacity: 1; }

.metric-value {
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
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
    font-family: 'Nunito', sans-serif;
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
    border-color: rgba(42,29,126,0.16);
}

.stat-card:hover::before { opacity: 1; }

.stat-value {
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
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
    font-family: 'Nunito', sans-serif;
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
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
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
    font-family: 'Nunito', sans-serif;
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
    background: linear-gradient(90deg, rgba(42,29,126,0.07), rgba(196,144,42,0.07));
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
    box-shadow: 0 0 12px rgba(42,29,126,0.30);
    transition: width 0.8s cubic-bezier(0.22,1,0.36,1);
}

.progress-label {
    font-size: 12px;
    color: var(--lp-text-3);
    margin-top: 8px;
    font-weight: 700;
    font-family: 'Nunito', sans-serif;
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
    font-family: 'Spectral', 'EB Garamond', Georgia, serif;
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
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
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
    font-family: 'Nunito', sans-serif;
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
    font-family: 'Spectral', 'EB Garamond', Georgia, serif;
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
.cat-name  { font-size: 13px; font-weight: 800; letter-spacing: 0.3px; font-family: 'Nunito', sans-serif; }
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
    font-family: 'Nunito', sans-serif;
}

.wizard-step-title {
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
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
    font-family: 'Nunito', sans-serif;
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
    font-family: 'Cinzel', Georgia, serif;
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
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
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
    font-family: 'Cinzel', sans-serif;
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
    font-family: 'Nunito', sans-serif;
}

.cal-day, .heatmap-day {
    text-align: center;
    border-radius: 8px;
    padding: 6px 4px;
    font-size: 13px;
    font-weight: 600;
    margin: 2px;
    font-family: 'Nunito', sans-serif;
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
.day-name       { font-weight: 800; width: 100px; color: var(--lp-text); font-family: 'Nunito', sans-serif; }
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
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
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
    font-family: 'Nunito', sans-serif;
}

/* ================================================================
   SIDEBAR
   ================================================================ */
[data-testid="stSidebar"] > div:first-child {
    background:
        radial-gradient(ellipse at 50% 0%,   rgba(42,29,126,0.060) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 100%,  rgba(196,144,42,0.035) 0%, transparent 50%),
        linear-gradient(180deg, #EDE9DF 0%, #E8E4DC 100%) !important;
    border-right: 1px solid rgba(42,29,126,0.07) !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 14px !important;
    transition: all 0.22s ease !important;
    color: var(--lp-text-2) !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
    background: rgba(42,29,126,0.06) !important;
    transform: translateX(3px);
}

[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
    background: rgba(42,29,126,0.09) !important;
    border-left: 3px solid var(--lp-gold) !important;
    color: var(--lp-primary) !important;
    font-weight: 800 !important;
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
    font-family: 'Nunito', sans-serif !important;
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
    font-family: 'Nunito', sans-serif !important;
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
    font-family: 'Nunito', sans-serif !important;
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
    font-family: 'Nunito', sans-serif !important;
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
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
}

/* ================================================================
   DOWNLOAD BUTTON
   ================================================================ */
[data-testid="stDownloadButton"] > button {
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-family: 'Nunito', sans-serif !important;
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
        font-family: 'Nunito', sans-serif !important;
        font-weight: 600 !important;
        color: #3A3255 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderTrack"] {
        background: rgba(42,29,126,0.10) !important;
    }
    .stCaption {
        font-family: 'Nunito', sans-serif !important;
        color: #8A85A0 !important;
    }
    [data-baseweb="select"] [data-baseweb="menu"] {
        border-radius: 12px !important;
        border: 1px solid rgba(42,29,126,0.10) !important;
        box-shadow: 0 8px 28px rgba(42,29,126,0.10) !important;
        font-family: 'Nunito', sans-serif !important;
    }
    [data-baseweb="tag"] {
        background: rgba(42,29,126,0.09) !important;
        border-radius: 8px !important;
        color: #2A1D7E !important;
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
        <div class="lp-footer-brand">&#9997; Logos Pulse</div>
        <div class="lp-footer-sub">Spiritual Growth Tracker &bull; Built with faith</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Render the sidebar logo block."""
    st.markdown("""
    <div style="text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:36px; margin-bottom:8px;">&#128591;</div>
        <div style="
            font-family:'Cinzel','Playfair Display',Georgia,serif;
            font-size:18px;
            font-weight:600;
            background: linear-gradient(135deg, #2A1D7E, #C4902A);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 0.06em;
        ">
            Logos Pulse
        </div>
        <div style="
            font-size:9px;
            color:#8A85A0;
            letter-spacing:2.5px;
            text-transform:uppercase;
            font-weight:800;
            margin-top:3px;
            font-family:'Nunito',sans-serif;
        ">
            Spiritual Tracker
        </div>
    </div>
    """, unsafe_allow_html=True)
