# Responsive System Layer — Safe Responsive Architecture

## ⚠️ THE GOLDEN RULE OF RESPONSIVENESS

> **Desktop styles are IMMUTABLE.**
> **Responsive styles EXTEND, never destructively override.**
> **UI stability > aggressive responsiveness.**

---

## 1. Breakpoint System

```css
/* src/styles/responsive/breakpoints.css */
:root {
  --bp-mobile-max:  480px;
  --bp-tablet-min:  481px;
  --bp-tablet-max:  1024px;
  --bp-desktop-min: 1025px;
  --bp-wide-min:    1441px;
}
```

| Device | Range | Media Query |
|--------|-------|-------------|
| Mobile | 0–480px | `@media (max-width: 480px)` |
| Tablet | 481–1024px | `@media (min-width: 481px) and (max-width: 1024px)` |
| Desktop | 1025–1440px | `@media (min-width: 1025px)` |
| Wide | 1441px+ | `@media (min-width: 1441px)` |

---

## 2. Folder Structure (Responsive Layer)

```
src/
├── styles/
│   ├── base/
│   │   └── globals.css
│   └── responsive/                  ← 🔥 NEW — global responsive layer
│       ├── breakpoints.css          ← Breakpoint token definitions
│       ├── mobile.css               ← Global mobile overrides (typography, spacing)
│       └── tablet.css               ← Global tablet overrides
│
└── modules/
    └── [feature]/
        └── styles/
            ├── desktop.module.css   ← Base desktop styles (IMMUTABLE)
            └── responsive.module.css ← 🔥 NEW — mobile/tablet only
```

### Per-Module Responsive Pattern

```css
/* desktop.module.css — DO NOT TOUCH FOR RESPONSIVE */
.container {
  display: flex;
  flex-direction: row;
  gap: var(--space-8);
  padding: var(--space-20);
}

/* responsive.module.css — ONLY MEDIA QUERIES HERE */
@media (max-width: 480px) {
  .container {
    flex-direction: column;
    padding: var(--space-6);
    gap: var(--space-4);
  }
}

@media (min-width: 481px) and (max-width: 1024px) {
  .container {
    padding: var(--space-12);
    gap: var(--space-6);
  }
}
```

---

## 3. Responsive Spacing Scale

Apply proportional scaling — never arbitrary values:

| Token | Desktop | Tablet | Mobile |
|-------|---------|--------|--------|
| Section padding | 80px (`--space-20`) | 48px (`--space-12`) | 24px (`--space-6`) |
| Container padding | 32px (`--space-8`) | 24px (`--space-6`) | 16px (`--space-4`) |
| Card padding | 24px (`--space-6`) | 20px (`--space-5`) | 16px (`--space-4`) |
| Component gap | 24px (`--space-6`) | 16px (`--space-4`) | 12px (`--space-3`) |

---

## 4. Responsive Typography Scale

```css
/* src/styles/responsive/mobile.css */
@media (max-width: 480px) {
  :root {
    --text-h1: 28px;   /* was 48px+ */
    --text-h2: 22px;   /* was 36px  */
    --text-h3: 18px;   /* was 28px  */
    --text-body: 15px; /* was 16px  */
    --text-small: 13px;
  }
}

@media (min-width: 481px) and (max-width: 1024px) {
  :root {
    --text-h1: 36px;
    --text-h2: 28px;
    --text-h3: 22px;
    --text-body: 16px;
    --text-small: 14px;
  }
}
```

---

## 5. Layout Transformation Rules

### Flex
```css
/* Mobile: row → column */
@media (max-width: 480px) {
  .row { flex-direction: column; }
}
```

### Grid
```css
/* Desktop: 3 cols → Tablet: 2 cols → Mobile: 1 col */
@media (max-width: 1024px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 480px) {
  .grid { grid-template-columns: 1fr; }
}
```

### Absolute Positioning
- Convert `position: absolute` elements to `position: relative` on mobile when they cause overflow
- Stack absolutely-positioned overlays below content on mobile

---

## 6. Touch Optimization Rules

```css
/* Apply globally in styles/responsive/mobile.css */
@media (max-width: 480px) {
  /* Minimum tap target size */
  button, a, [role="button"] {
    min-height: 44px;
    min-width: 44px;
  }

  /* Space between clickable elements */
  nav a + a,
  .action-group > * + * {
    margin-top: 8px;
  }
}
```

---

## 7. Overflow & Image Rules

```css
/* Global safe defaults — apply in styles/base/globals.css */
* { box-sizing: border-box; }
html, body { overflow-x: hidden; }

img, video, canvas, svg {
  max-width: 100%;
  height: auto;
  object-fit: cover;
}
```

---

## 8. Conflict Prevention Rules

| Rule | ❌ Forbidden | ✅ Correct |
|------|-------------|-----------|
| No global overrides | `.container { padding: 10px !important; }` | Scoped CSS module + media query |
| No inline responsive | `style={{ padding: isMobile ? 10 : 40 }}` | CSS media query in responsive.module.css |
| No desktop re-declaration | Re-writing desktop values in responsive file | Only write what CHANGES for that breakpoint |
| No breakpoint conflicts | Two files setting same property at same breakpoint | One source of truth per breakpoint per property |

---

## 9. Responsive Workflow (Step-by-Step)

```
1. SCAN       — List all UI components in src/ui/ + src/modules/*/ui/
2. ANALYZE    — Detect layout type: flex/grid/absolute for each component
3. MAP        — Record desktop spacing, typography, widths for each section
4. PLAN       — Create responsive layer plan (what changes per breakpoint)
5. CREATE     — Generate responsive.module.css for each module
6. GENERATE   — Generate global styles/responsive/mobile.css + tablet.css
7. VALIDATE   — Check desktop render is pixel-identical to pre-change
8. TEST       — Verify mobile/tablet layout at each breakpoint
9. OVERFLOW   — Confirm zero horizontal scroll at any viewport width
10. REPORT    — Output: what was added, what was preserved, what needs manual review
```

---

## 10. Pre-Execution Validation Checklist

Before applying any responsive changes, confirm:

- [ ] Desktop CSS files are **read-only** during this phase (no edits)
- [ ] Responsive files contain **only** `@media` blocks — no bare selectors
- [ ] All class names in responsive files match exactly those in desktop files
- [ ] No `!important` used anywhere in responsive styles
- [ ] `overflow-x: hidden` applied at root level
- [ ] All images have `max-width: 100%`
- [ ] All buttons/links have `min-height: 44px` on mobile
