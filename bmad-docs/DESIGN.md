# Logos Pulse — Design System (Google Stitch Guardrails)

## App Identity
- **App Name:** Logos Pulse
- **Purpose:** Spiritual disciplines tracker for a church community (prayer, Bible reading, sermon notes)
- **Personality:** Reverent, warm, intimate — like a digital devotional journal, not a corporate SaaS product
- **Platform:** Web app, wide-column layout, max-width 1200px, must be mobile-responsive at 768px

## Color Palette (NEVER deviate from these)
- Primary: deep indigo `#3B2F8E`
- Primary light: `#5B4FC4`
- Gold accent: `#C9982A`
- Success / Completed: `#2D6A4F` (forest green)
- Warning / Pending: `#C26B2C` (warm orange)
- Danger: `#B5383C` (muted red)
- Background: `#F8F7FF` (soft off-white with purple tint)
- Card surface: `#FFFFFF`
- Sidebar background: `#1E1733` (very dark indigo)
- Text primary: `#1A1A2E`
- Text muted: `#6B7280`

## Typography
- **Headings (H1–H3):** Playfair Display, serif — use for page titles, card titles, Bible verses, names
- **Body & UI text:** Nunito, rounded sans-serif — use for labels, paragraphs, form fields
- **Scripture / devotional quotes:** EB Garamond, italic — use inside scripture blocks only
- **Scale:** H1 32px / H2 24px / H3 20px / Body 15px / Small 13px / Scripture 18px

## Layout Rules
- Card border-radius: 12px
- Card shadow: `0 2px 12px rgba(59, 47, 142, 0.08)`
- Section padding: 24px
- Sidebar width: 240px, dark indigo background, white text
- Content area: white/off-white background
- Max 3 columns on desktop; collapse to 1 column on mobile

## Component Rules
- **Buttons — Primary:** deep indigo fill `#3B2F8E`, white text, 8px radius, no flat look — keep subtle inner shadow
- **Buttons — Secondary:** white fill, indigo border and text
- **Buttons — Danger:** muted red `#B5383C`
- Never use flat, clinic-white enterprise buttons — always keep warmth and depth
- **Progress bars:** indigo fill, light purple track, animated shimmer on active bars
- **Cards:** always white surface, left border accent in category color, 12px radius

## DO NOTs (hard rules)
- Never use flat/clinical enterprise aesthetic (no cold grays, no Helvetica, no SaaS-dashboard look)
- Never use gradients on primary action buttons — only on hero banners
- Never use serif fonts for body text or UI labels
- Never use bright/neon colors outside the defined palette
- Never stack more than 3 columns on a card grid
- Never show a blank empty state — always include an icon + message + CTA button

## Emotional Tone by State
- **Completed / Logged:** Warm green glow, checkmark, calm satisfaction
- **Pending / Not done:** Gentle breathing orange pulse animation — motivating, not alarming
- **Celebration:** Soft confetti or balloons animation — reverent joy
- **Scripture text:** Parchment-like background `#FFF8EE`, gold left border, italic EB Garamond

## Sidebar (Global)
- Dark indigo `#1E1733` background
- Top: app logo + "Logos Pulse" in Playfair Display, gold
- User avatar circle (initials), preferred name, role badge (color-coded pill)
- Notification bell with unread count badge
- Navigation links with active state (gold left border + light indigo bg)
- Bottom: Logout button

## Role Badge Colors
- Prayer Warrior: indigo `#3B2F8E`
- Pastor: teal `#0D7377`
- Bishop: gold `#C9982A`
- Admin: red `#B5383C`