# Personal Life Tracker - Test Suite Documentation

## 📋 Overview

This test suite provides comprehensive coverage for the Personal Life Tracker application, ensuring reliability and correctness across all components.

## 🏗️ Test Structure

```
tests/
├── __init__.py                    # Package initializer
├── conftest.py                    # Shared fixtures and configuration
├── test_logic.py                  # Core business logic tests (22 test classes, 50+ tests)
├── test_cli.py                    # CLI interface tests (5 test classes, 20+ tests)
├── test_streamlit_app.py          # Web interface tests (6 test classes, 15+ tests)
├── test_integration.py            # End-to-end tests (4 test classes, 10+ tests)
└── fixtures/                      # Test data and mock responses
    ├── sample_data.csv            # Sample activity data
    └── mock_responses.json        # Mock API responses
```

## 🚀 Running Tests

### Quick Start
```bash
# Run all tests with coverage
pytest

# Or use the test runner script
./run_tests.sh
```

### Test Runner Options
```bash
./run_tests.sh all          # All tests with coverage (default)
./run_tests.sh unit         # Unit tests only
./run_tests.sh integration  # Integration tests only
./run_tests.sh quick        # Tests without coverage
./run_tests.sh specific <path>  # Run specific test
./run_tests.sh watch        # Watch mode (auto-rerun)
./run_tests.sh debug        # With debugger
./run_tests.sh coverage     # Detailed coverage report
```

### Direct pytest Commands
```bash
# Run specific test file
pytest tests/test_logic.py

# Run specific test class
pytest tests/test_logic.py::TestConfigurationManagement

# Run specific test
pytest tests/test_logic.py::TestConfigurationManagement::test_load_config_default

# Run with markers
pytest -m "not slow"        # Skip slow tests
pytest -m integration       # Only integration tests
pytest -m "api"            # Only API-related tests

# Verbose output
pytest -v

# With coverage
pytest --cov=. --cov-report=html
```

## 📊 Test Categories

### 1. **Unit Tests** (`test_logic.py`, `test_cli.py`, `test_streamlit_app.py`)
- Test individual functions in isolation
- Mock external dependencies (API, file I/O)
- Fast execution
- High coverage of edge cases

### 2. **Integration Tests** (`test_integration.py`)
- Test complete workflows
- Minimal mocking
- Verify component interactions
- Test data persistence

### 3. **Test Organization**

#### test_logic.py (Core Logic Tests)
- **TestConfigurationManagement**: Config file operations
- **TestActivityLogging**: AI analysis and logging
- **TestDataLoading**: CSV loading and cleaning
- **TestAnalysisFunctions**: Data analysis operations
- **TestUtilityFunctions**: Helper functions
- **TestVisualizationHelpers**: Chart data preparation
- **TestEdgeCases**: Performance and edge cases

#### test_cli.py (CLI Tests)
- **TestLogCommand**: Activity logging via CLI
- **TestConfigCommand**: Configuration management
- **TestAnalyzeCommand**: Analysis operations
- **TestMainFunction**: Argument parsing
- **TestErrorHandling**: Error scenarios

#### test_streamlit_app.py (Web Interface Tests)
- **TestSessionStateManagement**: Data caching
- **TestMainAppFlow**: Application initialization
- **TestActivityLogging**: Web-based logging
- **TestDataFiltering**: Filter operations
- **TestVisualizationData**: Chart preparation
- **TestErrorHandling**: Web error handling

#### test_integration.py (Integration Tests)
- **TestFullWorkflow**: Complete user workflows
- **TestCrossInterfaceCompatibility**: CLI/Web interop
- **TestDataPersistence**: Data storage reliability
- **TestErrorRecovery**: Failure handling

## 🔧 Test Fixtures (conftest.py)

### Key Fixtures

