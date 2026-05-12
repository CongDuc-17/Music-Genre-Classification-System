# Design System Inspired by Spotify

## 1. Visual Theme & Atmosphere

Spotify's design system embodies a dark, immersive music-centric experience with a bold, modern aesthetic. The visual language prioritizes content—album artwork, artist imagery, and music—by using a deep, near-black canvas that allows vibrant accents and high-contrast white text to command attention. The system balances minimalist navigation with generous whitespace, creating a focused listening environment. The overall mood is sophisticated, energetic, and accessible, with smooth interactions and clear visual hierarchy that guides users through discovery and playback seamlessly.

**Key Characteristics**
- Deep dark palette (`#121212`, `#1F1F1F`) for reduced eye strain during extended listening
- Bright white (`#FFFFFF`) and neutral gray (`#B3B3B3`) for legible text and secondary information
- Spotify green (`#1ED760`, `#1DB954`) as the signature success and active state indicator
- Rounded, pill-shaped buttons and inputs that feel modern and approachable
- Content-first layout with transparent card backgrounds allowing imagery to breathe
- High contrast for accessibility and visual clarity in a dark theme

## 2. Color Palette & Roles

### Primary
- **Spotify Green** (`#1ED760`): Primary call-to-action, play buttons, active states, and success confirmations
- **Spotify Green Hover** (`#1DB954`): Darker shade for interactive hover and focus states on green elements

### Accent Colors
- **Brand Magenta** (`#DB2D79`): Secondary accent for highlights and special promotions
- **Cool Neutral** (`#667A7A`): Subtle accent for secondary UI elements and hover states

### Interactive
- **Icon Active** (`#FFFFFF`): Primary interactive icon color for buttons and navigation
- **Icon Inactive** (`#B3B3B3`): Secondary/disabled state for icons and secondary buttons
- **Link Blue** (`#0000EE`): Hyperlink color for web standards compliance

### Neutral Scale
- **Pure White** (`#FFFFFF`): Primary text, headings, and high-contrast elements
- **Secondary Gray** (`#B3B3B3`): Secondary text, subheadings, and disabled states (most frequently used neutral)
- **Tertiary Gray** (`#7C7C7C`): Tertiary text and subtle UI separators
- **Placeholder Gray** (`#9D968E`): Input placeholder text and de-emphasized content

### Surface & Borders
- **Surface Dark Primary** (`#121212`): Main app background and primary surface layer
- **Surface Dark Secondary** (`#1F1F1F`): Secondary surfaces, cards, and elevated containers
- **Surface Dark Tertiary** (`#282828`): Tertiary surfaces for progressive elevation
- **Background Overlay Light** (`#383840`): Subtle overlays and modal backgrounds
- **Border Subtle** (`#383840`): Minimal borders on light surfaces or dividers

### Semantic / Status
- **Success** (`#1ED760`): Confirmations, completed actions, and premium indicators
- **Error** (`#B84840`): Error messages, alerts, and destructive states

## 3. Typography Rules

### Font Family
**Primary Font:** SpotifyMixUI (fallback: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif)

**Secondary Font:** SpotifyMixUITitle (fallback: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif)

Both fonts are optimized for screen readability and support the full Spotify typographic hierarchy from display text to micro labels.

### Hierarchy

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|------|--------|-------------|-----------------|-------|
| Display / Page Title | SpotifyMixUITitle | 32px | 700 | 40px | 0px | Large headings for major sections |
| Section Heading | SpotifyMixUITitle | 24px | 700 | 32px | 0px | Primary section headers (e.g., "Trending songs") |
| Heading Level 1 | SpotifyMixUI | 16px | 700 | 20px | 0px | Card titles, dialog titles |
| Heading Level 4 | SpotifyMixUI | 14.08px | 600 | 21.12px | 0px | Subheadings, category labels |
| Heading Level 5 | SpotifyMixUI | 13px | 700 | 20px | 0px | Strong secondary text |
| Body / Standard | SpotifyMixUI | 14px | 700 | 20px | 0px | Primary body text and labels |
| Body Regular | SpotifyMixUI | 16px | 400 | 20px | 0px | Regular body and link text |
| Caption / Small | SpotifyMixUI | 12px | 400 | 16px | 0px | Fine print, timestamps, metadata |
| Code / Mono | Courier New | 13px | 400 | 18px | 0px | Technical text and code snippets |

