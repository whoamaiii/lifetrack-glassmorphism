"""
Pytest Configuration and Shared Fixtures
========================================

This module provides shared test fixtures and configuration for all test modules.
It includes mock data, API responses, temporary files, and utility functions
that are used across multiple test files.

Fixtures:
- mock_api_key: Provides a valid test API key
- sample_activities: Returns a list of test activity dictionaries
- temp_csv_file: Creates a temporary CSV file for testing
- mock_api_response: Generates mock API responses
- sample_dataframe: Creates a test DataFrame with activity data
- temp_config_file: Creates a temporary config.json file
"""

import pytest
import pandas as pd
import json
import tempfile
from pathlib import Path
from datetime import datetime, date, timedelta
import os


@pytest.fixture
def mock_api_key():
    """
    Provides a mock API key for testing.
    
    Returns:
        str: A valid-format test API key
    """
    return "sk-or-v1-test1234567890abcdef1234567890abcdef1234567890abcdef1234567890"


@pytest.fixture
def sample_activities():
    """
    Provides sample activity data for testing.
    
    Returns:
        List[Dict]: A list of activity dictionaries with various types
    """
    return [
        {"activity": "Water", "quantity": 500, "unit": "ml"},
        {"activity": "Walk", "quantity": 2.5, "unit": "km"},
        {"activity": "Food", "quantity": 1, "unit": "meal"},
        {"activity": "Cannabis", "quantity": 1, "unit": "unit"},
        {"activity": "Cigarette", "quantity": 3, "unit": "unit"},
        {"activity": "Alcohol", "quantity": 2, "unit": "drinks"},
        {"activity": "Sex", "quantity": 1, "unit": "session"}
    ]


@pytest.fixture
def temp_csv_file(tmp_path):
    """
    Creates a temporary CSV file for testing file operations.
    
    Args:
        tmp_path: Pytest's temporary directory fixture
        
    Returns:
        Path: Path to the temporary CSV file
    """
    csv_file = tmp_path / "test_livslogg.csv"
    return csv_file


@pytest.fixture
def sample_dataframe():
    """
    Creates a sample DataFrame with test data.
    
    Returns:
        pd.DataFrame: DataFrame with activity data spanning multiple days
    """
    base_date = datetime.now()
    data = []
    
    # Create data for the last 7 days
    for days_ago in range(7):
        current_date = base_date - timedelta(days=days_ago)
        
        # Morning water
        data.append({
            'timestamp': current_date.replace(hour=8, minute=0),
            'activity': 'Water',
            'quantity': 500,
            'unit': 'ml'
        })
        
        # Walk
        if days_ago % 2 == 0:  # Every other day
            data.append({
                'timestamp': current_date.replace(hour=10, minute=30),
                'activity': 'Walk',
                'quantity': 3.5,
                'unit': 'km'
            })
        
        # Food
        data.append({
            'timestamp': current_date.replace(hour=12, minute=0),
            'activity': 'Food',
            'quantity': 1,
            'unit': 'meal'
        })
        
        # Evening water
        data.append({
            'timestamp': current_date.replace(hour=18, minute=0),
            'activity': 'Water',
            'quantity': 300,
            'unit': 'ml'
        })
    
    df = pd.DataFrame(data)
    df['date'] = df['timestamp'].dt.date
    return df


@pytest.fixture
def sample_dataframe_norwegian():
    """
    Creates a sample DataFrame with Norwegian column names for backward compatibility testing.
    
    Returns:
        pd.DataFrame: DataFrame with Norwegian column names
    """
    return pd.DataFrame({
        'tidspunkt': [datetime.now() - timedelta(days=i) for i in range(3)],
        'aktivitet': ['Vann', 'Gåtur', 'Mat'],
        'mengde': [500, 5, 1],
        'enhet': ['ml', 'km', 'måltid']
    })


@pytest.fixture
def mock_api_response():
    """
    Creates mock API responses for testing AI analysis.
    
    Returns:
        Dict: Function that generates different API responses based on input
    """
    def _generate_response(scenario="success"):
        """Generate API response based on scenario."""
        
        if scenario == "success":
            return {
                "choices": [{
                    "message": {
                        "content": json.dumps([
                            {"activity": "Water", "quantity": 500, "unit": "ml"},
                            {"activity": "Walk", "quantity": 2, "unit": "km"}
                        ])
                    }
                }]
            }
        elif scenario == "empty":
            return {
                "choices": [{
                    "message": {
                        "content": "[]"
                    }
                }]
            }
        elif scenario == "invalid_json":
            return {
                "choices": [{
                    "message": {
                        "content": "This is not valid JSON"
                    }
                }]
            }
        elif scenario == "missing_fields":
            return {
                "choices": [{
                    "message": {}
                }]
            }
        else:
            raise ValueError(f"Unknown scenario: {scenario}")
    
    return _generate_response


@pytest.fixture
def temp_config_file(tmp_path, mock_api_key):
    """
    Creates a temporary config.json file for testing.
    
    Args:
        tmp_path: Pytest's temporary directory fixture
        mock_api_key: Mock API key fixture
        
    Returns:
        Path: Path to the temporary config file
    """
    config_file = tmp_path / "config.json"
    config_data = {
        "api_key": mock_api_key,
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "google/gemini-flash-1.5",
        "csv_filename": "test_livslogg.csv"
    }
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    return config_file


@pytest.fixture
def mock_env_vars(monkeypatch, mock_api_key):
    """
    Sets up mock environment variables for testing.
    
    Args:
        monkeypatch: Pytest's monkeypatch fixture
        mock_api_key: Mock API key fixture
    """
    monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
    yield
    # Cleanup happens automatically with monkeypatch


@pytest.fixture
def mock_requests(monkeypatch, mock_api_response):
    """
    Mocks the requests library for API testing.
    
    Args:
        monkeypatch: Pytest's monkeypatch fixture
        mock_api_response: Mock API response generator
    """
    class MockResponse:
        def __init__(self, json_data, status_code=200):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json.dumps(json_data) if isinstance(json_data, dict) else str(json_data)
        
        def json(self):
            return self.json_data
        
        def raise_for_status(self):
            if self.status_code >= 400:
                raise Exception(f"HTTP {self.status_code}")
    
    def mock_post(url, **kwargs):
        # Default to success scenario
        return MockResponse(mock_api_response("success"))
    
    monkeypatch.setattr("requests.post", mock_post)
    return mock_post


@pytest.fixture(autouse=True)
def reset_imports():
    """
    Ensures clean imports for each test by clearing module cache.
    This prevents state leakage between tests.
    """
    import sys
    modules_to_reset = ['logic', 'cli', 'streamlit_app']
    for module in modules_to_reset:
        if module in sys.modules:
            del sys.modules[module]
    yield