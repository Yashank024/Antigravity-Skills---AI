# Pre-Deployment Security Checklist

## 1. Secrets & Credentials
- [ ] No hardcoded passwords or API keys in the source code.
- [ ] `.env` files are excluded from version control (`.gitignore`).
- [ ] Secrets are managed via a secure vault (e.g., AWS Secrets Manager, HashiCorp Vault, Azure Key Vault).

## 2. Dependencies
- [ ] Lockfiles (`package-lock.json`, `requirements.txt`, etc.) are present and used.
- [ ] Dependency versions are pinned.
- [ ] `npm audit`, `pip-audit`, or equivalent tools report no HIGH or CRITICAL findings.
- [ ] Unused or unnecessary packages are removed.

## 3. Configuration & Infrastructure
- [ ] Debug mode is disabled (`DEBUG=false`, etc.).
- [ ] Detailed error messages and stack traces are suppressed in production.
- [ ] Security HTTP headers (HSTS, CSP, X-Frame-Options) are configured.
- [ ] Default credentials (like admin/admin) for databases and third-party tools have been changed.

## 4. Encryption & Network
- [ ] TLS (HTTPS) is enforced for all external endpoints.
- [ ] Insecure protocols (HTTP, Telnet) are disabled.
- [ ] Databases and storage buckets are not publicly accessible (unless explicitly intended).
- [ ] Internal microservices communicate over encrypted channels.

## 5. Authentication & Session
- [ ] MFA required for admin access.
- [ ] Password hashes use modern algorithms (Argon2, bcrypt), not MD5/SHA1.
- [ ] Cookies are configured with `Secure` and `HttpOnly` flags.
- [ ] CSRF protections are active on all state-changing endpoints.
