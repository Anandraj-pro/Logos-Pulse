"""
Shared styles and UI menu_style for Logos Pulse.
Provides a cohesive design system across all pages.
"""

import streamlit as st

# ==================== DESIGN TOKENS ====================
COLORS = {
    "primary": "#5B4FC4",
    "primary_light": "#7B6FD4",
    "primary_dark": "#3D35A0",
    "accent_gold": "#D4A843",
    "accent_warm": "#C47A3A",
    "surface": "#FAFAF8",
    "surface_warm": "#FFF9F0",
    "card_bg": "#FFFFFF",
    "card_border": "#EDE8F5",
    "text_primary": "#2A2438",
    "text_secondary": "#6B6580",
    "text_muted": "#9E96AB",
    "success": "#3A8F5C",
    "success_bg": "#E8F5E9",
    "warning": "#D4853A",
    "warning_bg": "#FFF3E0",
    "danger": "#C44B5B",
    "streak_fire": "#E85D3A",
    "streak_gold": "#D4A843",
}

# ==================== SHARED CSS ====================
SHARED_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600;700&display=swap');

    /* ---- Global Overrides ---- */
    .stApp {
        font-family: 'DM Sans', -apple-system, sans-serif;
    }
    h1, h2, h3 {
        font-family: 'DM Serif Display', Georgia, serif !important;
        color: #2A2438 !important;
    }

    /* ---- Streamlit Mobile Overrides ---- */
    @media (max-width: 768px) {
        /* Tighter column gaps on mobile */
        [data-testid="column"] {
            padding: 0 4px !important;
        }
        /* Smaller tab font */
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 13px !important;
            padding: 8px 12px !important;
        }
        /* Compact form elements */
        .stTextInput > div, .stSelectbox > div, .stMultiSelect > div {
            font-size: 14px !important;
        }
        /* Segmented control */
        [data-testid="stSegmentedControl"] button {
            font-size: 12px !important;
            padding: 6px 10px !important;
        }
    }

    /* ---- Page Header ---- */
    .page-header {
        background: linear-gradient(135deg, #5B4FC4 0%, #7B4FA0 50%, #9B5FA8 100%);
        border-radius: 18px;
        padding: 28px 28px 24px 28px;
        margin-bottom: 24px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: -40%;
        right: -15%;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .page-header-title {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 26px;
        font-weight: 400;
        letter-spacing: 0.3px;
        position: relative;
    }
    .page-header-sub {
        font-size: 13px;
        color: rgba(255,255,255,0.65);
        margin-top: 4px;
        font-weight: 400;
        letter-spacing: 0.2px;
        position: relative;
    }

    /* ---- Hero (Dashboard) ---- */
    .hero-section {
        background: linear-gradient(135deg, #5B4FC4 0%, #7B4FA0 50%, #9B5FA8 100%);
        border-radius: 20px;
        padding: 40px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-greeting {
        font-size: 13px;
        color: rgba(255,255,255,0.6);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
        font-weight: 500;
        position: relative;
    }
    .hero-name {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 36px;
        font-weight: 400;
        color: white;
        margin-bottom: 4px;
        line-height: 1.2;
        position: relative;
    }
    .hero-date {
        font-size: 14px;
        color: rgba(255,255,255,0.55);
        position: relative;
    }
    .hero-verse {
        margin-top: 20px;
        padding: 16px 20px;
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        font-family: 'DM Serif Display', Georgia, serif;
        font-style: italic;
        font-size: 15px;
        color: rgba(255,255,255,0.88);
        line-height: 1.7;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.06);
        position: relative;
    }

    /* ---- Metric Cards ---- */
    .metric-card {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(91, 79, 196, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(91, 79, 196, 0.1);
    }
    .metric-value {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 32px;
        font-weight: 400;
        line-height: 1;
        margin-bottom: 4px;
    }
    .metric-label {
        font-size: 11px;
        color: #9E96AB;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }

    /* ---- Section Cards ---- */
    .section-card {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .section-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(91, 79, 196, 0.08);
    }
    .section-icon { font-size: 28px; margin-bottom: 8px; }
    .section-title {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 18px;
        font-weight: 400;
        color: #2A2438;
        margin-bottom: 4px;
    }
    .section-desc {
        font-size: 13px;
        color: #9E96AB;
        line-height: 1.5;
    }

    /* ---- Section Labels ---- */
    .section-label {
        font-size: 11px;
        color: #9E96AB;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        font-weight: 600;
        margin: 20px 0 10px 0;
    }

    /* ---- Today Status Cards ---- */
    .today-card {
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .today-done {
        background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
        border: 1px solid #C8E6C9;
    }
    .today-pending {
        background: linear-gradient(135deg, #FFF3E0, #FFF8E1);
        border: 1px solid #FFE0B2;
    }
    .today-title { font-size: 16px; font-weight: 600; margin-bottom: 8px; }
    .today-detail { font-size: 14px; color: #6B6580; line-height: 1.6; }

    /* ---- Progress Bars ---- */
    .progress-section {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .progress-title {
        font-size: 14px;
        font-weight: 600;
        color: #6B6580;
        margin-bottom: 12px;
    }
    .progress-bar-bg {
        background: #EDE8F5;
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #5B4FC4, #9B5FA8);
        transition: width 0.6s ease;
    }
    .progress-label {
        font-size: 12px;
        color: #9E96AB;
        margin-top: 6px;
    }

    /* ---- Entry / Data Cards ---- */
    .entry-card {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 10px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.02);
        transition: box-shadow 0.15s ease;
    }
    .entry-card:hover {
        box-shadow: 0 3px 12px rgba(91, 79, 196, 0.07);
    }

    /* ---- Report Card (scripture/parchment feel) ---- */
    .report-card {
        background: linear-gradient(135deg, #FFF9F0, #FFFEF8);
        border: 1px solid #E8DCC8;
        border-radius: 14px;
        padding: 24px;
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 16px;
        line-height: 1.8;
        color: #3C2F1E;
        white-space: pre-line;
    }

    /* ---- Goal / Info Banners ---- */
    .goal-banner {
        background: linear-gradient(135deg, #EDEBFA, #F5EEFA);
        border: 1px solid #D1C4E9;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 14px;
        color: #3D35A0;
        font-weight: 500;
        margin-bottom: 12px;
    }

    /* ---- Calendar Styles ---- */
    .cal-header, .heatmap-header {
        text-align: center;
        font-size: 11px;
        color: #9E96AB;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 4px;
    }
    .cal-day, .heatmap-day {
        text-align: center;
        border-radius: 8px;
        padding: 6px 4px;
        font-size: 13px;
        font-weight: 500;
        margin: 2px;
    }
    .cal-done, .heatmap-done {
        background: linear-gradient(135deg, #5B4FC4, #9B5FA8);
        color: white;
        font-weight: 700;
    }
    .cal-empty { color: #D0C8DB; }
    .heatmap-missed { background: #FFEBEE; color: #FFAB91; }
    .heatmap-future { color: #D0C8DB; }

    /* ---- Day Rows (Weekly Assignment) ---- */
    .day-row {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        margin: 4px 0;
        border-radius: 10px;
        font-size: 15px;
    }
    .day-done { background: #E8F5E9; }
    .day-pending { background: #FFF3E0; }
    .day-name { font-weight: 600; width: 100px; }
    .day-chapters { flex: 1; color: #6B6580; }
    .day-status { font-size: 18px; }

    /* ---- Streak Hero ---- */
    .streak-hero {
        border-radius: 16px;
        padding: 32px 28px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    .streak-num {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 64px;
        font-weight: 400;
        line-height: 1;
    }
    .streak-label {
        font-size: 12px;
        color: rgba(255,255,255,0.75);
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 6px;
        font-weight: 500;
    }

    /* ---- Stat Cards ---- */
    .stat-card {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        transition: transform 0.15s ease;
    }
    .stat-card:hover {
        transform: translateY(-1px);
    }
    .stat-value {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 28px;
        font-weight: 400;
        line-height: 1;
    }
    .stat-label {
        font-size: 11px;
        color: #9E96AB;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 6px;
        font-weight: 500;
    }

    /* ---- Settings ---- */
    .settings-section {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.02);
    }

    /* ---- Prayer Journal ---- */
    .cat-card {
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        border: 2px solid transparent;
    }
    .cat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .cat-card-active {
        border: 2px solid currentColor;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .cat-icon { font-size: 28px; margin-bottom: 4px; }
    .cat-name { font-size: 13px; font-weight: 600; }
    .cat-count { font-size: 11px; opacity: 0.7; }

    .wizard-step {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.02);
    }
    .wizard-step-num {
        display: inline-block;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        text-align: center;
        line-height: 28px;
        font-size: 14px;
        font-weight: 700;
        color: white;
        margin-right: 10px;
    }
    .wizard-step-title {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 16px;
        font-weight: 400;
        color: #2A2438;
        display: inline;
    }
    .wizard-step-desc {
        font-size: 13px;
        color: #9E96AB;
        margin: 4px 0 12px 38px;
    }

    .prayer-card {
        background: white;
        border: 1px solid #EDE8F5;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 12px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.02);
        transition: box-shadow 0.15s ease;
    }
    .prayer-card:hover {
        box-shadow: 0 3px 12px rgba(91, 79, 196, 0.07);
    }
    .prayer-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .prayer-name {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 16px;
        font-weight: 400;
        color: #2A2438;
    }
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }
    .scripture-block {
        background: #FFF9F0;
        border-left: 3px solid;
        padding: 10px 14px;
        margin: 6px 0;
        border-radius: 6px;
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 14px;
        line-height: 1.7;
        color: #3C2F1E;
    }
    .confession-block {
        background: #E8F5E9;
        border-radius: 10px;
        padding: 12px 16px;
        font-weight: 500;
        color: #2E7D32;
        line-height: 1.7;
    }
    .declaration-block {
        background: #FFF3E0;
        border-radius: 10px;
        padding: 12px 16px;
        font-weight: 600;
        color: #E65100;
        line-height: 1.7;
    }

    /* ---- Prayer Pills ---- */
    .prayer-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        margin: 3px 4px;
    }

    /* ---- Sermon Notes ---- */
    .sermon-card {
        background: linear-gradient(135deg, #FEFEFE, #FFF9F0);
        border: 1px solid #E8DCC8;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 10px 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
        transition: box-shadow 0.15s ease, transform 0.15s ease;
    }
    .sermon-card:hover {
        box-shadow: 0 4px 16px rgba(91, 79, 196, 0.08);
        transform: translateY(-1px);
    }

    /* ---- Empty States ---- */
    .empty-state {
        text-align: center;
        padding: 48px 20px;
    }
    .empty-state-icon { font-size: 48px; margin-bottom: 12px; opacity: 0.6; }
    .empty-state-title { font-size: 16px; color: #9E96AB; font-weight: 500; }
    .empty-state-sub { font-size: 13px; color: #C0B8CC; margin-top: 4px; }

    /* ============================================================
       MOBILE RESPONSIVE (max-width: 768px)
       ============================================================ */
    @media (max-width: 768px) {
        /* Reduce main padding */
        .stApp > header + div > div > div > div {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }

        /* Hero section */
        .hero-section {
            padding: 24px 18px;
            border-radius: 14px;
            margin-bottom: 16px;
        }
        .hero-name {
            font-size: 26px;
        }
        .hero-greeting {
            font-size: 11px;
            letter-spacing: 1.5px;
        }
        .hero-date {
            font-size: 12px;
        }
        .hero-verse {
            font-size: 13px;
            padding: 12px 14px;
            margin-top: 14px;
        }

        /* Page header */
        .page-header {
            padding: 20px 18px 16px 18px;
            border-radius: 14px;
            margin-bottom: 16px;
        }
        .page-header-title {
            font-size: 20px;
        }
        .page-header-sub {
            font-size: 12px;
        }

        /* Metric & stat cards */
        .metric-card, .stat-card {
            padding: 14px 10px;
            border-radius: 12px;
        }
        .metric-value {
            font-size: 24px;
        }
        .stat-value {
            font-size: 22px;
        }
        .metric-label, .stat-label {
            font-size: 9px;
            letter-spacing: 0.8px;
        }

        /* Section cards */
        .section-card {
            padding: 16px;
            border-radius: 12px;
        }
        .section-icon { font-size: 24px; }
        .section-title { font-size: 15px; }
        .section-desc { font-size: 12px; }

        /* Entry cards */
        .entry-card {
            padding: 12px 14px;
            border-radius: 12px;
        }

        /* Today cards */
        .today-card {
            padding: 14px 16px;
            border-radius: 12px;
        }
        .today-title { font-size: 14px; }
        .today-detail { font-size: 13px; }

        /* Progress sections */
        .progress-section {
            padding: 14px 16px;
            border-radius: 12px;
        }

        /* Day rows */
        .day-row {
            padding: 10px 12px;
            font-size: 13px;
        }
        .day-name {
            width: 70px;
            font-size: 13px;
        }

        /* Streak hero */
        .streak-hero {
            padding: 20px 16px;
            border-radius: 12px;
        }
        .streak-num {
            font-size: 48px;
        }

        /* Report card */
        .report-card {
            padding: 16px;
            font-size: 14px;
        }

        /* Prayer cards */
        .prayer-card {
            padding: 14px 16px;
        }
        .prayer-name {
            font-size: 14px;
        }
        .prayer-title-row {
            flex-wrap: wrap;
            gap: 6px;
        }

        /* Category cards */
        .cat-card {
            padding: 12px 8px;
            border-radius: 10px;
        }
        .cat-icon { font-size: 22px; }
        .cat-name { font-size: 11px; }
        .cat-count { font-size: 10px; }

        /* Wizard */
        .wizard-step {
            padding: 14px 16px;
        }
        .wizard-step-title { font-size: 14px; }
        .wizard-step-desc {
            margin-left: 0;
            margin-top: 8px;
        }

        /* Sermon cards */
        .sermon-card {
            padding: 14px 16px;
        }

        /* Scripture blocks */
        .scripture-block {
            font-size: 13px;
            padding: 8px 12px;
        }

        /* Section label */
        .section-label {
            font-size: 10px;
            letter-spacing: 1.5px;
        }

        /* Prayer pills */
        .prayer-pill {
            padding: 4px 10px;
            font-size: 11px;
            margin: 2px 3px;
        }

        /* Goal banner */
        .goal-banner {
            font-size: 13px;
            padding: 10px 14px;
        }

        /* Empty state */
        .empty-state {
            padding: 32px 16px;
        }
        .empty-state-icon { font-size: 36px; }
        .empty-state-title { font-size: 14px; }
    }

    /* ============================================================
       SMALL MOBILE (max-width: 480px)
       ============================================================ */
    @media (max-width: 480px) {
        .hero-name { font-size: 22px; }
        .hero-section { padding: 20px 14px; }
        .page-header { padding: 16px 14px 14px 14px; }
        .page-header-title { font-size: 18px; }
        .metric-value { font-size: 20px; }
        .stat-value { font-size: 18px; }
        .streak-num { font-size: 40px; }
        .day-name { width: 60px; font-size: 12px; }
        .day-row { padding: 8px 10px; font-size: 12px; }
    }

    /* ============================================================
       V2 DESIGN SYSTEM — Glowing borders, background, animations
       ============================================================ */

    /* ---- Third font for scripture ---- */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&display=swap');

    /* ---- CSS Custom Properties ---- */
    :root {
        --lp-primary: #4A3FB0;
        --lp-primary-light: #6B5FD4;
        --lp-primary-dark: #362E8A;
        --lp-gold: #C9982A;
        --lp-gold-light: #E8C560;
        --lp-gold-dark: #9B7420;
        --lp-cream: #FFF9F0;
        --lp-surface: #FAFAF8;
        --lp-card-glow: rgba(74, 63, 176, 0.08);
        --lp-gold-glow: rgba(201, 152, 42, 0.12);
    }

    /* ---- Subtle background texture ---- */
    .stApp {
        background:
            radial-gradient(circle at 20% 20%, rgba(74, 63, 176, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(201, 152, 42, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(155, 95, 168, 0.02) 0%, transparent 70%),
            #FAFAF8 !important;
    }

    /* ---- Keyframe animations ---- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 8px rgba(74, 63, 176, 0.1); }
        50% { box-shadow: 0 0 20px rgba(74, 63, 176, 0.2); }
    }
    @keyframes goldShimmer {
        0% { background-position: -300% 50%; }
        100% { background-position: 300% 50%; }
    }

    /* ---- Staggered page load ---- */
    .page-header { animation: fadeInUp 0.4s ease both; }
    .hero-section { animation: fadeInUp 0.5s ease both; }
    .metric-card { animation: fadeInUp 0.4s ease both; }
    .stat-card { animation: fadeInUp 0.4s ease both; }
    .section-card { animation: fadeInUp 0.5s ease both; }
    .entry-card { animation: fadeInUp 0.3s ease both; }
    .today-card { animation: fadeInUp 0.4s ease both; }
    .progress-section { animation: fadeInUp 0.5s ease both; }

    /* ---- Glowing card borders ---- */
    .entry-card {
        border: 1px solid rgba(74, 63, 176, 0.08);
        transition: all 0.25s ease;
    }
    .entry-card:hover {
        border-color: rgba(74, 63, 176, 0.15);
        box-shadow:
            0 4px 16px rgba(74, 63, 176, 0.08),
            0 0 0 1px rgba(74, 63, 176, 0.05);
    }

    .section-card {
        border: 1px solid rgba(74, 63, 176, 0.06);
        transition: all 0.3s ease;
    }
    .section-card:hover {
        border-color: rgba(201, 152, 42, 0.2);
        box-shadow:
            0 8px 24px rgba(74, 63, 176, 0.06),
            0 0 0 1px rgba(201, 152, 42, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        transform: translateY(-3px);
    }

    .metric-card {
        border: 1px solid rgba(74, 63, 176, 0.06);
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold), var(--lp-primary));
        background-size: 200% 100%;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .metric-card:hover::after {
        opacity: 1;
        animation: shimmer 2s linear infinite;
    }
    .metric-card:hover {
        box-shadow: 0 6px 20px rgba(74, 63, 176, 0.1);
        transform: translateY(-2px);
    }

    .stat-card {
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
        opacity: 0;
        transition: opacity 0.3s;
    }
    .stat-card:hover::after { opacity: 1; }
    .stat-card:hover {
        box-shadow: 0 6px 18px rgba(74, 63, 176, 0.08);
        transform: translateY(-2px);
    }

    /* ---- Enhanced hero ---- */
    .hero-section {
        background:
            radial-gradient(ellipse at 30% 20%, rgba(201, 152, 42, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at 70% 80%, rgba(155, 95, 168, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, #4A3FB0 0%, #6B4FA0 40%, #9B5FA8 70%, #4A3FB0 100%);
        background-size: 100% 100%, 100% 100%, 200% 200%;
        animation: fadeInUp 0.5s ease both;
    }

    .hero-verse {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(201, 152, 42, 0.15);
        position: relative;
    }
    .hero-verse::before {
        content: '\201C';
        position: absolute;
        top: -8px;
        left: 12px;
        font-size: 40px;
        color: rgba(201, 152, 42, 0.3);
        font-family: 'Cormorant Garamond', Georgia, serif;
        line-height: 1;
    }

    /* ---- Enhanced page header ---- */
    .page-header {
        background:
            radial-gradient(ellipse at 80% 20%, rgba(201, 152, 42, 0.12) 0%, transparent 50%),
            linear-gradient(135deg, #4A3FB0 0%, #6B4FA0 50%, #9B5FA8 100%);
    }

    /* ---- Gold accent progress bar ---- */
    .progress-bar-fill {
        background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold), var(--lp-primary));
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }

    /* ---- Scripture typography ---- */
    .report-card,
    .scripture-block {
        font-family: 'Cormorant Garamond', 'DM Serif Display', Georgia, serif;
    }

    /* ---- Prayer card glow ---- */
    .prayer-card {
        transition: all 0.25s ease;
    }
    .prayer-card:hover {
        border-color: rgba(74, 63, 176, 0.12);
        box-shadow:
            0 4px 16px rgba(74, 63, 176, 0.06),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }

    /* ---- Sermon card warmth ---- */
    .sermon-card {
        transition: all 0.25s ease;
    }
    .sermon-card:hover {
        border-color: rgba(201, 152, 42, 0.2);
        box-shadow: 0 6px 20px rgba(201, 152, 42, 0.08);
    }

    /* ---- Today card pulse ---- */
    .today-pending {
        animation: fadeInUp 0.4s ease both, pulseGlow 3s ease-in-out infinite;
        border-color: rgba(212, 133, 58, 0.3);
    }

    /* ---- Sidebar branding ---- */
    [data-testid="stSidebar"] > div:first-child {
        background:
            linear-gradient(180deg, rgba(74, 63, 176, 0.03) 0%, transparent 30%),
            #FAFAF8;
    }

    /* ---- Streamlit tab pills ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(74, 63, 176, 0.04);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: white !important;
        box-shadow: 0 2px 8px rgba(74, 63, 176, 0.1) !important;
    }

    /* ---- Button improvements ---- */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--lp-primary), var(--lp-primary-light)) !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 16px rgba(74, 63, 176, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* ---- Form input focus ---- */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--lp-primary) !important;
        box-shadow: 0 0 0 2px rgba(74, 63, 176, 0.1) !important;
    }

    /* ---- Footer ---- */
    .lp-footer {
        text-align: center;
        padding: 24px 16px;
        margin-top: 40px;
        border-top: 1px solid rgba(74, 63, 176, 0.08);
        position: relative;
    }
    .lp-footer::before {
        content: '';
        position: absolute;
        top: -1px;
        left: 20%;
        right: 20%;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--lp-gold), transparent);
    }
    .lp-footer-brand {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 14px;
        background: linear-gradient(135deg, var(--lp-primary), var(--lp-gold));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .lp-footer-sub {
        font-size: 11px;
        color: #C0B8CC;
        margin-top: 4px;
    }
</style>
"""

# ==================== V2 ENHANCEMENT CSS ====================
ENHANCEMENT_CSS = """
<style>
    /* Additional Streamlit-specific overrides that need separate injection */
    [data-testid="stForm"] {
        border: 1px solid rgba(74, 63, 176, 0.08) !important;
        border-radius: 14px !important;
        padding: 20px !important;
        background: white !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02) !important;
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(74, 63, 176, 0.08) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(74, 63, 176, 0.15) !important;
    }
</style>
"""


def inject_styles():
    """Inject the shared CSS into the current page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    st.markdown(ENHANCEMENT_CSS, unsafe_allow_html=True)


def page_header(icon: str, title: str, subtitle: str = ""):
    """Render a consistent gradient page header."""
    sub_html = f'<div class="page-header-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-title">{icon} {title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def section_label(text: str):
    """Render a consistent section label."""
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def empty_state(icon: str, title: str, subtitle: str = ""):
    """Render a consistent empty state."""
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
    """Render the branded app footer."""
    st.markdown("""
    <div class="lp-footer">
        <div class="lp-footer-brand">\U0001f64f Logos Pulse</div>
        <div class="lp-footer-sub">Spiritual Growth Tracker &bull; Built with faith</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_logo():
    """Render the logo in the sidebar."""
    st.markdown("""
    <div style="text-align:center; padding:8px 0 16px 0;">
        <div style="font-size:32px; margin-bottom:4px;">\U0001f64f</div>
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:18px;
                    background:linear-gradient(135deg, #4A3FB0, #C9982A);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text;">
            Logos Pulse
        </div>
    </div>
    """, unsafe_allow_html=True)
