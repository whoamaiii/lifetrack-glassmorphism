# Security Policy

## 🔒 Security Considerations

Personal Life Tracker handles potentially sensitive personal data. This document outlines security best practices and how to report security issues.

## 🚨 Reporting Security Vulnerabilities

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:
1. Email to the project maintainers
2. Private message to repository owners
3. GitHub Security Advisories (if enabled)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## 🛡️ Security Best Practices

### API Key Management

#### ❌ Never Do This:
```python
# NEVER hardcode API keys
API_KEY = "sk-or-v1-abc123..."  # BAD!
```

#### ✅ Always Do This:
```python
# Use environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("API key not configured")
```

### Secure API Key Storage

#### Development
```bash
# .env file (add to .gitignore)
OPENROUTER_API_KEY=your-key-here

# Load in Python
from dotenv import load_dotenv
load_dotenv()
```

#### Production
- Use environment variables
- Use secrets management services
- Never commit keys to version control

### Data Protection

#### Local Storage
- Data is stored in `livslogg.csv` locally
- No automatic cloud synchronization
- User has full control over their data

#### Sensitive Data
The tracker may contain sensitive personal information:
- Health-related activities
- Personal habits
- Location information (if extended)

**Recommendations:**
1. Store data in encrypted folders
2. Use full-disk encryption
3. Regular backups to secure locations
4. Limit access to the data file

### Network Security

#### API Communications
- All API calls use HTTPS
- TLS encryption for data in transit
- No sensitive data in URL parameters

#### Web Interface
When running the Streamlit app:
```bash
# Local-only access (default)
streamlit run streamlit_app.py

# Network access (be cautious)
streamlit run streamlit_app.py --server.address 0.0.0.0
```

⚠️ **Warning**: Exposing to network allows others to access your data!

## 🔍 Security Checklist

### For Users

- [ ] API key stored in environment variable
- [ ] No API keys in code or commits
- [ ] Data file has appropriate permissions
- [ ] Regular backups of data
- [ ] Web interface not exposed to internet
- [ ] Using HTTPS for all API calls

### For Developers

- [ ] Never log API keys
- [ ] Validate all user input
- [ ] Sanitize data before display
- [ ] Use parameterized queries (if adding DB)
- [ ] Keep dependencies updated
- [ ] Review security advisories

## 🛠️ Secure Configuration

### Environment Setup
```bash
# Create .env file
cat > .env << EOF
OPENROUTER_API_KEY=your-key-here
EOF

# Set restrictive permissions
chmod 600 .env
chmod 600 livslogg.csv
```

### Git Configuration
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo "livslogg.csv" >> .gitignore
echo "*.log" >> .gitignore
```

## 🚫 Common Security Mistakes

### 1. Exposed API Keys
```python
# BAD: Key in code
requests.post(url, headers={"Authorization": "Bearer sk-123..."})

# GOOD: Key from environment
requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"})
```

### 2. Unvalidated Input
```python
# BAD: Direct use of user input
activity = user_input  # Could contain malicious data

# GOOD: Validate against allowed values
if activity not in ACTIVITY_CATEGORIES:
    raise ValueError("Invalid activity")
```

### 3. Insecure File Permissions
```bash
# BAD: World-readable
-rw-rw-rw- 1 user user 1234 Jan 1 00:00 livslogg.csv

# GOOD: User-only
-rw------- 1 user user 1234 Jan 1 00:00 livslogg.csv
```

## 📊 Data Privacy

### What Data is Collected
- Activity timestamps
- Activity types and quantities
- No personal identification
- No location tracking (unless extended)
- No third-party analytics

### Data Transmission
- API calls to OpenRouter for AI processing
- Text descriptions sent for parsing
- No storage on external servers
- All processing results stored locally

### GDPR Compliance
For EU users:
- All data stored locally
- User has full control
- Can delete at any time
- No data sharing
- No tracking cookies (web interface)

## 🔄 Security Updates

### Dependency Management
```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt

# Review changes
pip list --outdated
```

### Security Patches
- Monitor GitHub Security Advisories
- Subscribe to security mailing lists
- Regular dependency updates
- Prompt patching of vulnerabilities

## 🚀 Deployment Security

### Local Deployment (Recommended)
- Run only on localhost
- No external access
- Personal use only

### Network Deployment (Advanced)
If exposing to network:
1. Use HTTPS/TLS certificates
2. Implement authentication
3. Use firewall rules
4. Monitor access logs
5. Regular security audits

### Container Security
If using Docker:
```dockerfile
# Use specific versions
FROM python:3.9-slim

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Copy only necessary files
COPY --chown=appuser:appuser . /app
```

## 📝 Security Audit Log

Keep track of security-related changes:

### Version 3.0
- Removed hardcoded API key from tracker.py
- Implemented environment variable usage
- Added input validation for activities
- Improved error handling to not expose internals

### Future Improvements
- [ ] Add encryption for CSV storage
- [ ] Implement API key rotation
- [ ] Add rate limiting for API calls
- [ ] Create security test suite
- [ ] Add authentication to web interface

## 🆘 Incident Response

If a security issue is discovered:

1. **Assess** the impact and scope
2. **Contain** the issue (revoke keys, patch code)
3. **Notify** affected users if applicable
4. **Fix** the vulnerability
5. **Document** lessons learned
6. **Update** security measures

## 📚 Resources

- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Best Practices](https://python.plainenglish.io/python-security-best-practices)
- [Streamlit Security](https://docs.streamlit.io/knowledge-base/deploy/security)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)

---

Remember: Security is everyone's responsibility. When in doubt, ask for help!