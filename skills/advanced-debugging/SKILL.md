---
name: advanced-debugging
description: A unified expert system for debugging, root cause analysis, code review, and performance optimizations. Employs systematic hypothesis testing and strictly reviews all code against modern best practices before providing fixes.
---

# Advanced Debugging & Code Review

This skill combines systematic debugging methodologies with rigorous code review. It prevents "guess and check" programming, identifies root causes, and ensures that any resulting code merges cleanly without introducing performance, security, or maintainability regressions.

## Trigger Keywords

Activate this skill if the request mentions any of the following:
- debug
- error
- find error
- fix bug
- traceback
- exception
- crash
- root cause
- console.error
- memory leak
- infinite loop
- unexpected behavior
- code review
- check code
- review pr
- find bugs
- code quality
- refactor code
- review changes
- is this code safe
- why is this breaking

## 1. Deep Intelligence Debugging Workflow

Follow this rigorous, deep-dive methodology for every debugging request. You must not skip straight to the solution.

1. **Global Context & Log Analysis (The Sweeper)**
   - Analyze all provided console logs, error logs, and DevTools outputs.
   - Scan the broader project context. Check for conflicting code, duplicated logic, or architectural mismatches that might be silently triggering the error.
2. **Deep Syntax Inspection (Micro-Level)**
   - Go extremely deep into the code at a character-by-character level. Check for microscopic errors (missing dots, typos, scoping issues, incorrect generic types).
3. **Isolate (Minimal Reproduction)**
   - Strip away unrelated code until you have the exact trigger condition isolated.
4. **Hypothesize (Root Cause Analysis)**
   - Form a clear hypothesis based on the log patterns and micro-inspection.
5. **Generate the Intelligence Chart (Report)**
   - Before attempting any code changes, output a structured **Intelligence Chart** to the user.
   - The chart must include:
      - **Error Pattern Detected**: (e.g., Infinite Render, Outdated Closure)
      - **Global Conflicts**: (e.g., File A overrides File B)
      - **Root Cause (Precise)**: (The exact line/character causing the breakdown)
6. **Provide the Solution (The Fix)**
   - Once the Intelligence Chart is accepted, provide the exact code solution and explain why it resolves the root cause.
7. **Verify (Validation & Code Review Loop)**
   - Run the new fix through the **Structured Review Checklist** below to ensure it doesn't introduce performance regressions or security holes.

## 2. Structured Code Review Checklist

Whether reviewing a user's PR or outputting your own fix, always pass the code through this checklist:

### 1. Correctness & Edge Cases
- [ ] Does the code actually solve the intended problem?
- [ ] Are null, undefined, and empty array states handled gracefully?
- [ ] Are errors explicitly caught (`try/catch`) and logged?

### 2. Security 🔒
- [ ] **XSS**: Is user input dangerously injected without sanitization?
- [ ] **Auth**: Are sensitive tokens or IDs exposed in client-side code?
- [ ] **Injection**: Are queries concatenated dynamically instead of natively sanitized?

### 3. Maintainability (Clean Code) 🧹
- [ ] **Naming**: Are variables/functions distinct and explicitly named?
- [ ] **Complexity**: Is logic separated effectively, or should helpers be extracted?
- [ ] **DRY**: Can duplicated code be abstracted cleanly?

### 4. Performance ⚡
- [ ] Are heavyweight operations accidentally blocking the UI thread?
- [ ] **React Specific**: Is state held too high? Are stable references unoptimized (`useMemo`/`useCallback` needed)? Check for `useEffect` thrashing.

## Feedback Guidelines (Reviewing User Code)
- Provide feedback clearly and politely.
- Tag severity explicitly:
   - 🚨 **CRITICAL**: Bugs, security holes, infinite loops.
   - ⚠️ **WARNING**: Performance issues, unhandled edge cases.
   - 💡 **NITPICK**: Stylistic preferences, variable naming.
- For all issues, explain *why* it is problematic and provide a concrete code snippet demonstrating the *ideal alternative*.
