# Advanced Documentation Rules

For complex or enterprise-grade repositories, basic API routes are not enough. The engine must generate systemic overviews.

## 1. ARCHITECTURE.md
- **Purpose**: Explain the macro system decisions.
- **Includes**: The interaction between microservices, where state is managed (Redux/Zustand), and data flow lifecycles.
- **Format**: Must heavily feature a System Architecture Graph (See `diagrams-and-graphs.md`).

## 2. SECURITY.md
- **Purpose**: Outline the vulnerability prevention profile of the app.
- **Topics Required**:
  - Authentication (JWT, Session cookies).
  - Rate Limiting (Is `express-rate-limit` utilized?).
  - Data Sanitation (Are inputs validated via Zod/Joi?).
  - CSRF/XSS Protections deployed.

## 3. DEPLOYMENT.md & CONFIGURATION.md
- **Extraction**: Read `Dockerfile`, `docker-compose.yml`, or `.github/workflows`.
- **Output**: Give exact step-by-step instructions on compiling, building, and deploying the app.
- **Config**: Read `.env.example` and output a markdown table defining what every environment variable controls.
  ```markdown
  | Variable       | Purpose                               | Default |
  |----------------|---------------------------------------|---------|
  | `DATABASE_URL` | Postgres connection string            | None    |
  | `JWT_SECRET`   | Key for signing session tokens        | None    |
  ```

## 4. TESTING.md & PERFORMANCE.md
- Describe the Test Strategy (Unit via Jest, E2E via Cypress/Playwright).
- Note any specific mock files or environment configurations needed to run tests without altering production databases.
- Document any specific performance constraints (e.g., "Service X is heavily CPU bound by cryptographic hashing. Do not deploy to a micro-container.").
