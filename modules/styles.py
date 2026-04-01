"""
Shared styles and UI components for Logos Pulse.
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
</style>
"""


def inject_styles():
    """Inject the shared CSS into the current page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)


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
