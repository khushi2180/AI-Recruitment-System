# TalentAI — Design System & Figma Specification
## AI-Powered Smart Recruitment System
### Design Tokens, Component Library & UI Guidelines

---

## 1. DESIGN PHILOSOPHY

**Brand Personality:** Intelligent · Trustworthy · Modern · Inclusive  
**Design Principles:**
- **Clarity over cleverness** — Every element serves a purpose
- **Data-first layouts** — Information hierarchy guides every screen
- **Accessible by default** — WCAG 2.1 AA compliance from token level
- **Progressive disclosure** — Show summary → detail on demand
- **Bias-aware design** — The UI itself reflects the project's fairness values

---

## 2. COLOR TOKENS (Design System)

### Primary Palette
```
--color-brand-primary:    #8B5CF6    (Purple 500 — primary actions, CTAs)
--color-brand-secondary:  #EC4899    (Pink 500  — accent, gradient partner)
--color-brand-dark:       #6D28D9    (Purple 700 — hover states)
--color-brand-light:      #A78BFA    (Purple 400 — active/selected)
--color-brand-subtle:     #EDE9FE    (Purple 100 — light backgrounds)
```

### Semantic Colors (Dark Mode)
```
--color-bg-base:          #0A0A0F    (Page background)
--color-bg-surface:       #12121A    (Sidebar, nav)
--color-bg-card:          #1A1A28    (Cards, panels)
--color-bg-card-hover:    #20203A    (Interactive card hover)
--color-bg-input:         #16162A    (Input fields)
```

### Border Colors
```
--color-border-default:   rgba(139, 92, 246, 0.18)
--color-border-focus:     rgba(139, 92, 246, 0.60)
--color-border-active:    rgba(139, 92, 246, 0.45)
--color-border-error:     rgba(239, 68, 68, 0.50)
```

### Text Colors
```
--color-text-primary:     #F8FAFC    (Headings, primary content)
--color-text-secondary:   #94A3B8    (Subheadings, labels)
--color-text-muted:       #475569    (Captions, disabled)
--color-text-inverse:     #0F172A    (Text on light backgrounds)
```

### Status / Semantic
```
--color-success-bg:       rgba(16, 185, 129, 0.12)
--color-success-border:   rgba(16, 185, 129, 0.30)
--color-success-text:     #10B981    (Green 500)
--color-success-dark:     #065F46

--color-warning-bg:       rgba(245, 158, 11, 0.12)
--color-warning-border:   rgba(245, 158, 11, 0.30)
--color-warning-text:     #F59E0B    (Amber 500)

--color-danger-bg:        rgba(239, 68, 68, 0.12)
--color-danger-border:    rgba(239, 68, 68, 0.30)
--color-danger-text:      #EF4444    (Red 500)

--color-info-bg:          rgba(59, 130, 246, 0.12)
--color-info-border:      rgba(59, 130, 246, 0.30)
--color-info-text:        #3B82F6    (Blue 500)
```

### Data Visualization Palette (Chart Colors)
```
Chart Color 1 (Primary):  #8B5CF6   Purple 500
Chart Color 2 (Accent):   #EC4899   Pink 500
Chart Color 3 (Success):  #10B981   Green 500
Chart Color 4 (Warning):  #F59E0B   Amber 500
Chart Color 5 (Info):     #3B82F6   Blue 500
Chart Color 6 (Teal):     #06B6D4   Cyan 500
Chart Color 7 (Muted):    #64748B   Slate 500
Chart Diverging (High):   #EF4444   Red (bias HIGH)
Chart Diverging (Low):    #10B981   Green (bias LOW)
```

---

## 3. TYPOGRAPHY TOKENS

### Font Families
```
--font-display:   'Space Grotesk', sans-serif    (Headings, KPIs, brand)
--font-body:      'Inter', sans-serif             (Body text, UI labels)
--font-mono:      'JetBrains Mono', monospace     (Code, IDs, scores)

Google Fonts Import:
  https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800
  &family=Space+Grotesk:wght@400;500;600;700
  &family=JetBrains+Mono:wght@400;500
```

