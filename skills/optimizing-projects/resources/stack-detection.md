# Tech Stack Detection & Static Analysis

Different technology stacks require fundamentally different optimization strategies. The agent must profile the codebase first and route its logic through a Decision Tree.

## 1. Decision Tree: Project Scale
- **Small Project (< 20 files)**: Perform Basic Cleanup. Fast linting, direct unused file deletion.
- **Large Project (> 200 files)**: Perform Deep Analysis. Map dependency graphs, check for circular dependencies, rely entirely on AST/compiler signals.

## 2. Tech Stack Detection & Actions
Read `package.json` to detect the primary stack, then traverse the decision tree:

| Detected Stack | Action Plan (Target Optimizations) |
|----------------|------------------------------------|
| **React** | Apply Render Optimization (memoization, `useCallback`, `useMemo`). Reduce unnecessary re-renders. Check for heavy `useEffect` blocks. |
| **Next.js** | Enforce Code Splitting. Hunt for heavy client-side bundles. Replace massive generic imports with specific ones to reduce bundle size. Ensure lazy loading for heavy chart/3D components. |
| **Node.js (Backend)** | Async Optimization. Replace blocking synchronous functions with Promises. Consolidate database calls, batch queries (destroy N+1 queries). Add caching. |
| **Three.js / WebGL** | Asset Generation / Render Optimization. Apply **Frustum Culling** (disable off-screen rendering), Object Pooling (stop destroying/re-creating particles), and Level of Detail (LOD) swaps. |

## 3. Static Analysis Integration
Do not guess. The optimization engine is only as good as the tools it uses. Always leverage available CLI tools:
- **ESLint**: Run `eslint . --ignore-pattern node_modules` looking specifically for unused variables, imports, and expressions.
- **TypeScript (TSC)**: Look for dead code identified by the compiler.
- **Webpack/Vite Analyzer**: If available, generate a bundle report to find the heaviest node_modules taking up space.
- **Dependency Graph Analysis**: Check the import graph. If A imports B and B imports A (Circular Dependency), manually intervene and refactor into C.
