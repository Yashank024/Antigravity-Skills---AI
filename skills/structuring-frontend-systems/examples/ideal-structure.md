# Ideal Frontend Structure — Reference Target

This is the exact target structure the `structuring-frontend-systems` skill produces.

```
src/
│
├── app/                          # Entry point only
│   ├── App.jsx                   # Root component, provider wrappers
│   └── routes.jsx                # All route definitions
│
├── core/                         # System-level, framework-agnostic code
│   ├── config/
│   │   └── app.config.js         # Env vars, feature flags
│   ├── constants/
│   │   └── routes.js             # Route names, API keys, enums
│   └── utils/
│       ├── formatDate.js         # Pure utility functions
│       ├── cn.js                 # className utility
│       └── validators.js
│
├── ui/                           # Pure UI — zero logic, zero WebGL
│   ├── components/               # Reusable, generic components
│   │   ├── Button/
│   │   │   ├── Button.jsx
│   │   │   └── Button.module.css
│   │   ├── Heading/
│   │   │   ├── Heading.jsx
│   │   │   └── Heading.module.css
│   │   └── Card/
│   │       ├── Card.jsx
│   │       └── Card.module.css
│   └── primitives/               # Atomic UI: Icon, Text, Divider
│       ├── Icon.jsx
│       └── Text.jsx
│
├── layout/                       # Structural layout components
│   ├── Navbar/
│   │   ├── Navbar.jsx
│   │   └── Navbar.module.css
│   ├── Footer/
│   │   ├── Footer.jsx
│   │   └── Footer.module.css
│   └── Container.jsx             # Max-width wrapper
│
├── modules/                      # Feature-based, self-contained modules
│   │
│   ├── hero/
│   │   ├── ui/
│   │   │   └── HeroSection.jsx   # UI only — no logic
│   │   ├── logic/
│   │   │   ├── useHeroData.js    # Data fetching hook
│   │   │   └── heroApi.js        # API call functions
│   │   ├── styles/
│   │   │   ├── hero.module.css        # Desktop styles (IMMUTABLE)
│   │   │   └── responsive.module.css  # 🔥 Mobile/tablet only (@media blocks)
│   │   └── index.js              # Public API surface
│   │
│   ├── about/
│   │   ├── ui/
│   │   ├── logic/
│   │   ├── styles/
│   │   └── index.js
│   │
│   ├── projects/
│   │   ├── ui/
│   │   │   ├── ProjectGrid.jsx
│   │   │   └── ProjectCard.jsx
│   │   ├── logic/
│   │   │   └── useProjects.js
│   │   ├── styles/
│   │   │   └── projects.module.css
│   │   └── index.js
│   │
│   └── contact/
│       ├── ui/
│       ├── logic/
│       ├── styles/
│       └── index.js
│
├── graphics/                     # 🔥 ALL WebGL / Three.js — completely isolated
│   ├── scenes/                   # Three.js scene setups
│   │   ├── HeroScene.js
│   │   └── BackgroundScene.js
│   ├── shaders/                  # GLSL shaders
│   │   ├── particle.vert.glsl
│   │   └── particle.frag.glsl
│   ├── hooks/                    # React hooks wrapping Three.js
│   │   ├── useHeroScene.js
│   │   └── useParticles.js
│   └── utils/                   # WebGL helpers
│       ├── textureLoader.js
│       └── geometryHelpers.js
│
├── hooks/                        # Shared React hooks (non-graphics)
│   ├── useAnimation.js
│   ├── useResponsive.js
│   ├── useScrollProgress.js
│   └── useIntersectionObserver.js
│
├── styles/                       # Global styles and design tokens
│   ├── base/
│   │   ├── reset.css             # CSS reset / normalize
│   │   └── global.css            # Body, html defaults
│   ├── tokens/
│   │   ├── _colors.css           # --color-* tokens
│   │   ├── _spacing.css          # --space-* tokens
│   │   ├── _typography.css       # --text-* tokens
│   │   └── _breakpoints.css      # Breakpoint values
│   ├── responsive/               # 🔥 Global responsive layer
│   │   ├── breakpoints.css       # Breakpoint token definitions
│   │   ├── mobile.css            # Global mobile typography + spacing
│   │   └── tablet.css            # Global tablet typography + spacing
│   └── utilities/
│       ├── animations.css        # Shared @keyframes
│       └── helpers.css           # .visually-hidden, .sr-only, etc.
│
└── assets/                       # Static files
    ├── images/
    ├── videos/
    └── fonts/
```

---

## Key Boundaries (Visual Summary)

```
┌─────────────────────────────────────────────────────────┐
│                    src/                                  │
│                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────┐  │
│  │  ui/     │    │ modules/ │    │   graphics/      │  │
│  │ (visual) │    │(features)│    │ (WebGL/Three.js) │  │
│  └────┬─────┘    └────┬─────┘    └──────────────────┘  │
│       │               │                    ▲            │
│       │               │                    │            │
│       └───────────────┘                    │            │
│               │                            │            │
│               ▼                            │            │
│           hooks/ ───────────────────────── ┘            │
│           (abstraction boundary)                        │
│                                                         │
│  core/ ←── imported by ALL layers                       │
│  styles/ ←── imported by UI and layout only             │
│                                                         │
│  ⚠️  ui/ → graphics/ = ALWAYS A BUG                    │
└─────────────────────────────────────────────────────────┘
```

---

## Module `index.js` Pattern

```js
// src/modules/hero/index.js
// ✅ Export only what consumers need
export { HeroSection } from './ui/HeroSection';
export { useHeroData } from './logic/useHeroData';
// Do NOT export internal API functions or raw selectors
```

## Canvas Bridge Pattern (WebGL ↔ UI)

```jsx
// src/ui/components/GraphicsCanvas.jsx
// The ONLY UI component that touches WebGL — via hook only
import { useHeroScene } from '@hooks/useHeroScene'; // hook abstracts Three.js

export function GraphicsCanvas() {
  const canvasRef = useHeroScene(); // hook sets up Three.js internally
  return <canvas ref={canvasRef} className={styles.canvas} />;
}
```
