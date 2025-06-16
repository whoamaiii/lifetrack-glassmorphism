# ⚙️ Configuration Guide

> **Complete setup and configuration reference**

This document covers all configuration options for the Personal Life Tracker application.

## 📋 Table of Contents

1. [Quick Setup](#quick-setup)
2. [Environment Variables](#environment-variables)
3. [Configuration Files](#configuration-files)
4. [AI Provider Setup](#ai-provider-setup)
5. [Development Configuration](#development-configuration)
6. [Production Configuration](#production-configuration)
7. [Performance Tuning](#performance-tuning)
8. [Security Configuration](#security-configuration)

---

## ⚡ Quick Setup

### Minimal Configuration
Only one environment variable is required:

```bash
# Create .env file
echo "OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here" > .env
```

### Complete Setup
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit with your values
nano .env

# 3. Test configuration
python3 -c "from logic import validate_api_key; print('API Key Valid:', validate_api_key())"
```

---

## 🔧 Environment Variables

### Required Variables

#### `OPENROUTER_API_KEY`
- **Purpose**: Primary AI provider for natural language processing
- **Format**: `sk-or-v1-[your-key-here]`
- **Source**: https://openrouter.ai/
- **Example**: `OPENROUTER_API_KEY=sk-or-v1-abc123def456...`

### Optional AI Provider Variables

#### `OPENAI_API_KEY`
- **Purpose**: Alternative AI provider
- **Format**: `sk-[your-key-here]`
- **Source**: https://platform.openai.com/
- **Usage**: Set `AI_PROVIDER=openai` to use

#### `ANTHROPIC_API_KEY`
- **Purpose**: Alternative AI provider (Claude)
- **Format**: `sk-ant-[your-key-here]`
- **Source**: https://console.anthropic.com/
- **Usage**: Set `AI_PROVIDER=anthropic` to use

### Application Configuration

#### `DEBUG`
- **Purpose**: Enable detailed logging and debug features
- **Values**: `true`, `false`
- **Default**: `false`
- **Example**: `DEBUG=true`

#### `LOG_LEVEL`
- **Purpose**: Set logging verbosity
- **Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Default**: `INFO`
- **Example**: `LOG_LEVEL=DEBUG`

#### `AI_MODEL`
- **Purpose**: Specify AI model to use
- **Default**: `google/gemini-flash-1.5`
- **Examples**: 
  - `AI_MODEL=openai/gpt-4`
  - `AI_MODEL=anthropic/claude-3-sonnet`

#### `AI_PROVIDER`
- **Purpose**: Select AI provider
- **Values**: `openrouter`, `openai`, `anthropic`, `local`
- **Default**: `openrouter`
- **Example**: `AI_PROVIDER=openai`

### Data Configuration

#### `CSV_FILENAME`
- **Purpose**: Name of the data file
- **Default**: `livslogg.csv`
- **Example**: `CSV_FILENAME=my_activities.csv`

#### `BACKUP_DIR`
- **Purpose**: Directory for automatic backups
- **Default**: `./backups`
- **Example**: `BACKUP_DIR=/home/user/tracker_backups`

#### `BACKUP_FREQUENCY`
- **Purpose**: Automatic backup frequency in days
- **Default**: `7`
- **Example**: `BACKUP_FREQUENCY=1`

### Performance Configuration

#### `API_TIMEOUT`
- **Purpose**: Timeout for AI API requests (seconds)
- **Default**: `30`
- **Example**: `API_TIMEOUT=60`

#### `MAX_CSV_SIZE_MB`
- **Purpose**: Warning threshold for CSV file size
- **Default**: `100`
- **Example**: `MAX_CSV_SIZE_MB=500`

#### `AI_RATE_LIMIT`
- **Purpose**: Rate limiting for AI requests (per minute)
- **Default**: `60`
- **Example**: `AI_RATE_LIMIT=30`

### Web Application Configuration

#### `STREAMLIT_PORT`
- **Purpose**: Port for Streamlit web interface
- **Default**: `8501`
- **Example**: `STREAMLIT_PORT=8502`

#### `STREAMLIT_THEME`
- **Purpose**: Web interface theme
- **Values**: `light`, `dark`
- **Default**: `light`
- **Example**: `STREAMLIT_THEME=dark`

### Local AI Configuration

#### `OLLAMA_BASE_URL`
- **Purpose**: URL for local Ollama AI server
- **Default**: `http://localhost:11434/api`
- **Example**: `OLLAMA_BASE_URL=http://192.168.1.100:11434/api`

#### `OLLAMA_MODEL`
- **Purpose**: Local AI model name
- **Default**: `llama2`
- **Example**: `OLLAMA_MODEL=mistral`

---

## 📄 Configuration Files

### `.env` File
Primary configuration file for environment variables:

```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-your-key

# Optional
DEBUG=false
LOG_LEVEL=INFO
AI_MODEL=google/gemini-flash-1.5
```

### File Location
- **Development**: Project root directory
- **Production**: Secure location with proper permissions

### Security Notes
- Never commit `.env` to version control
- Use `.env.example` as a template
- Set proper file permissions: `chmod 600 .env`

---

## 🤖 AI Provider Setup

### OpenRouter (Recommended)
```bash
# 1. Sign up at https://openrouter.ai/
# 2. Create API key
# 3. Set environment variable
OPENROUTER_API_KEY=sk-or-v1-your-key
```

**Advantages**:
- Access to multiple models
- Cost-effective pricing
- Good rate limits
- Easy switching between models

### OpenAI Direct
```bash
# Configuration
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-key
AI_MODEL=gpt-4
```

**Advantages**:
- Direct access to GPT models
- Predictable performance
- Extensive documentation

### Anthropic Claude
```bash
# Configuration
AI_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key
AI_MODEL=claude-3-sonnet
```

**Advantages**:
- Excellent reasoning capabilities
- Long context windows
- Safety-focused responses

### Local AI (Ollama)
```bash
# Setup Ollama first
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2

# Configuration
AI_PROVIDER=local
OLLAMA_BASE_URL=http://localhost:11434/api
OLLAMA_MODEL=llama2
```

**Advantages**:
- No API costs
- Complete privacy
- No internet required
- Full control over models

---

## 🛠️ Development Configuration

### Recommended Development Setup
```bash
# Enable debugging
DEBUG=true
LOG_LEVEL=DEBUG

# Use fast, cheap model for testing
AI_MODEL=google/gemini-flash-1.5

# Enable test mode
TEST_MODE=true

# Smaller timeout for faster iteration
API_TIMEOUT=15
```

### Development Tools Integration
```bash
# Install development dependencies
pip install black isort mypy pytest

# Format code
black *.py
isort *.py

# Type checking
mypy logic.py

# Run tests
pytest tests/
```

### Local Testing
```bash
# Test AI integration
python3 -c "from logic import analyze_with_ai; print(analyze_with_ai('test input'))"

# Test data loading
python3 -c "from logic import load_data; print(load_data().head() if load_data() is not None else 'No data')"

# Test CLI
python3 cli.py --help

# Test web app
python3 -m streamlit run streamlit_app.py --server.port 8502
```

---

## 🚀 Production Configuration

### Security-First Setup
```bash
# Minimal logging for security
LOG_LEVEL=WARNING

# Disable debug mode
DEBUG=false

# Use stable, reliable model
AI_MODEL=google/gemini-flash-1.5

# Enable security features
FORCE_HTTPS=true
SESSION_SECRET=your-random-secret-key
```

### Performance Optimization
```bash
# Optimize for production load
API_TIMEOUT=30
AI_RATE_LIMIT=100
MAX_CSV_SIZE_MB=1000

# Enable automatic backups
BACKUP_FREQUENCY=1
BACKUP_DIR=/secure/backup/location
```

### Deployment Configuration
```bash
# Environment-specific settings
ENVIRONMENT=production
STREAMLIT_PORT=80
STREAMLIT_THEME=light

# Monitoring
ANALYTICS_ENABLED=true
HEALTH_CHECK_ENABLED=true
```

---

## ⚡ Performance Tuning

### For High Usage
```bash
# Increase rate limits
AI_RATE_LIMIT=200

# Longer timeout for stability
API_TIMEOUT=60

# Efficient model selection
AI_MODEL=google/gemini-flash-1.5  # Fast and cost-effective
```

### For Large Datasets
```bash
# Higher CSV size limit
MAX_CSV_SIZE_MB=1000

# More frequent backups
BACKUP_FREQUENCY=1

# Consider database migration
DATABASE_URL=sqlite:///livslogg.db
```

### For Cost Optimization
```bash
# Use cheapest effective model
AI_MODEL=google/gemini-flash-1.5

# Limit rate to control costs
AI_RATE_LIMIT=30

# Enable request caching (future feature)
ENABLE_CACHING=true
```

---

## 🔒 Security Configuration

### API Key Security
```bash
# Use environment variables, never hardcode
OPENROUTER_API_KEY=sk-or-v1-your-key

# Rotate keys regularly
# Set expiration dates in provider dashboard
# Monitor usage for anomalies
```

### File Permissions
```bash
# Secure .env file
chmod 600 .env

# Secure data files
chmod 640 livslogg.csv

# Secure backup directory
chmod 750 ./backups
```

### Production Security
```bash
# Force HTTPS in production
FORCE_HTTPS=true

# Use strong session secrets
SESSION_SECRET=$(openssl rand -base64 32)

# Disable debug features
DEBUG=false
TEST_MODE=false
```

### Network Security
```bash
# For server deployments, consider:
# - Firewall rules for API endpoints
# - VPN access for sensitive data
# - Rate limiting at network level
# - SSL/TLS certificates
```

---

## 🔧 Troubleshooting Configuration

### Common Issues

#### "API Key not found"
```bash
# Check environment variable
echo $OPENROUTER_API_KEY

# Verify .env file exists and has correct format
cat .env | grep OPENROUTER_API_KEY

# Test in Python
python3 -c "import os; print(os.getenv('OPENROUTER_API_KEY', 'NOT SET'))"
```

#### "Permission denied"
```bash
# Fix file permissions
chmod 600 .env
chmod +x cli.py
```

#### "Module not found"
```bash
# Install dependencies
pip install -r requirements.txt

# Check Python path
python3 -c "import sys; print(sys.path)"
```

#### "Port already in use"
```bash
# Use different port
STREAMLIT_PORT=8502

# Or kill existing process
lsof -ti:8501 | xargs kill -9
```

### Validation Scripts
```bash
# Test all configuration
python3 -c "
from logic import validate_api_key, load_data
print('API Key:', 'Valid' if validate_api_key() else 'Invalid')
print('Data File:', 'Found' if load_data() is not None else 'Missing')
print('Config complete!')
"
```

---

## 📝 Configuration Examples

### Example 1: Basic Personal Use
```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-your-key
```

### Example 2: Development Setup
```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-your-key
DEBUG=true
LOG_LEVEL=DEBUG
STREAMLIT_PORT=8502
```

### Example 3: Production Server
```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-your-key
LOG_LEVEL=WARNING
BACKUP_FREQUENCY=1
FORCE_HTTPS=true
SESSION_SECRET=your-secure-random-key
```

### Example 4: High-Performance Setup
```bash
# .env
OPENROUTER_API_KEY=sk-or-v1-your-key
AI_RATE_LIMIT=200
API_TIMEOUT=60
MAX_CSV_SIZE_MB=1000
BACKUP_DIR=/fast/ssd/backups
```

### Example 5: Local AI Setup
```bash
# .env
AI_PROVIDER=local
OLLAMA_BASE_URL=http://localhost:11434/api
OLLAMA_MODEL=llama2
DEBUG=true
```

---

*This configuration guide ensures your Personal Life Tracker is set up optimally for your specific use case, from development to production deployment.* 