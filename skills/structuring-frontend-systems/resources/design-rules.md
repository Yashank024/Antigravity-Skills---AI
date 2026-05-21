# Design Rules — Frontend Architecture Engine

## 1. Typography Scale

| Token | Size | Usage |
|-------|------|-------|
| `--text-h1` | 48px+ | Page-level hero headings |
| `--text-h2` | 36px | Section headings |
| `--text-h3` | 28px | Sub-section headings |
| `--text-h4` | 22px | Card/component headings |
| `--text-body` | 16px | Default body copy |
| `--text-small` | 14px | Captions, labels, helper text |
| `--text-xs` | 12px | Metadata, badges |

**Rules:**
- Never use font sizes below 12px (accessibility)
- Always use CSS custom properties (`--text-*`), never hardcoded `px` values in components
- Line height: `1.5` for body, `1.2` for headings
- Font weight: 700 for headings, 400 for body, 600 for UI labels

---

## 2. Color System

Define all colors as CSS custom properties in `src/styles/tokens/_colors.css`.

```css
:root {
  /* Brand */
  --color-primary:    #6c63ff;   /* Primary actions, CTAs */
  --color-secondary:  #3ecf8e;   /* Secondary actions, success */
  --color-accent:     #ff6584;   /* Highlights, notifications */

  /* Backgrounds */
  --color-bg:         #0d0d0d;   /* Page background */
  --color-bg-surface: #1a1a1a;   /* Cards, panels */
  --color-bg-muted:   #2a2a2a;   /* Subtle containers */

  /* Text */
  --color-text:       #f0f0f0;   /* Primary text */
  --color-text-muted: #a0a0a0;   /* Secondary / helper text */
  --color-text-dim:   #606060;   /* Disabled / placeholder */

  /* Borders */
  --color-border:     #333333;
  --color-border-focus: var(--color-primary);

  /* Feedback */
  --color-error:      #ff4d4d;
  --color-warning:    #ffa500;
  --color-info:       #4da6ff;
}
```

**Rules:**
- NEVER use raw hex values in component CSS — always reference a `--color-*` token
- Dark mode overrides go inside `[data-theme="light"] {}` block
- Opacity variants: use `color-mix(in srgb, var(--color-primary) 20%, transparent)` instead of alpha hex codes

---

## 3. Component Rules

### One Responsibility Per Component
- Each component must do exactly ONE thing
- If a component renders a list AND handles API data → split into `<List />` + `<ListContainer />`

### No Inline Styling
```jsx
// ❌ FORBIDDEN
<div style={{ marginTop: '24px', color: '#fff' }}>

// ✅ CORRECT
<div className={styles.section}>
```

### No Logic in UI Components
```jsx
// ❌ FORBIDDEN — logic in UI
function HeroSection() {
  const [data, setData] = useState(null);
  useEffect(() => { fetch('/api/hero').then(...) }, []);
  return <h1>{data?.title}</h1>;
}

// ✅ CORRECT — UI only
function HeroSection({ title }) {
  return <h1 className={styles.heroTitle}>{title}</h1>;
}
// Logic goes in modules/hero/logic/useHeroData.js
```

### No Mixed CSS Strategies
- Pick ONE: CSS Modules OR Tailwind OR Scoped Styles
- NEVER mix global `className="text-white"` Tailwind with CSS module `styles.title`
- Global CSS (`base.css`) is ONLY for resets and root token definitions

---

## 4. Responsive Design Rules

- **Mobile-first** breakpoints: write default styles for mobile, override for larger screens
- Breakpoints:

```css
/* in src/styles/tokens/_breakpoints.css */
:root {
  --bp-sm: 480px;
  --bp-md: 768px;
  --bp-lg: 1024px;
  --bp-xl: 1280px;
}

/* Usage */
@media (min-width: 768px) { ... }
```

- NEVER use `px` for media query widths — use the token value or define breakpoints in JS constants for consistency
- Touch targets minimum size: 44×44px
- No horizontal scroll on any viewport
