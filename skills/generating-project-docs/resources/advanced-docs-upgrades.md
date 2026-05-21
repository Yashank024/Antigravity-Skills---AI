# Advanced Documentation Upgrades (Production Level)

The AI Documentation Intelligence Engine must enforce enterprise-grade standards by applying validation routines and strict version control to its generated outputs.

## 1. Version Awareness Hierarchy
Documentation must not exist in a flat structure over time.
- **Rule**: Scan `package.json` to extract the current project version.
- **Action**: All generated detailed documentation must be written into a versioned subdirectory (e.g., `docs/v1/`, `docs/v2/`).
- **Index Linking**: The root `README.md` must link specifically to the active version's `INDEX.md`.

## 2. API Schema Detection
Static JSON/Markdown parsing of API routes is rudimentary. The agent must seek existing centralized schema definitions.
- **Tools**: Search for `swagger.json`, `openapi.yaml`, or GraphQL `.graphql` schema files.
- **Output**: If found, generate a dedicated `API_SCHEMA.md`. Convert the raw schema into readable tables representing Queries, Mutations, or REST Payloads. Do not just blindly copy the JSON.

## 3. Documentation Coverage Check
Before finalizing the documentation run, the engine must grade the codebase it just analyzed.
- **Rule**: Scan for all exported public functions, classes, and controller execution routes. Check if a JSDoc, Docstring, or standard comment exists above it.
- **Output**: Inject a **Coverage Report** block at the beginning of the `INDEX.md` or `README.md`.
  - *Example*: `[WARNING]: 3 routes in users.controller.js are completely undocumented. 85% overall API code coverage.`

## 4. Search Indexing (Optional/Advanced)
If dealing with massive repositories (> 20+ large `.md` files):
- Generate a `docs/search-index.json`.
- This file should map Heading IDs and keywords to exactly which Markdown file contains them, allowing frontend developers to quickly wire up a search bar for the docs.
