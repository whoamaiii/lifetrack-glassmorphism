# Changelog

All notable changes to Personal Life Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2024-01-15

### 🎉 Major Architecture Refactor

This release introduces a professional software architecture with complete separation of concerns.

### Added
- **logic.py**: New centralized business logic module
  - All core functionality in one place
  - Type hints throughout
  - Comprehensive error handling
  - Extensive documentation
  
- **cli.py**: New dedicated CLI interface
  - Cleaner command structure
  - Better error messages
  - Colored output with emojis
  - Help text improvements

- **Professional Documentation**:
  - README.md with architecture overview
  - API_REFERENCE.md with complete function documentation
  - DATA_SCHEMA.md with detailed data format specs
  - CONTRIBUTING.md with contribution guidelines
  - SECURITY.md with security best practices
  - CHANGELOG.md (this file)

### Changed
- **streamlit_app.py**: Refactored to use logic.py
  - Removed duplicate business logic
  - Imports all functionality from core module
  - Cleaner, more maintainable code
  - English UI text throughout

- **Data Format**: Standardized to English
  - Column names now in English
  - Activity names in English
  - Backwards compatible with existing data

### Deprecated
- **main.py**: Original combined implementation
  - Functionality split between logic.py and cli.py
  - Kept for backwards compatibility
  
- **tracker.py**: Original Norwegian version
  - Core logic moved to logic.py
  - Contains hardcoded API key (security issue)
  
- **analyser.py**: Original analysis tool
  - Functionality integrated into logic.py
  - Charts available in both CLI and web interfaces

### Fixed
- Security: API key no longer hardcoded
- Performance: Optimized data loading and processing
- UI: Consistent styling across interfaces
- Errors: Better error messages and handling

### Security
- Removed hardcoded API key from tracker.py
- Added environment variable requirement
- Created comprehensive security documentation
- Added input validation

## [2.0.0] - 2024-01-10

### Added
- Web interface using Streamlit
- Interactive Plotly charts
- Real-time data updates
- Mobile-friendly responsive design
- Date filtering capabilities
- Activity filtering
- run_webapp.sh launcher script

### Changed
- Improved AI parsing accuracy
- Better error handling
- Enhanced UI with animations

## [1.5.0] - 2024-01-05

### Added
- Command-line argument parsing
- Graph visualizations with matplotlib
- Timeline analysis features
- Daily summaries
- Weekly averages

### Changed
- Restructured into main.py
- Added argparse for better CLI
- Improved data analysis functions

## [1.0.0] - 2024-01-01

### Initial Release
- Basic activity tracking
- AI-powered natural language parsing
- CSV data storage
- Norwegian language interface
- Simple text-based analysis

---

## Upgrade Guide

### From 2.x to 3.0

1. **Update imports in custom scripts**:
   ```python
   # Old
   from main import log_activity
   
   # New
   from logic import log_activity
   ```

2. **Use new CLI interface**:
   ```bash
   # Old
   python main.py log "activity"
   
   # New (same syntax, different file)
   python cli.py log "activity"
   ```

3. **Environment variables**:
   - Ensure OPENROUTER_API_KEY is set
   - Remove any hardcoded keys

### From 1.x to 3.0

1. **Data migration**:
   - Your livslogg.csv is compatible
   - Column names will auto-translate
   - No action required

2. **Update commands**:
   ```bash
   # Old interactive mode
   python tracker.py
   
   # New CLI mode
   python cli.py log "your activity"
   ```

3. **Set API key**:
   ```bash
   export OPENROUTER_API_KEY='your-key'
   ```