# Refactor Rules — File Movement + Import Fixing Engine

## Phase 1 — Scan & Classify

For every file in `src/`, classify it:

| File Type | Detected By | Target Location |
|-----------|-------------|-----------------|
| Three.js / WebGL scene | imports `three`, uses `Scene`, `Camera`, `Renderer` | `src/graphics/scenes/` |
| GLSL shader | `.glsl`, `.vert`, `.frag` extension | `src/graphics/shaders/` |
| Graphics hook | `useThree`, `useFrame`, `useWebGL` in name | `src/graphics/hooks/` |
| Pure UI component | JSX returning HTML, no API calls, no state stores | `src/ui/components/` |
| Layout component | `Navbar`, `Footer`, `Container`, `Sidebar` in name | `src/layout/` |
| Feature UI | used exclusively in one feature | `src/modules/[feature]/ui/` |
| Feature logic | API calls, state, data transforms for one feature | `src/modules/[feature]/logic/` |
| Feature styles | CSS module used only in one feature | `src/modules/[feature]/styles/` |
| Shared hook | `use*` hook used in 2+ features | `src/hooks/` |
| Graphics hook (React) | wraps Three.js, returns refs/canvases | `src/hooks/` if shared, `src/graphics/hooks/` if isolated |
| Config / env | `config`, `env`, `settings` | `src/core/config/` |
| Constants / enums | `ROUTES`, `KEYS`, `ENUM` | `src/core/constants/` |
| Pure utility function | no JSX, no side effects | `src/core/utils/` |
| Design tokens CSS | `--color-*`, `--space-*`, `--text-*` | `src/styles/tokens/` |
| Base / reset CSS | `*, body, html` selectors | `src/styles/base/` |

---

## Phase 2 — Dry Run Output Format

Before any file moves, output a table like:

```
REFACTOR PLAN (DRY RUN)
══════════════════════════════════════════════════════
ACTION      CURRENT PATH                          TARGET PATH
──────────────────────────────────────────────────────
MOVE        src/components/HeroScene.jsx           src/graphics/scenes/HeroScene.jsx
MOVE        src/components/Navbar.jsx              src/layout/Navbar.jsx
MOVE        src/utils/formatDate.js                src/core/utils/formatDate.js
FIX IMPORT  src/pages/Home.jsx:3                  '../graphics/scenes/HeroScene' → '@graphics/scenes/HeroScene'
DELETE      src/components/temp_backup.jsx         (remove unused file)
══════════════════════════════════════════════════════
Total: 3 moves, 1 import fix, 1 delete
```

**Wait for user approval before executing.**

---

## Phase 3 — Import Fixing Rules

After moving files, update ALL import paths:

### Rule: Use Path Aliases
```js
// ❌ BEFORE (relative, brittle)
import { Button } from '../../ui/components/Button';

// ✅ AFTER (alias, stable)
import { Button } from '@ui/components/Button';
```

### Rule: Module Public API Only
```js
// ❌ BEFORE (deep import)
import { useHeroData } from '../modules/hero/logic/useHeroData';

// ✅ AFTER (via index.js)
import { useHeroData } from '@modules/hero';
```

### Rule: Remove WebGL from UI
```jsx
// ❌ BEFORE — UI component importing WebGL
import { createParticleSystem } from '../utils/particles'; // three.js code

// ✅ AFTER — UI uses hook only
import { useParticleScene } from '@hooks/useParticleScene';
```

### Automated Import Scan

Use this command to find all broken imports after moves:
```bash
npx tsc --noEmit
# or for JS projects:
npx eslint src/ --rule '{"import/no-unresolved": "error"}'
```

---

## Phase 4 — Conflict Resolution

### Duplicate File Detection
If two files have identical/near-identical content:
1. Keep the one in the correct target location
2. Delete the other
3. Update all references to point to the kept file

### Conflicting CSS Classes
If two CSS files define the same class name with different values:
1. Determine which is the "truth" definition (closest to design tokens)
2. Remove the other
3. Reference only the design token variable

### Barrel Index Conflicts
If an `index.js` re-exports from unrelated modules, split it:
```js
// ❌ BEFORE — messy barrel
export { Button } from './Button';
export { HeroScene } from './HeroScene'; // WebGL should NOT be here
export { formatDate } from './formatDate';

// ✅ AFTER — each in correct location
// src/ui/components/index.js
export { Button } from './Button';

// src/graphics/scenes/index.js
export { HeroScene } from './HeroScene';

// src/core/utils/index.js
export { formatDate } from './formatDate';
```

---

## Phase 5 — Safety Checklist

Before marking any phase complete, confirm:

- [ ] All moved files still have their original content (no corruption)
- [ ] No import points to a path that no longer exists
- [ ] `npm run dev` starts without import errors
- [ ] Visual output matches pre-refactor (NO UI changes)
- [ ] No circular dependencies: `npx madge --circular src/`
- [ ] All CSS modules are correctly scoped (no leaked globals)
