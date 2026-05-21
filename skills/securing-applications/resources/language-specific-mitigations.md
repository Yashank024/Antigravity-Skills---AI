# Prevention Systems — Language-Specific

## Python Security
- **Input Validation**: Use pydantic or marshmallow schemas. Never trust raw request.args or request.json.
- **SQL**: Use SQLAlchemy ORM or parameterized queries. Never string-format SQL: `cursor.execute("SELECT * FROM users WHERE username = %s", (username,))`
- **Secrets**: Use python-decouple or os.environ. Never hardcode credentials.
- **Deserialization**: Never use `pickle` on untrusted data. Use JSON or MessagePack.
- **File Uploads**: Validate extension + MIME type + file content. Store outside web root. Rename files.
- **Dependencies**: Run: `pip-audit`, `safety check`. Use `requirements.txt` with hashes.
- **SAST Tools**: Bandit (static), Semgrep, PyLint-security plugin.
- **Django Framework**: Use `CSRF_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`, `ALLOWED_HOSTS`. 
  ```python
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  SESSION_COOKIE_HTTPONLY = True
  CSRF_COOKIE_SECURE = True
  X_FRAME_OPTIONS = 'DENY'
  SECURE_CONTENT_TYPE_NOSNIFF = True
  SECURE_BROWSER_XSS_FILTER = True
  SECURE_HSTS_SECONDS = 31536000
  SECURE_HSTS_INCLUDE_SUBDOMAINS = True
  SECURE_HSTS_PRELOAD = True
  CONTENT_SECURITY_POLICY = "default-src 'self'"
  ```

## JavaScript / Node.js Security
- **Helmet.js**: Use `helmet()` middleware in Express to set 14+ security HTTP headers automatically.
- **Input Validation**: Use joi, zod, or express-validator. Never trust req.body directly.
- **Rate Limiting**: `express-rate-limit`: 100 requests per 15 minutes per IP as baseline.
- **SQL**: Use Sequelize/Prisma ORM or pg parameterized queries. Never template SQL strings.
- **XSS Prevention**: DOMPurify for client-side. express-validator sanitization on server.
- **Dependencies**: `npm audit`, Snyk, Socket.dev. Avoid packages with 0 downloads.
- **Prototype Pollution**: Use `Object.create(null)`, avoid deep merge of user data.
- **SAST Tools**: ESLint-security plugin, njsscan, Semgrep JS rules.
  ```javascript
  const helmet = require('helmet');
  const rateLimit = require('express-rate-limit');
  const mongoSanitize = require('express-mongo-sanitize');
  app.use(helmet()); 
  app.use(mongoSanitize()); 
  app.use(rateLimit({ windowMs: 15*60*1000, max: 100 }));
  app.use(helmet.contentSecurityPolicy({
    directives: { defaultSrc: ["'self'"], scriptSrc: ["'self'"] }
  }));
  ```

## Java / Spring Boot Security
- **Spring Security**: Use for authentication, CSRF protection, and method-level authorization.
- **Input Validation**: Jakarta Bean Validation (`@NotNull`, `@Size`, `@Pattern`). Use `@Valid` on all controller params.
- **SQL**: Use JPA/Hibernate or JdbcTemplate with `?` placeholders. Never concatenate SQL.
- **Deserialization**: Disable Java deserialization where possible. Use lookAheadObjectInputStream.
- **Secrets**: Spring Cloud Config + Vault. Never put credentials in application.properties in VCS.
- **SAST Tools**: SpotBugs + FindSecBugs plugin, OWASP Dependency-Check, Semgrep.
  ```java
  @Configuration @EnableWebSecurity
  public class SecurityConfig extends WebSecurityConfigurerAdapter {
      protected void configure(HttpSecurity http) throws Exception {
          http
          .csrf().csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
          .and().headers().frameOptions().deny()
          .and().sessionManagement()
          .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
          .and().authorizeRequests()
          .antMatchers("/public/**").permitAll()
          .anyRequest().authenticated();
      }
  }
  ```

## Go Security
- **SQL**: Use database/sql with `?` placeholders or sqlx. Never `fmt.Sprintf` into queries.
- **Input Validation**: Use `github.com/go-playground/validator`. Validate all struct fields from external input.
- **Crypto**: Use `crypto/tls`, `crypto/rand`. Never use `math/rand` for security-sensitive values.
- **File Paths**: Use `filepath.Clean`, restrict to allowed directories. Check for path traversal.
- **HTTP Security**: Use `gorilla/handlers` for security headers. Set timeouts on all `http.Server`.
- **SAST Tools**: gosec (formerly gas), staticcheck, golangci-lint with security rules.
  ```go
  srv := &http.Server{
      ReadTimeout: 5 * time.Second,
      WriteTimeout: 10 * time.Second,
      IdleTimeout: 120 * time.Second,
      ReadHeaderTimeout: 2 * time.Second,
      TLSConfig: &tls.Config{
          MinVersion: tls.VersionTLS13,
          CurvePreferences: []tls.CurveID{tls.X25519, tls.CurveP256},
          PreferServerCipherSuites: true,
      },
  }
  ```
