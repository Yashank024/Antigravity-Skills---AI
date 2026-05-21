# API Security Checklist

## 1. Authentication & Authorization
- [ ] Every API endpoint (except health/public routes) requires authentication.
- [ ] Implementing standard mechanisms (OAuth2, well-configured JWTs).
- [ ] JWTs use RS256 (asymmetric) instead of HS256 for inter-service communication.
- [ ] The `alg` header in JWTs is explicitly verified and `none` is rejected.
- [ ] APIs use Role-Based Access Control (RBAC) or Attribute-Based (ABAC).
- [ ] Prevent BOLA/IDOR by ensuring the authenticated user actually owns the requested resource ID.

## 2. Rate Limiting & DoS Prevention
- [ ] Global rate limiting is implemented (e.g., 100 req/min per IP).
- [ ] Specialized rate limits are applied to auth routes (e.g., 5 login attempts/15 min).
- [ ] Payload size limits are enforced (e.g., reject bodies > 2MB).
- [ ] Pagination limits are hardcapped (e.g., `limit` cannot exceed 100).

## 3. Data Exposure & Integrity
- [ ] API responses do not leak internal stack traces or database errors.
- [ ] Mass assignment is prevented (e.g., only explicitly allowed fields can be updated via PUT/PATCH).
- [ ] Sensitive fields (like password hashes) are stripped from JSON responses before serialization.
- [ ] `Content-Type` headers are strictly checked (e.g., reject `application/json` if it actually contains XML/XXE payloads).

## 4. Operations & Monitoring
- [ ] Rate limit triggers and authorization failures are logged.
- [ ] CORS is explicitly configured with a strict whitelist (`Access-Control-Allow-Origin` is not `*` for authenticated routes).
- [ ] All endpoints are served over HTTPS exclusively.
