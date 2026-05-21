# Execution Safeguards

Before modifying the AST or touching the disk, the engine must protect the codebase through rigorous simulation.

## 1. Dry Run Mode
Autonomous execution without review is prohibited.
- **Requirement**: The agent must simulate the entire optimization pass in memory.
- **Output**: Present the **Prioritized Optimization Plan** to the user in a readable format.
- **Wait State**: The agent MUST explicitly ask: *"Review the Dry Run report. Reply 'Yes' or 'Execute' to begin physical file modifications."*

## 2. Change Impact Analysis
During the Dry Run, the engine must predict the collateral damage of every deletion or refactor.
- **Prediction Logic**: "If I delete `components/HeaderOld.jsx`, how many imports break?"
- **If Count > 0**: Do not propose deletion under any circumstances. Propose refactoring the calling imports first.
- **Format**: Feature the Impact Analysis prominently next to every proposed change in the dry run report (e.g., `Delete api/legacy.js [Impact: 0 local imports severed]`).

## 3. Multi-Environment Awareness
Optimization rules change drastically depending on the environment context (`development` vs `production`).
- **Production Build Awareness**: Do not strip `console.log` or debug statements blindly from the source if they are meant for local dev. Implement Babel/Webpack plugins (`terser-webpack-plugin` with `drop_console: true`) to strip them *only* at build time.
## 4. Optimization State Detection & Scoring
Before applying any optimization, the agent MUST determine whether the project is already optimized.
The engine must calculate an **Optimization Score (0-100)**:
- **90-100**: Already Optimized.
- **70-89**: Minor improvements required.
- **0-69**: Major optimization needed.

Indicators of an already optimized project:
- Minimal unused dependencies.
- No circular dependencies or dead code.
- A strong, logical file structure (`src/services/`, `src/routes/`, `src/utils/`).

**Over-Optimization Protection**:
- If the Score is `≥ 90`, the agent MUST NOT apply structural or code modifications.
- The engine must avoid over-optimization. If no measurable improvement is possible, it must stop.
- **Action**: Generate a report, clean up minor unused files, and exit safely. Do not force-merge modules if the architecture is already modular.

## 5. Temporary Artifact Cleanup Phase
Optimization skills generate heavy analysis artifacts (profiling logs, AST trees, bundle stats). The agent MUST remove all temporary files created during analysis before finishing execution.

- **Dedicated Sandbox**: NEVER generate temp files randomly in the root. Always write them to `.temp-optimization/` (e.g., `.temp-optimization/dependency-graph.json`).
- **Safety Condition**: ONLY delete files inside `.temp-optimization/` during this phase.
- **Rule**: NEVER mistake project source files for temporary artifacts.
- **Report Log**: Output a log in the final Optimization Report confirming the cleanup (e.g., "Removed temp artifacts from .temp-optimization/").
