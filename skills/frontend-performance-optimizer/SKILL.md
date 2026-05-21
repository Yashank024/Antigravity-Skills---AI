---
name: frontend-performance-optimizer
description: Analyzes and improves frontend performance. Use when apps are slow, laggy, or the user requests performance audits and optimizations.
---

# Frontend Performance Optimizer

This skill focuses on delivering lightning-fast web experiences.

## Trigger Keywords

Activate this skill if the request mentions:
- laggy
- slow rendering
- performance optimization
- lazy loading
- optimize bundle size
- code splitting
- lighthouse score
- web vitals

## When to use

- The user complains about React rendering performance or "lag".
- Optimizing bundle sizes or Lighthouse scores.
- Implementing lazy loading or caching strategies.

## Optimization Workflow

1. **Render Optimization**: Identify unnecessary re-renders in React and suggest `React.memo`, `useMemo`, or `useCallback` where statistically significant.
2. **Code Splitting**: Suggest dynamic imports (`React.lazy`) for heavy components or routes.
3. **Asset Optimization**: Check for unoptimized images, uncompressed assets, or excessive third-party dependencies.
4. **Actionable Metrics**: Focus on optimizations that improve Core Web Vitals (LCP, FID, CLS).
