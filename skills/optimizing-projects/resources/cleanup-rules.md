# Project Cleanup Rules

## 1. Dead Code Detection
Systematically hunt for and remove:
- Unused functions and classes.
- Unused `import` statements (e.g., `import axios from "axios"` when axios is never called).
- Unused variables that clutter scope.
- Unused components.

## 2. Unused Files Removal
Look for orphan files in the directory tree:
- Unused images and static assets.
- Duplicate assets (e.g., identical icons with different names).
- Old/Deprecated components (e.g., if `header-old.jsx` and `header.jsx` both exist, delete the unused `header-old.jsx`).

## 3. File Structure Optimization
Modularize flat and confusing architectures.
- Bad: Mixed domain files (`api.js`, `auth.js`, `userApi.js`).
- Good: Nested modular domains:
  ```
  api/
    authApi.js
    userApi.js
  ```

## 4. Code Consolidation
Do not use 3 files for 1 logical outcome if they share exact responsibilities.
- Example: `validate.js`, `validateUser.js`, `validateEmail.js` → Combine into a single `validation.js` utility file.
- **Rule**: Only combine if it is logically correct and improves long-term maintainability.

## 5. Conflict & Dependency Cleanup
- **Duplicate Routes/Calls**: If a frontend uses both `axios baseURL` and `fetch baseURL` to hit the same endpoint, unify them to use a single method.
- **Dependency Graph**: Detect circular dependencies (`A imports B`, `B imports A`) and refactor to extract shared logic into `C`.
- **Package.json**: Eliminate duplicate tools (`axios` + `node-fetch`). If one is already heavily used, standardize on it and remove the other.

## 6. Image & Static Asset Optimization
- Detect and compress excessively large images.
- Remove images no longer referenced in the codebase.
