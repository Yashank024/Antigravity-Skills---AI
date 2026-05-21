---
name: generating-project-docs
description: Acts as an AI Documentation Intelligence Engine. Automatically scans projects, detects tech stacks, builds dependency graphs, and generates a fully structured `docs/` folder with architecture diagrams, API references, security rules, and a clean root README.
---

# Generating Project Docs (Documentation Intelligence Engine)

## Core Purpose & Rules
**Primary Goal**: Analyze an existing undocumented or poorly documented project and automatically generate professional, deeply structured documentation.
- ❌ **DO NOT clutter the root.** Only the `README.md` goes in the root.
- ✅ **DO create a dedicated `docs/` directory.** All detailed markdown files belong here.
- ✅ **DO generate visual graphs.** Automatically map dependencies and architectures using Mermaid.js syntax.

## When to use this skill
- readme
- create readme
- update readme
- md
- .md
- md file
- txt
- document
- documentation
- project documentation
- generate documentation
- format markdown
- document project
- generate architecture docs
- auto-document codebase
- create API docs
- generate Swagger / OpenAPI schemas
- check documentation coverage

## Engine Workflow
- [ ] **Step 1: Scan & Version Check**: Detect project stack, current app version (e.g., v1), and target the `docs/v1/` output folder (Version Awareness).
- [ ] **Step 2: Schema & Metadata Extraction**: Pull REST routes, Swagger/OpenAPI files, GraphQL schemas, database models, and JSDoc blocks.
- [ ] **Step 3: Build Graph**: Map module relationships (e.g., `UserModule -> Auth -> DB`).
- [ ] **Step 4: Generate Diagrams**: Convert the dependency map into Mermaid/PlantUML syntax.
- [ ] **Step 5: Coverage Check**: Run a documentation coverage check. Log missing docstrings or undocumented API endpoints. 
- [ ] **Step 6: Generate Core Files**: Output `INDEX.md`, `API_REFERENCE.md` (with cURL examples), and `PROJECT_STRUCTURE.md` into `/docs/v1/`. Update root `README.md`.
- [ ] **Step 7: Generate Advanced Files**: Output `ARCHITECTURE.md`, `API_SCHEMA.md` (if Swagger/GQL detected), `SECURITY.md`, etc.
- [ ] **Step 8: Markdown Validation**: Run a linter pass. Ensure all cross-links work, headings are correct, and code blocks have syntax highlighting.
- [ ] **Step 9: Output Search Index**: Generate `docs/v1/search-index.json` to map all keywords and anchor tags for fast UI searching.
- [ ] **Step 10: CI/CD & Preview Hook**: Output instructions for the CI pipeline documentation coverage check (`Fail PR if docs < 80% coverage`), and offer to spin up a live preview doc server.

## Deep Dive Resources
The agent must follow the rigid templates and design rules defined in these resources:
- [Advanced Upgrades: Coverage, Schema & Versions](resources/advanced-docs-upgrades.md)
- [Core Documentation Standards](resources/core-docs-rules.md)
- [Advanced Documentation Rules](resources/advanced-docs-rules.md)
- [Diagrams & Graphs (Mermaid)](resources/diagrams-and-graphs.md)
- [Root README Template Example](examples/root-readme-template.md)
- [Execution Script](scripts/generate-docs.js)
