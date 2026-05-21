# Performance Profiling & Optimization Priority System

Not all optimizations are created equal. The engine must actively profile and prioritize.

## 1. Performance Profiler Integration
Optimization without profiling is guesswork. Instruct the user to run, or internally execute (if capable), the following tools:
- **Frontend/Web**: Run Lighthouse audits (targeting Performance category). Run Webpack Bundle Analyzer or Vite's rollup-plugin-visualizer to find exactly which modules bloat the bundle. Use Chrome DevTools Trace for render blocking.
- **Backend (Node.js)**: Use `--prof` or `--cpu-prof` flags to generate V8 execution traces. Detect heavy event loop blocking.
- **Action**: Target the 20% of code causing 80% of the slowdown (Pareto Principle).

## 2. Optimization Priority System
Assign every detected issue one of the following priority levels before presenting the plan:

| Priority | Definition | Examples |
|----------|------------|----------|
| **Critical** | Actively harms stability, causes memory leaks, or crashes the app. | Unbounded event listeners, infinite `useEffect` loops, circular dependencies, N+1 DB queries on high-traffic routes. |
| **High** | Severely degrades UX or drastically inflates bundle size. | Unused heavy libraries (e.g., Lodash full import), synchronous blocking operations, missing database indexes on core tables. |
| **Medium** | Measurable architecture flaws, dead code, logic duplication. | Unused components, overlapping API calls, duplicate CSS files, orphan static assets. |
| **Low** | Minor cleanups that do not impact app execution speed. | Extraneous comments, unused tiny utility functions, unoptimized small images. |
