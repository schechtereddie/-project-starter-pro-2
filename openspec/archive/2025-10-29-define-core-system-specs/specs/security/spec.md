# Security Specification

**Version**: 1.0.0  
**Last Updated**: 2025-10-30  
**Status**: Draft  

## Purpose

Protect user data and ensure safe operation of Project Starter Pro 2 through comprehensive security measures including authentication, authorization, data protection, and security monitoring.

---

## Security Principles

### Core Principles

1. **Defense in Depth**: Multiple layers of security controls
2. **Least Privilege**: Minimal access rights by default
3. **Secure by Default**: Security enabled out of the box
4. **Privacy First**: User data protection is paramount
5. **Transparency**: Clear security policies and practices
6. **Zero Trust**: Verify all access requests

### Threat Model

**Local Mode Threats**:
- Unauthorized file system access
- Malicious local processes
- Data theft from unencrypted storage
- Credential exposure in configuration files

**Team Mode Threats**:
- Unauthorized network access
- Man-in-the-middle attacks
- Session hijacking
- Brute force authentication attempts
- API abuse and rate limit violations

**External Integration Threats**:
- Compromised API keys
- Malicious third-party services
- Data leakage through integrations
- Webhook injection attacks

---

## Authentication

### Local Mode Authentication

#### OS-Level Identity

**Approach**: Rely on operating system user authentication
- No additional authentication layer required
- File system permissions protect data
- User's OS credentials provide access control

**File Permissions**:
```bash
# Project data - owner read/write only
chmod 700 /data/projects/
chmod 600 /data/projects/*/project.json

# Configuration - owner read/write only
chmod 600 /config/settings.yaml
chmod 600 /config/.env

# Credentials - owner read only
chmod 400 ~/.psp/credentials

# Executable scripts - owner read/write/execute
chmod 700 /scripts/*.sh
```

**Security Measures**:
- Verify user ownership before file operations
- Prevent symlink attacks
- Validate file paths to prevent traversal
- Use secure temporary file creation

---

### Team Mode Authentication

#### Token-Based Authentication (JWT)

**Token Structure**:
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_123",
    "name": "John Doe",
    "email": "john@example.com",
    "iat": 1635724800,
    "exp": 1635811200,
    "scopes": ["project:read", "project:write", "note:write"]
  },
  "signature": "..."
}
```

**Authentication Flow**:

1. **Login Request**:
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john@example.com",
  "password": "secure_password_123"
}
```

2. **Token Response**:
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "user": {
      "id": "user_123",
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

3. **Authenticated Request**:
```http
GET /projects
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Management**:
- **Access Token Lifetime**: 24 hours (configurable)
- **Refresh Token Lifetime**: 30 days (configurable)
- **Token Storage**: Secure HTTP-only cookies or local storage
- **Token Revocation**: Immediate on logout or security event
- **Token Rotation**: Automatic refresh before expiration

**Password Requirements**:
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character
- Not in common password list
- Not similar to username/email

**Password Hashing**:
```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )
```

**Multi-Factor Authentication (MFA)** (Optional):
- TOTP (Time-based One-Time Password)
- SMS verification
- Email verification
- Backup codes

---

## Authorization

### Role-Based Access Control (RBAC)

#### Roles

```python
from enum import Enum

class Role(Enum):
    """User roles with hierarchical permissions."""
    
    VIEWER = "viewer"           # Read-only access
    CONTRIBUTOR = "contributor" # Read + create/update
    ADMIN = "admin"            # Full access except ownership transfer
    OWNER = "owner"            # Complete control
