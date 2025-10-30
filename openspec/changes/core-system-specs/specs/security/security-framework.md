# Security Framework Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Define security policies, authentication mechanisms, authorization models, and data protection strategies for Project Starter Pro 2.

---

## 1. Security Principles

### Core Principles
1. **Defense in Depth**: Multiple layers of security
2. **Least Privilege**: Minimal access rights by default
3. **Secure by Default**: Security enabled out of the box
4. **Privacy First**: User data protection paramount
5. **Transparency**: Clear security policies and practices

### Threat Model
- **Local Mode**: OS-level security, file system permissions
- **Team Mode**: Network security, authentication, authorization
- **Data at Rest**: Encryption of sensitive data
- **Data in Transit**: HTTPS for all external communications
- **Third-Party Integrations**: Secure credential storage

---

## 2. Authentication

### Local Mode Authentication

#### OS-Level Security
- Relies on operating system user authentication
- File system permissions protect data
- No additional authentication required

#### File Permissions
```bash
# Project data
chmod 700 /data/projects/
chmod 600 /data/projects/*/project.json

# Configuration
chmod 600 /config/.env
chmod 600 /config/integrations/*.json

# Credentials
chmod 600 ~/.psp/credentials
```

### Team Mode Authentication

#### Token-Based Authentication
```python
class AuthToken:
    """Authentication token for team mode."""
    
    token: str          # JWT token
    user_id: str        # User identifier
    issued_at: datetime # Token creation time
    expires_at: datetime # Token expiration
    scopes: list[str]   # Permissions granted
```

#### JWT Structure
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "iat": 1635724800,
    "exp": 1635811200,
    "scopes": ["project:read", "project:write"]
  },
  "signature": "..."
}
```

#### Authentication Flow
1. User provides credentials (username/password or API key)
2. System validates credentials
3. System generates JWT token
4. Client includes token in subsequent requests
5. System validates token on each request
6. Token refreshed before expiration

#### Session Management
- **Session Timeout**: 24 hours (configurable)
- **Refresh Tokens**: 30 days validity
- **Token Revocation**: Immediate on logout
- **Concurrent Sessions**: Allowed (max 5 per user)

---

## 3. Authorization

### Role-Based Access Control (RBAC)

#### Roles
```python
class Role(Enum):
    """User roles with hierarchical permissions."""
    
    VIEWER = "viewer"       # Read-only access
    CONTRIBUTOR = "contributor"  # Read + create/update
    ADMIN = "admin"         # Full access
    OWNER = "owner"         # Full access + transfer ownership
```

#### Permissions
```python
ROLE_PERMISSIONS = {
    Role.VIEWER: [
        "project:read",
        "task:read",
        "research:read",
        "analytics:read"
    ],
    Role.CONTRIBUTOR: [
        "project:read",
        "project:update",
        "task:read",
        "task:write",
        "research:read",
        "research:write",
        "analytics:read"
    ],
    Role.ADMIN: [
        "project:*",
        "task:*",
        "research:*",
        "analytics:*",
        "integration:*",
        "user:read",
        "user:write"
    ],
    Role.OWNER: [
        "*:*"  # All permissions
    ]
}
```

### Resource-Level Permissions

#### Project Permissions
```python
class ProjectPermission:
    """Project-level access control."""
    
    project_id: str
    user_id: str
    role: Role
    granted_at: datetime
    granted_by: str
```

#### Permission Checks
```python
def check_permission(
    user_id: str,
    resource: str,
    action: str,
    resource_id: str = None
) -> bool:
    """
    Check if user has permission for action on resource.
    
    Args:
        user_id: User identifier
        resource: Resource type (project, task, etc.)
        action: Action to perform (read, write, delete)
        resource_id: Specific resource ID (optional)
        
    Returns:
        True if permission granted, False otherwise
    """
```

### Access Control Lists (ACL)

#### Project ACL
```json
{
  "project_id": "proj_123",
  "owner": "user_1",
  "permissions": [
    {
      "user_id": "user_2",
      "role": "contributor",
      "granted_at": "2025-10-30T10:00:00Z"
    },
    {
      "user_id": "user_3",
      "role": "viewer",
      "granted_at": "2025-10-30T11:00:00Z"
    }
  ],
  "public": false
}
```

---

## 4. Data Protection

### Encryption at Rest

#### Sensitive Data Encryption
- **Algorithm**: AES-256-GCM
- **Key Management**: OS keyring or environment variables
- **Encrypted Fields**: Credentials, API keys, tokens

```python
class EncryptionService:
    """Handles data encryption/decryption."""
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt sensitive data."""
        
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt sensitive data."""
        
    def rotate_key(self) -> bool:
        """Rotate encryption key."""