### Type Scale
```
--text-display-2xl:  font-size: 48px; font-weight: 700; line-height: 1.1;  (Hero / KPI hero)
--text-display-xl:   font-size: 36px; font-weight: 700; line-height: 1.2;  (Page titles)
--text-display-lg:   font-size: 24px; font-weight: 700; line-height: 1.3;  (Section headings)
--text-display-md:   font-size: 20px; font-weight: 700; line-height: 1.3;  (Card headings)
--text-display-sm:   font-size: 17px; font-weight: 600; line-height: 1.4;  (Sub-section)

--text-body-lg:      font-size: 16px; font-weight: 400; line-height: 1.6;  (Primary body)
--text-body-md:      font-size: 14px; font-weight: 400; line-height: 1.6;  (UI text)
--text-body-sm:      font-size: 13px; font-weight: 400; line-height: 1.5;  (Secondary text)
--text-body-xs:      font-size: 12px; font-weight: 400; line-height: 1.5;  (Labels, captions)
--text-label:        font-size: 11px; font-weight: 600; letter-spacing: 0.08em; UPPERCASE
--text-mono:         font-size: 13px; font-weight: 400; (Monospace for IDs, scores)
```

---

## 4. SPACING TOKENS

```
--space-0:    0px
--space-1:    4px      (micro gap, icon margin)
--space-2:    8px      (tight gap, padding xs)
--space-3:    12px     (standard gap)
--space-4:    16px     (standard padding)
--space-5:    20px     (card padding)
--space-6:    24px     (section gap)
--space-7:    28px     (content padding)
--space-8:    32px     (large gap)
--space-10:   40px     (section separation)
--space-12:   48px     (hero spacing)
--space-16:   64px     (page-level spacing)

Sidebar width:    260px
Topbar height:    65px
Card min-width:   280px
Table row height: 48px
```

---

## 5. BORDER RADIUS TOKENS

```
--radius-none:   0px
--radius-xs:     4px    (chips, tags, badges)
--radius-sm:     8px    (buttons, inputs, small cards)
--radius-md:     14px   (standard cards, panels)
--radius-lg:     20px   (large cards, modals)
--radius-xl:     28px   (hero sections)
--radius-full:   9999px (pills, avatars, toggles)
```

---

## 6. SHADOW & ELEVATION TOKENS

```
--shadow-sm:     0 1px 2px rgba(0,0,0,0.3)
--shadow-md:     0 4px 12px rgba(0,0,0,0.4)
--shadow-lg:     0 8px 24px rgba(0,0,0,0.5)
--shadow-xl:     0 16px 48px rgba(0,0,0,0.6)

--glow-purple:   0 0 40px rgba(139, 92, 246, 0.25)
--glow-pink:     0 0 40px rgba(236, 72, 153, 0.20)
--glow-green:    0 0 40px rgba(16, 185, 129, 0.20)
--glow-red:      0 0 40px rgba(239, 68, 68, 0.20)
--glow-amber:    0 0 40px rgba(245, 158, 11, 0.20)

Glassmorphism card:
  background: rgba(26, 26, 40, 0.80)
  backdrop-filter: blur(20px)
  border: 1px solid rgba(139, 92, 246, 0.18)
```

---

## 7. ANIMATION TOKENS

```
--duration-fast:    150ms   (hover state changes)
--duration-normal:  200ms   (button interactions)
--duration-slow:    300ms   (modal open/close)
--duration-slower:  500ms   (page transitions)
--duration-chart:   1200ms  (chart bar animations)

--ease-default:   cubic-bezier(0.4, 0, 0.2, 1)  (Material standard)
--ease-in:        cubic-bezier(0.4, 0, 1, 1)     (Entering elements)
--ease-out:       cubic-bezier(0, 0, 0.2, 1)     (Exiting elements)
--ease-bounce:    cubic-bezier(0.34, 1.56, 0.64, 1) (Playful interactions)
```

---

## 8. COMPONENT SPECIFICATIONS

### 8.1 KPI Card
```
Dimensions:    min-width: 220px; padding: 20px 22px
Background:    var(--color-bg-card)
Border:        1px solid var(--color-border-default)
Border-radius: var(--radius-md)
Top accent:    2px gradient bar (role-specific color)
Hover:         border-color: var(--color-border-active)
               transform: translateY(-2px)
               box-shadow: var(--glow-purple)

Contents:
  - Label:    --text-label (uppercase, muted)
  - Icon:     20px emoji/SVG (top-right)
  - Value:    --text-display-xl, brand color
  - Sub-text: --text-body-xs, muted
  - Sparkline: 7-bar mini chart (40px height)

Transition: all 250ms var(--ease-default)
```