```

#### Permissions Matrix

| Resource | Viewer | Contributor | Admin | Owner |
|----------|--------|-------------|-------|-------|
| Project Read | ✓ | ✓ | ✓ | ✓ |
| Project Create | ✗ | ✓ | ✓ | ✓ |
| Project Update | ✗ | ✓ | ✓ | ✓ |
| Project Delete | ✗ | ✗ | ✓ | ✓ |
| Project Archive | ✗ | ✗ | ✓ | ✓ |
| Note Read | ✓ | ✓ | ✓ | ✓ |
| Note Write | ✗ | ✓ | ✓ | ✓ |
| Research Read | ✓ | ✓ | ✓ | ✓ |
| Research Write | ✗ | ✓ | ✓ | ✓ |
| Analytics Read | ✓ | ✓ | ✓ | ✓ |
| User Management | ✗ | ✗ | ✓ | ✓ |
| Settings Update | ✗ | ✗ | ✓ | ✓ |
| Integration Config | ✗ | ✗ | ✓ | ✓ |
| Ownership Transfer | ✗ | ✗ | ✗ | ✓ |

#### Permission Checking

```python
from typing import Protocol

class PermissionChecker(Protocol):
    """Protocol for permission checking."""
    
    def check_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
        resource_id: str | None = None
    ) -> bool:
        """Check if user has permission for action on resource."""
        ...

class RBACPermissionChecker:
    """RBAC-based permission checker."""
    
    def check_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
        resource_id: str | None = None
    ) -> bool:
        """Check permission based on user role."""
        user_role = self._get_user_role(user_id, resource_id)
        required_permission = f"{resource}:{action}"
        
        return self._has_permission(user_role, required_permission)
    
    def _get_user_role(self, user_id: str, resource_id: str | None) -> Role:
        """Get user's role for resource."""
        # Implementation
        pass
    
    def _has_permission(self, role: Role, permission: str) -> bool:
        """Check if role has permission."""
        # Implementation
        pass
```

### Access Control Lists (ACL)

**Project ACL**:
```json
{
  "project_id": "proj_abc123",
  "owner": "user_1",
  "acl": [
    {
      "user_id": "user_2",
      "role": "contributor",
      "granted_at": "2025-10-30T10:00:00Z",
      "granted_by": "user_1"
    },
    {
      "user_id": "user_3",
      "role": "viewer",
      "granted_at": "2025-10-30T11:00:00Z",
      "granted_by": "user_1"
    }
  ],
  "public": false,
  "inherit_permissions": true
}
```

---

## Data Protection

### Encryption at Rest

#### Sensitive Data Encryption

**Algorithm**: AES-256-GCM (Galois/Counter Mode)

**Encrypted Fields**:
- API keys and tokens
- OAuth credentials
- Database passwords
- Integration secrets
- User passwords (hashed, not encrypted)

**Encryption Implementation**:
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import os
import base64

class EncryptionService:
    """Handles data encryption and decryption."""
    
    def __init__(self, master_key: bytes):
        """Initialize with master encryption key."""
        self.aesgcm = AESGCM(master_key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext data.
        
        Returns:
            Base64-encoded encrypted data with nonce
        """
        nonce = os.urandom(12)  # 96-bit nonce for GCM
        plaintext_bytes = plaintext.encode('utf-8')
        
        ciphertext = self.aesgcm.encrypt(nonce, plaintext_bytes, None)
        
        # Combine nonce + ciphertext and encode
        encrypted = nonce + ciphertext
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, encrypted: str) -> str:
        """Decrypt encrypted data."""
        encrypted_bytes = base64.b64decode(encrypted.encode('utf-8'))
        
        # Extract nonce and ciphertext
        nonce = encrypted_bytes[:12]
        ciphertext = encrypted_bytes[12:]
        
        plaintext_bytes = self.aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext_bytes.decode('utf-8')
```

**Key Management**:
- Master key stored in OS keyring or environment variable
- Key rotation supported (re-encrypt with new key)
- Key derivation using PBKDF2 for password-based keys
- Never log or display encryption keys

**Encrypted Storage Format**:
```json
{
  "integration_id": "int_github_123",
  "service": "github",
  "credentials": {
    "encrypted": true,
    "algorithm": "AES-256-GCM",
    "data": "base64_encoded_encrypted_data",
    "key_id": "key_v1",
    "created_at": "2025-10-30T10:00:00Z"
  }
}
```

### Encryption in Transit

#### HTTPS Requirements

**TLS Configuration**:
- **Minimum Version**: TLS 1.2
- **Preferred Version**: TLS 1.3
- **Certificate Validation**: Required (no self-signed in production)
- **Cipher Suites**: Strong ciphers only (AES-GCM, ChaCha20-Poly1305)

