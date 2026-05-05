---
name: Peaceful Sanctuary
colors:
  surface: '#fbfaf1'
  surface-dim: '#dbdad2'
  surface-bright: '#fbfaf1'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f4eb'
  surface-container: '#efeee6'
  surface-container-high: '#e9e8e0'
  surface-container-highest: '#e3e3da'
  on-surface: '#1b1c17'
  on-surface-variant: '#45483c'
  inverse-surface: '#30312b'
  inverse-on-surface: '#f2f1e8'
  outline: '#75796b'
  outline-variant: '#c5c8b8'
  surface-tint: '#50652a'
  primary: '#3e5219'
  on-primary: '#ffffff'
  primary-container: '#556b2f'
  on-primary-container: '#d0eba1'
  inverse-primary: '#b6d088'
  secondary: '#655e4b'
  on-secondary: '#ffffff'
  secondary-container: '#ece2c9'
  on-secondary-container: '#6b6450'
  tertiary: '#445030'
  on-tertiary: '#ffffff'
  tertiary-container: '#5b6846'
  on-tertiary-container: '#d8e6bc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d2eca2'
  primary-fixed-dim: '#b6d088'
  on-primary-fixed: '#131f00'
  on-primary-fixed-variant: '#394d14'
  secondary-fixed: '#ece2c9'
  secondary-fixed-dim: '#cfc6ae'
  on-secondary-fixed: '#201b0c'
  on-secondary-fixed-variant: '#4c4634'
  tertiary-fixed: '#dae8be'
  tertiary-fixed-dim: '#becca3'
  on-tertiary-fixed: '#141f05'
  on-tertiary-fixed-variant: '#3f4b2c'
  background: '#fbfaf1'
  on-background: '#1b1c17'
  surface-variant: '#e3e3da'
typography:
  h1:
    fontFamily: Noto Serif
    fontSize: 40px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  h2:
    fontFamily: Noto Serif
    fontSize: 32px
    fontWeight: '400'
    lineHeight: '1.3'
    letterSpacing: 0em
  h3:
    fontFamily: Noto Serif
    fontSize: 24px
    fontWeight: '400'
    lineHeight: '1.4'
    letterSpacing: 0em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1140px
  gutter: 24px
  margin-mobile: 20px
  section-gap: 80px
  stack-sm: 12px
  stack-md: 24px
---

## Brand & Style

This design system is anchored in the concept of a digital glade—a space for pause, reflection, and spiritual nourishment. The brand personality is quiet, humble, and intentional, aiming to lower the user's heart rate through visual harmony. It targets a mindful audience seeking a reprieve from the high-intensity, "loud" interfaces of traditional social media.

The visual direction follows a **Minimalist-Organic** movement. It prioritizes vast amounts of whitespace (negative space) to represent mental clarity. Rather than using rigid lines to define structure, the system uses soft light, subtle tonal shifts, and natural curves to guide the eye, creating a UI that feels grown rather than built.

## Colors

The palette is derived from a forest floor at dawn. The primary **Peaceful Sage Green** is used for moments of focus and key actions, while the **Soft Cream** background provides a warm, paper-like canvas that reduces eye strain compared to pure white.

**Muted Earthy Stone** and **Moss Green** serve as grounding accents for secondary information and decorative elements. Typography utilizes **Deep Charcoal Stone** for maximum legibility, while secondary labels use a desaturated, muted sage to maintain a soft visual hierarchy. Surfaces should transition from the warm background to pure white to signify elevation and importance.

## Typography

The typographic system relies on the interplay between the reverent, timeless **Noto Serif** and the functional, modern **Inter**. 

Headings should be treated with editorial care, allowing ample line height to let the "poetry" of the content breathe. The body text is set with a slightly increased letter spacing (tracking) to enhance clarity and provide a sense of lightness. Labels and small UI metadata should use a medium weight in Inter with generous tracking to ensure they remain legible despite their smaller scale.

## Layout & Spacing

This design system employs a **Fixed Grid** philosophy for desktop to maintain a centered, focused reading experience, while transitioning to a fluid model for mobile. 

The spacing rhythm is intentionally generous. Layouts should utilize "Macro-whitespace" (large gaps between sections) to prevent the user from feeling overwhelmed. Elements are organized in a 12-column grid, but content should frequently occupy the center 6 or 8 columns to create a sense of breathability and focus. Vertical stacking should favor larger gaps to distinguish between different thoughts or meditative exercises.

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and tonal layering rather than lines. 

- **Level 0 (Background):** The Soft Cream base layer.
- **Level 1 (Cards/Surfaces):** Pure white surfaces with "feathered" shadows. These shadows should have a large blur radius (24px-40px) and very low opacity (5-8%), using a slight tint of the Primary Sage color instead of pure black to maintain a natural feel.
- **Level 2 (Interactive/Floating):** Elements like menus or active buttons may use a slightly deeper shadow or a subtle 1px inner glow to suggest tangibility. 

No harsh borders or high-contrast dividers are permitted. Use 1px "Soft Earth" lines only when absolutely necessary for accessibility.

## Shapes

The shape language is rooted in organic geometry. Every container and interactive element must have **softly rounded corners** (12px to 16px). This avoids the "aggressiveness" of sharp corners and aligns with the meditative theme. 

Iconography must follow a **thin-stroke (1.5px) organic style**, featuring slightly rounded ends rather than square caps. Decorative elements—such as progress rings or separators—should favor hand-drawn, imperfect circles or soft waves over perfect geometric precision.

## Components

### Buttons
Primary buttons are solid Sage Green with white text and 12px rounded corners. Secondary buttons use a Moss Green ghost style (no fill, subtle border). There should be no "hover" state that uses harsh color flashes; instead, use a gentle deepening of the hue or a subtle scale-up (1.02x).

### Cards
Cards are the primary container. They should be pure white against the Soft Cream background, featuring 16px rounded corners and feathered ambient shadows. Padding inside cards should be generous (min 32px).

### Input Fields
Inputs should not have a full border. Use a Soft Cream fill with a subtle bottom-border in Stone. Focus states are indicated by a gentle Sage Green glow.

### Lists
Lists of spiritual exercises or readings should have no dividers. Use vertical spacing and subtle Noto Serif headers to distinguish items.

### Interactive Elements
- **Chips:** Used for "Moods" or "Topics." Low-contrast Moss Green background with Sage Green text.
- **Progress Indicators:** Use soft, circular "breath" animations rather than linear bars.
- **Modals:** Centered, taking up minimal screen real estate, with a blurred "backdrop-filter" to keep the user grounded in their current context.