```

#### Encrypted Storage
```json
{
  "integration_id": "int_123",
  "service": "github",
  "credentials": {
    "type": "encrypted",
    "algorithm": "AES-256-GCM",
    "data": "encrypted_base64_string",
    "iv": "initialization_vector",
    "tag": "authentication_tag"
  }
}
```

### Encryption in Transit

#### HTTPS Requirements
- All external API calls use HTTPS
- TLS 1.2 minimum (prefer TLS 1.3)
- Certificate validation required
- No self-signed certificates in production

#### API Security Headers
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```

---

## 5. Credential Management

### Storage Options

#### Environment Variables (Recommended)
```bash
# .env file (never commit)
PSP_DB_PASSWORD=secret123
PSP_API_KEY=key_abc123
PSP_ENCRYPTION_KEY=enc_xyz789
```

#### OS Keyring (Most Secure)
```python
import keyring

# Store credential
keyring.set_password("psp", "github_token", "ghp_abc123")

# Retrieve credential
token = keyring.get_password("psp", "github_token")
```

#### Encrypted File (Fallback)
```json
{
  "credentials": {
    "github": {
      "encrypted": true,
      "data": "encrypted_token"
    }
  }
}
```

### Credential Rotation
- **API Keys**: Rotate every 90 days
- **Passwords**: Rotate every 180 days
- **Encryption Keys**: Rotate annually
- **Automated Reminders**: 30 days before expiration

---

## 6. Input Validation & Sanitization

### Validation Rules

#### Input Validation
```python
def validate_project_name(name: str) -> bool:
    """Validate project name."""
    if not name or len(name) > 200:
        raise ValidationError("Name must be 1-200 characters")
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
        raise ValidationError("Name contains invalid characters")
    return True
```

#### SQL Injection Prevention
- Use parameterized queries
- Never concatenate user input into queries
- Use ORM when possible

#### Path Traversal Prevention
```python
def safe_path(base_dir: str, user_path: str) -> str:
    """Ensure path is within base directory."""
    full_path = os.path.realpath(os.path.join(base_dir, user_path))
    if not full_path.startswith(os.path.realpath(base_dir)):
        raise SecurityError("Path traversal detected")
    return full_path
```

#### Command Injection Prevention
```python
# BAD: Never do this
os.system(f"git clone {user_url}")

# GOOD: Use subprocess with list
subprocess.run(["git", "clone", user_url], check=True)
```

---

## 7. Audit Logging

### Security Events to Log

```python
class SecurityEvent(Enum):
    """Security-relevant events."""
    
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    PERMISSION_DENIED = "permission_denied"
    CREDENTIAL_CREATED = "credential_created"
    CREDENTIAL_UPDATED = "credential_updated"
    CREDENTIAL_DELETED = "credential_deleted"
    ENCRYPTION_KEY_ROTATED = "encryption_key_rotated"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
```

### Audit Log Format
```json
{
  "timestamp": "2025-10-30T12:00:00Z",
  "event": "login_success",
  "user_id": "user_123",
  "ip_address": "192.168.1.100",
  "user_agent": "PSP-CLI/1.0.0",
  "resource": "auth",
  "action": "login",
  "result": "success",
  "metadata": {
    "session_id": "sess_abc123"
  }
}
```

### Log Retention
- **Security Logs**: 1 year minimum
- **Access Logs**: 90 days
- **Error Logs**: 30 days
- **Debug Logs**: 7 days

---

## 8. Security Best Practices

### Development
- [ ] Never commit secrets to version control
- [ ] Use `.gitignore` for sensitive files
- [ ] Run security linters (bandit, safety)
- [ ] Keep dependencies updated
- [ ] Review security advisories

### Deployment
- [ ] Use environment-specific configurations
- [ ] Enable encryption for sensitive data
- [ ] Configure proper file permissions
- [ ] Use HTTPS for all external communications
- [ ] Implement rate limiting

### Operations
- [ ] Regular security audits
- [ ] Monitor for suspicious activity
- [ ] Keep audit logs
- [ ] Incident response plan
- [ ] Regular backups

---

## 9. Vulnerability Management

### Dependency Scanning
```bash
# Python
pip-audit
safety check

# Node.js
npm audit
pnpm audit
```

### Security Updates
- **Critical**: Patch within 24 hours
- **High**: Patch within 7 days
- **Medium**: Patch within 30 days
- **Low**: Patch in next release

### Vulnerability Disclosure
- Security email: security@example.com
- Responsible disclosure policy
- 90-day disclosure timeline
- Security advisories published

---

## 10. Compliance & Privacy

### Data Privacy
- **GDPR Compliance**: User data rights (access, deletion, portability)
- **Data Minimization**: Collect only necessary data
- **Consent**: Explicit consent for data collection
- **Anonymization**: Remove PII when possible

### Data Retention
- **Active Projects**: Indefinite
- **Archived Projects**: 1 year
- **Deleted Projects**: 30-day soft delete, then permanent
- **Audit Logs**: 1 year

### User Rights
- Right to access data
- Right to delete data
- Right to export data
- Right to correct data

---

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- GDPR: https://gdpr.eu/
- Python Security: https://bandit.readthedocs.io/

