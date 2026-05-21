# Architecture Rules — Frontend Architecture Engine

## 1. The Three-Layer Law

Every file must belong to exactly ONE layer:

| Layer | Location | Allowed Imports | Forbidden Imports |
|-------|----------|-----------------|-------------------|
| **UI** | `src/ui/`, `src/layout/` | hooks, styles, core/utils | `graphics/`, API calls, state stores |
| **Logic** | `src/modules/[feature]/logic/` | core, hooks, external libs | other modules directly |
| **Graphics** | `src/graphics/` | Three.js, WebGL libs, own hooks | `ui/`, `modules/` |
| **Responsive** | `src/styles/responsive/`, `src/modules/[f]/styles/responsive.module.css` | `@media` only | desktop files — **immutable** |

> **Rule:** An arrow from UI → Graphics is ALWAYS a bug. Fix it immediately.

---

## 2. Feature-Based Module Structure

Each feature is fully self-contained:

```
src/modules/[feature-name]/
├── ui/              # Feature-specific UI components
│   └── FeatureCard.jsx
├── logic/           # State, API, transforms
│   ├── useFeatureData.js
│   └── featureApi.js
├── styles/          # Feature-scoped CSS modules
│   └── feature.module.css
└── index.js         # Public API — only export what's needed
```

**Rules:**
- Module `index.js` is the ONLY entry point. Consumers import from `modules/hero`, not `modules/hero/logic/useHeroData`
- No module imports from another module's internal files
- Shared utilities go to `core/utils/`, not inside a module

---

## 3. WebGL / Three.js Isolation Rules

```
src/graphics/
├── scenes/          # Three.js scene setups
│   └── HeroScene.js
├── shaders/         # GLSL shader files
│   └── particleVert.glsl
│   └── particleFrag.glsl
├── hooks/           # React hooks that wrap Three.js
│   └── useThreeScene.js
└── utils/           # WebGL math, loaders, helpers
    └── textureLoader.js
```

**Isolation Laws:**
- `graphics/` files may ONLY be consumed via hooks (`useThreeScene`, `useParticles`, etc.)
- React components use the HOOK, not the raw Three.js scene:

```jsx
// ❌ FORBIDDEN — direct import of graphics in UI
import { HeroScene } from '../graphics/scenes/HeroScene';

// ✅ CORRECT — via abstracted hook
import { useHeroScene } from '../hooks/useHeroScene';
```

- The canvas element lives in a dedicated `<GraphicsCanvas />` component inside `ui/` that receives refs from hooks — it contains NO scene logic

---

## 4. `core/` — System-Level Utilities

```
src/core/
├── config/          # App-wide config (env vars, feature flags)
│   └── app.config.js
├── constants/       # Shared constants (routes, keys, enums)
│   └── routes.js
└── utils/           # Pure functions (format, parse, validate)
    └── formatDate.js
```

**Rules:**
- `core/` has ZERO React-specific code (no JSX, no hooks)
- `core/` can be imported by any layer
- `core/utils/` functions must be pure (no side effects)

---

## 5. Import Depth Rules

```
// ❌ FORBIDDEN — too deep, brittle
import { fn } from '../../../modules/hero/logic/helpers/transform';

// ✅ CORRECT — via module public API
import { fn } from 'modules/hero';

// ✅ CORRECT — via path alias
import { fn } from '@modules/hero';
```

**Configure path aliases in `vite.config.js` or `tsconfig.json`:**

```js
// vite.config.js
resolve: {
  alias: {
    '@ui':       '/src/ui',
    '@modules':  '/src/modules',
    '@graphics': '/src/graphics',
    '@hooks':    '/src/hooks',
    '@core':     '/src/core',
    '@styles':   '/src/styles',
  }
}
```

---

## 6. Circular Dependency Detection

Run this check after every refactor:

```bash
npx madge --circular src/
```

If circular dependencies are found:
1. Identify the cycle: `A → B → C → A`
2. Extract the shared piece into `core/` or a new shared module
3. Re-run to confirm resolution

---

## 7. `app/` — Entry Points Only

```
src/app/
├── App.jsx          # Root component, provider wrappers
└── routes.jsx       # All route definitions (React Router / Next.js pages)
```

- `App.jsx` only wraps providers and renders `<RouterProvider />`
- `routes.jsx` only maps paths to page-level components
- NO business logic in `app/`