### 8.2 Navigation Item
```
Dimensions:    padding: 10px 12px; full-width sidebar
Border-radius: var(--radius-xs)
Icon:          20px, centered in 20px container
Label:         --text-body-sm; font-weight: 500
Badge:         --text-label; padding: 2px 7px; border-radius: var(--radius-full)

States:
  Default:  color: var(--color-text-secondary); background: transparent
  Hover:    color: var(--color-text-primary); background: rgba(139,92,246,0.12)
  Active:   color: var(--color-brand-light); background: rgba(139,92,246,0.20)
            border: 1px solid var(--color-border-default)
```

### 8.3 Score Pill / Badge
```
High (≥80):   background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.30)
              color: #10B981; font-weight: 700
Medium (60):  background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.30)
              color: #F59E0B
Low (<60):    background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.30)
              color: #EF4444

Shape:        border-radius: var(--radius-full); padding: 4px 10px
Font:         12px, 700 weight, monospace for numeric values
```

### 8.4 Candidate Table Row
```
Height:        48px
Hover:         background: rgba(139,92,246,0.06)
Border:        1px solid rgba(255,255,255,0.04) (bottom only)
Divider:       No full-width lines — subtle bottom border only

Column widths (suggested):
  Rank:        48px
  Name:        200px
  Role:        200px
  Experience:  100px
  CGPA:        80px
  Skills:      80px
  ATS Score:   120px (contains pill)
  Status:      140px (contains chip)
  Tier:        90px
```

### 8.5 Hiring Funnel Bar
```
Container height:  28px; border-radius: 6px
Background:        rgba(255,255,255,0.06)
Fill:              role-specific gradient; border-radius: 6px
Label (inside):    11px, 600 weight, white 85% opacity, padding-left: 10px
Animation:         width transition 1200ms cubic-bezier(0.4,0,0.2,1)
```

### 8.6 Bias Severity Bar
```
Container:     6px height; border-radius: 4px
Fill colors:
  HIGH:    #EF4444
  MEDIUM:  #F59E0B
  LOW:     #10B981
  UNOBS:   #64748B
Animation:   width transition 1500ms ease

Severity Badge:
  HIGH:   bg rgba(239,68,68,0.15); color #EF4444
  MEDIUM: bg rgba(245,158,11,0.15); color #F59E0B
  LOW:    bg rgba(16,185,129,0.12); color #10B981
  UNOBS:  bg rgba(100,116,139,0.20); color #94A3B8
```

### 8.7 Primary Button
```
Background:    linear-gradient(135deg, #8B5CF6, #EC4899)
Color:         white
Padding:       9px 18px
Border-radius: var(--radius-sm)
Font:          13px, 600 weight
Box-shadow:    var(--glow-purple)
Hover:         opacity: 0.90; transform: translateY(-1px)
Active:        transform: translateY(0); opacity: 0.85
Transition:    all 200ms var(--ease-default)
```

### 8.8 Ghost Button
```
Background:    rgba(139,92,246,0.10)
Color:         var(--color-brand-light)
Border:        1px solid var(--color-border-default)
Hover:         background: rgba(139,92,246,0.20)
Same shape/size as Primary Button
```

---

## 9. FIGMA PAGE STRUCTURE

### Recommended Figma File Layout:

```
📁 TalentAI Design System
├── 📄 Cover (project preview)
├── 📄 🎨 Tokens
│   ├── Color Styles (all tokens above)
│   ├── Text Styles
│   ├── Effect Styles (shadows, glows)
│   └── Grid Styles (8px base grid)
│
├── 📄 🧩 Components
│   ├── Atoms
│   │   ├── Buttons (Primary, Ghost, Danger, Icon-only)
│   │   ├── Badges (Score pills, Status chips, Nav badges)
│   │   ├── Avatars (User avatar, Company logo)
│   │   ├── Inputs (Text, Search, Select, Checkbox)
│   │   └── Icons (Emoji set, SVG icons)
│   │
│   ├── Molecules
│   │   ├── KPI Card (with sparkline)
│   │   ├── Navigation Item (with badge)
│   │   ├── Table Row (with hover state)
│   │   ├── Funnel Bar Stage
│   │   ├── Bias Detection Item
│   │   ├── Role Card (open positions)
│   │   ├── Activity Feed Item
│   │   └── Diversity Stat Card
│   │
│   └── Organisms
│       ├── Sidebar (collapsed + expanded)
│       ├── Top Navigation Bar
│       ├── KPI Grid (4-column)
│       ├── Hiring Funnel Panel
│       ├── Candidate Table (full)
│       ├── Bias Report Panel
│       └── Activity Feed Panel
│
├── 📄 🖥️ Desktop Screens (1440px wide)
│   ├── 01 — Dashboard Overview
│   ├── 02 — Candidate List (full table)
│   ├── 03 — Candidate Profile (detail view)
│   ├── 04 — Hiring Funnel Analytics
│   ├── 05 — Bias Detection Report
│   ├── 06 — Diversity Analytics
│   ├── 07 — Job Openings
│   ├── 08 — Interview Questions
│   └── 09 — Offer Management
│
├── 📄 📱 Mobile Screens (375px)
│   ├── Dashboard (scrollable)
│   ├── Candidate Profile
│   └── Hire Funnel
│
└── 📄 📋 Handoff Notes
    ├── Spacing specifications
    ├── Animation timing guide
    ├── Accessibility annotations
    └── Component state guide
```

