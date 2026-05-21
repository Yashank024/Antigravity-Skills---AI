---
name: building-backends
description: Assists with designing and implementing backend systems for web projects. Use this skill when creating server-side logic, setting up REST/GraphQL APIs, designing databases, configuring authentication, or integrating with frontends across Node.js, Python, or serverless stacks.
---
# Building Backends Skill

This skill helps the agent generate or improve backend code and architecture for web applications.

## When to use this skill
- Creating a new backend (server-side) for a web or mobile app
- Setting up RESTful or GraphQL API endpoints
- Designing or updating database schemas (SQL or NoSQL)
- Implementing user authentication/authorization (login, JWT, OAuth)
- Connecting a frontend (React, Next.js, etc.) to server APIs
- Refactoring backend architecture for better modularity or performance
- Migrating a monolith to microservices or serverless functions

## Workflow
- **Plan Architecture:** Identify components (API layer, business logic, DB, cache). Decide on monolith vs microservices vs serverless. Sketch out required endpoints and data models.
- **Define Data Models:** Map out the database schema or collections for all data entities (users, products, orders, etc.).
- **Design API:** List API routes and HTTP methods. Use noun-based URIs and standard status codes. Plan input/output formats (JSON).
- **Setup Project Structure:** Create folders by feature/domain, following a layered pattern (controllers/entry-points, domain/services, data-access/models).
- **Implement Core Logic:** Write controllers or route handlers for each endpoint. In each handler, call service/business logic functions and database models.
- **Add Security:** Implement authentication (e.g. JWT login endpoint) and authorization (check user roles). Hash passwords and validate tokens on protected routes.
- **Integrate with Frontend:** Enable CORS or use same-origin. For Next.js or similar, use built-in API routes to proxy or serve data.
- **Test & Validate:** Write tests for endpoints, edge cases, and database queries. Perform integration tests by simulating frontend requests.
- **Optimize & Document:** Add caching where needed. Ensure API documentation (Swagger/OpenAPI) is updated. Prepare deployment (CI/CD pipeline, Docker containers, environment configs).

## Instructions
- Use this skill to automatically scaffold or review a backend setup.
- Encourage the agent to run any provided helper scripts (e.g. `scripts/setup-backend.sh`) with `--help` to understand options before execution.
- Focus on clean code: separate concerns, use modern language features (async/await, TypeScript generics), and include comments for complex logic.
- Follow language-specific conventions (e.g. `npm` scripts and `package.json` for Node; `requirements.txt` or `Pipenv` for Python).
- When integrating with frontends, remember to handle CORS and consistent data formats.
- Include validation at each step: the agent should verify its plan against requirements and check for missing pieces.

## Resources
- `scripts/` – Utility scripts (e.g. project initialization, database migration).
- `examples/` – Sample implementations (e.g. `express-endpoint.js`, `flask-endpoint.py`).
- `resources/` – Templates or snippets (e.g. `schema.sql`, `auth-jwt-example.js`).
- Documentation templates (e.g. sample OpenAPI spec) may be included under `resources/`.