### Principles
- **Contrast First:** All text meets WCAG AA standards against dark backgrounds
- **Hierarchy Through Weight:** Bold (`700`) and semi-bold (`600`) carry semantic weight; regular (`400`) provides hierarchy breaks
- **Generous Line Height:** Minimum `1.4x` multiplier ensures breathing room in dark mode
- **No Letter Spacing Abuse:** Track remains `0px` for natural readability; justified by font design
- **Responsive Sizing:** Base size (`14px`) scales up for larger viewports; never below `12px` for readability

## 4. Component Stylings

### Buttons

#### Primary CTA Button
- **Background:** `#1ED760`
- **Text Color:** `#000000`
- **Font:** SpotifyMixUI, `16px`, weight `700`
- **Padding:** `12px 32px`
- **Border Radius:** `9999px` (full pill)
- **Border:** `0px none`
- **Height:** `48px`
- **Box Shadow:** `none`
- **Hover State:** background `#1DB954`, cursor pointer
- **Active State:** background `#1DB954`, scale `0.98`

#### Secondary Button (Outlined)
- **Background:** `rgba(0, 0, 0, 0)`
- **Text Color:** `#B3B3B3`
- **Font:** SpotifyMixUI, `16px`, weight `400`
- **Padding:** `0px 12px`
- **Border Radius:** `9999px`
- **Border:** `1px solid #B3B3B3`
- **Height:** `48px`
- **Box Shadow:** `none`
- **Hover State:** text color `#FFFFFF`, border color `#FFFFFF`
- **Focus State:** outline `2px solid #1ED760` offset `2px`

#### Ghost Button (Icon)
- **Background:** `rgba(0, 0, 0, 0)`
- **Text Color:** `#B3B3B3`
- **Font:** SpotifyMixUI, `16px`, weight `400`
- **Padding:** `12px 12px`
- **Border Radius:** `9999px`
- **Border:** `0px none`
- **Height:** `48px`
- **Width:** `48px`
- **Box Shadow:** `none`
- **Hover State:** text color `#FFFFFF`, background `rgba(255, 255, 255, 0.1)`
- **Active State:** background `#1ED760`, text color `#000000`

#### Mini Icon Button
- **Background:** `rgba(0, 0, 0, 0)`
- **Text Color:** `#B3B3B3`
- **Font:** SpotifyMixUI, `16px`, weight `400`
- **Padding:** `0px 0px`
- **Border Radius:** `9999px`
- **Border:** `0px none`
- **Height:** `24px`
- **Width:** `24px`
- **Box Shadow:** `none`
- **Hover State:** text color `#FFFFFF`, scale `1.1`

### Cards & Containers

#### Content Card (Album/Podcast)
- **Background:** `rgba(0, 0, 0, 0)` (transparent, image visible)
- **Text Color:** `#FFFFFF`
- **Font:** SpotifyMixUI, `14px`, weight `400`
- **Padding:** `12px 12px 12px 12px`
- **Border Radius:** `6px`
- **Border:** `0px none`
- **Width:** `195.5px`
- **Height:** `251px`
- **Box Shadow:** `0px 8px 16px rgba(0, 0, 0, 0.4)`
- **Hover State:** background `rgba(255, 255, 255, 0.1)`, transform `translateY(-4px)`

#### Surface Card (Dark Background)
- **Background:** `#1F1F1F`
- **Text Color:** `#FFFFFF`
- **Font:** SpotifyMixUI, `14px`, weight `400`
- **Padding:** `16px 16px 16px 16px`
- **Border Radius:** `6px`
- **Border:** `0px none`
- **Box Shadow:** `0px 4px 8px rgba(0, 0, 0, 0.3)`
- **Hover State:** background `#282828`, cursor pointer

#### Artist/Profile Circle
- **Background:** Image-backed or `#282828`
- **Text Color:** `#FFFFFF`
- **Border Radius:** `50%`
- **Padding:** `0px`
- **Box Shadow:** `0px 8px 16px rgba(0, 0, 0, 0.4)`
- **Hover State:** filter `brightness(1.1)`

### Inputs & Forms

