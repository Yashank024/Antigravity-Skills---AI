# Safety & Confidence Systems

Optimization is dangerous. Without extreme caution, you will break the user's working codebase. You **must** adhere strictly to these systems before altering any code.

## 1. The Safety System (Backups)
Before deleting ANY files or making wide-ranging module changes:
- **Rule**: Create a snapshot of the project.
- **Action**: Check if git is initialized. If yes, create a new branch: `git checkout -b optimize-cleanup-pass`. Commit all current working states.
- **Action**: If git is not present, physically copy the working directory folder to a timestamped backup folder: `cp -r project-folder project-folder-backup`.

## 2. The Rollback Mechanism
If post-optimization validation fails (e.g., `npm run build` crashes, or tests fail):
- **Rule**: The agent must trigger a rollback instantly.
- **Action**: Switch back to the master branch or restore from the copied backup folder. Inform the user of exactly which optimization step caused the break.

## 3. The Confidence Scoring System
Assign a confidence score internally before proposing an optimization.

| Confidence Level | Criteria | Required Action |
|------------------|----------|-----------------|
| **95-100% (High)** | ESLint/TS unequivocally marks as unused. File is entirely disconnected from entry points. Orphan component. | **Safe to Delete** automatically. |
| **70-94% (Med)** | Logic appears duplicated across files, but edge-case exports exist. | **Propose Consolidation**, request explicit user approval. |
| **0-69% (Low)** | Code seems unnecessary, but it uses dynamic imports, global window objects, or reflective metaprogramming. | **Mark for Review**. Do NOT delete. Add `// TODO(optimize): check if needed`. |
