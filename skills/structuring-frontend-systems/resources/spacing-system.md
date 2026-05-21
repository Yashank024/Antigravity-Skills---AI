# Spacing System — 4px Base Scale

## Core Scale

All spacing values MUST be multiples of 4px.

```css
/* src/styles/tokens/_spacing.css */
:root {
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
  --space-32: 128px;
}
```

---

## Usage Guidelines

### Section Padding
Sections (full-width page sections) must use large spacing:

| Context | Min | Recommended | Max |
|---------|-----|-------------|-----|
| Section padding-top/bottom | 48px (`--space-12`) | 64px (`--space-16`) | 80px (`--space-20`) |
| Section margin between sections | 64px (`--space-16`) | 80px (`--space-20`) | 128px (`--space-32`) |

```css
/* ✅ CORRECT */
.section {
  padding-block: var(--space-16);
  margin-bottom: var(--space-20);
}
```

### Container Padding
Horizontal padding to keep content away from screen edges:

| Context | Mobile | Tablet | Desktop |
|---------|--------|--------|---------|
| Container side padding | 16px (`--space-4`) | 24px (`--space-6`) | 32px (`--space-8`) |

```css
.container {
  padding-inline: var(--space-4);
  max-width: 1200px;
  margin-inline: auto;
}

@media (min-width: 768px) {
  .container { padding-inline: var(--space-6); }
}

@media (min-width: 1024px) {
  .container { padding-inline: var(--space-8); }
}
```

### Component Padding (Cards, Buttons, Tags)

| Component | Padding |
|-----------|---------|
| Button (large) | 12px 24px (`--space-3` `--space-6`) |
| Button (medium) | 8px 16px (`--space-2` `--space-4`) |
| Button (small) | 4px 12px (`--space-1` `--space-3`) |
| Card | 24px (`--space-6`) |
| Form input | 12px 16px (`--space-3` `--space-4`) |
| Badge / Tag | 4px 8px (`--space-1` `--space-2`) |

### Component Margins (Gaps Between Siblings)

| Context | Spacing |
|---------|---------|
| Between heading and body text | 16px (`--space-4`) |
| Between body and CTA button | 24px (`--space-6`) |
| Between cards in a grid | 24px (`--space-6`) |
| Between nav items | 16px (`--space-4`) |
| Between form fields | 16px (`--space-4`) |

---

## Rules

- **NEVER** use raw pixel values in component CSS files: `margin: 13px` → **BUG**
- **ALWAYS** use the nearest 4px multiple and reference the token
- Gap between components: `16px–24px`
- Gap between sections: `64px+`
- Exception: 1px borders and borders are allowed as raw values

---

## Quick Lookup

```
4px  = --space-1  = micro gap (between icon and text)
8px  = --space-2  = small gap (badge padding)
16px = --space-4  = standard component gap
24px = --space-6  = card padding / section padding min
32px = --space-8  = medium separation
48px = --space-12 = section padding
64px = --space-16 = section-to-section gap
80px = --space-20 = large hero padding
```