1. **mock_api_key**: Valid test API key
2. **sample_activities**: List of test activities
3. **temp_csv_file**: Temporary CSV for testing
4. **sample_dataframe**: Pre-populated DataFrame
5. **mock_api_response**: API response generator
6. **temp_config_file**: Temporary config.json
7. **mock_requests**: Mocked requests library

### Usage Example
```python
def test_example(sample_activities, temp_csv_file):
    # Fixtures are automatically injected
    assert len(sample_activities) > 0
    assert not temp_csv_file.exists()
```

## 📈 Coverage Goals

- **Target**: 90%+ for `logic.py`, 80%+ overall
- **Current**: Run `pytest --cov` to check
- **Report**: HTML report in `htmlcov/index.html`

### Coverage Commands
```bash
# Generate coverage report
pytest --cov=. --cov-report=html

# View coverage in terminal
pytest --cov=. --cov-report=term-missing

# Generate multiple formats
pytest --cov=. --cov-report=html --cov-report=xml --cov-report=json
```

## 🏷️ Test Markers

Tests are marked for easy filtering:

- `@pytest.mark.slow`: Long-running tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.api`: Tests requiring API mocking
- `@pytest.mark.file_io`: File operation tests
- `@pytest.mark.visualization`: Visualization tests

### Using Markers
```bash
# Skip slow tests
pytest -m "not slow"

# Run only API tests
pytest -m api

# Combine markers
pytest -m "unit and not slow"
```

## 🐛 Debugging Tests

### Using pytest debugger
```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Use IPython debugger
pytest --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### Print debugging
```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l
```

## 💡 Best Practices

1. **Test Naming**: Use descriptive names that explain what is being tested
   ```python
   def test_load_data_with_norwegian_columns_converts_to_english():
       # Clear test purpose from name
   ```

2. **Arrange-Act-Assert**: Structure tests clearly
   ```python
   def test_example():
       # Arrange
       data = create_test_data()
       
       # Act
       result = process_data(data)
       
       # Assert
       assert result.success is True
   ```

3. **One Assertion Per Test**: Keep tests focused
4. **Use Fixtures**: Don't repeat setup code
5. **Mock External Dependencies**: Keep tests fast and reliable
6. **Test Edge Cases**: Empty data, invalid input, etc.

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure project root is in PYTHONPATH
   export PYTHONPATH=$PYTHONPATH:.
   ```

2. **Fixture Not Found**
   - Check fixture is defined in `conftest.py`
   - Ensure `conftest.py` is in test directory

3. **Test Discovery Issues**
   - Test files must start with `test_`
   - Test functions must start with `test_`
   - Test classes must start with `Test`

4. **Coverage Missing Files**
   - Check `.coveragerc` configuration
   - Ensure source files are imported in tests

## 📝 Adding New Tests

1. **Choose the right test file** based on what you're testing
2. **Create a test class** for related tests
3. **Use appropriate fixtures** from `conftest.py`
4. **Add docstrings** explaining the test purpose
5. **Run the test** to ensure it works
6. **Check coverage** to ensure new code is tested

### Example Template
```python
class TestNewFeature:
    """Tests for the new feature functionality."""
    
    def test_feature_happy_path(self, sample_activities):
        """
        Test the feature with valid input.
        Should process correctly and return expected result.
        """
        # Arrange
        input_data = sample_activities[:2]
        
        # Act
        result = new_feature(input_data)
        
        # Assert
        assert result is not None
        assert len(result) == 2
    
    def test_feature_error_handling(self):
        """
        Test the feature with invalid input.
        Should handle gracefully and raise appropriate error.
        """
        # Arrange
        invalid_data = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid input"):
            new_feature(invalid_data)
```

## 🎯 Goals

- ✅ High code coverage (90%+)
- ✅ Fast test execution (< 30 seconds)
- ✅ Reliable and deterministic
- ✅ Easy to understand and maintain
- ✅ Comprehensive error handling
- ✅ Good documentation

---

Happy Testing! 🧪✨