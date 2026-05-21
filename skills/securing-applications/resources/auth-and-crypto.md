# Authentication & Authorization Systems

## JWT Security Best Practices
- **Algorithm**: Use RS256 (asymmetric), not HS256 for inter-service tokens (private key signs, public key verifies). ALWAYS verify the 'alg' header. Reject 'none'. Never accept alg from the token itself.
- **Expiration**: Set short expiry: access tokens 15 min, refresh tokens 7 days max. Include 'iss' (issuer), 'aud' (audience), 'iat' (issued-at) claims and validate all.
- **Refresh Tokens**: Store refresh tokens server-side with rotation. Invalidate old tokens on refresh.
- **Storage**: Never store JWTs in localStorage. Use HttpOnly cookies with SameSite=Strict.
- **Revocation**: Implement token revocation list (Redis) for critical operations (password change, logout).

## Password Security
- Never use MD5, SHA1, SHA256 for passwords — they are fast hashes designed for speed, not security.
- Use **bcrypt** or **argon2**.
- Example Python:
  ```python
  from argon2 import PasswordHasher
  ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2)
  hash = ph.hash(password) # Store this
  ph.verify(hash, input_password)
  ```
- Example Node.js:
  ```javascript
  const bcrypt = require('bcrypt');
  const hash = await bcrypt.hash(password, 12);
  const match = await bcrypt.compare(input, hash);
  ```
- Example Go:
  ```go
  import "golang.org/x/crypto/bcrypt"
  hash, _ := bcrypt.GenerateFromPassword([]byte(pwd), bcrypt.DefaultCost)
  err := bcrypt.CompareHashAndPassword(hash, []byte(input))
  ```

## RBAC Implementation Pattern
Role-Based Access Control (RBAC) restricts system access based on roles. Always enforce at the server/API level — never rely on client-side checks.
Example Python decorator for role enforcement:
```python
def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_user.role not in roles:
                abort(403) # Forbidden
            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/admin/users')
@require_role('admin', 'superadmin')
def list_users():
    ...
```
