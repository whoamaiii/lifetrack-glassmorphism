"""
Core Logic Tests
================

This module contains comprehensive tests for the core business logic in logic.py.
It tests all functions including configuration management, activity logging,
data loading, analysis functions, and utility functions.

Test Categories:
1. Configuration Management Tests
2. Activity Logging and AI Analysis Tests
3. Data Loading and Cleaning Tests
4. Analysis Function Tests
5. Visualization Helper Tests
6. Utility Function Tests

Each test is thoroughly documented with its purpose, setup, and expected outcomes.
"""

import pytest
import pandas as pd
import json
from datetime import datetime, date, timedelta
from pathlib import Path
import os
from unittest.mock import Mock, patch, MagicMock
import tempfile


class TestConfigurationManagement:
    """Tests for configuration-related functions."""
    
    def test_load_config_default(self, tmp_path, monkeypatch):
        """
        Test loading configuration when no config file exists.
        Should return default configuration values.
        """
        # Setup: Use temporary directory without config file
        monkeypatch.chdir(tmp_path)
        
        # Import after changing directory
        from logic import load_config
        
        # Execute
        config = load_config()
        
        # Assert: Should return default config
        assert config["api_key"] == ""
        assert config["api_url"] == "https://openrouter.ai/api/v1/chat/completions"
        assert config["model"] == "google/gemini-flash-1.5"
        assert config["csv_filename"] == "livslogg.csv"
    
    def test_load_config_existing(self, temp_config_file, monkeypatch):
        """
        Test loading configuration from existing config.json file.
        Should merge with defaults and return saved values.
        """
        # Setup: Change to directory with config file
        monkeypatch.chdir(temp_config_file.parent)
        monkeypatch.setattr("logic.CONFIG_FILE", Path("config.json"))
        
        from logic import load_config
        
        # Execute
        config = load_config()
        
        # Assert: Should load saved config
        assert config["api_key"].startswith("sk-or-v1-test")
        assert config["csv_filename"] == "test_livslogg.csv"
    
    def test_save_config_success(self, tmp_path, monkeypatch):
        """
        Test saving configuration to file.
        Should create/update config.json with provided data.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("logic.CONFIG_FILE", Path("config.json"))
        
        from logic import save_config
        
        test_config = {
            "api_key": "test-key-123",
            "model": "test-model",
            "csv_filename": "test.csv"
        }
        
        # Execute
        result = save_config(test_config)
        
        # Assert
        assert result is True
        assert Path("config.json").exists()
        
        # Verify saved content
        with open("config.json", 'r') as f:
            saved_data = json.load(f)
        assert saved_data["api_key"] == "test-key-123"
        assert saved_data["model"] == "test-model"
    
    def test_get_api_key_from_config(self, temp_config_file, monkeypatch):
        """
        Test retrieving API key from config file.
        Should prioritize config file over environment variable.
        """
        # Setup
        monkeypatch.chdir(temp_config_file.parent)
        monkeypatch.setattr("logic.CONFIG_FILE", Path("config.json"))
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
        
        from logic import get_api_key
        
        # Execute
        api_key = get_api_key()
        
        # Assert
        assert api_key.startswith("sk-or-v1-test")
    
    def test_get_api_key_from_env(self, tmp_path, monkeypatch):
        """
        Test retrieving API key from environment variable.
        Should use env var when config file doesn't have key.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("OPENROUTER_API_KEY", "env-test-key")
        
        from logic import get_api_key
        
        # Execute
        api_key = get_api_key()
        
        # Assert
        assert api_key == "env-test-key"
    
    def test_set_api_key(self, tmp_path, monkeypatch):
        """
        Test setting API key in configuration.
        Should save key to config file and be retrievable.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("logic.CONFIG_FILE", Path("config.json"))
        
        from logic import set_api_key, get_api_key
        
        # Execute
        result = set_api_key("new-test-key-456")
        
        # Assert
        assert result is True
        assert get_api_key() == "new-test-key-456"


class TestActivityLogging:
    """Tests for activity logging and AI analysis functions."""
    
    def test_log_activity_success(self, mock_env_vars, mock_requests, temp_csv_file, monkeypatch):
        """
        Test successful activity logging flow.
        Should analyze input, extract activities, and save to CSV.
        """
        # Setup
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import log_activity
        
        # Execute
        result = log_activity("drank 500ml of water and walked 2km")
        
        # Assert
        assert result is True
        assert temp_csv_file.exists()
        
        # Verify CSV content
        df = pd.read_csv(temp_csv_file)
        assert len(df) == 2
        assert df.iloc[0]['activity'] == 'Water'
        assert df.iloc[0]['quantity'] == 500
        assert df.iloc[1]['activity'] == 'Walk'
        assert df.iloc[1]['quantity'] == 2
    
    def test_log_activity_no_api_key(self, tmp_path, monkeypatch):
        """
        Test activity logging without API key.
        Should raise ValueError with appropriate message.
        """
        # Setup: No API key in env or config
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
        
        from logic import log_activity
        
        # Execute & Assert
        with pytest.raises(ValueError, match="API key is not set"):
            log_activity("test input")
    
    def test_analyze_with_ai_valid_response(self, mock_api_key, monkeypatch):
        """
        Test AI analysis with valid API response.
        Should parse activities correctly from AI response.
        """
        # Setup mock response
        def mock_post(url, **kwargs):
            class MockResponse:
                status_code = 200
                text = '{"choices": [{"message": {"content": "[{\\"activity\\": \\"Water\\", \\"quantity\\": 750, \\"unit\\": \\"ml\\"}]"}}]}'
                
                def json(self):
                    return json.loads(self.text)
                
                def raise_for_status(self):
                    pass
            
            return MockResponse()
        
        monkeypatch.setattr("requests.post", mock_post)
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        
        from logic import analyze_with_ai
        
        # Execute
        activities = analyze_with_ai("drank 750ml of water")
        
        # Assert
        assert len(activities) == 1
        assert activities[0]['activity'] == 'Water'
        assert activities[0]['quantity'] == 750
        assert activities[0]['unit'] == 'ml'
    
    def test_analyze_with_ai_empty_response(self, mock_api_key, monkeypatch):
        """
        Test AI analysis when no activities are detected.
        Should return empty list without error.
        """
        # Setup mock empty response
        def mock_post(url, **kwargs):
            class MockResponse:
                status_code = 200
                text = '{"choices": [{"message": {"content": "[]"}}]}'
                
                def json(self):
                    return json.loads(self.text)
                
                def raise_for_status(self):
                    pass
            
            return MockResponse()
        
        monkeypatch.setattr("requests.post", mock_post)
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        
        from logic import analyze_with_ai
        
        # Execute
        activities = analyze_with_ai("watched TV")
        
        # Assert
        assert activities == []
    
    def test_analyze_with_ai_network_error(self, mock_api_key, monkeypatch):
        """
        Test AI analysis with network error.
        Should raise exception with descriptive message.
        """
        # Setup mock network error
        def mock_post(url, **kwargs):
            raise Exception("Network error")
        
        monkeypatch.setattr("requests.post", mock_post)
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        
        from logic import analyze_with_ai
        
        # Execute & Assert
        with pytest.raises(Exception, match="AI analysis failed"):
            analyze_with_ai("test input")
    
    def test_save_to_csv_new_file(self, temp_csv_file, sample_activities, monkeypatch):
        """
        Test saving activities to new CSV file.
        Should create file with headers and data.
        """
        # Setup
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import save_to_csv
        
        # Execute
        result = save_to_csv(sample_activities[:2])
        
        # Assert
        assert result is True
        assert temp_csv_file.exists()
        
        # Verify content
        df = pd.read_csv(temp_csv_file)
        assert list(df.columns) == ['timestamp', 'activity', 'quantity', 'unit', 'date']
    
    def test_save_to_csv_append(self, temp_csv_file, sample_activities, monkeypatch):
        """
        Test appending activities to existing CSV file.
        Should add new rows without overwriting existing data.
        """
        # Setup: Create initial file
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import save_to_csv
        
        # First save
        save_to_csv(sample_activities[:2])
        
        # Execute: Second save (append)
        result = save_to_csv(sample_activities[2:4])
        
        # Assert
        assert result is True
        df = pd.read_csv(temp_csv_file)
        assert len(df) == 4  # 2 initial + 2 appended
        assert df.iloc[2]['activity'] == 'Food'


class TestDataLoading:
    """Tests for data loading and cleaning functions."""
    
    def test_load_data_valid_file(self, temp_csv_file, sample_activities, monkeypatch):
        """
        Test loading data from valid CSV file.
        Should return DataFrame with proper types and date column.
        """
        # Setup: Create CSV with test data
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import save_to_csv, load_data
        save_to_csv(sample_activities[:3])
        
        # Execute
        df = load_data()
        
        # Assert
        assert df is not None
        assert len(df) == 3
        assert 'date' in df.columns
        assert df['timestamp'].dtype == 'datetime64[ns]'
        assert df['quantity'].dtype == 'float64'
    
    def test_load_data_no_file(self, tmp_path, monkeypatch):
        """
        Test loading data when file doesn't exist.
        Should return None without error.
        """
        # Setup
        monkeypatch.setattr("logic.CSV_FILENAME", str(tmp_path / "nonexistent.csv"))
        
        from logic import load_data
        
        # Execute
        df = load_data()
        
        # Assert
        assert df is None
    
    def test_load_data_norwegian_columns(self, temp_csv_file, monkeypatch):
        """
        Test loading data with Norwegian column names.
        Should convert to English names for backward compatibility.
        """
        # Setup: Create CSV with Norwegian columns
        norwegian_data = """tidspunkt,aktivitet,mengde,enhet
