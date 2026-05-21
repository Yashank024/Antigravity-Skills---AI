# Attack Taxonomy & Prevention Guide

## 1. Injection Attacks
Injection attacks occur when untrusted data is sent to an interpreter as part of a command or query.
- **SQL Injection (SQLi)** (CRITICAL): Prevent with Parameterized queries, ORM. Example: `' OR '1'='1`
- **NoSQL Injection** (HIGH): Prevent with Schema validation, sanitize operators. Example: `{"$gt": ""}`
- **Command Injection (OS)** (CRITICAL): Never pass user input to shell. Example: `; rm -rf /`
- **LDAP Injection** (HIGH): Escape special chars, whitelist. Example: `*)(`
- **XML Injection / XXE** (HIGH): Disable external entities. Example: `<!ENTITY xxe SYSTEM "file:///etc/passwd">`
- **SSTI (Template)** (CRITICAL): Use logic-less templates, sandbox. Example: `{{7*7}} -> 49`
- **XPath Injection** (MEDIUM): Parameterized XPath queries. Example: `' or '1'='1`
- **Header Injection** (MEDIUM): Validate/strip CRLF chars. Example: `value\r\nSet-Cookie: admin=1`

## 2. Authentication & Session Attacks
- **Brute Force** (HIGH): Rate limiting, lockout, CAPTCHA (Limit to 5 attempts/15 min).
- **Credential Stuffing** (HIGH): MFA, breach-password checks (Use HaveIBeenPwned API).
- **Password Spraying** (HIGH): MFA, anomaly detection (Low-and-slow variant of brute force).
- **Session Hijacking** (CRITICAL): Secure cookies, HttpOnly, SameSite (Regenerate session ID on login).
- **Session Fixation** (HIGH): Regenerate session ID post-auth (Never accept external session IDs).
- **JWT Attacks** (CRITICAL): Verify alg, use RS256, check exp (Reject "alg: none" tokens).
- **CSRF** (HIGH): CSRF tokens, SameSite cookies (Double-submit cookie pattern).
- **OAuth Misconfig** (HIGH): Validate redirect_uri, state param (Never allow wildcard redirects).
- **Account Takeover** (CRITICAL): MFA, email verification flows (Monitor for impossible logins).

## 3. Cross-Site Scripting (XSS)
- **Reflected XSS**: Payload is in the request, reflected in the response. No persistence. Typically requires user to click a crafted link.
- **Stored XSS**: Payload stored in the database. Executes for every user who views the infected page. Most dangerous type.
- **DOM-based XSS**: Payload executed via client-side JavaScript manipulating the DOM. Server never sees the payload.
- **mXSS (Mutation)**: Browser mutates safe HTML into dangerous HTML during parsing. Bypasses many filters.
- **Prevention**: `document.getElementById('output').textContent = userInput;` // Never innerHTML with user data. React automatically escapes `{userInput}`. Use DOMPurify for rich HTML.

## 4. Network & Infrastructure Attacks
- **DDoS (Volumetric)** (HIGH): CDN, rate limiting, anycast (Cloudflare, AWS Shield).
- **Man-in-the-Middle** (CRITICAL): TLS everywhere, HSTS, cert pinning (Never allow HTTP for sensitive ops).
- **DNS Poisoning** (HIGH): DNSSEC, DoH/DoT (Use trusted resolvers).
- **ARP Spoofing** (HIGH): Dynamic ARP Inspection, VPN (Layer 2 attack on LAN).
- **Port Scanning** (MEDIUM): Firewall, IDS/IPS, fail2ban (Block after N scan attempts).
- **SSL Stripping** (HIGH): HSTS preloading, redirect HTTP->HTTPS (Use includeSubDomains).
- **BGP Hijacking** (HIGH): RPKI, monitor BGP routes (ISP-level mitigation needed).
- **SSRF** (CRITICAL): Allowlist internal IPs, block metadata (AWS: block 169.254.169.254).

## 5. Client-Side Attacks
- **Clickjacking** (MEDIUM): X-Frame-Options, CSP frame-ancestors (Set: X-Frame-Options: DENY).
- **Open Redirect** (MEDIUM): Whitelist redirect URLs (Never use user-supplied redirect URLs).
- **Prototype Pollution (JS)** (HIGH): Object.freeze, use Map/Set (`__proto__` and `constructor.prototype`).
- **Subdomain Takeover** (HIGH): Audit DNS, remove stale records (Check CNAME to unclaimed services).
- **CSS Injection** (MEDIUM): Sanitize style inputs, CSP (Can leak data via attribute selectors).
- **Tabnapping** (MEDIUM): `rel='noopener noreferrer'` on links (Attacker controls opener tab).
- **Browser Cache Poisoning** (MEDIUM): `Cache-Control: no-store` for sensitive (Vary header usage).

## 6. Supply Chain Attacks
Compromise the software build process, dependencies, or update mechanisms to inject malicious code into trusted software.
- **Dependency Confusion**: Attacker publishes malicious package to public registry with same name as internal package.
- **Typosquatting**: Malicious packages with names similar to popular ones.
- **Compromised Maintainer**: Legitimate package maintainer account is hijacked.
- **Build System Compromise**: CI/CD pipeline is compromised.
- **Prevention**: Pin exact dependency versions, use lockfiles. Use private registries. Enable Sigstore/Cosign. Run dependency audit tools: npm audit, pip-audit, Dependabot, Snyk, Socket.dev. SBOM.
