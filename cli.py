"""
📱 Personal Life Tracker - CLI Interface
=======================================

Command-line interface for the Personal Life Tracker.
This file handles ONLY the command-line presentation layer.
All business logic is imported from logic.py.

Usage:
    python cli.py log "drank 500ml of water"
    python cli.py analyze --totals
    python cli.py analyze --today
    python cli.py analyze --graph-totals
    python cli.py analyze --graph-timeline
"""

import argparse
import sys
from datetime import datetime

# Import all business logic from our core module
from logic import (
    log_activity, analyze_with_ai, load_data, validate_api_key,
    get_totals, get_today_activities, show_totals_graph, show_timeline_graph,
    format_activity_summary, get_data_summary, set_api_key, get_api_key
)


def handle_log_command(text: str) -> None:
    """
    Handle the 'log' command to record new activities.
    
    Processes natural language input through AI analysis and saves
    detected activities to the CSV file. Provides user feedback on
    success or failure.
    
    Args:
        text: Natural language description of activities to log
              Examples: "drank 500ml of water"
                       "walked 2km and had lunch"
                       
    Side Effects:
        - Prints status messages to console
        - Makes API call to analyze text
        - Writes to CSV file if activities detected
        - May exit early if API key not configured
        
    Error Handling:
        - Validates API key before processing
        - Catches and displays all exceptions
        - Provides helpful error messages for common issues
    """
    try:
        if not validate_api_key():
            print("❌ ERROR: API key not configured.")
            print("Please set your API key with: python cli.py config --set-api-key")
            print("Or set environment variable: export OPENROUTER_API_KEY='your-key-here'")
            return
        
        print(f"📝 Analyzing: '{text}'")
        
        # Use the core logic to analyze and save
        activities = analyze_with_ai(text)
        if activities:
            from logic import save_to_csv
            success = save_to_csv(activities)
            if success:
                print("\n✅ Successfully logged the following:")
                print(format_activity_summary(activities))
            else:
                print("❌ Failed to save activities to file.")
        else:
            print("⚠️ No activities were detected in your input.")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def handle_config_command(args) -> None:
    """
    Handle the 'config' command for managing configuration settings.
    
    Allows users to view and set configuration options including API keys.
    Provides a secure way to store API keys persistently in a config file.
    
    Args:
        args: Namespace object from argparse containing:
              - show (bool): Display current configuration
              - set_api_key (bool): Prompt for and save API key
              
    Side Effects:
        - May prompt for user input (API key)
        - Creates or updates config.json file
        - Prints configuration status to console
        
    Security Notes:
        - API key input is hidden during typing
        - Stored API keys are displayed in masked format
    """
    try:
        if args.show:
            print("\n⚙️ === CURRENT CONFIGURATION ===")
            api_key = get_api_key()
            if api_key:
                # Show masked key
                masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
                print(f"   🔑 API Key: {masked_key}")
                if validate_api_key():
                    print("   ✅ API Key Status: Valid")
                else:
                    print("   ⚠️ API Key Status: Invalid format")
            else:
                print("   🔑 API Key: Not configured")
                print("   ❌ API Key Status: Missing")
            
            from logic import load_config
            config = load_config()
            print(f"   🤖 AI Model: {config.get('model', 'Not set')}")
            print(f"   📄 CSV File: {config.get('csv_filename', 'Not set')}")
            return
        
        if args.set_api_key:
            print("\n🔑 === API KEY CONFIGURATION ===")
            print("💡 Get your API key from: https://openrouter.ai/")
            print("📋 Your key should start with 'sk-or-v1-...'")
            
            import getpass
            try:
                api_key = getpass.getpass("Enter your OpenRouter API Key (hidden): ")
                
                if not api_key.strip():
                    print("❌ No API key entered.")
                    return
                
                if set_api_key(api_key):
                    print("✅ API key saved successfully!")
                    
                    # Validate the saved key
                    if validate_api_key():
                        print("✅ API key validation: PASSED")
                        print("🎉 You're all set! You can now log activities.")
                    else:
                        print("⚠️ API key validation: FAILED")
                        print("   Please check your key format (should start with 'sk-or-v1-')")
                else:
                    print("❌ Failed to save API key.")
                    
            except KeyboardInterrupt:
                print("\n❌ Configuration cancelled by user.")
                return
                
    except Exception as e:
        print(f"❌ Configuration error: {e}")