#### Search Input (Dark)
- **Background:** `#1F1F1F`
- **Text Color:** `#FFFFFF`
- **Placeholder Color:** `#B3B3B3`
- **Font:** SpotifyMixUI, `16px`, weight `400`
- **Padding:** `12px 48px 12px 48px`
- **Border Radius:** `500px`
- **Border:** `0px none`
- **Height:** `48px`
- **Width:** `100%` (up to `474px`)
- **Box Shadow:** `inset 0px 0px 0px 1px rgba(255, 255, 255, 0.1)`
- **Focus State:** outline `2px solid #1ED760`, box shadow `inset 0px 0px 0px 2px #1ED760`

#### Standard Input (Light)
- **Background:** `#FFFFFF`
- **Text Color:** `#000000`
- **Placeholder Color:** `#B3B3B3`
- **Font:** SpotifyMixUI, `13.33px`, weight `400`
- **Padding:** `0px 0px`
- **Border Radius:** `0px`
- **Border:** `1px solid #C1C1C1`
- **Height:** `40px`
- **Width:** `250px`
- **Box Shadow:** `none`
- **Focus State:** border color `#1ED760`, outline `2px solid #1ED760`

#### Small Search/Filter Input
- **Background:** `#FFFFFF`
- **Text Color:** `#000000`
- **Placeholder Color:** `#9D968E`
- **Font:** SpotifyMixUI, `12.8px`, weight `400`
- **Padding:** `6px 35px 6px 15px`
- **Border Radius:** `50px`
- **Border:** `1px solid #707070`
- **Height:** `31px`
- **Width:** `100%`
- **Box Shadow:** `none`
- **Focus State:** border color `#1ED760`, background `#FFFBF5`

### Navigation

#### Sidebar Navigation
- **Background:** `#000000` or `#121212`
- **Text Color:** `#B3B3B3`
- **Font:** SpotifyMixUI, `14px`, weight `700`
- **Padding:** `0px 0px`
- **Border Radius:** `0px`
- **Border:** `0px none`
- **Height:** `100vh` (full viewport)
- **Width:** `331px`
- **Box Shadow:** `none`
- **Active Item:** text color `#FFFFFF`, background `rgba(255, 255, 255, 0.1)`, left border `4px solid #1ED760`
- **Hover State:** text color `#FFFFFF`, background `rgba(255, 255, 255, 0.05)`

#### Top Navigation Bar
- **Background:** `rgba(0, 0, 0, 0.6)` (semi-transparent dark)
- **Text Color:** `#FFFFFF`
- **Font:** SpotifyMixUI, `14px`, weight `400`
- **Padding:** `16px 24px`
- **Border Radius:** `0px`
- **Border:** `0px none`
- **Height:** `64px`
- **Box Shadow:** `0px 2px 8px rgba(0, 0, 0, 0.2)`

### Links

#### Text Link
- **Color:** `#1ED760`
- **Font:** SpotifyMixUI, `14px`, weight `400`
- **Text Decoration:** `none`
- **Hover State:** text decoration `underline`, color `#1DB954`

#### Navigation Link
- **Color:** `#B3B3B3`
- **Font:** SpotifyMixUI, `14px`, weight `700`
- **Padding:** `4px 16px 4px 36px`
- **Border Radius:** `9999px`
- **Hover State:** color `#FFFFFF`, background `rgba(255, 255, 255, 0.1)`
- **Active State:** color `#FFFFFF`, background `#1ED760`, font weight `700`

## 5. Layout Principles

### Spacing System

**Base Unit:** `4px`

