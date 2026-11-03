# DESIGN.md — Digital Twin (Atmospheric Glass & Dynamic Slate)

A dual-mode (Dark & Light) design specification and token architecture for Antonio Cacciapuoti's Interactive Digital Twin conversational chat interface.

---

## 1. Design Philosophy & Conversational Stage

- **Quiet Focus & Cognitive Ergonomics**: A calm, distraction-free conversational canvas. Telemetry clutter, debug bars, and extraneous panels are eliminated in favor of clean dialog affordances.
- **Floating Conversational Stage**: The persona presence (portrait avatar, verified badge, and greeting) anchors the upper half, leading naturally into the core card container and bottom input dock.
- **Instant Gratification**: Prominently presented suggestion chips allowing one-click inquiry into Antonio's background, philosophy, and availability.
- **Seamless Modal Cohesion**: Shares identical backdrop blurs, corner radii, and color harmonies with the Portfolio, guaranteeing zero visual friction when transitioning between screens.

---

## 2. Design Tokens: Dark & Light Mode

| Token Role | Dark Mode Value | Light Mode Value | Description / Usage |
| :--- | :--- | :--- | :--- |
| **Canvas Background** | `#0B0D14` | `#FAFBFD` | Page body background |
| **Backdrop Radial Glow** | `radial-gradient(circle, rgba(62,123,250,0.14) 0%, transparent 70%)` | `radial-gradient(circle, rgba(147,197,253,0.35) 0%, rgba(243,244,246,0) 70%)` | Ambient halo behind conversational card |
| **Central Stage Card Bg** | `rgba(26, 27, 35, 0.70)` | `rgba(255, 255, 255, 0.85)` | Primary chat workspace card |
| **Central Stage Card Border**| `rgba(255, 255, 255, 0.08)` | `rgba(226, 232, 240, 0.80)` | Glass container outer outline |
| **Avatar Glow Ring** | `0 0 0 3px rgba(62, 123, 250, 0.25)` | `0 0 0 3px rgba(37, 99, 235, 0.15)` | Profile photo halo |
| **Text Primary (Headlines)**| `#FFFFFF` | `#0F172A` | Name, "Ask me about my experience..." |
| **Text Secondary (Subheads)**| `#94A3B8` | `#475569` | Model context description |
| **Text Placeholder** | `#64748B` | `#94A3B8` | Input field prompt text |
| **Suggestion Pill Bg** | `rgba(255, 255, 255, 0.04)` | `rgba(255, 255, 255, 0.90)` | Floating chip background |
| **Suggestion Pill Border** | `rgba(255, 255, 255, 0.10)` | `rgba(203, 213, 225, 0.60)` | Chip outline |
| **Suggestion Pill Text** | `#E2E8F0` | `#334155` | Chip question label |
| **Suggestion Pill Hover** | `rgba(62, 123, 250, 0.15)` | `rgba(241, 245, 249, 1.00)` | Interactive chip hover state |
| **Input Dock Surface** | `rgba(18, 19, 27, 0.85)` | `#FFFFFF` | Floating conversational input dock |
| **Input Dock Border** | `rgba(255, 255, 255, 0.12)` | `rgba(226, 232, 240, 0.90)` | Input border outline |
| **Send Action Button** | `#2563EB` | `#2563EB` | Circular submit button (`↑` icon) |
| **Send Action Icon** | `#FFFFFF` | `#FFFFFF` | Icon color |

---

## 3. Typography & Hierarchy

- **Primary Font Family**: `Plus Jakarta Sans`, `-apple-system`, `BlinkMacSystemFont`, `sans-serif`
- **Typographic Scale & Spacing**:
  - **Persona Name**: `font-size: 1.5rem` (24px), `font-weight: 700`, `letter-spacing: -0.02em`.
  - **Persona Subtitle**: `font-size: 0.875rem` (14px), `font-weight: 500`, `letter-spacing: 0.02em`, uppercase/subtle.
  - **Hero Greeting Headline**: `font-size: 2.25rem` (36px), `font-weight: 700`, `letter-spacing: -0.025em`, `line-height: 1.25`. Centered.
  - **Model Training Notice**: `font-size: 1rem` (16px), `font-weight: 400`, `line-height: 1.6`. Max width constrained to `540px` for optimal readability.
  - **Prompt Suggestion Chips**: `font-size: 0.875rem` (14px), `font-weight: 500`, with diagonal up-right arrow (`↗`).
  - **Input Placeholder Text**: `font-size: 0.9375rem` (15px), `font-weight: 400`.

---

## 4. Conversational Stage Geometry

1. **Header Avatar Cluster**:
   - Centered circular avatar (`w-16 h-16` / 64px) with rounded border and subtle active presence indicator ring.
   - Persona title directly underneath.
2. **Main Stage Card**:
   - `max-width: 860px`, `min-height: 520px`.
   - `border-radius: 2rem` (32px).
   - `backdrop-filter: blur(24px) saturate(180%)`.
   - Centered content layout with generous vertical padding (`padding: 3.5rem 2.5rem`).
3. **Suggestion Pill Flow**:
   - Flex wrap row with `gap: 0.75rem`, centered.
   - Pill radius: `9999px`.
   - Micro-interaction: `transform: translateY(-1px)` and subtle border highlight on hover.
4. **Docked Input Bar**:
   - Nested inside or floating at the lower anchor of the card stage.
   - Height: `56px` with `border-radius: 9999px`.
   - Seamless input field paired with a circular submit button (`w-10 h-10`).
   - Subtle sub-text below the bar stating model provenance and inquiry routing.

---

## 5. Implementation Notes for Gradio & Web Frontends

- **CSS Variables Mapping**: All tokens map directly to Gradio custom theme variables (`primary_hue`, `neutral_hue`, `body_background_fill`, `block_background_fill`, `button_primary_background_fill`).
- **Glass Blur Fallback**: For browsers or environments where `backdrop-filter` is disabled, fallback to `rgba(26, 27, 35, 0.95)` (Dark) and `rgba(255, 255, 255, 0.98)` (Light) ensures full opacity and contrast.
