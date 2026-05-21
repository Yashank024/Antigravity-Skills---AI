---
name: structuring-frontend-systems
description: Analyzes, restructures, and enforces architecture rules for frontend projects. Separates UI, business logic, and WebGL/Three.js concerns into clean feature-based folder structures. Applies design system tokens (spacing, typography, color). Use when asked to fix frontend structure, clean UI architecture, organize frontend code, restructure project, fix design system, separate WebGL from UI, or resolve circular imports.
---

# Frontend Architecture + Design System Engine

## ⚠️ GOLDEN RULE (NON-NEGOTIABLE)
> **DO NOT change any UI output.**
> **DO NOT break existing visuals.**
> **ONLY restructure code, fix imports, and enforce architecture.**

## When to Use This Skill
- `fix frontend structure` / `fix my project structure`
- `clean UI architecture` / `organize frontend code`
- `restructure project` / `fix design system`
- `separate WebGL from UI` / `fix circular imports`
- `apply design system` / `enforce spacing system`

---

## Workflow

### Phase 1 — Scan & Detect
- [ ] **Scan** the project file tree (list all files in `src/` or root)
- [ ] **Detect** current framework: React / Next.js / Vanilla HTML/JS
- [ ] **Identify** misplaced files: WebGL inside UI folders, logic inside components, etc.
- [ ] **Map** circular or deep import chains
- [ ] **Flag** inline styles, global CSS overrides, missing design tokens

### Phase 2 — Plan (Dry Run)
- [ ] **Create** a refactor plan mapping current paths → target paths
- [ ] **Simulate** all file moves (output a table: `CURRENT PATH → TARGET PATH`)
- [ ] **List** all import paths that need updating
- [ ] **Present the plan to the user and ask for approval before executing**

### Phase 3 — Execute (Only After Approval)
- [ ] **Backup** note: instruct user to commit/backup before execution
- [ ] Move files to correct folders following the Ideal Structure (see `examples/ideal-structure.md`)
- [ ] Fix all import paths after moves
- [ ] Remove conflicting or duplicate imports
- [ ] Apply design tokens where missing (see `resources/spacing-system.md`)
- [ ] Isolate WebGL/Three.js into `graphics/` (see `resources/architecture-rules.md`)

### Phase 3b — Responsive System Layer (Safe Mode)
- [ ] **Scan** all UI components — detect layout type (flex / grid / absolute) for each
- [ ] **Map** existing desktop spacing, typography, widths — record as baseline (DO NOT TOUCH)
- [ ] **Create** `styles/responsive/` folder with `breakpoints.css`, `mobile.css`, `tablet.css`
- [ ] **Generate** per-module `responsive.module.css` files (media queries ONLY — zero bare selectors)
- [ ] **Apply** layout transformations: row→column, grid→single column on mobile
- [ ] **Scale** spacing: 80px → 48px → 24px per breakpoint
- [ ] **Scale** typography: h1 48px → 36px → 28px; body 16px → 15px
- [ ] **Enforce** touch targets: `min-height: 44px` on all buttons/links on mobile
- [ ] **Add** `overflow-x: hidden` at root, `max-width: 100%` on all media elements
- [ ] **Verify** desktop CSS files were NOT modified (git diff check)

### Phase 4 — Validate
- [ ] Confirm UI components contain NO direct WebGL imports
- [ ] Confirm no circular dependencies exist
- [ ] Confirm all moved files have correct updated imports
- [ ] **Run** the project dev server and confirm no errors (`npm run dev`)

### Phase 5 — Report
- [ ] Output a markdown summary: files moved, imports fixed, issues resolved
- [ ] List any remaining issues that require manual intervention

---

## Instructions

### Separation of Concerns (STRICT)
* **UI Layer** → `src/ui/` — only visual, zero business logic, zero WebGL
* **Logic Layer** → `src/modules/[feature]/logic/` — state, API calls, transforms
* **Graphics Layer** → `src/graphics/` — ALL Three.js / WebGL / shader code
* **Hooks** → `src/hooks/` — shared React hooks only
* **Styles** → `src/styles/` — tokens, base resets, utility classes

### Import Rules (STRICT)
* UI components must NEVER import from `graphics/`
* Modules must NEVER import from sibling modules directly (use a shared `core/`)
* No import depth greater than 3 levels (`../../..` is the max)
* No barrel imports (`index.js`) that re-export from multiple unrelated folders

### Responsive Rules (STRICT)
* `desktop.module.css` is **read-only** during responsive work — never edit it
* `responsive.module.css` must contain **only** `@media` blocks — no bare selectors allowed
* **No** `!important` anywhere in responsive styles
* **No** inline `style={{}}` responsive logic — use CSS media queries exclusively
* **No** global class overrides — all responsive styles are scoped to their module

### Design System Enforcement
* Apply 4px spacing scale — see `resources/spacing-system.md`
* Apply typography scale — see `resources/design-rules.md`
* Replace ALL inline `style={{}}` with CSS module classes or design tokens
* Replace ALL hardcoded pixel values with spacing variables

### Safety System
* Always perform a **dry run** first (Phase 2) and show the plan
* Ask for explicit user approval before moving files
* Instruct user to `git commit` or take backup before Phase 3

---

## Resources

- [Design Rules](resources/design-rules.md) — Typography, color system, component rules
- [Architecture Rules](resources/architecture-rules.md) — Folder laws, import laws, feature isolation
- [Spacing System](resources/spacing-system.md) — 4px base scale, padding/margin standards
- [Refactor Rules](resources/refactor-rules.md) — File movement engine, import fixing, conflict removal
- [Responsive System](resources/responsive-system.md) — Breakpoints, safe layering, touch rules, conflict prevention
- [Ideal Structure Example](examples/ideal-structure.md) — Target folder tree