2024-01-01T10:00:00,Vann,500,ml
2024-01-01T14:00:00,Gåtur,3,km"""
        
        temp_csv_file.write_text(norwegian_data)
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import load_data
        
        # Execute
        df = load_data()
        
        # Assert
        assert df is not None
        assert 'timestamp' in df.columns
        assert 'activity' in df.columns
        assert 'quantity' in df.columns
        assert 'unit' in df.columns
        assert len(df) == 2
    
    def test_load_data_invalid_rows(self, temp_csv_file, monkeypatch):
        """
        Test loading data with invalid rows.
        Should clean data by removing invalid entries.
        """
        # Setup: Create CSV with some invalid data
        invalid_data = """timestamp,activity,quantity,unit
2024-01-01T10:00:00,Water,500,ml
invalid-date,Walk,2,km
2024-01-01T14:00:00,Food,not-a-number,meal
2024-01-01T16:00:00,Cannabis,1,unit"""
        
        temp_csv_file.write_text(invalid_data)
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import load_data
        
        # Execute
        df = load_data()
        
        # Assert
        assert df is not None
        assert len(df) == 2  # Only valid rows remain
        assert df.iloc[0]['activity'] == 'Water'
        assert df.iloc[1]['activity'] == 'Cannabis'


class TestAnalysisFunctions:
    """Tests for data analysis functions."""
    
    def test_get_totals(self, sample_dataframe):
        """
        Test calculating total quantities per activity.
        Should return Series with summed quantities.
        """
        from logic import get_totals
        
        # Execute
        totals = get_totals(sample_dataframe)
        
        # Assert
        assert isinstance(totals, pd.Series)
        assert totals['Water'] == 800 * 7  # 800ml per day for 7 days
        assert totals['Walk'] == 3.5 * 4   # 3.5km every other day
        assert totals['Food'] == 7          # 1 meal per day
    
    def test_get_today_activities(self, sample_dataframe):
        """
        Test filtering activities for today only.
        Should return DataFrame with only today's entries.
        """
        from logic import get_today_activities
        
        # Execute
        today_df = get_today_activities(sample_dataframe)
        
        # Assert
        assert len(today_df) > 0  # Should have today's activities
        assert all(today_df['date'] == date.today())
        assert today_df['timestamp'].is_monotonic_increasing  # Should be sorted
    
    def test_get_date_range_activities(self, sample_dataframe):
        """
        Test filtering activities by date range.
        Should return activities within specified dates inclusive.
        """
        from logic import get_date_range_activities
        
        # Setup: Define date range
        end_date = date.today()
        start_date = end_date - timedelta(days=3)
        
        # Execute
        filtered_df = get_date_range_activities(sample_dataframe, start_date, end_date)
        
        # Assert
        assert len(filtered_df) > 0
        assert all(filtered_df['date'] >= start_date)
        assert all(filtered_df['date'] <= end_date)
    
    def test_get_date_range_activities_invalid_range(self, sample_dataframe):
        """
        Test date range filtering with invalid range.
        Should raise ValueError when start > end.
        """
        from logic import get_date_range_activities
        
        # Setup: Invalid range (start after end)
        start_date = date.today()
        end_date = date.today() - timedelta(days=5)
        
        # Execute & Assert
        with pytest.raises(ValueError, match="start_date.*must be before"):
            get_date_range_activities(sample_dataframe, start_date, end_date)
    
    def test_get_activity_timeline_daily(self, sample_dataframe):
        """
        Test generating daily timeline for specific activity.
        Should aggregate quantities by day.
        """
        from logic import get_activity_timeline
        
        # Execute
        timeline = get_activity_timeline(sample_dataframe, 'Water', 'day')
        
        # Assert
        assert len(timeline) == 7  # 7 days of data
        assert list(timeline.columns) == ['date', 'quantity']
        assert timeline['quantity'].iloc[0] == 800  # 500 + 300 ml per day
    
    def test_get_activity_timeline_invalid_activity(self, sample_dataframe):
        """
        Test timeline generation for non-existent activity.
        Should raise ValueError with helpful message.
        """
        from logic import get_activity_timeline
        
        # Execute & Assert
        with pytest.raises(ValueError, match="Activity 'InvalidActivity' not found"):
            get_activity_timeline(sample_dataframe, 'InvalidActivity')
    
    def test_get_data_summary(self, sample_dataframe):
        """
        Test generating comprehensive data summary.
        Should return dict with various statistics.
        """
        from logic import get_data_summary
        
        # Execute
        summary = get_data_summary(sample_dataframe)
        
        # Assert
        assert 'total_activities' in summary
        assert 'unique_activities' in summary
        assert 'date_range' in summary
        assert summary['total_activities'] == len(sample_dataframe)
        assert summary['unique_activities'] == 3  # Water, Walk, Food
        assert summary['date_range']['days_tracked'] >= 7


class TestUtilityFunctions:
    """Tests for utility and helper functions."""
    
    def test_validate_api_key_valid(self, mock_api_key, monkeypatch):
        """
        Test API key validation with valid key.
        Should return True for properly formatted key.
        """
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        
        from logic import validate_api_key
        
        # Execute & Assert
        assert validate_api_key() is True
    
    def test_validate_api_key_invalid(self, monkeypatch, tmp_path):
        """
        Test API key validation with invalid keys.
        Should return False for various invalid formats.
        """
        # Setup: Ensure we're in a clean directory without config
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("logic.CONFIG_FILE", Path("config.json"))
        
        from logic import validate_api_key
        
        # Test cases
        invalid_keys = [
            "",                    # Empty
            "invalid-key",        # Wrong format
            "sk-tooshort",        # Too short
            "api-key-123",        # Wrong prefix
        ]
        
        for key in invalid_keys:
            monkeypatch.setenv("OPENROUTER_API_KEY", key)
            assert validate_api_key() is False, f"Key '{key}' should be invalid"
    
    def test_get_available_activities(self, sample_dataframe):
        """
        Test extracting unique activities from DataFrame.
        Should return sorted list of activity names.
        """
        from logic import get_available_activities
        
        # Execute
        activities = get_available_activities(sample_dataframe)
        
        # Assert
        assert activities == ['Food', 'Walk', 'Water']  # Alphabetically sorted
    
    def test_get_available_activities_empty(self):
        """
        Test getting activities from empty DataFrame.
        Should return empty list without error.
        """
        from logic import get_available_activities
        
        # Execute
        activities = get_available_activities(pd.DataFrame())
        
        # Assert
        assert activities == []
    
    def test_format_activity_summary(self, sample_activities):
        """
        Test formatting activities for display.
        Should create readable multi-line string.
        """
        from logic import format_activity_summary
        
        # Execute
        summary = format_activity_summary(sample_activities[:3])
        
        # Assert
        assert "- Water: 500.0 ml" in summary
        assert "- Walk: 2.5 km" in summary
        assert "- Food: 1.0 meal" in summary
    
    def test_format_activity_summary_empty(self):
        """
        Test formatting empty activity list.
        Should return appropriate message.
        """
        from logic import format_activity_summary
        
        # Execute
        summary = format_activity_summary([])
        
        # Assert
        assert summary == "No activities logged yet."


class TestVisualizationHelpers:
    """Tests for visualization data preparation functions."""
    
    def test_create_totals_chart_data(self, sample_dataframe):
        """
        Test preparing data for totals bar chart.
        Should return parallel lists of activities and quantities.
        """
        from logic import create_totals_chart_data
        
        # Execute
        activities, quantities = create_totals_chart_data(sample_dataframe)
        
        # Assert
        assert len(activities) == len(quantities)
        assert 'Water' in activities
        assert 'Walk' in activities
        assert all(q > 0 for q in quantities)
    
    def test_create_timeline_chart_data(self, sample_dataframe):
        """
        Test preparing data for timeline chart.
        Should return parallel lists of dates and quantities.
        """
        from logic import create_timeline_chart_data
        
        # Execute
        dates, quantities = create_timeline_chart_data(sample_dataframe, 'Water')
        
        # Assert
        assert len(dates) == len(quantities)
        assert all(isinstance(d, date) for d in dates)
        assert all(q == 800 for q in quantities)  # 500 + 300 ml per day


class TestEdgeCases:
    """Tests for edge cases and error conditions."""
    
    def test_large_dataset_performance(self, temp_csv_file, monkeypatch):
        """
        Test performance with large dataset.
        Should handle 1000+ activities efficiently.
        """
        import time
        
        # Setup: Create large dataset
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import save_to_csv, load_data, get_totals
        
        # Generate 1000 activities
        large_activities = []
        for i in range(1000):
            large_activities.append({
                "activity": "Water" if i % 2 == 0 else "Walk",
                "quantity": 500 if i % 2 == 0 else 2,
                "unit": "ml" if i % 2 == 0 else "km"
            })
        
        # Save activities
        save_to_csv(large_activities)
        
        # Execute: Time the analysis
        start_time = time.time()
        df = load_data()
        totals = get_totals(df)
        end_time = time.time()
        
        # Assert
        assert len(df) == 1000
        assert end_time - start_time < 1.0  # Should complete in under 1 second
    
    def test_concurrent_file_access(self, temp_csv_file, sample_activities, monkeypatch):
        """
        Test handling concurrent file access.
        Should handle multiple saves gracefully.
        """
        import threading
        
        monkeypatch.setattr("logic.CSV_FILENAME", str(temp_csv_file))
        
        from logic import save_to_csv
        
        # Setup: Function to save activities
        results = []
        
        def save_activities():
            try:
                result = save_to_csv(sample_activities[:2])
                results.append(result)
            except Exception as e:
                results.append(e)
        
        # Execute: Run multiple saves concurrently
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=save_activities)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Assert: All saves should succeed
        assert all(r is True for r in results)
        
        # Verify file has data
        df = pd.read_csv(temp_csv_file)
        assert len(df) >= 2  # At least one save succeeded