# 🛠️ Developer Guide - Personal Life Tracker

> **Make this codebase easy to understand and maintain**

This guide provides everything you need to understand, modify, and maintain the Personal Life Tracker application.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [Data Flow](#data-flow)
5. [Development Setup](#development-setup)
6. [Code Standards](#code-standards)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenRouter API key (for AI features)
- Basic understanding of Python, pandas, and Streamlit

### 5-Minute Setup
```bash
# 1. Clone and navigate
cd personal-life-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env with your OpenRouter API key

# 4. Test the CLI
python3 cli.py --help

# 5. Launch web app
python3 -m streamlit run streamlit_app.py
```

---

## 🏗️ Architecture Overview

### Design Philosophy
The application follows **separation of concerns** with a clean 3-layer architecture:

```
┌─────────────────┐    ┌─────────────────┐
│   Interfaces    │    │   Interfaces    │
│                 │    │                 │
│   cli.py        │    │ streamlit_app.py│
│   (Terminal)    │    │   (Web App)     │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
          ┌─────────────────┐
          │   Core Logic    │
          │                 │
          │   logic.py      │
          │ (Business Logic)│
          └─────────┬───────┘
                    │
          ┌─────────────────┐
          │   Data Layer    │
          │                 │
          │  livslogg.csv   │
          │ (Data Storage)  │
          └─────────────────┘
```

### Why This Architecture?

1. **🔄 DRY (Don't Repeat Yourself)**: All business logic is centralized in `logic.py`
2. **🔧 Easy Maintenance**: Fix bugs in one place, and both interfaces benefit
3. **📱 Multiple Interfaces**: Easy to add new interfaces (mobile app, API, etc.)
4. **🧪 Testable**: Core logic is isolated and can be tested independently
5. **📖 Clear Separation**: Each file has a single, clear responsibility

---

## 🧩 Core Components

### 1. `logic.py` - The Brain 🧠
**Purpose**: Contains all business logic and data processing
**Key Responsibilities**:
- AI integration for parsing natural language
- Data validation and cleaning
- CSV file management
- Analysis and visualization helpers
- All mathematical calculations

**When to modify**: When adding new features, changing data processing, or fixing bugs

### 2. `cli.py` - Terminal Interface 📱
**Purpose**: Command-line interface for power users
**Key Responsibilities**:
- Argument parsing
- User interaction in terminal
- Calling functions from `logic.py`
- Formatting output for terminal

**When to modify**: When changing CLI commands, adding new CLI features, or improving terminal UX

### 3. `streamlit_app.py` - Web Interface 🌐
**Purpose**: Browser-based interface for visual users
**Key Responsibilities**:
- Web UI components
- Interactive charts and graphs
- User input handling
- Calling functions from `logic.py`
- Session state management

**When to modify**: When changing web UI, adding new visualizations, or improving user experience

---

## 📊 Data Flow

### Input Processing Flow
```
User Input → AI Analysis → Data Extraction → Validation → CSV Storage
```

1. **User Input**: Natural language (e.g., "drank 500ml water")
2. **AI Analysis**: OpenRouter API processes the text
3. **Data Extraction**: Structured data extracted (activity, quantity, unit)
4. **Validation**: Data types and formats validated
5. **CSV Storage**: Data appended to `livslogg.csv`

### Analysis Flow
```
CSV Data → Data Loading → Column Mapping → Analysis → Visualization
```

1. **CSV Data**: Raw data from `livslogg.csv`
2. **Data Loading**: `load_data()` function processes CSV
3. **Column Mapping**: Norwegian ↔ English column names
4. **Analysis**: Aggregations, filtering, calculations
5. **Visualization**: Charts, graphs, tables

---

## 💻 Development Setup

### Environment Setup
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### Environment Variables
Create `.env` file with:
```bash
# Required - Get from https://openrouter.ai/
OPENROUTER_API_KEY=your-api-key-here

# Optional - For debugging
DEBUG=true
LOG_LEVEL=INFO
```

### Development Tools
```bash
# Code formatting
pip install black isort

# Format code
black *.py
isort *.py

# Type checking
pip install mypy
mypy logic.py
```

---

## 📏 Code Standards

### Python Style Guide
- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names

### Function Documentation
```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
        
    Examples:
        >>> example_function("test", 5)
        True
    """
    # Implementation here
    pass
```

### Error Handling
```python
# Good: Specific error handling
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Specific error occurred: {e}")
    raise Exception(f"Failed to process: {e}")

# Bad: Generic error handling
try:
    result = risky_operation()
except:
    pass  # Never do this!
```

### Logging
```python
import logging

# Use throughout the codebase
logger = logging.getLogger(__name__)

# Log levels
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Something unexpected happened")
logger.error("An error occurred")
logger.critical("A critical error occurred")
```

---

## 🧪 Testing

### Manual Testing
```bash
# Test CLI functionality
python3 cli.py log "test activity"
python3 cli.py analyze --totals

# Test web app
python3 -m streamlit run streamlit_app.py

# Test core logic
python3 -c "from logic import load_data; print(load_data())"
```

### Unit Testing (Future)
```bash
# Install testing framework
pip install pytest pytest-cov

# Run tests (when implemented)
pytest tests/
pytest --cov=logic tests/
```

### Integration Testing
```bash
# Test full workflow
echo "drank 500ml water" | python3 cli.py log
python3 cli.py analyze --today
```

---

## 🚀 Deployment

### Local Development
```bash
# CLI usage
python3 cli.py log "your activity"

# Web app
python3 -m streamlit run streamlit_app.py
```

### Production Deployment
```bash
# Using Streamlit Cloud
# 1. Push to GitHub
# 2. Connect to Streamlit Cloud
# 3. Deploy from repository

# Using Docker (create Dockerfile)
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Environment Configuration
- Development: Use `.env` file
- Production: Use environment variables or secrets management

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Failed to load data: 'timestamp'"
**Cause**: Column name mismatch between CSV and code
**Solution**: The `load_data()` function handles this automatically by mapping Norwegian → English column names

#### 2. "API key not found"
**Cause**: Missing or incorrect OpenRouter API key
**Solution**: 
```bash
# Check if API key is set
echo $OPENROUTER_API_KEY

# Set API key
export OPENROUTER_API_KEY=your-key-here
```

#### 3. "No module named 'streamlit'"
**Cause**: Missing dependencies
**Solution**:
```bash
pip install -r requirements.txt
```

#### 4. "Port already in use"
**Cause**: Streamlit port 8501 is occupied
**Solution**:
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

#### 5. Charts not displaying
**Cause**: No data in CSV file
**Solution**: Log some activities first using CLI or web interface

### Debugging Steps
1. Check Python version: `python3 --version`
2. Verify dependencies: `pip list`
3. Test API key: `python3 -c "from logic import validate_api_key; print(validate_api_key())"`
4. Check data file: `head livslogg.csv`
5. Test core functions: `python3 -c "from logic import load_data; print(load_data())"`

---

## 🤝 Contributing

### Before Making Changes
1. Read this guide thoroughly
2. Understand the architecture
3. Test your changes locally
4. Follow code standards

### Making Changes
1. **Small Changes**: Edit directly
2. **New Features**: Plan the changes first
3. **Bug Fixes**: Identify root cause first
4. **Refactoring**: Ensure no functionality is lost

### Change Process
1. Make your changes
2. Test thoroughly
3. Update documentation if needed
4. Commit with clear messages

### Git Commit Messages
```bash
# Good commit messages
git commit -m "fix: resolve column name mismatch in load_data()"
git commit -m "feat: add new visualization for weekly trends"
git commit -m "docs: update API integration guide"

# Bad commit messages
git commit -m "fix stuff"
git commit -m "update"
```

---

## 📚 Additional Resources

### Key Documentation Files
- `README.md` - Project overview and basic usage
- `DATA_STRUCTURE.md` - Data format and CSV structure
- `API_INTEGRATION.md` - OpenRouter API details
- `ARCHITECTURE.md` - Technical architecture deep dive

### External Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [OpenRouter API Docs](https://openrouter.ai/docs)

### Support
- Check existing issues in this repository
- Create new issues for bugs or feature requests
- Follow the code standards and contribution guidelines

---

## 📝 Notes for Maintainers

### Regular Maintenance Tasks
- [ ] Update dependencies monthly
- [ ] Review and update API key security
- [ ] Check for deprecated Streamlit features
- [ ] Monitor CSV file size and performance
- [ ] Update documentation when adding features

### Performance Considerations
- CSV file size: Consider database migration if > 100MB
- API rate limits: Monitor OpenRouter usage
- Memory usage: Profile with large datasets
- Streamlit performance: Cache expensive operations

---

*This guide is designed to make the Personal Life Tracker codebase maintainable and accessible to developers of all skill levels. Keep it updated as the project evolves!* 