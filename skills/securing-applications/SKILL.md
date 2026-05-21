---
name: securing-applications
description: Provides 360° security auditing, vulnerability detection, and secure implementation across all major languages and frameworks. Uses the CVSS framework for impact assessment.
---

# Securing Applications

## When to use this skill
- security
- add security
- add security in this application
- secure
- secure this website
- secure this app
- security audit
- vulnerability scan
- penetration testing
- fix security issues
- secure implementation
- authentication & authorization
- cryptography & data protection
- finding code vulnerabilities

## Workflow
- [ ] **Analyze**: Identify the language, framework, and architecture. Look for injection, authentication, network, and client-side vulnerabilities.
- [ ] **Assess**: Score vulnerabilities using CVSS and Risk Prioritization Matrix (Likelihood x Impact).
- [ ] **Mitigate**: Apply language-specific prevention systems (Python, Node.js, Java, Go).
- [ ] **Verify**: Ensure the fix adheres to the CIA Triad (Confidentiality, Integrity, Availability) and core principles like Least Privilege and Defense in Depth.

## Core Principles (Security Mindset)
- **Assume Breach**: Design systems assuming an attacker already has partial access. Minimize blast radius.
- **Least Privilege**: Every user, service, and component gets only the minimum permissions required.
- **Defense in Depth**: Layer multiple independent security controls. No single point of failure.
- **Fail Securely**: When a system fails, it must default to a secure state — deny all by default.
- **Zero Trust**: Never trust, always verify. Authenticate and authorize every request, even internal ones.
- **Shift Left**: Integrate security checks early in development, not as a final gate before release.
- **Security by Design**: Security is an architectural concern, not a feature you bolt on later.

## Instructions
* **Injection Prevention**: Always use parameterized queries or ORMs for SQL. Never use raw variable interpolation or string formatting. For NoSQL, validate schemas.
* **Authentication**: Enforce MFA, rate limiting (e.g., 100 req/15 min), and secure sessions (HttpOnly, SameSite cookies). Implement proper JWT (RS256, check exp, reject "none" alg).
* **XSS Prevention**: Never use `innerHTML` directly. Use framework-specific safe escaping (like React's `{userInput}`) or DOMPurify.
* **Security Headers**: Always implement security HTTP headers (e.g., via Helmet.js in Node, or Django's `SECURE_*` settings).
* **Transport Security (SSL/TLS)**: Always enforce HTTPS using SSL/TLS certificates across all branches and environments. Configure strong cipher suites (TLS 1.2/1.3 only), enforce HSTS (HTTP Strict Transport Security), and manage certificate lifecycles.
* **Secrets Management**: Never hardcode credentials. Use environment variables, `.env`, or Vault services.
* **Dependency Checks**: Always run dependency audits (`npm audit`, `pip-audit`, etc.) to prevent supply chain attacks like typosquatting or dependency confusion.

## Vulnerability Severity Framework (CVSS)
Assess severity using the following framework when reporting to the user:
- **CRITICAL** (9.0-10.0): RCE, unauthenticated data breach, auth bypass. Fix immediately (0-24h).
- **HIGH** (7.0-8.9): Privilege escalation, significant data exposure. Fix within 7 days.
- **MEDIUM** (4.0-6.9): XSS, CSRF, information disclosure. Fix within 30 days.
- **LOW** (0.1-3.9): Missing security headers, verbose error messages. Fix within 90 days.
- **INFO** (0.0): Outdated banners, non-exploitable misconfigs. Fix at best effort.

## Resources
- [Language Specific Mitigations](resources/language-specific-mitigations.md)
- [Authentication & Crypto Rules](resources/auth-and-crypto.md)
- [Attack Taxonomy Guide](resources/attack-taxonomy.md)
