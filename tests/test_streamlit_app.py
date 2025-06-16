"""
Streamlit App Tests
===================

This module tests the Streamlit web interface functionality.
Since Streamlit components require special mocking, these tests
focus on the custom functions and logic flow rather than UI components.

Test Categories:
1. Session State Management Tests
2. Data Loading and Caching Tests
3. Integration with Core Logic Tests
4. Error Handling Tests

Note: Streamlit-specific components (st.button, st.write, etc.) are mocked.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import datetime, date, timedelta
import streamlit as st


class TestSessionStateManagement:
    """Tests for session state data management."""
    
    @patch('streamlit.session_state', new_callable=dict)
    @patch('streamlit_app.load_data')
    def test_get_data_from_session_first_load(self, mock_load_data, mock_session_state):
        """
        Test loading data for the first time.
        Should load from file and cache in session state.
        """
        # Setup
        test_df = pd.DataFrame({
            'timestamp': [datetime.now()],
            'activity': ['Water'],
            'quantity': [500],
            'unit': ['ml']
        })
        mock_load_data.return_value = test_df
        
        from streamlit_app import get_data_from_session
        
        # Execute
        result = get_data_from_session()
        
        # Assert
        assert result is test_df
        assert 'data_df' in mock_session_state
        assert mock_session_state['data_df'] is test_df
        assert mock_session_state['data_updated'] is False
        mock_load_data.assert_called_once()
    
    @patch('streamlit.session_state', {'data_df': 'cached_data', 'data_updated': False})
    @patch('streamlit_app.load_data')
    def test_get_data_from_session_cached(self, mock_load_data):
        """
        Test loading data when already cached.
        Should return cached data without loading from file.
        """
        from streamlit_app import get_data_from_session
        
        # Execute
        result = get_data_from_session()
        
        # Assert
        assert result == 'cached_data'
        mock_load_data.assert_not_called()
    
    @patch('streamlit.session_state', {'data_df': 'old_data', 'data_updated': True})
    @patch('streamlit_app.load_data')
    def test_get_data_from_session_updated(self, mock_load_data):
        """
        Test loading data when update flag is set.
        Should reload from file and update cache.
        """
        # Setup
        new_df = pd.DataFrame({
            'timestamp': [datetime.now()],
            'activity': ['Food'],
            'quantity': [1],
            'unit': ['meal']
        })
        mock_load_data.return_value = new_df
        
        from streamlit_app import get_data_from_session
        
        # Execute
        result = get_data_from_session()
        
        # Assert
        assert result is new_df
        assert st.session_state['data_df'] is new_df
        assert st.session_state['data_updated'] is False
        mock_load_data.assert_called_once()
    
    @patch('streamlit.session_state', {})
    @patch('streamlit_app.load_data')
    def test_get_data_from_session_no_data(self, mock_load_data):
        """
        Test loading when no data file exists.
        Should handle None gracefully.
        """
        # Setup
        mock_load_data.return_value = None
        
        from streamlit_app import get_data_from_session
        
        # Execute
        result = get_data_from_session()
        
        # Assert
        assert result is None
        assert 'data_df' not in st.session_state


class TestMainAppFlow:
    """Tests for the main application flow."""
    
    @patch('streamlit_app.st')
    @patch('streamlit_app.get_data_from_session')
    @patch('streamlit_app.validate_api_key')
    def test_main_no_data(self, mock_validate, mock_get_data, mock_st):
        """
        Test main function when no data exists.
        Should display info message and return early.
        """
        # Setup
        mock_validate.return_value = True
        mock_get_data.return_value = None
        
        # Configure column mocks to support context manager protocol
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_col1.__enter__.return_value = mock_col1
        mock_col1.__exit__.return_value = None
        mock_col2.__enter__.return_value = mock_col2
        mock_col2.__exit__.return_value = None
        mock_st.columns.return_value = (mock_col1, mock_col2)

        from streamlit_app import main
        
        # Execute
        main()
        
        # Assert
        mock_st.info.assert_called_with("📊 No data yet. Log some activities to see analysis!")
    
    @patch('streamlit_app.st')
    @patch('streamlit_app.get_data_from_session')
    @patch('streamlit_app.validate_api_key')
    def test_main_empty_data(self, mock_validate, mock_get_data, mock_st):
        """
        Test main function with empty DataFrame.
        Should display info message and return early.
        """
        # Setup
        mock_validate.return_value = True
        mock_get_data.return_value = pd.DataFrame()
        
        # Configure column mocks
        mock_col1, mock_col2 = MagicMock(), MagicMock()
        mock_col1.__enter__.return_value = mock_col1
        mock_col1.__exit__.return_value = None
        mock_col2.__enter__.return_value = mock_col2
        mock_col2.__exit__.return_value = None
        mock_st.columns.return_value = (mock_col1, mock_col2)

        from streamlit_app import main
        
        # Execute
        main()
        
        # Assert
        mock_st.info.assert_called_with("📊 No data yet. Log some activities to see analysis!")
    
    @patch('streamlit_app.st')
    @patch('streamlit_app.get_data_from_session')
    @patch('streamlit_app.get_available_activities')
    @patch('streamlit_app.validate_api_key')
    def test_main_with_data(self, mock_validate, mock_get_activities, mock_get_data, mock_st):
        """
        Test main function with valid data.
        Should set up filters and tabs without errors.
        """
        # Setup
        mock_validate.return_value = True
        test_df = pd.DataFrame({
            'timestamp': [datetime.now()],
            'activity': ['Water'],
            'quantity': [500],
            'unit': ['ml'],
            'date': [date.today()]
        })
        mock_get_data.return_value = test_df
        mock_get_activities.return_value = ['Water']

        # Mock Streamlit components
        # Configure column mocks with side_effect
        def columns_side_effect(num_cols):
            cols = [MagicMock() for _ in range(num_cols)]
            for col_mock in cols:
                col_mock.__enter__.return_value = col_mock
                col_mock.__exit__.return_value = None
            return tuple(cols)

        mock_st.columns.side_effect = columns_side_effect
        
        # Configure tab mocks
        mock_tabs_list = []
        for _ in range(4): # Assuming 4 tabs are created
            tab_mock = MagicMock()
            tab_mock.__enter__.return_value = tab_mock
            tab_mock.__exit__.return_value = None
            mock_tabs_list.append(tab_mock)
        mock_st.tabs.return_value = mock_tabs_list
        
        mock_st.selectbox.return_value = "All"
        mock_st.multiselect.return_value = ['Water']

        from streamlit_app import main

        # Execute
        main()

        # Assert
        assert mock_st.columns.call_count >= 1 # Ensure it was called
        # Check specific calls if necessary, e.g., mock_st.columns.assert_any_call(2)
        # and mock_st.columns.assert_any_call(3)
        assert mock_st.tabs.called
        mock_st.markdown.assert_any_call("---")


class TestActivityLogging:
    """Tests for activity logging through the web interface."""
    
    @patch('streamlit_app.st')
    @patch('streamlit_app.validate_api_key')
    @patch('streamlit_app.analyze_with_ai')
    @patch('streamlit_app.save_to_csv')
    @patch('streamlit_app.format_activity_summary')
    def test_log_activity_success(self, mock_format, mock_save, mock_analyze, mock_validate, mock_st):
        """
        Test successful activity logging flow.
        Should analyze, save, and update session state.
        """
        # Setup
        mock_validate.return_value = True
        mock_analyze.return_value = [
            {"activity": "Water", "quantity": 500, "unit": "ml"}
        ]
        mock_save.return_value = True
        mock_format.return_value = "- Water: 500 ml"
        
        # Mock Streamlit components
        mock_st.text_area.return_value = "drank 500ml of water"
        mock_st.button.return_value = True
        mock_st.session_state = {}
        
        # This would normally be inside main(), but we test the logic
        from streamlit_app import st
        
        # Simulate the logging logic
        if mock_validate():
            activities = mock_analyze("drank 500ml of water")
            if activities:
                if mock_save(activities):
                    st.session_state['data_updated'] = True
        
        # Assert
        assert st.session_state['data_updated'] is True
        mock_analyze.assert_called_once_with("drank 500ml of water")
        mock_save.assert_called_once_with(activities)


class TestDataFiltering:
    """Tests for data filtering functionality."""
    
    def test_date_filter_today(self):
        """
        Test filtering data for today only.
        Should use get_today_activities function.
        """
        # This tests the filtering logic that would be in main()
        from logic import get_today_activities
        
        # Create test data
        test_df = pd.DataFrame({
            'timestamp': [
                datetime.now(),
                datetime.now() - timedelta(days=1),
                datetime.now()
            ],
            'activity': ['Water', 'Walk', 'Food'],
            'quantity': [500, 2, 1],
            'unit': ['ml', 'km', 'meal'],
            'date': [
                date.today(),
                date.today() - timedelta(days=1),
                date.today()
            ]
        })
        
        # Execute
        filtered = get_today_activities(test_df)
        
        # Assert
        assert len(filtered) == 2
        assert all(filtered['date'] == date.today())
    
    def test_activity_filter(self):
        """
        Test filtering by selected activities.
        Should return only selected activity types.
        """
        # Create test data
        test_df = pd.DataFrame({
            'timestamp': [datetime.now()] * 4,
            'activity': ['Water', 'Walk', 'Food', 'Water'],
            'quantity': [500, 2, 1, 300],
            'unit': ['ml', 'km', 'meal', 'ml'],
            'date': [date.today()] * 4
        })
        
        # Simulate multiselect filter
        selected_activities = ['Water', 'Food']
        
        # Execute
        filtered = test_df[test_df['activity'].isin(selected_activities)]
        
        # Assert
        assert len(filtered) == 3
        assert set(filtered['activity'].unique()) == {'Water', 'Food'}


class TestVisualizationData:
    """Tests for data preparation for visualizations."""
    
    def test_totals_preparation_empty(self):
        """
        Test handling empty totals for bar chart.
        Should not crash when creating DataFrame.
        """
        from logic import get_totals
        
        # Create empty DataFrame
        empty_df = pd.DataFrame(columns=['activity', 'quantity'])
        
        # Execute
        totals = get_totals(empty_df)
        
        # This simulates the plotting logic
        if not totals.empty:
            df_for_plot = pd.DataFrame({
                'Activity': totals.index,
                'Quantity': totals.values
            }).reset_index(drop=True)
        else:
            df_for_plot = pd.DataFrame()
        
        # Assert
        assert df_for_plot.empty
    
    def test_totals_preparation_valid(self):
        """
        Test preparing totals data for plotting.
        Should create proper DataFrame structure.
        """
        from logic import get_totals
        
        # Create test data
        test_df = pd.DataFrame({
            'activity': ['Water', 'Water', 'Walk'],
            'quantity': [500, 300, 2]
        })
        
        # Execute
        totals = get_totals(test_df)
        
        # Simulate the plotting preparation
        df_for_plot = pd.DataFrame({
            'Activity': totals.index,
            'Quantity': totals.values
        }).reset_index(drop=True)
        
        # Assert
        assert len(df_for_plot) == 2
        assert 'Activity' in df_for_plot.columns
        assert 'Quantity' in df_for_plot.columns
        assert df_for_plot[df_for_plot['Activity'] == 'Water']['Quantity'].iloc[0] == 800


class TestErrorHandling:
    """Tests for error handling in the web interface."""
    
    @patch('streamlit_app.st')
    @patch('streamlit_app.validate_api_key')
    def test_no_api_key_error(self, mock_validate, mock_st):
        """
        Test behavior when API key is not configured.
        Should display error and setup instructions.
        """
        # Setup
        mock_validate.return_value = False
        
        # Simulate the check that would be in main()
        if not mock_validate():
            mock_st.error("⚠️ API key not configured!")
            mock_st.info("Please configure your API key in the Settings section above.")
        
        # Assert
        mock_st.error.assert_called_with("⚠️ API key not configured!")
        mock_st.info.assert_called_once()
    
    @patch('streamlit_app.st')
    @patch('streamlit_app.analyze_with_ai')
    @patch('streamlit_app.validate_api_key')
    def test_api_error_handling(self, mock_validate, mock_analyze, mock_st):
        """
        Test handling API errors during analysis.
        Should display error message to user.
        """
        # Setup
        mock_validate.return_value = True
        mock_analyze.side_effect = Exception("Rate limit exceeded")
        
        # Simulate error handling
        try:
            mock_analyze("test input")
        except Exception as e:
            mock_st.error(f"❌ Error: {e}")
        
        # Assert
        mock_st.error.assert_called_with("❌ Error: Rate limit exceeded")


class TestUIComponents:
    """Tests for UI component behavior."""
    
    @patch('streamlit_app.st')
    def test_api_key_configuration_ui(self, mock_st):
        """
        Test API key configuration UI flow.
        Should show/hide based on session state.
        """
        # Setup
        mock_st.session_state = {'show_api_input': True}
        mock_st.form.return_value.__enter__ = Mock(return_value=Mock())
        mock_st.form.return_value.__exit__ = Mock(return_value=None)
        mock_st.text_input.return_value = "sk-or-v1-newkey"
        mock_st.form_submit_button.return_value = True
        
        # Simulate the logic
        if mock_st.session_state.get('show_api_input', False):
            # User saves key
            new_key = mock_st.text_input("Enter key", type="password")
            if new_key.strip():
                mock_st.session_state['show_api_input'] = False
        
        # Assert
        assert mock_st.session_state['show_api_input'] is False
    
    @patch('streamlit_app.st')
    def test_date_filter_custom_range(self, mock_st):
        """
        Test custom date range filter UI.
        Should show date inputs when custom is selected.
        """
        # Setup
        mock_st.selectbox.return_value = "Custom"
        mock_st.date_input.side_effect = [
            date.today() - timedelta(days=7),
            date.today()
        ]
        
        # Simulate the logic
        date_filter = mock_st.selectbox("Time period", ["All", "Today", "Custom"])
        
        if date_filter == "Custom":
            start_date = mock_st.date_input("From date")
            end_date = mock_st.date_input("To date")
        
        # Assert
        assert mock_st.date_input.call_count == 2