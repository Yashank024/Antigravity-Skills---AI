---
name: optimizing-projects
description: Acts as an Autonomous AI Refactor Engine (Production Grade). Analyzes project dependency graphs, runs dry simulations, profiles performance, detects semantic usage, and applies impact analysis before executing optimizations.
---

# Optimizing Projects (Production Grade Autonomous Refactor Engine)

## Core Purpose & Rules
**Primary Goal**: Analyze an existing project and make it clean, stable, and highly performant.
- ❌ **DO NOT add new features.**
- ✅ **DO optimize the existing system.**
- 🛡️ **DO NOT rely solely on static syntax analysis.** Use semantic understanding and dependency graphs.
- ⚠️ **MANDATORY DRY RUN**: Never execute without running a dry simulation and outputting the impact analysis first.

## When to use this skill
- optimize
- optimization
- optimized
- optimize this project
- is project ko optimize karo
- optimize my code
- optimize project
- cleanup codebase
- remove unused files
- fix project structure
- refactor project
- reduce bundle size
- improve performance
- profile app speed
- scan dependencies for vulnerabilities
- suggest architecture improvements

## Production-Grade 10-Step Workflow
- [ ] **Step 1: Scan & Detect**: Scan directory structure. Detect the Tech Stack (React, Node, Next.js) and Multi-Environment rules (Dev vs Prod).
- [ ] **Step 2: Dependency Graphing**: Build the import graph. Detect circular dependencies (`A->B->C->A`).
- [ ] **Step 3: Semantic Analysis**: Run deep semantic code understanding. Ensure unused functions aren't called dynamically before marking as dead.
- [ ] **Step 4: Static & Security Analysis**: Hook into external tools (ESLint, TSC, Webpack analyzers). Run `npm audit` or `snyk` to map dependency vulnerabilities.
- [ ] **Step 5: Performance Profiling**: Profile execution speed (Lighthouse, Chrome DevTools Traces, Node profiler) to root-cause bottlenecks.
- [ ] **Step 6: Optimization Score (Early Exit Check)**: Calculate the Optimization Score. If `Score >= 90`, the project is already optimized. Generate the final report, remove unused files, and **EXIT SAFELY** without structural changes.
- [ ] **Step 7: Prioritized Optimization Plan**: Categorize all detected issues by Priority (Critical, High, Medium, Low). Include Change Impact Analysis. Check for AI Suggestion Mode.
- [ ] **Step 8: Dry Run Simulation**: Simulate the execution. Output the plan to the user and wait for explicit confirmation.
- [ ] **Step 9: Execute**: Create a git snapshot, then run the optimizations incrementally based on stack-specific rules.
- [ ] **Step 10: Final Report & Continuous Memory**: Generate the Optimization Report and update execution memory patterns.
- [ ] **Step 11: Cleanup Phase**: The agent MUST delete all temporary artifacts from the `.temp-optimization/` directory. NEVER delete project source files during this phase.

## Expert System Resources
- [Advanced Upgrades: CI/CD, Suggestions, Memory & Security](resources/advanced-upgrades.md)
- [Advanced Analysis: Dependency Graphs & Semantics](resources/advanced-analysis.md)
- [Performance Profiling & Priority System](resources/profiling-priority.md)
- [Execution Safeguards: Dry Runs & Impact Analysis](resources/execution-safeguards.md)
- [Stack Detection & Multi-Environment Logic](resources/stack-detection.md)
- [Cleanup Rules & Dead Code Analysis](resources/cleanup-rules.md)
- [Safety, Rollbacks & Confidence](resources/safety-rules.md)
- [Optimization Report Example](examples/optimization-report.md)
- [Analysis Script](scripts/analyze-project.js)