**Scale:** `4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `28px`, `32px`, `40px`, `48px`, `64px`, `160px`

**Usage Context:**
- **4px–12px:** Padding within components (buttons, badges, tags)
- **16px–24px:** Gap between elements, card padding, section margins
- **32px–48px:** Section spacing, vertical rhythm between content blocks
- **64px:** Major section breaks, page-level spacing
- **160px:** Full-screen height offsets, hero section spacing

### Grid & Container

- **Max Width:** `1400px` (main content area)
- **Sidebar Width:** `331px` (fixed left navigation)
- **Content Area:** Remaining width after sidebar
- **Columns:** Responsive—12 columns on desktop, 6 on tablet, 1 on mobile
- **Gutter:** `16px` between columns
- **Section Pattern:** Sidebar + Header + Main content (3-part layout)
- **Card Grid:** Horizontal scrolling or flex-wrap at `195.5px` card width + `16px` gap

### Whitespace Philosophy

Spotify's design prioritizes breathing room around content. The dark background is used intentionally as negative space, making imagery and text pop. Generous margins between sections (`32px–64px`) create visual hierarchy without adding borders. Within cards and containers, padding of `12px–16px` ensures content doesn't feel cramped. The philosophy treats whitespace as a design element, not wasted space.

### Border Radius Scale

- **4px:** Minimal rounding for subtle definition (rare)
- **6px:** Standard card and container rounding (most common)
- **9999px:** Pill buttons, badges, and fully rounded interactive elements
- **50px:** Larger pill inputs and soft-cornered containers
- **50%:** Perfect circles for avatars and profile pictures

## 6. Depth & Elevation

| Level | Treatment | Use |
|-------|-----------|-----|
| Flat / Level 0 | No shadow; `box-shadow: none` | Text, icons, flat backgrounds |
| Level 1 (Raised) | `0px 2px 4px rgba(0, 0, 0, 0.2)` | Hovered buttons, subtle lift |
| Level 2 (Floating) | `0px 4px 8px rgba(0, 0, 0, 0.3)` | Cards, popovers, secondary surfaces |
| Level 3 (Modal) | `0px 8px 16px rgba(0, 0, 0, 0.4)` | Dialogs, modals, primary cards |
| Level 4 (Overlay) | `0px 16px 32px rgba(0, 0, 0, 0.5)` | Full-screen overlays, heavy lift effects |

**Shadow Philosophy:** Spotify uses subtle, dark shadows to create depth without harshness. Shadows are produced purely through alpha transparency (`rgba(0, 0, 0, X%)`), never pure black, maintaining the warm, modern aesthetic. Shadows increase in blur and spread as elevation increases. Hover states employ small transforms (`translateY(-4px)`) combined with Level 2 shadows to signal interactivity without jarring jumps.

## 7. Do's and Don'ts

### Do
- Use `#1ED760` (Spotify Green) as the primary call-to-action and to highlight active states
- Maintain minimum `48px` height and width for interactive touch targets (buttons, icon buttons)
- Apply `#B3B3B3` for secondary text and disabled states for consistent visual hierarchy
- Use pill-shaped buttons (`border-radius: 9999px`) for all primary interactive elements
- Layer content with dark backgrounds (`#121212`, `#1F1F1F`) to allow imagery to dominate
- Apply subtle shadows (`0px 4px 8px rgba(0, 0, 0, 0.3)`) for card elevation
- Use SpotifyMixUI for all body text and interfaces; SpotifyMixUITitle for major headings
- Pair high contrast (white on black) for accessibility in dark mode
- Employ generous spacing (`16px–24px`) between major sections for visual breathing room
- Test all interactive elements for keyboard navigation and screen reader compatibility

### Don't
- Use harsh, pure black (`#000000`) shadows; always use `rgba(0, 0, 0, X%)` for depth
- Apply `#1ED760` for non-primary actions or as a neutral color—reserve it for success and CTAs
- Create interactive elements smaller than `48px` on any dimension
- Use light backgrounds (`#FFFFFF`) as primary surfaces; dark (`#121212`, `#1F1F1F`) is the default
- Mix multiple sans-serif font families; stick to SpotifyMixUI and SpotifyMixUITitle
- Reduce line height below `1.4x` for body text; maintain `20px` minimum for `14px` text
- Add borders to dark containers; use shadows and color separation instead
- Use pure white (`#FFFFFF`) for all text; leverage `#B3B3B3` for secondary/disabled states
- Disable focus states or keyboard navigation indicators; all interactive elements must be keyboard-accessible
- Forget to test color contrast; ensure minimum `7:1` ratio for small text against dark backgrounds

## 8. Responsive Behavior

### Breakpoints

