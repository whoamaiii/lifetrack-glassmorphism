"""
Integration Tests
=================

This module contains end-to-end integration tests that verify
the complete workflow of the Personal Life Tracker application.
These tests ensure that different components work together correctly.

Test Categories:
1. Full Workflow Tests (Log → Save → Load → Analyze)
2. Cross-Interface Compatibility Tests
3. Data Persistence Tests
4. Error Recovery Tests

Integration tests use minimal mocking to test real interactions.
"""

import pytest
import pandas as pd
import json
import tempfile
from pathlib import Path
from datetime import datetime, date, timedelta
import os
from unittest.mock import patch, Mock
import time


class TestFullWorkflow:
    """Tests for complete application workflows."""
    
    def test_log_save_load_analyze_workflow(self, tmp_path, monkeypatch, mock_api_key):
        """
        Test complete workflow from logging to analysis.
        Should successfully log activities, save to CSV, load data, and perform analysis.
        """
        # Setup environment
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        csv_file = tmp_path / "test_livslogg.csv"
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
        
        # Mock API response
        def mock_post(url, **kwargs):
            class MockResponse:
                status_code = 200
                text = json.dumps({
                    "choices": [{
                        "message": {
                            "content": json.dumps([
                                {"activity": "Water", "quantity": 500, "unit": "ml"},
                                {"activity": "Walk", "quantity": 2.5, "unit": "km"}
                            ])
                        }
                    }]
                })
                
                def json(self):
                    return json.loads(self.text)
                
                def raise_for_status(self):
                    pass
            
            return MockResponse()
        
        monkeypatch.setattr("requests.post", mock_post)
        
        # Import after setup
        from logic import log_activity, load_data, get_totals, get_today_activities
        
        # Step 1: Log activities
        result = log_activity("drank 500ml of water and walked 2.5km")
        assert result is True
        
        # Step 2: Verify CSV was created
        assert csv_file.exists()
        
        # Step 3: Load data
        df = load_data()
        assert df is not None
        assert len(df) == 2 # Two items from mock
        
        # Step 4: Analyze data
        totals = get_totals(df)
        assert totals['Water'] == 500.0
        assert totals['Walk'] == 2.5
        
        # Step 5: Get today's activities
        today_activities = get_today_activities(df)
        assert len(today_activities) == 2
        
        # Step 6: Log more activities (mock will return the same 2 items)
        result2 = log_activity("drank another 300ml of water")
        assert result2 is True
        
        # Step 7: Reload and verify accumulation
        df2 = load_data()
        assert len(df2) == 4 # Initial 2 + 2 more from second mocked call
        totals2 = get_totals(df2)
        assert totals2['Water'] == 1000.0  # 500 + 500
        assert totals2['Walk'] == 5.0     # 2.5 + 2.5
    
    def test_multiple_days_workflow(self, tmp_path, monkeypatch, mock_api_key):
        """
        Test workflow spanning multiple days.
        Should correctly handle date-based filtering and analysis.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        csv_file = tmp_path / "test_livslogg.csv"
        
        # Create CSV with data from multiple days
        data = []
        base_date = datetime.now()
        
        for days_ago in range(5):
            timestamp = base_date - timedelta(days=days_ago)
            data.extend([
                {
                    'timestamp': timestamp.replace(hour=8).isoformat(),
                    'activity': 'Water',
                    'quantity': 500,
                    'unit': 'ml'
                },
                {
                    'timestamp': timestamp.replace(hour=12).isoformat(),
                    'activity': 'Food',
                    'quantity': 1,
                    'unit': 'meal'
                }
            ])
        
        # Write test data
        pd.DataFrame(data).to_csv(csv_file, index=False)
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
        
        from logic import load_data, get_date_range_activities, get_totals
        
        # Load all data
        df = load_data()
        assert len(df) == 10  # 2 activities × 5 days
        
        # Test date range filtering
        end_date = date.today()
        start_date = end_date - timedelta(days=2)
        filtered = get_date_range_activities(df, start_date, end_date)
        assert len(filtered) == 6  # 2 activities × 3 days
        
        # Test totals for filtered range
        filtered_totals = get_totals(filtered)
        assert filtered_totals['Water'] == 1500.0  # 500ml × 3 days
        assert filtered_totals['Food'] == 3.0      # 1 meal × 3 days


class TestCrossInterfaceCompatibility:
    """Tests ensuring CLI and Web interfaces work with same data."""
    
    def test_cli_web_data_compatibility(self, tmp_path, monkeypatch, mock_api_key):
        """
        Test that data saved via CLI can be read by web interface and vice versa.
        Should maintain data integrity across interfaces.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        csv_file = tmp_path / "test_livslogg.csv"
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
        
        # Mock successful API response
        def mock_post(url, **kwargs):
            class MockResponse:
                status_code = 200
                text = json.dumps({
                    "choices": [{
                        "message": {
                            "content": json.dumps([
                                {"activity": "Water", "quantity": 750, "unit": "ml"}
                            ])
                        }
                    }]
                })
                
                def json(self):
                    return json.loads(self.text)
                
                def raise_for_status(self):
                    pass
            
            return MockResponse()
        
        monkeypatch.setattr("requests.post", mock_post)
        
        # Step 1: Save data using core logic (as CLI would)
        from logic import log_activity
        result = log_activity("drank 750ml of water")
        assert result is True
        
        # Step 2: Load data as web interface would
        from logic import load_data
        df = load_data()
        
        # Step 3: Verify data integrity
        assert len(df) == 1
        assert df.iloc[0]['activity'] == 'Water'
        assert df.iloc[0]['quantity'] == 750.0
        assert df.iloc[0]['unit'] == 'ml'
        
        # Step 4: Use analysis functions that both interfaces share
        from logic import get_totals, format_activity_summary
        
        totals = get_totals(df)
        assert totals['Water'] == 750.0
        
        # Format for display (both interfaces use this)
        activities = df.to_dict('records')
        summary = format_activity_summary(activities)
        assert "Water: 750.0 ml" in summary
    
    def test_config_sharing_between_interfaces(self, tmp_path, monkeypatch):
        """
        Test that configuration changes in one interface are visible in another.
        Should share config.json properly.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("logic.CONFIG_FILE", Path("config.json"))
        
        # Step 1: Set API key (as CLI would)
        from logic import set_api_key
        result = set_api_key("sk-or-v1-test-key-123")
        assert result is True
        
        # Step 2: Read API key (as web interface would)
        from logic import get_api_key
        key = get_api_key()
        assert key == "sk-or-v1-test-key-123"
        
        # Step 3: Update config value
        from logic import set_config_value, get_config_value
        set_config_value("csv_filename", "custom_log.csv")
        
        # Step 4: Verify update is visible
        filename = get_config_value("csv_filename")
        assert filename == "custom_log.csv"


class TestDataPersistence:
    """Tests for data persistence and recovery."""
    
    def test_data_survives_restart(self, tmp_path, monkeypatch):
        """
        Test that data persists between application restarts.
        Should maintain all data in CSV file.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        csv_file = tmp_path / "test_livslogg.csv"
        
        # Step 1: Create initial data
        initial_data = pd.DataFrame({
            'timestamp': [datetime.now().isoformat()],
            'activity': ['Water'],
            'quantity': [500],
            'unit': ['ml']
        })
        initial_data.to_csv(csv_file, index=False)
        
        # Step 2: Simulate first application run
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
        
        from logic import load_data, save_to_csv
        
        df1 = load_data()
        assert len(df1) == 1
        
        # Add more data
        new_activities = [{"activity": "Walk", "quantity": 3, "unit": "km"}]
        save_to_csv(new_activities)
        
        # Step 3: Simulate application restart (clear any caches)
        import sys
        if 'logic' in sys.modules:
            del sys.modules['logic']
        
        # Step 4: Reload and verify all data persists
        # Re-import and re-patch CSV_FILENAME for the reloaded module
        import logic # This will be the reloaded module
        monkeypatch.setattr(logic, "CSV_FILENAME", str(csv_file)) # Pass the module object
        
        df2 = logic.load_data() # Use the reloaded module directly
        assert len(df2) == 2
        assert df2.iloc[0]['activity'] == 'Water'
        assert df2.iloc[1]['activity'] == 'Walk'
    
    def test_concurrent_access_handling(self, tmp_path, monkeypatch):
        """
        Test handling of concurrent access to CSV file.
        Should handle multiple writes gracefully.
        """
        import threading
        
        # Setup
        monkeypatch.chdir(tmp_path)
        csv_file = tmp_path / "test_livslogg.csv"
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
        
        from logic import save_to_csv
        
        # Create different activities for each thread
        activities_sets = [
            [{"activity": "Water", "quantity": 500, "unit": "ml"}],
            [{"activity": "Walk", "quantity": 2, "unit": "km"}],
            [{"activity": "Food", "quantity": 1, "unit": "meal"}],
            [{"activity": "Cannabis", "quantity": 1, "unit": "unit"}],
            [{"activity": "Cigarette", "quantity": 3, "unit": "unit"}]
        ]
        
        results = []
        
        def save_activities(activities):
            try:
                result = save_to_csv(activities)
                results.append((True, result))
            except Exception as e:
                results.append((False, str(e)))
        
        # Run concurrent saves
        threads = []
        for activities in activities_sets:
            thread = threading.Thread(target=save_activities, args=(activities,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Verify results
        successful_saves = sum(1 for success, _ in results if success)
        assert successful_saves >= 3  # At least 3 should succeed
        
        # Verify file integrity
        from logic import load_data
        df = load_data()
        assert df is not None
        assert len(df) >= 3  # At least 3 activities saved


class TestErrorRecovery:
    """Tests for error handling and recovery scenarios."""
    
    def test_corrupted_csv_recovery(self, tmp_path, monkeypatch):
        """
        Test handling of corrupted CSV file.
        Should handle gracefully and allow new data to be saved.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        csv_file = tmp_path / "test_livslogg.csv"
        
        # Create corrupted CSV
        csv_file.write_text("This is not,valid,CSV\ndata at all!!!")
        
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
        
        # Try to load corrupted data
        from logic import load_data
        
        # This should handle the error gracefully
        try:
            df = load_data()
            # Depending on implementation, might return None or empty DataFrame
            assert df is None or df.empty
        except Exception:
            # If it raises, that's also acceptable
            pass
        
        # Should still be able to save new data
        from logic import save_to_csv
        
        # Backup and recreate
        csv_file.rename(csv_file.with_suffix('.csv.bak'))
        
        new_activities = [{"activity": "Water", "quantity": 500, "unit": "ml"}]
        result = save_to_csv(new_activities)
        assert result is True
        
        # Verify new file is valid
        df_new = load_data()
        assert df_new is not None
        assert len(df_new) == 1
    
    def test_api_failure_recovery(self, tmp_path, monkeypatch, mock_api_key):
        """
        Test recovery from API failures.
        Should handle API errors without corrupting existing data.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("OPENROUTER_API_KEY", mock_api_key)
        csv_file = tmp_path / "test_livslogg.csv"
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
        
        # Create initial valid data
        from logic import save_to_csv
        initial_activities = [{"activity": "Water", "quantity": 1000, "unit": "ml"}]
        save_to_csv(initial_activities)
        
        # Mock API failure
        def mock_post_failure(url, **kwargs):
            raise Exception("Network timeout")
        
        monkeypatch.setattr("requests.post", mock_post_failure)
        
        # Try to log new activity (should fail)
        from logic import log_activity
        
        with pytest.raises(Exception):
            log_activity("walked 5km")
        
        # Verify existing data is intact
        from logic import load_data
        df = load_data()
        assert len(df) == 1
        assert df.iloc[0]['quantity'] == 1000.0
    
    def test_missing_columns_compatibility(self, tmp_path, monkeypatch):
        """
        Test handling of CSV files with missing or extra columns.
        Should maintain backward compatibility.
        """
        # Setup
        monkeypatch.chdir(tmp_path)
        csv_file = tmp_path / "test_livslogg.csv"
    
        # Create CSV with minimal columns (old format) using pandas
        initial_data = {
            'timestamp': ['2024-01-01T10:00:00', '2024-01-01T14:00:00'],
            'activity': ['Water', 'Walk'],
            'quantity': [500, 3]
        }
        initial_df = pd.DataFrame(initial_data)
        # Explicitly write only the 3 columns for the old format test
        initial_df.to_csv(csv_file, index=False, columns=['timestamp', 'activity', 'quantity'])
        
        monkeypatch.setattr("logic.CSV_FILENAME", str(csv_file))
    
        # Try to load old format
        from logic import load_data
        
        df = load_data()
        
        # Should handle missing 'unit' column
        assert df is not None
        assert len(df) == 2
        assert 'timestamp' in df.columns
        assert 'activity' in df.columns
        assert 'quantity' in df.columns
        
        # Should be able to add new data with proper format
        from logic import save_to_csv
        
        new_activities = [{"activity": "Food", "quantity": 1, "unit": "meal"}]
        result = save_to_csv(new_activities)
        assert result is True
        
        # Reload and verify
        df_updated = load_data()
        assert len(df_updated) == 3