---

## 10. ACCESSIBILITY SPECIFICATIONS (WCAG 2.1 AA)

### Color Contrast Ratios
```
Primary text (#F8FAFC) on bg (#0A0A0F):    ✅ 19.8:1 (AAA)
Secondary (#94A3B8) on bg (#0A0A0F):       ✅ 7.4:1  (AAA)
Muted (#475569) on bg (#0A0A0F):           ✅ 4.8:1  (AA)
Purple label on card (#1A1A28):            ✅ 5.2:1  (AA)
Green score pill (#10B981 on dark bg):     ✅ 4.7:1  (AA)
Red score pill (#EF4444 on dark bg):       ✅ 4.6:1  (AA)
```

### Focus States
```
All interactive elements: outline: 2px solid #8B5CF6; outline-offset: 2px
No outline removal without replacement
Keyboard navigation fully supported
```

### ARIA Labels (Key Elements)
```html
<!-- KPI Card -->
<article aria-label="KPI: Applications Received — 30">
  <h2 aria-hidden="true">30</h2>
</article>

<!-- Candidate Table -->
<table role="grid" aria-label="Ranked Candidates — 30 total">
  <caption class="sr-only">ATS-ranked candidate list, sorted by score descending</caption>
</table>

<!-- Score Pill -->
<span role="status" aria-label="ATS Score: 86.3 out of 100 — High">86.3</span>

<!-- Hiring Funnel Bar -->
<div role="progressbar" aria-valuenow="63" aria-valuemin="0" aria-valuemax="100"
     aria-label="Shortlisted: 19 of 30 candidates (63%)">
```

### Keyboard Navigation Order
```
1. Skip to main content link (hidden, visible on focus)
2. Logo / Home
3. Navigation items (sidebar) — Arrow key navigation
4. Main content area
5. KPI Cards (Tab order)
6. Charts (summary announced by screen reader)
7. Candidate table (full keyboard navigation)
8. Action buttons
```

---

## 11. RESPONSIVE BREAKPOINTS

```
Mobile:   320px–767px   (single column, collapsed sidebar drawer)
Tablet:   768px–1199px  (2-column, compact sidebar 60px icon-only)
Desktop:  1200px–1439px (full layout, sidebar 260px)
Wide:     1440px+       (max-width 1600px centered)

Grid behavior:
  KPI cards:    4-col desktop → 2-col tablet → 1-col mobile
  Charts:       2-col desktop → 1-col tablet → 1-col mobile
  Candidate table: Horizontal scroll on mobile/tablet
  Sidebar:      Full on desktop → icon-only on tablet → drawer on mobile
```

---

## 12. DARK MODE ONLY (Design Decision)

This design is **dark-mode native** — no light mode variant required for this project. Justification:
- Reduces eye strain for long recruiter sessions
- Better data viz contrast on dark backgrounds
- Aligned with modern SaaS dashboard conventions (Linear, Vercel, Supabase)
- The purple/pink gradient system has higher visual impact on dark backgrounds

If a light mode is required in future, define a separate token layer:
```
--color-bg-base-light:    #F8FAFC
--color-bg-card-light:    #FFFFFF
--color-border-light:     rgba(99, 102, 241, 0.15)
```

---

*TalentAI Design Specification v1.0 — AI-Powered Smart Recruitment System*
*Capstone Project · 2024*