**HTTP Security Headers**:
```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

**Certificate Pinning** (Optional for high-security deployments):
```python
import ssl
import certifi

def create_secure_context() -> ssl.SSLContext:
    """Create SSL context with certificate pinning."""
    context = ssl.create_default_context(cafile=certifi.where())
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    return context
```

---

## Credential Management

### Storage Options

#### 1. Environment Variables (Recommended)

**`.env` file** (never commit):
```bash
# Database
DB_PASSWORD=secure_password_123

# API Keys
GITHUB_API_KEY=ghp_abc123xyz789
OPENAI_API_KEY=sk-abc123xyz789

# Encryption
ENCRYPTION_MASTER_KEY=base64_encoded_key

# JWT
JWT_SECRET_KEY=random_secret_key_here
```

**Loading**:
```python
from dotenv import load_dotenv
import os

load_dotenv()

db_password = os.getenv('DB_PASSWORD')
github_key = os.getenv('GITHUB_API_KEY')
```

#### 2. OS Keyring (Most Secure)

**Using `keyring` library**:
```python
import keyring

# Store credential
keyring.set_password("psp", "github_token", "ghp_abc123xyz789")

# Retrieve credential
token = keyring.get_password("psp", "github_token")

# Delete credential
keyring.delete_password("psp", "github_token")
```

**Supported Backends**:
- macOS: Keychain
- Windows: Credential Locker
- Linux: Secret Service (GNOME Keyring, KWallet)

#### 3. Encrypted File (Fallback)

**Encrypted credentials file**:
```json
{
  "version": "1.0",
  "encrypted": true,
  "credentials": {
    "github": {
      "encrypted_data": "base64_encrypted_token",
      "key_id": "key_v1"
    },
    "openai": {
      "encrypted_data": "base64_encrypted_key",
      "key_id": "key_v1"
    }
  }
}
```

### Credential Rotation

**Rotation Schedule**:
- **API Keys**: Every 90 days
- **Passwords**: Every 180 days
- **Encryption Keys**: Annually
- **JWT Secrets**: Every 6 months

**Rotation Process**:
1. Generate new credential
2. Update in secure storage
3. Test with new credential
4. Revoke old credential
5. Update documentation
6. Notify relevant parties

**Automated Reminders**:
```python
from datetime import datetime, timedelta

def check_credential_expiry(credential_id: str) -> dict:
    """Check if credential needs rotation."""
    credential = get_credential(credential_id)
    created_at = credential['created_at']
    rotation_period = credential['rotation_period_days']
    
    expires_at = created_at + timedelta(days=rotation_period)
    days_until_expiry = (expires_at - datetime.utcnow()).days
    
    return {
        'credential_id': credential_id,
        'expires_at': expires_at,
        'days_until_expiry': days_until_expiry,
        'needs_rotation': days_until_expiry <= 30
    }
```

---

## Input Validation & Sanitization

### Validation Rules

#### Path Traversal Prevention

```python
import os
from pathlib import Path

def safe_path(base_dir: str, user_path: str) -> Path:
    """Ensure path is within base directory.
    
    Raises:
        SecurityError: If path traversal detected
    """
    base = Path(base_dir).resolve()
    target = (base / user_path).resolve()
    
    if not str(target).startswith(str(base)):
        raise SecurityError(f"Path traversal detected: {user_path}")
    
    return target
```

#### Command Injection Prevention

```python
import subprocess
import shlex

# BAD: Never concatenate user input into shell commands
def bad_example(user_url: str):
    os.system(f"git clone {user_url}")  # VULNERABLE!

# GOOD: Use subprocess with list arguments
def good_example(user_url: str):
    # Validate URL format first
    if not is_valid_url(user_url):
        raise ValueError("Invalid URL")
    
    # Use list arguments (no shell interpretation)
    subprocess.run(
        ["git", "clone", user_url],
        check=True,
        capture_output=True
    )
