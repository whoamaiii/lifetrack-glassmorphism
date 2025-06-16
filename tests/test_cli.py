"""
CLI Interface Tests
===================

This module tests the command-line interface functionality in cli.py.
It verifies argument parsing, command handling, and proper integration
with the core logic functions.

Test Categories:
1. Command Handling Tests
2. Argument Parsing Tests
3. Output Formatting Tests
4. Error Handling Tests

All tests mock the underlying logic functions to isolate CLI behavior.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock, call
import argparse
import sys
from io import StringIO
import pandas as pd
from datetime import datetime, date


class TestLogCommand:
    """Tests for the 'log' command functionality."""
    
    @patch('cli.validate_api_key')
    @patch('cli.analyze_with_ai')
    @patch('logic.save_to_csv')
    @patch('cli.format_activity_summary')
    def test_handle_log_command_success(self, mock_format, mock_save, mock_analyze, mock_validate):
        """
        Test successful activity logging through CLI.
        Should validate API key, analyze text, save activities, and display summary.
        """
        # Setup mocks
        mock_validate.return_value = True
        mock_analyze.return_value = [
            {"activity": "Water", "quantity": 500, "unit": "ml"}
        ]
        mock_save.return_value = True
        mock_format.return_value = "- Water: 500 ml"
        
        # Capture output
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_log_command
            
            # Execute
            handle_log_command("drank 500ml of water")
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        mock_validate.assert_called_once()
        mock_analyze.assert_called_once_with("drank 500ml of water")
        mock_save.assert_called_once()
        assert "✅ Successfully logged" in output
        assert "- Water: 500 ml" in output
    
    @patch('cli.validate_api_key')
    def test_handle_log_command_no_api_key(self, mock_validate):
        """
        Test log command when API key is not configured.
        Should display error message and configuration instructions.
        """
        # Setup
        mock_validate.return_value = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_log_command
            
            # Execute
            handle_log_command("test input")
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "❌ ERROR: API key not configured" in output
        assert "python cli.py config --set-api-key" in output
        assert "export OPENROUTER_API_KEY=" in output
    
    @patch('cli.validate_api_key')
    @patch('cli.analyze_with_ai')
    def test_handle_log_command_no_activities(self, mock_analyze, mock_validate):
        """
        Test log command when no activities are detected.
        Should display warning message.
        """
        # Setup
        mock_validate.return_value = True
        mock_analyze.return_value = []
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_log_command
            
            # Execute
            handle_log_command("watched TV")
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "⚠️ No activities were detected" in output
    
    @patch('cli.validate_api_key')
    @patch('cli.analyze_with_ai')
    def test_handle_log_command_api_error(self, mock_analyze, mock_validate):
        """
        Test log command when API analysis fails.
        Should display error message with details.
        """
        # Setup
        mock_validate.return_value = True
        mock_analyze.side_effect = Exception("API rate limit exceeded")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_log_command
            
            # Execute
            handle_log_command("test input")
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "❌ Error: API rate limit exceeded" in output


class TestConfigCommand:
    """Tests for the 'config' command functionality."""
    
    @patch('cli.get_api_key')
    @patch('cli.validate_api_key')
    @patch('logic.load_config')
    def test_handle_config_show(self, mock_load_config, mock_validate, mock_get_key):
        """
        Test showing current configuration.
        Should display API key status and other settings.
        """
        # Setup
        mock_get_key.return_value = "sk-or-v1-1234567890abcdef"
        mock_validate.return_value = True
        mock_load_config.return_value = {
            "model": "google/gemini-flash-1.5",
            "csv_filename": "livslogg.csv"
        }
        
        # Create mock args
        args = Mock()
        args.show = True
        args.set_api_key = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_config_command
            
            # Execute
            handle_config_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "⚙️ === CURRENT CONFIGURATION ===" in output
        assert "🔑 API Key: sk-or-v1...cdef" in output  # Masked
        assert "✅ API Key Status: Valid" in output
        assert "🤖 AI Model: google/gemini-flash-1.5" in output
        assert "📄 CSV File: livslogg.csv" in output
    
    @patch('cli.get_api_key')
    def test_handle_config_show_no_key(self, mock_get_key):
        """
        Test showing configuration when no API key is set.
        Should display missing key warning.
        """
        # Setup
        mock_get_key.return_value = ""
        
        args = Mock()
        args.show = True
        args.set_api_key = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_config_command
            
            # Execute
            handle_config_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "🔑 API Key: Not configured" in output
        assert "❌ API Key Status: Missing" in output
    
    @patch('getpass.getpass')
    @patch('cli.set_api_key')
    @patch('cli.validate_api_key')
    def test_handle_config_set_api_key(self, mock_validate, mock_set_key, mock_getpass):
        """
        Test setting API key through config command.
        Should prompt for key, save it, and validate.
        """
        # Setup
        mock_getpass.return_value = "sk-or-v1-newkey123"
        mock_set_key.return_value = True
        mock_validate.return_value = True
        
        args = Mock()
        args.show = False
        args.set_api_key = True
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_config_command
            
            # Execute
            handle_config_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        mock_getpass.assert_called_once_with("Enter your OpenRouter API Key (hidden): ")
        mock_set_key.assert_called_once_with("sk-or-v1-newkey123")
        assert "✅ API key saved successfully!" in output
        assert "✅ API key validation: PASSED" in output
    
    @patch('getpass.getpass')
    def test_handle_config_set_api_key_cancelled(self, mock_getpass):
        """
        Test cancelling API key input.
        Should handle KeyboardInterrupt gracefully.
        """
        # Setup
        mock_getpass.side_effect = KeyboardInterrupt()
        
        args = Mock()
        args.show = False
        args.set_api_key = True
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_config_command
            
            # Execute
            handle_config_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "❌ Configuration cancelled by user" in output


class TestAnalyzeCommand:
    """Tests for the 'analyze' command functionality."""
    
    @patch('cli.load_data')
    @patch('cli.get_totals')
    def test_handle_analyze_totals(self, mock_get_totals, mock_load_data):
        """
        Test analyze command with --totals flag.
        Should display total quantities for each activity.
        """
        # Setup
        mock_df = MagicMock()
        mock_df.empty = False
        mock_load_data.return_value = mock_df
        
        mock_get_totals.return_value = {
            'Water': 3500.0,
            'Walk': 15.5,
            'Food': 7.0
        }
        
        args = Mock()
        args.totals = True
        args.today = False
        args.graph_totals = False
        args.graph_timeline = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_analyze_command
            
            # Execute
            handle_analyze_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "📊 === TOTALS FOR ALL ACTIVITIES ===" in output
        assert "Water: 3500.0" in output
        assert "Walk: 15.5" in output
        assert "Food: 7.0" in output
    
    @patch('cli.load_data')
    @patch('cli.get_today_activities')
    def test_handle_analyze_today(self, mock_get_today, mock_load_data):
        """
        Test analyze command with --today flag.
        Should display today's activities chronologically.
        """
        # Setup
        mock_df = MagicMock()
        mock_df.empty = False
        mock_load_data.return_value = mock_df
        
        # Create mock today's data
        today_data = pd.DataFrame({
            'timestamp': [datetime.now().replace(hour=8), datetime.now().replace(hour=12)],
            'activity': ['Water', 'Food'],
            'quantity': [500, 1],
            'unit': ['ml', 'meal']
        })
        mock_get_today.return_value = today_data
        
        args = Mock()
        args.totals = False
        args.today = True
        args.graph_totals = False
        args.graph_timeline = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_analyze_command
            
            # Execute
            handle_analyze_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "📅 === TODAY'S LOG ===" in output
        assert "08:" in output  # Hour from timestamp
        assert "Water: 500 ml" in output
        assert "Food: 1 meal" in output
    
    @patch('cli.load_data')
    def test_handle_analyze_no_data(self, mock_load_data):
        """
        Test analyze command when no data exists.
        Should display helpful message.
        """
        # Setup
        mock_load_data.return_value = None
        
        args = Mock()
        args.totals = True
        args.today = False
        args.graph_totals = False
        args.graph_timeline = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_analyze_command
            
            # Execute
            handle_analyze_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "📭 No data found" in output
        assert "python cli.py log" in output
    
    @patch('cli.load_data')
    @patch('cli.get_data_summary')
    def test_handle_analyze_no_flags(self, mock_summary, mock_load_data):
        """
        Test analyze command without specific flags.
        Should display data overview and available options.
        """
        # Setup
        mock_df = MagicMock()
        mock_df.empty = False
        mock_load_data.return_value = mock_df
        
        mock_summary.return_value = {
            'total_activities': 150,
            'unique_activities': 5,
            'date_range': {
                'first_entry': '2024-01-01',
                'last_entry': '2024-01-15',
                'days_tracked': 15
            }
        }
        
        args = Mock()
        args.totals = False
        args.today = False
        args.graph_totals = False
        args.graph_timeline = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_analyze_command
            
            # Execute
            handle_analyze_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "📊 Data Overview:" in output
        assert "Total activities logged: 150" in output
        assert "Unique activity types: 5" in output
        assert "Days tracked: 15" in output
        assert "💡 Use --help to see available analysis options" in output


class TestMainFunction:
    """Tests for the main CLI entry point and argument parsing."""
    
    def test_main_log_command(self):
        """
        Test main function with log command.
        Should parse arguments and call handle_log_command.
        """
        # Setup
        test_args = ['cli.py', 'log', 'drank water']
        
        with patch('sys.argv', test_args):
            with patch('cli.handle_log_command') as mock_handler:
                from cli import main
                
                # Execute
                main()
                
                # Assert
                mock_handler.assert_called_once_with('drank water')
    
    def test_main_analyze_command(self):
        """
        Test main function with analyze command and flags.
        Should parse arguments correctly.
        """
        # Setup
        test_args = ['cli.py', 'analyze', '--totals', '--today']
        
        with patch('sys.argv', test_args):
            with patch('cli.handle_analyze_command') as mock_handler:
                from cli import main
                
                # Execute
                main()
                
                # Assert
                mock_handler.assert_called_once()
                args = mock_handler.call_args[0][0]
                assert args.totals is True
                assert args.today is True
    
    def test_main_config_command(self):
        """
        Test main function with config command.
        Should default to showing config if no flags provided.
        """
        # Setup
        test_args = ['cli.py', 'config']
        
        with patch('sys.argv', test_args):
            with patch('cli.handle_config_command') as mock_handler:
                from cli import main
                
                # Execute
                main()
                
                # Assert
                mock_handler.assert_called_once()
                args = mock_handler.call_args[0][0]
                assert args.show is True  # Default behavior
    
    def test_main_invalid_command(self):
        """
        Test main function with invalid command.
        Should exit with error message.
        """
        # Setup
        test_args = ['cli.py', 'invalid-command']
        
        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit):
                from cli import main
                main()
    
    def test_main_help(self):
        """
        Test main function with --help flag.
        Should display help message and exit.
        """
        # Setup
        test_args = ['cli.py', '--help']
        
        with patch('sys.argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with pytest.raises(SystemExit) as exc_info:
                    from cli import main
                    main()
                
                # Get output
                output = mock_stdout.getvalue()
        
        # Assert
        assert exc_info.value.code == 0  # Success exit
        assert "Personal Life Tracker" in output
        assert "Available commands" in output
        assert "log" in output
        assert "analyze" in output
        assert "config" in output


class TestErrorHandling:
    """Tests for error handling in CLI."""
    
    @patch('cli.validate_api_key')
    @patch('cli.analyze_with_ai')
    @patch('logic.save_to_csv')
    def test_handle_log_save_failure(self, mock_save, mock_analyze, mock_validate):
        """
        Test handling save failure during logging.
        Should display appropriate error message.
        """
        # Setup
        mock_validate.return_value = True
        mock_analyze.return_value = [{"activity": "Water", "quantity": 500, "unit": "ml"}]
        mock_save.return_value = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_log_command
            
            # Execute
            handle_log_command("test input")
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "❌ Failed to save activities" in output
    
    @patch('cli.load_data')
    def test_handle_analyze_data_error(self, mock_load_data):
        """
        Test handling data loading errors.
        Should display error message with details.
        """
        # Setup
        mock_load_data.side_effect = Exception("Permission denied")
        
        args = Mock()
        args.totals = True
        args.today = False
        args.graph_totals = False
        args.graph_timeline = False
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            from cli import handle_analyze_command
            
            # Execute
            handle_analyze_command(args)
            
            # Get output
            output = mock_stdout.getvalue()
        
        # Assert
        assert "❌ Error during analysis: Permission denied" in output