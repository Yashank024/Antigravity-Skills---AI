# Core Documentation Standards

These are the primary texts generated for every project analyzed. All files must be placed strictly within the versioned `/docs/v<X>` directory (e.g., `/docs/v1`).

## 0. INDEX.md (Documentation Gateway)
- **Purpose**: A master navigation file mapping all created documentation files.
- **Example**:
  ```markdown
  # Documentation Index
  - 🏛️ [System Architecture](ARCHITECTURE.md)
  - 🔌 [API Reference](API_REFERENCE.md)
  - 🗄️ [Database Schema](DATABASE_SCHEMA.md)
  - 🛡️ [Security](SECURITY.md)
  ```

## 1. PROJECT_STRUCTURE.md
- **Extraction Rule**: Perform a recursive read of the primary source directory (e.g., `src/`, `lib/`).
- **Format Requirement**: Use clean text-based file trees.
- **Example**:
  ```text
  src/
   ├ components/     (Shared UI elements)
   ├ pages/          (Next.js route definitions)
   ├ services/       (API interaction abstractions)
   └ utils/          (Pure helper functions)
  ```

## 2. API_REFERENCE.md
- **Extraction Rule**: Scan for Express/NestJS/FastAPI route files. Extract endpoint URL, HTTP method, required payloads, and authorization requirements.
- **Example Generation Requirement**: EVERY endpoint must include actionable Code Examples (`cURL`, `JavaScript fetch`, `Python requests`).
- **Format Requirement**:
  ```markdown
  ### Create User
  - **Endpoint**: `/api/users`
  - **Method**: `POST`
  - **Auth Required**: `Bearer Token`
  - **Input Payload**: `{ email: string, password: string }`
  - **Response**: `200 OK - { token: JWT }`
  
  **Example Request (cURL):**
  \`\`\`bash
  curl -X POST https://api.domain.com/v1/users \
       -H "Content-Type: application/json" \
       -H "Authorization: Bearer <TOKEN>" \
       -d '{"email":"test@test.com","password":"pass"}'
  \`\`\`
  ```

## 3. DATABASE_SCHEMA.md
- **Extraction Rule**: Look for ORM configuration files (Prisma, TypeORM, Sequelize, Mongoose) or raw `.sql` migration files.
- **Format Rule**: Create markdown tables mapping out tables/collections.
  ```markdown
  ### `users` Table
  | Column | Type | Constraints | Description |
  |--------|------|-------------|-------------|
  | `id`   | UUID | Primary Key | Auto-gen UUID |
  | `email`| Var  | Unique      | User login |
  ```

## 4. CHANGELOG.md (Version History)
- **Extraction Rule**: Run `git log` to summarize recent significant milestones or major version deployments based on tags.

## 5. CONTRIBUTING.md
- Output standard contribution guidelines covering: Branch naming conventions (`feature/xyz`, `bugfix/xyz`), PR submission rules, and core coding standards enforcement (e.g., "Run `npm run lint` before committing").
