# Code Review Security Checklist

## 1. Input Validation & Data Handling
- [ ] All input from the client (body, query params, headers) is validated against a strict schema (e.g., Zod, Pydantic).
- [ ] User-supplied data is properly escaped before being rendered in the UI (to prevent XSS).
- [ ] SQL queries use parameterized queries, prepared statements, or an ORM. No raw string interpolation (`f"{user_input}"`).
- [ ] Path traversal vectors are mitigated (e.g., validating file paths if reading/writing files based on user input).

## 2. Authentication & Authorization
- [ ] Endpoint access control is explicitly defined (no endpoints accidentally left public).
- [ ] The user's identity is verified server-side via trusted tokens (e.g., JWT) or sessions.
- [ ] Rate limits are applied to sensitive endpoints (login, password reset).
- [ ] Password resets invalidate existing sessions/tokens.
- [ ] Authorization checks prevent IDOR (Insecure Direct Object Reference). E.g., `user.id == requested_resource.owner_id`.

## 3. Cryptography & Secrets
- [ ] Cryptographic material (keys, nonces) is generated securely (`crypto.randomBytes`, `os.urandom`).
- [ ] Passwords and sensitive PII are hashed or encrypted before storage.
- [ ] Application does not log sensitive data (passwords, session IDs, credit card numbers).

## 4. Business Logic & Error Handling
- [ ] Errors fail securely (a failed open check should result in closed/denied access).
- [ ] Transactions are used to prevent race conditions in financial or state-critical operations.
- [ ] Business limits are enforced (e.g., maximum order quantities, string length bounds).