| Breakpoint Name | Width | Key Changes |
|-----------------|-------|-------------|
| Mobile | `< 480px` | Single column, sidebar collapses to bottom navigation, cards stack vertically |
| Tablet | `480px – 768px` | 2-column grid, sidebar toggleable, reduced padding (`12px`) |
| Desktop Small | `768px – 1024px` | 3-column grid, sidebar visible, full padding (`16px–24px`) |
| Desktop Medium | `1024px – 1400px` | 4–5 column grid, full-width sidebar, content max-width `1400px` |
| Desktop Large | `> 1400px` | Fixed max-width `1400px`, centered content, 6-column grid |

### Touch Targets

- **Minimum Size:** `48px × 48px` for all interactive buttons and icon buttons
- **Minimum Spacing:** `8px` between adjacent touch targets to prevent accidental triggers
- **Icon Size:** `24px` for micro icons, `32px` for primary icons, `48px` for large CTAs
- **Tap Area Expansion:** Extend clickable area to `56px` on mobile for comfort; use padding or invisible boundaries
- **Text Links:** Minimum `44px` height with `4px` vertical padding for comfortable tapping

### Collapsing Strategy

- **Mobile (< 480px):** 
  - Sidebar converts to bottom navigation tab bar or hamburger menu
  - Main content takes full width
  - Card grid switches to single-column vertical stack
  - Padding reduces to `12px` on all sides
  - Header height decreases to `56px`

- **Tablet (480px – 768px):**
  - Sidebar toggles via hamburger menu or drawer
  - Content area 2-column grid with 3–4 cards per row
  - Padding `12px–16px`
  - Top navigation remains fixed

- **Desktop (768px+):**
  - Sidebar visible and fixed at `331px`
  - Main content area flexible, max `1400px`
  - Full padding scheme (`16px–24px`) applied
  - Cards in 4–6 column horizontal scroll or grid
  - All features visible; no hide/show toggles

## 9. Agent Prompt Guide

### Quick Color Reference

- **Primary CTA:** Spotify Green (`#1ED760`) for play buttons, call-to-action buttons, active/success states
- **Primary CTA Hover:** Spotify Green Hover (`#1DB954`) for all `:hover` and `:active` states on green buttons
- **Primary Text:** Pure White (`#FFFFFF`) for all headings and primary body text on dark backgrounds
- **Secondary Text:** Secondary Gray (`#B3B3B3`) for meta text, subheadings, disabled states, and icon colors
- **Background:** Surface Dark Primary (`#121212`) for main app background; Surface Dark Secondary (`#1F1F1F`) for cards and containers
- **Error State:** Error Red (`#B84840`) for error messages and destructive actions
- **Success State:** Spotify Green (`#1ED760`) for confirmations and positive feedback

### Iteration Guide

1. **Always use dark backgrounds first.** Primary surface is `#121212`; secondary is `#1F1F1F`. Limit white backgrounds to forms and light-mode exceptions.

2. **Green is reserved for primary actions.** `#1ED760` signals play, confirm, active. Use `#B3B3B3` for secondary buttons and icons. Never use green for neutral UI.

3. **Text contrast is non-negotiable.** White on dark, dark on light. Secondary text (`#B3B3B3`) on `#121212` meets 7:1 WCAG AAA. Test all color pairs before shipping.

4. **Buttons are always rounded pills.** `border-radius: 9999px` is the default for buttons, badges, and input fields. Minimal rounding (`6px`) for cards; `50%` only for avatars.

5. **Padding and spacing follow the 4px scale.** All spacing must be `4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px`, `48px`, etc. No arbitrary values.

6. **Shadows are subtle and dark.** Use `rgba(0, 0, 0, X%)` with increasing blur as elevation rises. Level 2 cards = `0px 4px 8px rgba(0, 0, 0, 0.3)`.

7. **Font is SpotifyMixUI for all UI.** Use `400` weight for body, `600–700` for headings. Never go below `12px`. Minimum line height `1.4x`.

8. **Touch targets are minimum 48px.** All buttons, icons, and interactive areas must be at least `48px × 48px` on mobile. Spacing between targets = `8px` minimum.

9. **Sidebar is fixed 331px on desktop, collapses on mobile.** Left navigation shows full links on desktop; convert to hamburger menu or bottom tab bar below `768px`.

10. **Keyboard and screen reader accessibility is built-in.** All interactive elements need `:focus` states (outline `2px solid #1ED760`), proper ARIA labels, and full keyboard navigation support.