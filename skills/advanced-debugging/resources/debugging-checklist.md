# Debugging Checklist

Before declaring a bug "fixed", ensure you have completed this checklist:

## 1. Understanding & Isolation
- [ ] Is the bug consistently reproducible?
- [ ] Has the bug been isolated to a minimal reproducible example?
- [ ] Is the exact error message and stack trace understood?

## 2. Root Cause Analysis
- [ ] Was a specific hypothesis formulated?
- [ ] Was the hypothesis proven correct using logging, debugging, or tests?
- [ ] Did you avoid applying random fixes without understanding the underlying cause?

## 3. Implementation
- [ ] Does the fix directly address the root cause?
- [ ] Is the fix clean and maintainable?

## 4. Verification & Cleanup
- [ ] Has the issue been verified as resolved in the isolated environment?
- [ ] Have potential edge cases related to the fix been considered?
- [ ] Have all temporary `console.log` statements, `debugger` statements, or commented-out code been removed?
- [ ] (If applicable) Were tests added or updated to prevent this bug from recurring?
