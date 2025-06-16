# Contributing to Personal Life Tracker

Thank you for your interest in contributing to Personal Life Tracker! This document provides guidelines and instructions for contributing to the project.

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## 🚀 Getting Started

### Prerequisites

1. Python 3.8 or higher
2. Git for version control
3. A code editor (VS Code recommended)
4. An OpenRouter API key for testing

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/tracker.git
   cd tracker
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

5. **Set up environment variables**:
   ```bash
   export OPENROUTER_API_KEY='your-test-key'
   ```

## 📁 Project Structure

Understanding the architecture is crucial for contributing:

```
tracker/
├── logic.py           # Core business logic (main focus for features)
├── cli.py            # Command-line interface
├── streamlit_app.py  # Web interface
├── tests/            # Test files
│   ├── test_logic.py
│   ├── test_cli.py
│   └── test_web.py
└── docs/             # Documentation
```

### Key Principles

1. **Separation of Concerns**: Business logic in `logic.py`, presentation in interface files
2. **Type Safety**: Use type hints for all functions
3. **Documentation**: All functions must have docstrings
4. **Testing**: New features require tests

## 🔧 Development Workflow

### 1. Choose an Issue

- Check the [issue tracker](https://github.com/YOUR_REPO/tracker/issues)
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to claim it

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 3. Make Your Changes

Follow these guidelines:

#### Code Style

```python
# Good example
def calculate_weekly_average(df: pd.DataFrame, activity: str) -> float:
    """
    Calculate the weekly average for a specific activity.
    
    Args:
        df: DataFrame containing activity data
        activity: Name of the activity to calculate
        
    Returns:
        Weekly average quantity
        
    Raises:
        ValueError: If activity not found in data
    """
    if activity not in df['activity'].unique():
        raise ValueError(f"Activity '{activity}' not found in data")
    
    # Implementation here
    return average
```

#### Adding New Features

1. **Add business logic to `logic.py`**:
   ```python
   def new_analysis_function(df: pd.DataFrame) -> Dict:
       """Your new function with proper documentation."""
       # Implementation
       pass
   ```

2. **Update CLI if needed** in `cli.py`:
   ```python
   parser_analyze.add_argument(
       "--new-feature",
       action="store_true",
       help="Description of your feature"
   )
   ```

3. **Update Web UI if needed** in `streamlit_app.py`:
   ```python
   # Add new tab or feature to the interface
   ```

#### Adding New Activity Types

1. Update `ACTIVITY_CATEGORIES` in `logic.py`
2. Update AI prompt in `analyze_with_ai()`
3. Add examples to documentation
4. Update tests

### 4. Write Tests

Create tests for your changes:

```python
# tests/test_logic.py
def test_new_feature():
    """Test description."""
    # Arrange
    test_data = create_test_data()
    
    # Act
    result = new_function(test_data)
    
    # Assert
    assert result == expected_value
```

Run tests:
```bash
python -m pytest tests/
```

### 5. Update Documentation

- Update README.md if adding user-facing features
- Update API_REFERENCE.md for new functions
- Update inline documentation (docstrings)
- Add examples where appropriate

### 6. Commit Your Changes

Follow conventional commit format:

```bash
# Features
git commit -m "feat: add weekly average calculation"

# Bug fixes
git commit -m "fix: handle empty dataframes in totals calculation"

# Documentation
git commit -m "docs: add examples for new analysis features"

# Refactoring
git commit -m "refactor: extract common validation logic"

# Tests
git commit -m "test: add tests for edge cases in AI parsing"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what was changed and why
- Reference to any related issues
- Screenshots for UI changes

## 🧪 Testing Guidelines

### Test Structure

```python
def test_function_name_describes_scenario():
    """Test that function behaves correctly in specific scenario."""
    # Follow Arrange-Act-Assert pattern
```

### Test Categories

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test component interactions
3. **UI Tests**: Test Streamlit components (when applicable)

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_logic.py

# Run tests matching pattern
python -m pytest -k "test_analyze"
```

## 📝 Documentation Standards

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of function.
    
    Longer description if needed, explaining the purpose
    and any important details.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
        
    Example:
        >>> result = function_name(value1, value2)
        >>> print(result)
        expected_output
    """
```

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Installation steps (if changed)
- Configuration options

## 🐛 Bug Reports

When reporting bugs, include:

1. **Environment**:
   - Python version
   - OS (Windows/Mac/Linux)
   - Package versions (`pip freeze`)

2. **Steps to Reproduce**:
   - Exact commands/actions
   - Input data (if applicable)
   - Expected vs actual behavior

3. **Error Messages**:
   - Full traceback
   - Screenshots if UI-related

## 💡 Feature Requests

For feature requests, provide:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other ways to achieve the goal
4. **Examples**: Mock-ups or examples from other tools

## 🔍 Code Review Process

Pull requests will be reviewed for:

1. **Functionality**: Does it work as intended?
2. **Code Quality**: Is it clean and maintainable?
3. **Testing**: Are there adequate tests?
4. **Documentation**: Is it well-documented?
5. **Performance**: No significant performance regressions
6. **Security**: No security vulnerabilities introduced

## 🎯 Areas for Contribution

### High Priority

- [ ] Add data export features (JSON, Excel)
- [ ] Implement data visualization improvements
- [ ] Add more activity categories
- [ ] Improve AI parsing accuracy
- [ ] Add data validation features

### Good First Issues

- [ ] Add input validation for edge cases
- [ ] Improve error messages
- [ ] Add more examples to documentation
- [ ] Create additional chart types
- [ ] Add keyboard shortcuts to web UI

### Advanced Features

- [ ] Multi-user support
- [ ] Data synchronization
- [ ] Mobile app development
- [ ] REST API implementation
- [ ] Plugin system

## 📞 Getting Help

- Open an issue for bugs or features
- Join discussions in existing issues
- Ask questions in pull requests
- Email maintainers for sensitive issues

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in commit messages

Thank you for contributing to Personal Life Tracker! 🎉