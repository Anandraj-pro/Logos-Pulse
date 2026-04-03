# Logos Pulse UI Overhaul Plan v2.0

**Design Direction:** Modern Spiritual Warmth -- stained glass meets minimal tech.
**Framework:** Streamlit (Python) with `st.markdown(unsafe_allow_html=True)` for all custom CSS/HTML.
**Date:** 2026-03-31

---

## Table of Contents

1. [Logo & Branding](#1-logo--branding)
2. [Color System Upgrade](#2-color-system-upgrade)
3. [Typography Enhancement](#3-typography-enhancement)
4. [Header/Hero Redesign](#4-headerhero-redesign)
5. [Card System](#5-card-system)
6. [Navigation Improvements](#6-navigation-improvements)
7. [Button & Form Styling](#7-button--form-styling)
8. [Data Visualization Style](#8-data-visualization-style)
9. [Micro-interactions & Animations](#9-micro-interactions--animations)
10. [Footer](#10-footer)
11. [Empty States & Loading](#11-empty-states--loading)
12. [Mobile-specific Enhancements](#12-mobile-specific-enhancements)

---

## 1. Logo & Branding

### What's wrong now
No dedicated logo. The app name appears as plain text. No favicon. The sidebar has no branded header -- it looks like a default Streamlit sidebar.

### What to change
Create a CSS-based logo mark (cross + pulse line motif), add a branded sidebar header, and set a favicon.

### Priority: HIGH

### Implementation

**Favicon** -- add to `.streamlit/config.toml` or use `st.set_page_config`:
```python
st.set_page_config(
    page_title="Logos Pulse",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#x271A;</text></svg>",
    layout="wide"
)
```

**CSS Logo Component** -- inject in sidebar:
```html
<style>
    .lp-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 20px 0;
        border-bottom: 1px solid rgba(91, 79, 196, 0.12);
        margin-bottom: 16px;
    }
    .lp-logo-mark {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #5B4FC4 0%, #8B5FA8 50%, #D4A843 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 4px 12px rgba(91, 79, 196, 0.3);
    }
    .lp-logo-mark::after {
        content: '';
        width: 20px;
        height: 20px;
        border: 2.5px solid white;
        border-radius: 50%;
        position: relative;
    }
    .lp-logo-mark::before {
        content: '+';
        position: absolute;
        color: white;
        font-size: 20px;
        font-weight: 300;
        z-index: 1;
    }
    .lp-logo-text {
        display: flex;
        flex-direction: column;
    }
    .lp-logo-name {
        font-family: 'DM Serif Display', Georgia, serif;
        font-size: 18px;
        color: #2A2438;
        line-height: 1.1;
        letter-spacing: 0.5px;
    }
    .lp-logo-tagline {
        font-size: 10px;
        color: #9E96AB;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 500;
    }
</style>
```

**Python helper** -- add to `modules/styles.py`:
```python
def sidebar_branding():
    """Render branded sidebar header."""
    with st.sidebar:
        st.markdown("""
        <div class="lp-logo-container">
            <div class="lp-logo-mark"></div>
            <div class="lp-logo-text">
                <span class="lp-logo-name">Logos Pulse</span>
                <span class="lp-logo-tagline">Spiritual Growth</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
```

**SVG Logo alternative** (for pages that need inline SVG):
```html
<svg width="42" height="42" viewBox="0 0 42 42" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="logoBg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#5B4FC4"/>
            <stop offset="50%" style="stop-color:#8B5FA8"/>
            <stop offset="100%" style="stop-color:#D4A843"/>
        </linearGradient>
    </defs>
    <rect width="42" height="42" rx="12" fill="url(#logoBg)"/>
    <circle cx="21" cy="21" r="10" fill="none" stroke="white" stroke-width="2" opacity="0.9"/>
    <line x1="21" y1="13" x2="21" y2="29" stroke="white" stroke-width="2" opacity="0.9"/>
    <line x1="13" y1="21" x2="29" y2="21" stroke="white" stroke-width="2" opacity="0.9"/>
</svg>
```

---

## 2. Color System Upgrade

### What's wrong now
The current palette is decent but flat. The primary purple (`#5B4FC4`) lacks depth -- there is no dark/rich anchor. Gold accent exists but is underused. No dark mode tokens. The gradient palette is one-note (purple to purple-pink).

### What to change
Introduce a richer, layered palette with deep indigo anchors, warm gold as a true secondary, and cream/parchment tones. Add dark mode tokens. Create named gradient presets.

### Priority: HIGH

### Implementation

Replace the `COLORS` dict in `modules/styles.py`:

```python
COLORS = {
    # -- Primary Purple (deeper, more indigo) --
    "primary": "#4A3FB0",
    "primary_light": "#6B5FD4",
    "primary_lighter": "#8B7FE8",
    "primary_dark": "#2D2470",
    "primary_darkest": "#1A1545",

    # -- Sacred Gold (true warm secondary) --
    "gold": "#C9982A",
    "gold_light": "#E8C55A",
    "gold_lighter": "#FFF0C4",
    "gold_dark": "#8B6914",

    # -- Warm Neutrals (parchment system) --
    "surface": "#FAF8F5",
    "surface_warm": "#FFF8EE",
    "surface_parchment": "#FDF6E9",
    "card_bg": "#FFFFFF",
    "card_border": "#E8E0D4",

    # -- Text --
    "text_primary": "#1E1833",
    "text_secondary": "#5A5470",
    "text_muted": "#908AA0",
    "text_on_dark": "#F0ECF8",

    # -- Semantic --
    "success": "#2E7D4F",
    "success_bg": "#E4F5E8",
    "warning": "#C47A2A",
    "warning_bg": "#FFF3E0",
    "danger": "#B43D4D",
    "danger_bg": "#FDEDEF",

    # -- Accent / Decorative --
    "streak_fire": "#D4532A",
    "streak_gold": "#C9982A",
    "rose": "#B05A7A",
    "rose_light": "#F5E0EA",
    "teal": "#2A8B7A",
    "teal_light": "#E0F5F0",
}

# -- Dark Mode Tokens --
COLORS_DARK = {
    "primary": "#7B6FE8",
    "primary_light": "#9B8FF8",
    "primary_dark": "#3A2F90",
    "gold": "#E8C55A",
    "surface": "#141218",
    "surface_warm": "#1C1A22",
    "card_bg": "#1E1C26",
    "card_border": "#2E2A3A",
    "text_primary": "#EEEAF5",
    "text_secondary": "#A8A0B8",
    "text_muted": "#6B6580",
}

# -- Named Gradients --
GRADIENTS = {
    "hero": "linear-gradient(135deg, #1A1545 0%, #4A3FB0 40%, #6B5FD4 70%, #8B5FA8 100%)",
    "hero_warm": "linear-gradient(135deg, #2D2470 0%, #5B4FC4 30%, #8B5FA8 60%, #C9982A 100%)",
    "gold_shimmer": "linear-gradient(135deg, #C9982A 0%, #E8C55A 50%, #C9982A 100%)",
    "card_accent": "linear-gradient(135deg, #4A3FB0, #8B5FA8)",
    "stained_glass": "linear-gradient(135deg, #4A3FB0 0%, #6B5FD4 25%, #B05A7A 50%, #C9982A 75%, #E8C55A 100%)",
    "progress": "linear-gradient(90deg, #4A3FB0, #6B5FD4, #B05A7A)",
    "streak_fire": "linear-gradient(135deg, #D4532A, #C9982A)",
    "streak_ice": "linear-gradient(135deg, #4A3FB0, #2A8B7A)",
    "parchment": "linear-gradient(135deg, #FFF8EE, #FDF6E9, #FFF0C4)",
}
```

**CSS custom properties** -- add to `SHARED_CSS` at the top of the `<style>` block:
```css
:root {
    --lp-primary: #4A3FB0;
    --lp-primary-light: #6B5FD4;
    --lp-primary-dark: #2D2470;
    --lp-primary-darkest: #1A1545;
    --lp-gold: #C9982A;
    --lp-gold-light: #E8C55A;
    --lp-gold-lighter: #FFF0C4;
    --lp-surface: #FAF8F5;
    --lp-surface-warm: #FFF8EE;
    --lp-card-bg: #FFFFFF;
    --lp-card-border: #E8E0D4;
    --lp-text: #1E1833;
    --lp-text-secondary: #5A5470;
    --lp-text-muted: #908AA0;
    --lp-radius-sm: 8px;
    --lp-radius-md: 14px;
    --lp-radius-lg: 20px;
    --lp-radius-xl: 28px;
    --lp-shadow-sm: 0 1px 4px rgba(26, 21, 69, 0.06);
    --lp-shadow-md: 0 4px 16px rgba(26, 21, 69, 0.08);
    --lp-shadow-lg: 0 8px 32px rgba(26, 21, 69, 0.12);
    --lp-shadow-glow: 0 4px 20px rgba(74, 63, 176, 0.2);
}
```

**Update `.streamlit/config.toml`:**
```toml
[theme]
primaryColor = "#4A3FB0"
backgroundColor = "#FAF8F5"
secondaryBackgroundColor = "#F0ECF5"
textColor = "#1E1833"
font = "sans serif"
```

---

## 3. Typography Enhancement

### What's wrong now
DM Serif Display + DM Sans is a solid combo but the scale is arbitrary. Heading sizes are hardcoded without rhythm. Line heights vary. The Bible reader (scripture blocks) lacks the generous spacing that aids devotional reading.

### What to change
Establish a modular type scale (1.25 ratio). Add a third font for scripture passages (Cormorant Garamond -- it has a beautiful spiritual quality). Improve line heights and letter spacing across the board.

### Priority: HIGH

### Implementation

**Updated font import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
```

**Type scale CSS:**
```css
/* -- Type Scale (1.25 ratio, base 16px) -- */
:root {
    --lp-text-xs: 0.64rem;    /* 10.24px */
    --lp-text-sm: 0.8rem;     /* 12.8px */
    --lp-text-base: 1rem;     /* 16px */
    --lp-text-md: 1.125rem;   /* 18px */
    --lp-text-lg: 1.25rem;    /* 20px */
    --lp-text-xl: 1.563rem;   /* 25px */
    --lp-text-2xl: 1.953rem;  /* 31.25px */
    --lp-text-3xl: 2.441rem;  /* 39px */
    --lp-text-4xl: 3.052rem;  /* 48.8px */
}

/* -- Font families -- */
.stApp {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: var(--lp-text);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', Georgia, serif !important;
    color: var(--lp-text) !important;
    line-height: 1.2 !important;
}

h1 { font-size: var(--lp-text-3xl) !important; }
h2 { font-size: var(--lp-text-2xl) !important; }
h3 { font-size: var(--lp-text-xl) !important; }

/* Scripture / devotional text */
.scripture-text,
.scripture-block,
.report-card,
.hero-verse {
    font-family: 'Cormorant Garamond', 'DM Serif Display', Georgia, serif;
}

/* Optimized scripture reading */
.scripture-block {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.125rem;
    line-height: 2;
    letter-spacing: 0.01em;
    color: #2C1E0E;
    background: linear-gradient(135deg, #FFF8EE, #FDF6E9);
    border-left: 3px solid var(--lp-gold);
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
}

/* Labels and captions */
.metric-label, .stat-label, .section-label, .lp-logo-tagline {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}
```

---

## 4. Header/Hero Redesign

### What's wrong now
The hero gradient is a simple three-stop purple fade. The `::before` and `::after` decorative circles are barely visible. The verse card floats without visual anchor. Overall it reads as "colored box" rather than an immersive experience.

### What to change
Create a layered, deep hero with a stained-glass-inspired background effect using multiple CSS layers. Add a subtle animated shimmer. Elevate the verse card with gold accents.

### Priority: HIGH

### Implementation

```css
/* ---- Hero v2 ---- */
.hero-section {
    background:
        radial-gradient(ellipse at 20% 50%, rgba(176, 90, 122, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(201, 152, 42, 0.12) 0%, transparent 40%),
        radial-gradient(ellipse at 60% 80%, rgba(107, 95, 212, 0.2) 0%, transparent 50%),
        linear-gradient(135deg, #1A1545 0%, #2D2470 25%, #4A3FB0 50%, #6B5FD4 75%, #8B5FA8 100%);
    border-radius: 24px;
    padding: 48px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

/* Stained glass light beam effect */
.hero-section::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -20%;
    width: 500px;
    height: 500px;
    background:
        conic-gradient(
            from 180deg,
            transparent 0deg,
            rgba(201, 152, 42, 0.08) 60deg,
            transparent 120deg,
            rgba(255, 255, 255, 0.05) 180deg,
            transparent 240deg,
            rgba(176, 90, 122, 0.06) 300deg,
            transparent 360deg
        );
    border-radius: 50%;
    animation: hero-rotate 30s linear infinite;
}

/* Soft bottom vignette */
.hero-section::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40%;
    background: linear-gradient(to top, rgba(26, 21, 69, 0.3), transparent);
    pointer-events: none;
}

@keyframes hero-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Greeting text */
.hero-greeting {
    font-size: 11px;
    color: rgba(232, 197, 90, 0.7);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
    font-weight: 600;
    position: relative;
    z-index: 1;
}

.hero-name {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 40px;
    font-weight: 400;
    color: white;
    margin-bottom: 4px;
    line-height: 1.15;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 20px rgba(0, 0, 0, 0.15);
}

.hero-date {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.5);
    position: relative;
    z-index: 1;
}

/* Verse card v2 -- gold accent, glass effect */
.hero-verse {
    margin-top: 24px;
    padding: 20px 24px;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    border: 1px solid rgba(201, 152, 42, 0.2);
    border-left: 3px solid rgba(201, 152, 42, 0.5);
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-size: 17px;
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.8;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    position: relative;
    z-index: 1;
}

.hero-verse::before {
    content: '\201C';
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 48px;
    color: rgba(201, 152, 42, 0.3);
    position: absolute;
    top: -4px;
    left: 12px;
    line-height: 1;
}
```

**Verse reference styling** -- add a Python helper:
```python
def hero_verse_card(text: str, reference: str):
    st.markdown(f"""
    <div class="hero-verse">
        <div style="padding-left: 20px;">
            {text}
            <div style="margin-top: 10px; font-style: normal; font-size: 12px;
                        color: rgba(201, 152, 42, 0.7); letter-spacing: 1px;
                        text-transform: uppercase; font-family: 'DM Sans', sans-serif;
                        font-weight: 600;">
                {reference}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## 5. Card System

### What's wrong now
Cards are functional but samey -- white background, light purple border, minimal shadow. Every card type (metric, section, entry, prayer, sermon) looks nearly identical. No visual hierarchy. Hover effects are minimal and identical.

### What to change
Create a layered card system with distinct tiers. Introduce glassmorphism for overlay cards, warm-parchment for scripture content, and accent-bordered cards for action items. Add meaningful hover states.

### Priority: HIGH

### Implementation

```css
/* ======== CARD TIER SYSTEM ======== */

/* -- Tier 1: Elevated Card (primary actions, metrics) -- */
.card-elevated {
    background: white;
    border: 1px solid var(--lp-card-border);
    border-radius: var(--lp-radius-md);
    padding: 24px;
    box-shadow:
        0 1px 2px rgba(26, 21, 69, 0.04),
        0 4px 12px rgba(26, 21, 69, 0.06);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-elevated:hover {
    transform: translateY(-3px);
    box-shadow:
        0 4px 8px rgba(26, 21, 69, 0.06),
        0 12px 32px rgba(26, 21, 69, 0.1);
    border-color: rgba(107, 95, 212, 0.2);
}

/* -- Tier 2: Glass Card (overlays, stats on gradients) -- */
.card-glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: var(--lp-radius-md);
    padding: 24px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-glass:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(255, 255, 255, 0.2);
}

/* -- Tier 3: Parchment Card (scripture, devotional content) -- */
.card-parchment {
    background: linear-gradient(135deg, #FFF8EE 0%, #FDF6E9 50%, #FFF0C4 100%);
    border: 1px solid #E8D8B8;
    border-radius: var(--lp-radius-md);
    padding: 24px;
    box-shadow: 0 2px 8px rgba(139, 105, 20, 0.06);
    position: relative;
    overflow: hidden;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-parchment::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--lp-gold), var(--lp-gold-light), var(--lp-gold));
}
.card-parchment:hover {
    box-shadow: 0 6px 20px rgba(139, 105, 20, 0.1);
    transform: translateY(-2px);
}

/* -- Tier 4: Accent Card (with left border color indicator) -- */
.card-accent {
    background: white;
    border: 1px solid var(--lp-card-border);
    border-left: 4px solid var(--lp-primary);
    border-radius: 4px var(--lp-radius-md) var(--lp-radius-md) 4px;
    padding: 20px 24px;
    box-shadow: var(--lp-shadow-sm);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.card-accent:hover {
    border-left-color: var(--lp-gold);
    box-shadow: var(--lp-shadow-md);
}
.card-accent-gold { border-left-color: var(--lp-gold); }
.card-accent-success { border-left-color: #2E7D4F; }
.card-accent-rose { border-left-color: #B05A7A; }

/* -- Tier 5: Flat Card (minimal, for dense lists) -- */
.card-flat {
    background: var(--lp-surface);
    border: 1px solid transparent;
    border-radius: var(--lp-radius-sm);
    padding: 16px 20px;
    transition: all 0.2s ease;
}
.card-flat:hover {
    background: white;
    border-color: var(--lp-card-border);
    box-shadow: var(--lp-shadow-sm);
}

/* ======== UPGRADED METRIC CARDS ======== */
.metric-card {
    background: white;
    border: 1px solid var(--lp-card-border);
    border-radius: var(--lp-radius-md);
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: var(--lp-shadow-sm);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-primary-light));
    opacity: 0;
    transition: opacity 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--lp-shadow-lg);
}
.metric-card:hover::before {
    opacity: 1;
}
.metric-value {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 36px;
    font-weight: 400;
    line-height: 1;
    margin-bottom: 6px;
    background: linear-gradient(135deg, var(--lp-primary), var(--lp-primary-light));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: var(--lp-text-xs);
    color: var(--lp-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 600;
}

/* Metric card color variants */
.metric-card-gold .metric-value {
    background: linear-gradient(135deg, #C9982A, #E8C55A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card-gold::before {
    background: linear-gradient(90deg, #C9982A, #E8C55A);
}
.metric-card-rose .metric-value {
    background: linear-gradient(135deg, #B05A7A, #D48A9A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.metric-card-success .metric-value {
    background: linear-gradient(135deg, #2E7D4F, #4AAF6F);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

**Python helpers for the card system:**
```python
def card(content: str, tier: str = "elevated", extra_class: str = ""):
    """Render content inside a card. tier: elevated|glass|parchment|accent|flat"""
    st.markdown(f"""
    <div class="card-{tier} {extra_class}">
        {content}
    </div>
    """, unsafe_allow_html=True)
```

---

## 6. Navigation Improvements

### What's wrong now
Default Streamlit sidebar with no branding. Active page indicator is Streamlit's default blue line. No visual grouping of pages. The role badge (if present) has no custom styling.

### What to change
Style the sidebar with custom CSS. Group navigation items under labels. Add a custom active indicator. Style any role badges.

### Priority: MEDIUM

### Implementation

```css
/* ======== SIDEBAR OVERHAUL ======== */

/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FAF8F5 0%, #F0ECF5 100%) !important;
    border-right: 1px solid #E8E0D4 !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem !important;
}

/* Navigation links */
[data-testid="stSidebar"] .stPageLink a {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--lp-text-secondary) !important;
    padding: 10px 16px !important;
    border-radius: 10px !important;
    margin: 2px 8px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] .stPageLink a:hover {
    background: rgba(74, 63, 176, 0.06) !important;
    color: var(--lp-primary) !important;
}

/* Active page -- override Streamlit default */
[data-testid="stSidebar"] .stPageLink[aria-current="page"] a,
[data-testid="stSidebar"] .stPageLink a[aria-selected="true"] {
    background: rgba(74, 63, 176, 0.1) !important;
    color: var(--lp-primary) !important;
    font-weight: 600 !important;
    border-left: 3px solid var(--lp-primary) !important;
    padding-left: 13px !important;
}

/* Section dividers in sidebar */
.sidebar-section-label {
    font-size: 10px;
    color: var(--lp-text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 700;
    padding: 16px 16px 6px 16px;
    font-family: 'DM Sans', sans-serif;
}

/* Role badge */
.role-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    font-family: 'DM Sans', sans-serif;
}
.role-badge-admin {
    background: linear-gradient(135deg, rgba(74, 63, 176, 0.12), rgba(139, 95, 168, 0.12));
    color: var(--lp-primary);
    border: 1px solid rgba(74, 63, 176, 0.2);
}
.role-badge-member {
    background: linear-gradient(135deg, rgba(201, 152, 42, 0.12), rgba(232, 197, 90, 0.12));
    color: #8B6914;
    border: 1px solid rgba(201, 152, 42, 0.2);
}

/* Sidebar user info section */
.sidebar-user-info {
    padding: 12px 16px;
    margin: 8px;
    border-radius: 12px;
    background: rgba(74, 63, 176, 0.04);
    border: 1px solid rgba(74, 63, 176, 0.08);
}
.sidebar-user-name {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 15px;
    color: var(--lp-text);
}
.sidebar-user-role {
    font-size: 11px;
    color: var(--lp-text-muted);
    margin-top: 2px;
}
```

**Python helper:**
```python
def sidebar_nav_section(label: str):
    """Add a section label in the sidebar nav."""
    with st.sidebar:
        st.markdown(f'<div class="sidebar-section-label">{label}</div>',
                     unsafe_allow_html=True)

def sidebar_user_card(name: str, role: str):
    """Render user info in sidebar."""
    badge_class = "role-badge-admin" if role.lower() == "admin" else "role-badge-member"
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-user-info">
            <div class="sidebar-user-name">{name}</div>
            <span class="role-badge {badge_class}">{role}</span>
        </div>
        """, unsafe_allow_html=True)
```

---

## 7. Button & Form Styling

### What's wrong now
Buttons use Streamlit's default styling which fights with the spiritual aesthetic. No visual hierarchy between primary actions and secondary actions. Form inputs (text, select, multiselect) are default grey. No visual coherence with the rest of the design system.

### What to change
Override Streamlit button and form element styles. Create a three-tier button hierarchy. Style form inputs to match the warm surface palette.

### Priority: MEDIUM

### Implementation

```css
/* ======== BUTTON SYSTEM ======== */

/* Primary button */
[data-testid="stButton"] > button[kind="primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--lp-primary), var(--lp-primary-light)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 2px 8px rgba(74, 63, 176, 0.25) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 4px 16px rgba(74, 63, 176, 0.35) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button[kind="primary"]:active {
    transform: translateY(0) !important;
    box-shadow: 0 1px 4px rgba(74, 63, 176, 0.2) !important;
}

/* Secondary / default button */
[data-testid="stButton"] > button[kind="secondary"],
.stButton > button {
    background: white !important;
    color: var(--lp-primary) !important;
    border: 1.5px solid rgba(74, 63, 176, 0.25) !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover,
.stButton > button:hover {
    background: rgba(74, 63, 176, 0.05) !important;
    border-color: var(--lp-primary) !important;
}

/* Ghost button (using custom HTML) */
.btn-ghost {
    display: inline-block;
    padding: 8px 20px;
    color: var(--lp-text-secondary);
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 600;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.2s ease;
    text-decoration: none;
}
.btn-ghost:hover {
    background: rgba(74, 63, 176, 0.06);
    color: var(--lp-primary);
}

/* Gold CTA button (for special actions) */
.btn-gold {
    display: inline-block;
    padding: 12px 28px;
    background: linear-gradient(135deg, #C9982A, #E8C55A);
    color: #1A1545;
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(201, 152, 42, 0.3);
    transition: all 0.25s ease;
    text-decoration: none;
    letter-spacing: 0.3px;
}
.btn-gold:hover {
    box-shadow: 0 4px 16px rgba(201, 152, 42, 0.4);
    transform: translateY(-1px);
}

/* ======== FORM INPUTS ======== */

/* Text inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid var(--lp-card-border) !important;
    border-radius: 10px !important;
    background: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--lp-primary-light) !important;
    box-shadow: 0 0 0 3px rgba(74, 63, 176, 0.1) !important;
}

/* Select boxes */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-radius: 10px !important;
    border-color: var(--lp-card-border) !important;
}

/* Labels */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stMultiSelect label,
.stDateInput label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--lp-text-secondary) !important;
    letter-spacing: 0.3px !important;
}

/* Checkboxes */
.stCheckbox label span {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background-color: var(--lp-primary) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: var(--lp-surface);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
    color: var(--lp-text-secondary) !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: white !important;
    color: var(--lp-primary) !important;
    font-weight: 600 !important;
    box-shadow: var(--lp-shadow-sm) !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}
```

---

## 8. Data Visualization Style

### What's wrong now
Charts likely use Plotly's default blue color scheme or random colors. No consistent chart theme. Stat cards look the same as regular cards. No visual distinction for data-heavy sections.

### What to change
Create a Plotly theme that matches the spiritual warmth palette. Define a chart color sequence. Upgrade stat cards with icon badges.

### Priority: MEDIUM

### Implementation

**Plotly Theme** -- add to `modules/styles.py`:
```python
import plotly.graph_objects as go
import plotly.io as pio

# Define Logos Pulse Plotly template
lp_template = go.layout.Template(
    layout=go.Layout(
        font=dict(
            family="DM Sans, -apple-system, sans-serif",
            color="#1E1833",
            size=13,
        ),
        title=dict(
            font=dict(
                family="DM Serif Display, Georgia, serif",
                size=20,
                color="#1E1833",
            ),
            x=0,
            xanchor="left",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=[
            "#4A3FB0",  # primary
            "#C9982A",  # gold
            "#B05A7A",  # rose
            "#2A8B7A",  # teal
            "#6B5FD4",  # primary light
            "#E8C55A",  # gold light
            "#D48A9A",  # rose light
            "#4AAF8F",  # teal light
        ],
        xaxis=dict(
            gridcolor="rgba(144, 138, 160, 0.1)",
            linecolor="rgba(144, 138, 160, 0.2)",
            tickfont=dict(size=11, color="#908AA0"),
            title_font=dict(size=12, color="#5A5470"),
        ),
        yaxis=dict(
            gridcolor="rgba(144, 138, 160, 0.1)",
            linecolor="rgba(144, 138, 160, 0.2)",
            tickfont=dict(size=11, color="#908AA0"),
            title_font=dict(size=12, color="#5A5470"),
        ),
        margin=dict(l=40, r=20, t=40, b=40),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E8E0D4",
            font=dict(family="DM Sans", size=13, color="#1E1833"),
        ),
    )
)

pio.templates["logos_pulse"] = lp_template
pio.templates.default = "logos_pulse"


def apply_chart_style(fig):
    """Apply Logos Pulse styling to any Plotly figure."""
    fig.update_layout(template="logos_pulse")
    return fig
```

**Stat Card v2 with icon badge:**
```css
.stat-card-v2 {
    background: white;
    border: 1px solid var(--lp-card-border);
    border-radius: var(--lp-radius-md);
    padding: 20px;
    text-align: center;
    position: relative;
    box-shadow: var(--lp-shadow-sm);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.stat-card-v2:hover {
    transform: translateY(-2px);
    box-shadow: var(--lp-shadow-md);
}
.stat-card-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin: 0 auto 12px auto;
}
.stat-card-icon-purple {
    background: rgba(74, 63, 176, 0.1);
}
.stat-card-icon-gold {
    background: rgba(201, 152, 42, 0.1);
}
.stat-card-icon-rose {
    background: rgba(176, 90, 122, 0.1);
}
.stat-card-icon-teal {
    background: rgba(42, 139, 122, 0.1);
}

.stat-card-v2 .stat-value {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 32px;
    line-height: 1;
    margin-bottom: 4px;
}
.stat-card-v2 .stat-change {
    font-size: 11px;
    font-weight: 600;
    margin-top: 8px;
}
.stat-change-up { color: #2E7D4F; }
.stat-change-down { color: #B43D4D; }
```

**Python helper:**
```python
def stat_card(icon: str, value: str, label: str, color: str = "purple",
              change: str = None, change_dir: str = "up"):
    change_html = ""
    if change:
        arrow = "^" if change_dir == "up" else "v"
        cls = f"stat-change-{change_dir}"
        change_html = f'<div class="stat-change {cls}">{arrow} {change}</div>'
    st.markdown(f"""
    <div class="stat-card-v2">
        <div class="stat-card-icon stat-card-icon-{color}">{icon}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-label">{label}</div>
        {change_html}
    </div>
    """, unsafe_allow_html=True)
```

---

## 9. Micro-interactions & Animations

### What's wrong now
Only basic hover transitions exist (translateY + box-shadow). No page load animations. No staggered reveals. Cards appear instantly with no visual flow. The app feels static.

### What to change
Add CSS-only animations: fade-in-up on page load (staggered), smooth transitions on all interactive elements, a shimmer effect for loading states, and a subtle pulse for active streaks.

### Priority: MEDIUM

### Implementation

```css
/* ======== KEYFRAME LIBRARY ======== */

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(16px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(212, 83, 42, 0.2); }
    50% { box-shadow: 0 0 0 8px rgba(212, 83, 42, 0); }
}

@keyframes gold-shimmer {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ======== STAGGERED PAGE LOAD ======== */

.animate-in {
    animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    opacity: 0;
}
.delay-1 { animation-delay: 0.05s; }
.delay-2 { animation-delay: 0.1s; }
.delay-3 { animation-delay: 0.15s; }
.delay-4 { animation-delay: 0.2s; }
.delay-5 { animation-delay: 0.25s; }
.delay-6 { animation-delay: 0.3s; }
.delay-7 { animation-delay: 0.35s; }
.delay-8 { animation-delay: 0.4s; }

/* Apply to hero */
.hero-section {
    animation: scaleIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

/* Apply to metric cards (each column) */
.metric-card {
    animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    opacity: 0;
}

/* Page header */
.page-header {
    animation: fadeInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

/* Section cards stagger */
.section-card {
    animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    opacity: 0;
}

/* ======== INTERACTIVE STATES ======== */

/* Streak fire pulse */
.streak-active {
    animation: pulse-glow 2s ease-in-out infinite;
}

/* Gold shimmer on special elements */
.gold-shimmer {
    background: linear-gradient(
        90deg,
        #C9982A 0%,
        #E8C55A 25%,
        #FFF0C4 50%,
        #E8C55A 75%,
        #C9982A 100%
    );
    background-size: 200% auto;
    animation: gold-shimmer 3s ease-in-out infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Progress bar fill animation */
.progress-bar-fill {
    animation: progressFill 1s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    width: 0;
}
@keyframes progressFill {
    to { width: var(--fill-width); }
}

/* Smooth hover transitions on all cards */
.metric-card, .section-card, .entry-card, .prayer-card,
.stat-card, .sermon-card, .cat-card,
.card-elevated, .card-parchment, .card-accent {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Python helper for staggered animation:**
```python
def animated_cards(cards_html: list[str], base_class: str = "animate-in"):
    """Wrap a list of HTML card strings with stagger animation."""
    html = ""
    for i, card_html in enumerate(cards_html):
        delay_class = f"delay-{min(i + 1, 8)}"
        html += f'<div class="{base_class} {delay_class}">{card_html}</div>'
    st.markdown(html, unsafe_allow_html=True)
```

**Progress bar with animation** (replaces current progress bar):
```python
def animated_progress(value: int, label: str = "", color: str = "primary"):
    gradient_map = {
        "primary": "linear-gradient(90deg, #4A3FB0, #6B5FD4, #8B5FA8)",
        "gold": "linear-gradient(90deg, #C9982A, #E8C55A)",
        "success": "linear-gradient(90deg, #2E7D4F, #4AAF6F)",
        "rose": "linear-gradient(90deg, #B05A7A, #D48A9A)",
    }
    st.markdown(f"""
    <div class="progress-section">
        <div class="progress-title">{label}</div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill"
                 style="--fill-width: {value}%;
                        width: {value}%;
                        background: {gradient_map.get(color, gradient_map['primary'])};">
            </div>
        </div>
        <div class="progress-label">{value}% complete</div>
    </div>
    """, unsafe_allow_html=True)
```

---

## 10. Footer

### What's wrong now
No footer at all. The page just ends. No branding, no version info, no visual closure.

### What to change
Add a subtle, elegant footer with branding, version, and a spiritual touch. Two options: inline (end of page) and fixed (always visible).

### Priority: LOW

### Implementation

**Option A: Inline footer (recommended)** -- placed at end of each page:
```css
.lp-footer {
    margin-top: 60px;
    padding: 24px 0;
    border-top: 1px solid var(--lp-card-border);
    text-align: center;
}
.lp-footer-brand {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 14px;
    color: var(--lp-text-muted);
    letter-spacing: 0.5px;
}
.lp-footer-brand span {
    background: linear-gradient(135deg, var(--lp-primary), var(--lp-gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 400;
}
.lp-footer-sub {
    font-size: 11px;
    color: #C0B8CC;
    margin-top: 4px;
    letter-spacing: 0.5px;
}
.lp-footer-verse {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-style: italic;
    font-size: 13px;
    color: var(--lp-text-muted);
    margin-top: 12px;
    opacity: 0.7;
}
```

**Option B: Fixed footer** (subtle, stays at bottom):
```css
.lp-footer-fixed {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(250, 248, 245, 0.95);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-top: 1px solid var(--lp-card-border);
    padding: 8px 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    z-index: 999;
    font-size: 11px;
    color: var(--lp-text-muted);
}
/* Add bottom padding to main content so footer doesn't overlap */
.main .block-container {
    padding-bottom: 60px !important;
}
```

**Python helper:**
```python
APP_VERSION = "1.0.0"

def render_footer():
    """Render app footer at the bottom of the page."""
    st.markdown(f"""
    <div class="lp-footer">
        <div class="lp-footer-brand">
            <span>Logos Pulse</span> &middot; Spiritual Growth Tracker
        </div>
        <div class="lp-footer-sub">v{APP_VERSION}</div>
        <div class="lp-footer-verse">
            "Thy word is a lamp unto my feet, and a light unto my path." &mdash; Psalm 119:105
        </div>
    </div>
    """, unsafe_allow_html=True)
```

---

## 11. Empty States & Loading

### What's wrong now
Empty states are minimal -- just an emoji and grey text. No visual warmth. No skeleton loaders. The default Streamlit spinner is a generic rotating circle.

### What to change
Create illustrative empty states using CSS art + emoji compositions. Add skeleton loaders for data-heavy sections. Replace spinner with a branded loading state.

### Priority: LOW

### Implementation

**Enhanced empty state:**
```css
.empty-state-v2 {
    text-align: center;
    padding: 56px 24px;
    animation: fadeIn 0.5s ease forwards;
}
.empty-state-v2-icon {
    font-size: 56px;
    margin-bottom: 16px;
    filter: grayscale(30%);
    animation: scaleIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
.empty-state-v2-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 18px;
    color: var(--lp-text-secondary);
    margin-bottom: 6px;
}
.empty-state-v2-sub {
    font-size: 14px;
    color: var(--lp-text-muted);
    line-height: 1.6;
    max-width: 320px;
    margin: 0 auto;
}
.empty-state-v2-divider {
    width: 40px;
    height: 2px;
    background: linear-gradient(90deg, var(--lp-primary), var(--lp-gold));
    margin: 16px auto;
    border-radius: 2px;
}
```

**Skeleton loader:**
```css
.skeleton {
    background: linear-gradient(
        90deg,
        #F0ECF5 25%,
        #FAF8F5 50%,
        #F0ECF5 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
    border-radius: 8px;
}
.skeleton-card {
    height: 120px;
    border-radius: var(--lp-radius-md);
    margin-bottom: 12px;
}
.skeleton-line {
    height: 14px;
    margin-bottom: 8px;
    border-radius: 6px;
}
.skeleton-line-short { width: 60%; }
.skeleton-line-medium { width: 80%; }
.skeleton-circle {
    width: 44px;
    height: 44px;
    border-radius: 50%;
}
```

**Branded spinner:**
```css
.lp-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
}
.lp-spinner-ring {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 3px solid rgba(74, 63, 176, 0.15);
    border-top-color: var(--lp-primary);
    animation: spin 0.8s linear infinite;
}
.lp-spinner-text {
    margin-top: 12px;
    font-size: 13px;
    color: var(--lp-text-muted);
    font-weight: 500;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
```

**Python helpers:**
```python
def empty_state_v2(icon: str, title: str, subtitle: str = "",
                   emoji_stack: str = None):
    """Render an enhanced empty state with optional emoji composition."""
    icon_html = emoji_stack if emoji_stack else f'<div class="empty-state-v2-icon">{icon}</div>'
    sub_html = f'<div class="empty-state-v2-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="empty-state-v2">
        {icon_html}
        <div class="empty-state-v2-title">{title}</div>
        <div class="empty-state-v2-divider"></div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def skeleton_loader(lines: int = 3, card: bool = False):
    """Show a skeleton loading placeholder."""
    if card:
        st.markdown('<div class="skeleton skeleton-card"></div>',
                    unsafe_allow_html=True)
    else:
        html = ""
        for i in range(lines):
            width_class = "skeleton-line-short" if i == lines - 1 else (
                "skeleton-line-medium" if i % 2 else "")
            html += f'<div class="skeleton skeleton-line {width_class}"></div>'
        st.markdown(html, unsafe_allow_html=True)
```

---

## 12. Mobile-specific Enhancements

### What's wrong now
Mobile CSS exists but is purely responsive sizing. No mobile-specific UX patterns. Touch targets could be larger. No bottom action bar for key actions. The sidebar hamburger is the only navigation pattern.

### What to change
Add touch-friendly sizing, a floating action button for the most common action, and optimize card layouts for single-column mobile. Add swipe-hint styling where relevant.

### Priority: LOW

### Implementation

```css
/* ======== MOBILE ENHANCEMENTS ======== */

@media (max-width: 768px) {
    /* Minimum touch target size (48px per WCAG) */
    .stButton > button,
    [data-testid="stButton"] > button {
        min-height: 48px !important;
        min-width: 48px !important;
        font-size: 15px !important;
    }

    /* Full-width buttons on mobile */
    .stButton > button {
        width: 100% !important;
    }

    /* Larger tap areas for checkboxes */
    .stCheckbox {
        padding: 4px 0 !important;
    }
    .stCheckbox label {
        padding: 8px 0 !important;
    }

    /* Stack columns vertically with spacing */
    [data-testid="column"] {
        margin-bottom: 8px !important;
    }

    /* Tabs scroll horizontally */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none;
    }

    /* Card touch feedback */
    .metric-card:active,
    .section-card:active,
    .prayer-card:active,
    .entry-card:active {
        transform: scale(0.98) !important;
        transition: transform 0.1s ease !important;
    }

    /* Inline footer adjustments */
    .lp-footer {
        margin-top: 40px;
        padding: 20px 16px;
    }
    .lp-footer-verse {
        font-size: 12px;
    }
}

/* ======== FLOATING ACTION BUTTON ======== */
.fab {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 56px;
    height: 56px;
    border-radius: 16px;
    background: linear-gradient(135deg, var(--lp-primary), var(--lp-primary-light));
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow:
        0 4px 12px rgba(74, 63, 176, 0.3),
        0 8px 24px rgba(74, 63, 176, 0.15);
    z-index: 1000;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.fab:hover {
    transform: scale(1.08);
    box-shadow:
        0 6px 16px rgba(74, 63, 176, 0.35),
        0 12px 32px rgba(74, 63, 176, 0.2);
}
.fab:active {
    transform: scale(0.95);
}

/* Only show FAB on mobile */
@media (min-width: 769px) {
    .fab { display: none; }
}

/* ======== BOTTOM ACTION BAR (alternative to FAB) ======== */
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid var(--lp-card-border);
    padding: 8px 16px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    z-index: 1000;
}
.bottom-bar-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    padding: 6px 12px;
    border-radius: 10px;
    font-size: 10px;
    color: var(--lp-text-muted);
    font-weight: 500;
    transition: all 0.2s ease;
    text-decoration: none;
}
.bottom-bar-item-icon { font-size: 22px; }
.bottom-bar-item-active {
    color: var(--lp-primary);
    background: rgba(74, 63, 176, 0.06);
}

/* Only show bottom bar on mobile */
@media (min-width: 769px) {
    .bottom-bar { display: none; }
}

/* Add padding when bottom bar is present */
@media (max-width: 768px) {
    .has-bottom-bar .main .block-container {
        padding-bottom: 80px !important;
    }
}

/* ======== SWIPE HINT ======== */
.swipe-hint {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px;
    font-size: 11px;
    color: var(--lp-text-muted);
    opacity: 0.6;
}
.swipe-hint::before {
    content: '';
    width: 24px;
    height: 2px;
    background: var(--lp-text-muted);
    border-radius: 2px;
    opacity: 0.4;
}
.swipe-hint::after {
    content: '';
    width: 24px;
    height: 2px;
    background: var(--lp-text-muted);
    border-radius: 2px;
    opacity: 0.4;
}

@media (min-width: 769px) {
    .swipe-hint { display: none; }
}
```

---

## Implementation Roadmap

### Phase 1: Foundation (Days 1-2) -- HIGH PRIORITY
1. Update `COLORS` dict and CSS custom properties in `modules/styles.py`
2. Update `.streamlit/config.toml` theme
3. Add Cormorant Garamond font import
4. Add type scale variables
5. Replace hero section CSS
6. Add animation keyframes library

### Phase 2: Components (Days 3-4) -- HIGH PRIORITY
7. Implement card tier system (replace all card CSS)
8. Add metric card upgrades (gradient text, top accent bar)
9. Add sidebar branding + logo
10. Implement `sidebar_branding()` and `render_footer()` helpers

### Phase 3: Polish (Days 5-6) -- MEDIUM PRIORITY
11. Button and form input overrides
12. Plotly chart theme
13. Sidebar navigation CSS overrides
14. Tab restyling
15. Staggered animation classes

### Phase 4: Delight (Day 7) -- LOW PRIORITY
16. Empty state v2 + skeleton loaders
17. Mobile-specific enhancements (FAB, touch feedback)
18. Branded spinner
19. Footer with verse rotation
20. Gold shimmer effect on streak milestones

### Migration Strategy
- All changes go into `modules/styles.py` -- the existing `SHARED_CSS` string and `COLORS` dict
- Add new Python helpers alongside existing `page_header()`, `section_label()`, `empty_state()`, `spacer()`
- Existing class names are preserved (`.metric-card`, `.section-card`, etc.) so pages do not break
- New classes (`.card-elevated`, `.card-parchment`, etc.) are additive -- use them in new code or gradually migrate

### Files to modify
- `modules/styles.py` -- primary target, all CSS + design tokens + helpers
- `.streamlit/config.toml` -- theme colors
- Each page file -- gradually swap to new helpers (hero_verse_card, stat_card, render_footer, etc.)

---

## Quick Wins (implement right now for immediate impact)

1. **Deepen the hero gradient** -- swap the three-stop purple for the new dark-to-gold layered gradient
2. **Add CSS custom properties** -- enables future dark mode
3. **Gold accent on verse cards** -- change `border-left` from purple to gold
4. **Gradient text on metric values** -- makes numbers pop immediately
5. **Add the footer** -- 10 lines of Python, instant professional polish
6. **Import Cormorant Garamond** -- one line, scripture blocks look dramatically better

---

*Design system v2 for Logos Pulse -- modern spiritual warmth.*
*Stained glass meets minimal tech. Rich but not heavy.*