```

#### SQL Injection Prevention

```python
# BAD: String concatenation
def bad_query(user_id: str):
    query = f"SELECT * FROM users WHERE id = '{user_id}'"  # VULNERABLE!
    cursor.execute(query)

# GOOD: Parameterized queries
def good_query(user_id: str):
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
```

#### XSS Prevention

```python
import html

def sanitize_html(user_input: str) -> str:
    """Escape HTML special characters."""
    return html.escape(user_input)

def sanitize_markdown(user_input: str) -> str:
    """Sanitize markdown input."""
    # Remove potentially dangerous HTML tags
    allowed_tags = ['p', 'br', 'strong', 'em', 'code', 'pre', 'ul', 'ol', 'li']
    # Use markdown library with safe mode
    return markdown.markdown(user_input, safe_mode='escape')
```

---

## Security Monitoring

### Audit Logging

#### Security Events

```python
from enum import Enum

class SecurityEvent(Enum):
    """Security-relevant events to log."""
    
    # Authentication
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    MFA_ENABLED = "mfa_enabled"
    MFA_DISABLED = "mfa_disabled"
    
    # Authorization
    PERMISSION_DENIED = "permission_denied"
    ROLE_CHANGED = "role_changed"
    ACL_MODIFIED = "acl_modified"
    
    # Credentials
    CREDENTIAL_CREATED = "credential_created"
    CREDENTIAL_UPDATED = "credential_updated"
    CREDENTIAL_DELETED = "credential_deleted"
    CREDENTIAL_ACCESSED = "credential_accessed"
    
    # Security
    ENCRYPTION_KEY_ROTATED = "encryption_key_rotated"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    INVALID_TOKEN = "invalid_token"
```

#### Audit Log Format

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
    "session_id": "sess_abc123",
    "mfa_used": true
  }
}
```

#### Log Retention

- **Security Logs**: 1 year minimum
- **Access Logs**: 90 days
- **Error Logs**: 30 days
- **Debug Logs**: 7 days

### Intrusion Detection

**Suspicious Activity Patterns**:
- Multiple failed login attempts (>5 in 15 minutes)
- Access from unusual locations
- Unusual API usage patterns
- Rapid credential changes
- Large data exports
- Off-hours access (configurable)

**Automated Responses**:
- Temporary account lockout (15-30 minutes)
- Require MFA verification
- Send security alert email
- Log detailed audit trail
- Notify administrators

---

## Security Best Practices

### Development

- [ ] Never commit secrets to version control
- [ ] Use `.gitignore` for sensitive files
- [ ] Run security linters (`bandit`, `safety`, `npm audit`)
- [ ] Keep dependencies updated
- [ ] Review security advisories regularly
- [ ] Use dependency scanning tools
- [ ] Implement security unit tests

### Deployment

- [ ] Use environment-specific configurations
- [ ] Enable encryption for sensitive data
- [ ] Configure proper file permissions
- [ ] Use HTTPS for all external communications
- [ ] Implement rate limiting
- [ ] Enable security headers
- [ ] Use secure session management
- [ ] Implement CSRF protection

### Operations

- [ ] Regular security audits
- [ ] Monitor for suspicious activity
- [ ] Maintain audit logs
- [ ] Have incident response plan
- [ ] Regular backups (encrypted)
- [ ] Test disaster recovery
- [ ] Security training for team
- [ ] Vulnerability disclosure program

---

## Compliance & Privacy

### Data Privacy

**GDPR Compliance** (if applicable):
- User data rights (access, deletion, portability)
- Data minimization
- Explicit consent for data collection
- Privacy by design
- Data breach notification

**User Rights**:
- Right to access data
- Right to delete data
- Right to export data
- Right to correct data
- Right to opt-out of analytics

### Data Retention

- **Active Projects**: Indefinite
- **Archived Projects**: 1 year
- **Deleted Projects**: 30-day soft delete, then permanent
- **Audit Logs**: 1 year
- **Backups**: 30 days

---

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- JWT Best Practices: https://tools.ietf.org/html/rfc8725
- GDPR: https://gdpr.eu/
- Python Security: https://bandit.readthedocs.io/
- Node.js Security: https://nodejs.org/en/docs/guides/security/