def handle_analyze_command(args) -> None:
    """
    Handle the 'analyze' command with various analysis options.
    
    Loads activity data and performs requested analysis operations.
    Supports multiple analysis types that can be combined in one call.
    Shows summary overview if no specific analysis requested.
    
    Args:
        args: Namespace object from argparse containing:
              - totals (bool): Show total quantities
              - today (bool): Show today's activities
              - graph_totals (bool): Display totals bar chart
              - graph_timeline (bool): Display timeline chart
              
    Side Effects:
        - Prints analysis results to console
        - May display matplotlib windows for graphs
        - May prompt for user input (timeline selection)
        
    Data Requirements:
        - Requires livslogg.csv file to exist
        - File must contain valid activity data
        
    Example Output:
        When called with --totals:
        📊 === TOTALS FOR ALL ACTIVITIES ===
           Water: 5250.0
           Walk: 15.5
           Food: 12.0
    """
    try:
        # Load data using core logic
        data_df = load_data()
        if data_df is None:
            print("📭 No data found. Log some activities first!")
            print("Example: python cli.py log 'drank 500ml of water'")
            return
        
        if data_df.empty:
            print("📭 Data file is empty. Log some activities first!")
            return
        
        # Show data summary if no specific analysis is requested
        if not any([args.totals, args.today, args.graph_totals, args.graph_timeline]):
            summary = get_data_summary(data_df)
            print("\n📊 Data Overview:")
            print(f"   Total activities logged: {summary.get('total_activities', 0)}")
            print(f"   Unique activity types: {summary.get('unique_activities', 0)}")
            if 'date_range' in summary:
                date_range = summary['date_range']
                print(f"   Date range: {date_range.get('first_entry', 'Unknown')} to {date_range.get('last_entry', 'Unknown')}")
                print(f"   Days tracked: {date_range.get('days_tracked', 0)}")
            print("\n💡 Use --help to see available analysis options")
            return
        
        # Execute specific analysis based on arguments
        if args.totals:
            print("\n📊 === TOTALS FOR ALL ACTIVITIES ===")
            totals = get_totals(data_df)
            for activity, total in totals.items():
                print(f"   {activity}: {total}")
        
        if args.today:
            print("\n📅 === TODAY'S LOG ===")
            today_activities = get_today_activities(data_df)
            if today_activities.empty:
                print("   No activities logged today.")
            else:
                for _, row in today_activities.iterrows():
                    time_str = row['timestamp'].strftime('%H:%M')
                    print(f"   {time_str} - {row['activity']}: {row['quantity']} {row['unit']}")
        
        if args.graph_totals:
            print("\n📈 Generating totals graph...")
            show_totals_graph(data_df)
        
        if args.graph_timeline:
            print("\n📈 Generating timeline graph...")
            show_timeline_graph(data_df)
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")


def main():
    """
    Main CLI entry point and argument parser.
    
    Sets up the command-line interface with subcommands for logging
    and analyzing activities. Uses argparse for robust argument handling
    with helpful documentation.
    
    Commands:
        log <text>: Log new activities using natural language
        analyze [options]: Analyze logged data with various views
        config [options]: Manage configuration settings
        
    Exit Codes:
        0: Success
        1: Error (invalid arguments or runtime error)
        
    Example Usage:
        python cli.py config --set-api-key
        python cli.py log "drank 500ml of water"
        python cli.py analyze --totals --today
        python cli.py analyze --graph-timeline
    """
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="🎯 Personal Life Tracker - Track and analyze your daily activities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py config --set-api-key
  python cli.py config --show
  python cli.py log "drank 500ml of water and walked 2km"
  python cli.py analyze --totals
  python cli.py analyze --today
  python cli.py analyze --graph-totals
  python cli.py analyze --graph-timeline
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Create the parser for the "log" command
    parser_log = subparsers.add_parser(
        "log", 
        help="Log a new activity using natural language"
    )
    parser_log.add_argument(
        "text", 
        type=str, 
        help="The text describing your activity (e.g., 'drank 500ml of water')"
    )

    # Create the parser for the "analyze" command
    parser_analyze = subparsers.add_parser(
        "analyze", 
        help="Analyze and view your logged data"
    )
    parser_analyze.add_argument(
        "--totals", 
        action="store_true", 
        help="Show total quantities for all activities as text"
    )
    parser_analyze.add_argument(
        "--today", 
        action="store_true", 
        help="Show all activities logged today as text"
    )
    parser_analyze.add_argument(
        "--graph-totals", 
        action="store_true", 
        help="Show a bar graph of total quantities"
    )
    parser_analyze.add_argument(
        "--graph-timeline", 
        action="store_true", 
        help="Show a timeline graph for a specific activity"
    )

    # Create the parser for the "config" command
    parser_config = subparsers.add_parser(
        "config", 
        help="Manage configuration settings"
    )
    parser_config.add_argument(
        "--show", 
        action="store_true", 
        help="Display current configuration settings"
    )
    parser_config.add_argument(
        "--set-api-key", 
        action="store_true", 
        help="Set your OpenRouter API key"
    )

    # Parse the arguments provided by the user
    args = parser.parse_args()

    # Execute the correct function based on the command
    if args.command == "log":
        handle_log_command(args.text)
    elif args.command == "analyze":
        handle_analyze_command(args)
    elif args.command == "config":
        # Default to show config if no specific action
        if not args.show and not getattr(args, 'set_api_key', False):
            args.show = True
        handle_config_command(args)


if __name__ == "__main__":
    main() 