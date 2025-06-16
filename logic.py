"""
🧠 Personal Life Tracker - Core Logic
=====================================

This module contains all the core business logic for the Personal Life Tracker.
It's designed to be imported by different interfaces (CLI, Web App, etc.) to
ensure consistency and maintainability.

Separation of Concerns:
- This file contains ONLY the core functions (what the app does)
- Interface files (cli.py, streamlit_app.py) handle presentation (how it looks)
- This enables easy maintenance and adding new interfaces without code duplication

Architecture Benefits:
- DRY (Don't Repeat Yourself): Logic written once, used everywhere
- Testability: Core functions can be unit tested independently
- Extensibility: New interfaces can be added without touching core logic
- Maintainability: Bugs fixed in one place benefit all interfaces

Module Structure:
1. Configuration - API settings and constants
2. Logging Functions - Activity parsing and storage
3. Data Loading Functions - CSV reading and cleaning
4. Analysis Functions - Data aggregation and filtering
5. Visualization Helpers - Chart data preparation
6. Matplotlib Functions - CLI-specific visualizations
7. Utility Functions - Validation and formatting

Usage Example:
    from logic import log_activity, load_data, get_totals
    
    # Log a new activity
    success = log_activity("drank 500ml of water")
    
    # Load and analyze data
    df = load_data()
    totals = get_totals(df)
"""

import os
import requests
import json
from datetime import datetime, date
import csv
from typing import List, Dict, Optional, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- CONFIGURATION ---
# Configuration file path
CONFIG_FILE = Path("config.json")

def load_config() -> Dict:
    """
    Load configuration from config.json file.
    
    Returns:
        Dict: Configuration dictionary with default values if file doesn't exist
    """
    default_config = {
        "api_key": "",
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "google/gemini-flash-1.5",
        "csv_filename": "livslogg.csv"
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                default_config.update(config)
                return default_config
        except (json.JSONDecodeError, Exception):
            # If config file is corrupted, return defaults
            return default_config
    
    return default_config

def save_config(config: Dict) -> bool:
    """
    Save configuration to config.json file.
    
    Args:
        config: Configuration dictionary to save
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def get_api_key() -> str:
    """
    Get API key from config file or environment variable.
    
    Priority:
    1. Saved config file
    2. Environment variable
    
    Returns:
        str: API key or empty string if not found
    """
    # First try config file
    config = load_config()
    if config.get("api_key"):
        return config["api_key"]
    
    # Fallback to environment variable
    return os.getenv("OPENROUTER_API_KEY", "")

def set_api_key(api_key: str) -> bool:
    """
    Save API key to configuration file.
    
    Args:
        api_key: The API key to save
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    config = load_config()
    config["api_key"] = api_key
    return save_config(config)

def get_config_value(key: str, default=None):
    """
    Get a specific configuration value.
    
    Args:
        key: Configuration key to retrieve
        default: Default value if key not found
        
    Returns:
        Configuration value or default
    """
    config = load_config()
    return config.get(key, default)

def set_config_value(key: str, value) -> bool:
    """
    Set a specific configuration value.
    
    Args:
        key: Configuration key to set
        value: Value to set
        
    Returns:
        bool: True if saved successfully, False otherwise
    """
    config = load_config()
    config[key] = value
    return save_config(config)

# Update the global API_KEY to use the new system
API_KEY = get_api_key()
# Load other config values
config = load_config()
API_URL = config.get("api_url", "https://openrouter.ai/api/v1/chat/completions")
MODEL = config.get("model", "google/gemini-flash-1.5")
CSV_FILENAME = config.get("csv_filename", "livslogg.csv")

# Activity categories
ACTIVITY_CATEGORIES = ['Water', 'Cannabis', 'Cigarette', 'Alcohol', 'Sex', 'Walk', 'Food']

# --- CORE LOGGING FUNCTIONS ---

def log_activity(user_input: str) -> bool:
    """
    Analyzes user input with AI and saves activities to CSV.
    
    This is the main entry point for logging activities. It handles the complete
    flow from natural language input to persistent storage.
    
    Args:
        user_input: Natural language description of activities
                   Examples: "drank 500ml of water"
                            "walked 2km and smoked a cigarette"
                            "had 2 beers and a healthy dinner"
        
    Returns:
        bool: True if activities were successfully parsed and saved,
              False if no activities were detected
              
    Raises:
        ValueError: If API key is not set or invalid
        Exception: If AI analysis fails or file operations fail
        
    Example:
        >>> # Single activity
        >>> log_activity("drank a large glass of water")
        True
        
        >>> # Multiple activities
        >>> log_activity("walked 5km, had lunch, and drank 2 glasses of water")
        True
        
        >>> # Invalid input
        >>> log_activity("watched TV")  # Not a tracked activity
        False
    """
    if not validate_api_key():
        raise ValueError("API key is not set or invalid. Please configure your API key.")
    
    activities = analyze_with_ai(user_input)
    if activities:
        return save_to_csv(activities)
    return False


def analyze_with_ai(user_input: str) -> List[Dict]:
    """
    Sends user input to AI for analysis and parsing.
    
    Uses Google Gemini Flash 1.5 via OpenRouter API to parse natural language
    into structured activity data. The AI is prompted with specific categories
    and examples to ensure consistent parsing.
    
    Args:
        user_input: Natural language description of activities
                   Can be in various formats and languages
                   Can contain multiple activities in one sentence
        
    Returns:
        List[Dict]: List of parsed activities, each containing:
                   - 'activity' (str): Category from ACTIVITY_CATEGORIES
                   - 'quantity' (float): Numeric amount
                   - 'unit' (str): Unit of measurement
                   Empty list if no valid activities found
                   
    Raises:
        Exception: If API call fails, response parsing fails, or network error
        
    API Response Format:
        The AI returns JSON in this format:
        [
            {"activity": "Water", "quantity": 500, "unit": "ml"},
            {"activity": "Walk", "quantity": 2, "unit": "km"}
        ]
        
    Examples:
        >>> analyze_with_ai("drank 2 cups of water")
        [{"activity": "Water", "quantity": 2, "unit": "cups"}]
        
        >>> analyze_with_ai("went for a 5km walk and had a beer")
        [
            {"activity": "Walk", "quantity": 5, "unit": "km"},
            {"activity": "Alcohol", "quantity": 1, "unit": "unit"}
        ]
    """
    system_prompt = """
    You are an assistant that converts user's journal entries into structured data.
    Analyze the text and identify all trackable activities.
    Return a JSON list of objects, where each object contains 'activity', 'quantity', and 'unit'.
    Use these categories for 'activity': 'Water', 'Cannabis', 'Cigarette', 'Alcohol', 'Sex', 'Walk', 'Food'.
    If quantity is not specified, set it to 1.

    Example:
    User: "drank a large glass of water, about 500ml, and smoked a joint"
    You respond:
    [
      {"activity": "Water", "quantity": 500, "unit": "ml"},
      {"activity": "Cannabis", "quantity": 1, "unit": "unit"}
    ]
    """

    headers = {"Authorization": f"Bearer {get_api_key()}", "Content-Type": "application/json"}
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        # Try to parse the JSON response from the API
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError as json_err:
            raise Exception(f"Failed to decode API JSON response. Status: {response.status_code}. Response text: {response.text[:500]}... Error: {json_err}")

        # Extract content from the expected structure
        if 'choices' not in response_data or not response_data['choices']:
            raise Exception(f"API response missing 'choices'. Response: {response_data}")
        
        message = response_data['choices'][0].get('message')
        if not message or 'content' not in message:
            raise Exception(f"API response missing 'message' or 'content' in choices. Response: {response_data}")
            
        content_str = message['content']
        
        if not content_str or not content_str.strip():
            # Handle cases where content_str is empty or just whitespace
            return []

        try:
            activities = json.loads(content_str)
        except json.JSONDecodeError as e:
            # Add more context to the JSONDecodeError
            raise Exception(f"Failed to parse AI content string as JSON. Content: '{content_str}'. Error: {e}")
            
        return activities if isinstance(activities, list) else []

    except requests.exceptions.HTTPError as http_err:
        # Specific handling for HTTP errors
        error_message = f"AI analysis failed with HTTPError: {http_err}. "
        if response is not None:
            error_message += f"Status Code: {response.status_code}. Response: {response.text[:500]}..."
        raise Exception(error_message)
    except requests.exceptions.RequestException as req_err:
        # Specific handling for other request-related errors (e.g., network issues)
        raise Exception(f"AI analysis failed with RequestException: {req_err}")
    except Exception as e:
        # General exception for any other errors
        # Ensure the original error message includes enough detail
        if "AI analysis failed" not in str(e): # Avoid redundant prefix
             raise Exception(f"AI analysis failed: {e}")
        raise # Re-raise if already prefixed or a different type of well-formed error


def save_to_csv(activities: List[Dict]) -> bool:
    """
    Saves a list of activities to the CSV file.
    
    Appends activity data to the CSV file with automatic timestamping.
    Creates the file with headers if it doesn't exist. Thread-safe through
    file append mode. Each activity is timestamped with the current datetime.
    
    Args:
        activities: List of activity dictionaries, each containing:
                   - 'activity' (str): Activity type/category
                   - 'quantity' (float): Numeric amount
                   - 'unit' (str): Unit of measurement
                   Note: 'timestamp' field is added automatically
        
    Returns:
        bool: True if all activities saved successfully
              
    Raises:
        Exception: If file write operations fail, with detailed error message
        
    File Format:
        CSV with columns: timestamp, activity, quantity, unit
        Example row: 2024-01-15T14:30:00,Water,500,ml
        
    Example:
        >>> activities = [
        ...     {"activity": "Water", "quantity": 500, "unit": "ml"},
        ...     {"activity": "Walk", "quantity": 2, "unit": "km"}
        ... ]
        >>> save_to_csv(activities)
        True
    """
    # global CSV_FILENAME # No longer needed if relying on module-level global

    # Ensure timestamp exists for each activity
    for activity_entry in activities:
        if 'timestamp' not in activity_entry or activity_entry['timestamp'] is None:
            activity_entry['timestamp'] = datetime.now().isoformat()

    new_data_df = pd.DataFrame(activities)

    # Define the full schema to ensure all columns are present and ordered
    # The 'date' column will be derived if not present or overwritten from timestamp
    full_schema_columns = ['timestamp', 'activity', 'quantity', 'unit', 'date']

    # Ensure all columns from the schema exist in new_data_df, add if missing
    for col in full_schema_columns:
        if col not in new_data_df.columns:
            if col == 'date' and 'timestamp' in new_data_df.columns:
                # Attempt to parse timestamp and create date if not explicitly provided
                try:
                    new_data_df['date'] = pd.to_datetime(new_data_df['timestamp']).dt.date
                except Exception:
                    new_data_df[col] = pd.NaT # Or some other appropriate NA marker for date
            else:
                new_data_df[col] = None # Or pd.NA for pandas >= 1.0
    
    # Reorder columns to match the defined schema and select only these columns
    new_data_df = new_data_df[full_schema_columns]

    try:
        # Determine if header needs to be written. 
        # This is more robust for concurrency than just checking existence.
        needs_header = not os.path.exists(CSV_FILENAME) or os.path.getsize(CSV_FILENAME) == 0
        new_data_df.to_csv(
            CSV_FILENAME, # Use global CSV_FILENAME
            mode='a',
            header=needs_header,
            index=False
        )
        return True
    except Exception as e:
        # Log the exception or handle it as per application's error handling policy
        # For now, just re-raising to make it visible during testing/development
        raise Exception(f"Failed to save data to CSV: {e}") from e


# --- CORE DATA LOADING FUNCTIONS ---

def load_data() -> Optional[pd.DataFrame]:
    """
    Loads and cleans data from the CSV file.
    
    Reads activity data from the CSV file and performs data cleaning operations.
    Handles both Norwegian and English column names for backward compatibility
    with older data files. Ensures data integrity through type conversion and
    validation.
    
    Returns:
        Optional[pd.DataFrame]: Cleaned DataFrame with columns:
                              - timestamp (datetime): When activity was logged
                              - activity (str): Activity type/category
                              - quantity (float): Numeric amount
                              - unit (str): Unit of measurement
                              - date (date): Date extracted from timestamp
                              Returns None if file doesn't exist
                              
    Raises:
        Exception: If file reading or parsing fails
        
    Data Cleaning:
        - Converts Norwegian column names to English
        - Ensures timestamp is datetime type
        - Ensures quantity is numeric
        - Removes rows with invalid timestamp or quantity
        - Adds date column for easier daily aggregations
        
    Example:
        >>> df = load_data()
        >>> if df is not None:
        ...     print(f"Loaded {len(df)} activities")
        ...     print(df.columns.tolist())
        ['timestamp', 'activity', 'quantity', 'unit', 'date']
    """
    # global CSV_FILENAME # No longer needed if relying on module-level global

    if not os.path.exists(CSV_FILENAME): # Use global CSV_FILENAME
        return None

    try:
        df = pd.read_csv(CSV_FILENAME) # Use global CSV_FILENAME
    except pd.errors.ParserError as e:
        if "expected" in str(e).lower() and "fields" in str(e).lower() and "saw" in str(e).lower():
            try:
                # Fallback: Try reading with Python engine, no header inference, enforce full schema.
                # This helps with varying numbers of columns per row.
                # The original header row (if any) will be read as data and should be filtered
                # by subsequent cleaning steps (e.g., errors='coerce' and dropna).
                current_expected_columns = ['timestamp', 'activity', 'quantity', 'unit', 'date']
                df = pd.read_csv(CSV_FILENAME, engine='python', header=None, names=current_expected_columns)
            except Exception as inner_e:
                # If Python engine also fails, raise the original error
                raise Exception(f"Failed to load data with Python engine (enforcing schema). Original error: {e}. Inner error: {inner_e}") from e
        else: # Other parsing error
            raise Exception(f"Failed to load data due to parsing error: {e}") from e
    except Exception as e: # Catch other potential exceptions during loading
        raise Exception(f"Failed to load data: {e}") from e

    if df.empty:
        return pd.DataFrame(columns=['timestamp', 'activity', 'quantity', 'unit', 'date'])

    # Handle Norwegian column names (backward compatibility)
    column_map_norwegian_to_english = {
        'tidspunkt': 'timestamp',
        'aktivitet': 'activity',
        'mengde': 'quantity',
        'enhet': 'unit'
    }
    cols_to_rename = {k: v for k, v in column_map_norwegian_to_english.items() if k in df.columns and v not in df.columns}
    if cols_to_rename:
        df = df.rename(columns=cols_to_rename)

    final_columns = ['timestamp', 'activity', 'quantity', 'unit', 'date']
    
    for col in final_columns:
        if col not in df.columns:
            df[col] = pd.NA

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    df['activity'] = df['activity'].astype(str).replace("nan", "")
    df['unit'] = df['unit'].astype(str).replace("nan", "").fillna('')
    
    df = df.dropna(subset=['timestamp', 'quantity'])
    
    if df.empty:
        return pd.DataFrame(columns=final_columns)

    df['date'] = df['timestamp'].dt.date
    
    return df[final_columns]


def get_data_summary(df: pd.DataFrame) -> Dict:
    """
    Returns comprehensive summary statistics about the dataset.
    
    Generates a detailed overview of the activity data including counts,
    date ranges, and aggregated quantities. Useful for dashboards and
    quick data health checks.
    
    Args:
        df: DataFrame with activity data, must contain columns:
            'timestamp', 'activity', 'quantity'
        
    Returns:
        Dict: Summary statistics including:
              - total_activities (int): Total number of logged activities
              - unique_activities (int): Number of distinct activity types
              - date_range (dict): First/last entry dates and days tracked
              - activity_counts (dict): Count of entries per activity type
              - total_quantities (dict): Sum of quantities per activity type
              Returns empty dict if DataFrame is empty
              
    Example:
        >>> df = pd.DataFrame({
        ...     'timestamp': pd.to_datetime(['2024-01-01', '2024-01-02']),
        ...     'activity': ['Water', 'Water'],
        ...     'quantity': [500, 750]
        ... })
        >>> summary = get_data_summary(df)
        >>> summary['total_activities']
        2
        >>> summary['total_quantities']['Water']
        1250.0
    """
    if df.empty:
        return {}
    
    return {
        'total_activities': len(df),
        'unique_activities': df['activity'].nunique(),
        'date_range': {
            'first_entry': df['timestamp'].min(),
            'last_entry': df['timestamp'].max(),
            'days_tracked': (df['timestamp'].max() - df['timestamp'].min()).days + 1
        },
        'activity_counts': df['activity'].value_counts().to_dict(),
        'total_quantities': df.groupby('activity')['quantity'].sum().to_dict()
    }


# --- CORE ANALYSIS FUNCTIONS ---

def get_totals(df: pd.DataFrame) -> pd.Series:
    """
    Returns total quantities for each activity.
    
    Aggregates all quantities by activity type to show cumulative totals.
    Results are rounded to 2 decimal places for clean display.
    
    Args:
        df: DataFrame with activity data, must contain 'activity' and 'quantity' columns
        
    Returns:
        pd.Series: Index is activity names, values are total quantities
                   Sorted by activity name alphabetically
                   
    Example:
        >>> df = pd.DataFrame({
        ...     'activity': ['Water', 'Walk', 'Water', 'Walk'],
        ...     'quantity': [500, 2, 750, 3.5]
        ... })
        >>> totals = get_totals(df)
        >>> totals['Water']
        1250.0
        >>> totals['Walk']
        5.5
    """
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby('activity')['quantity'].sum().round(2)


def get_today_activities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns activities logged today.
    
    Filters the DataFrame to show only activities from the current date,
    sorted chronologically. Useful for daily summaries and progress tracking.
    
    Args:
        df: DataFrame with activity data, must contain 'date' and 'timestamp' columns
        
    Returns:
        pd.DataFrame: Subset of input DataFrame containing only today's activities
                      Sorted by timestamp (earliest first)
                      Empty DataFrame if no activities logged today
                      
    Example:
        >>> # Assuming today is 2024-01-15
        >>> df = pd.DataFrame({
        ...     'date': [date(2024, 1, 15), date(2024, 1, 14), date(2024, 1, 15)],
        ...     'timestamp': pd.to_datetime(['2024-01-15 08:00', '2024-01-14 10:00', '2024-01-15 12:00']),
        ...     'activity': ['Water', 'Walk', 'Food'],
        ...     'quantity': [500, 2, 1]
        ... })
        >>> today_df = get_today_activities(df)
        >>> len(today_df)
        2
        >>> today_df['activity'].tolist()
        ['Water', 'Food']
    """
    today = datetime.now().date()
    return df[df['date'] == today].sort_values(by='timestamp')


def get_date_range_activities(df: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    """
    Returns activities within a date range.
    
    Filters activities to a specific date range (inclusive on both ends).
    Useful for weekly/monthly reports or custom period analysis.
    
    Args:
        df: DataFrame with activity data, must contain 'date' column
        start_date: Start date (inclusive), as datetime.date object
        end_date: End date (inclusive), as datetime.date object
        
    Returns:
        pd.DataFrame: Subset of input DataFrame within the date range
                      Maintains original row order
                      Empty DataFrame if no activities in range
                      
    Raises:
        ValueError: If start_date is after end_date
        
    Example:
        >>> from datetime import date
        >>> df = pd.DataFrame({
        ...     'date': [date(2024, 1, 1), date(2024, 1, 5), date(2024, 1, 10)],
        ...     'activity': ['Water', 'Walk', 'Food'],
        ...     'quantity': [500, 2, 1]
        ... })
        >>> filtered = get_date_range_activities(df, date(2024, 1, 1), date(2024, 1, 7))
        >>> len(filtered)
        2
        >>> filtered['activity'].tolist()
        ['Water', 'Walk']
    """
    if start_date > end_date:
        raise ValueError(f"start_date ({start_date}) must be before or equal to end_date ({end_date})")
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]


def get_activity_timeline(df: pd.DataFrame, activity: str, group_by: str = 'day') -> pd.DataFrame:
    """
    Returns timeline data for a specific activity.
    
    Aggregates activity quantities over time periods for trend analysis.
    Supports daily, weekly, and monthly aggregations. Useful for creating
    time-series visualizations and identifying patterns.
    
    Args:
        df: DataFrame with activity data, must contain 'activity', 'timestamp', 
            'quantity', and 'date' columns
        activity: Activity name to filter by (case-sensitive)
        group_by: Grouping period - 'day', 'week', or 'month' (default: 'day')
        
    Returns:
        pd.DataFrame: Timeline data with columns:
                      - For 'day': ['date', 'quantity']
                      - For 'week': ['week', 'quantity'] (Period objects)
                      - For 'month': ['month', 'quantity'] (Period objects)
                      Sorted by time period, with aggregated quantities
                      
    Raises:
        ValueError: If group_by is not one of 'day', 'week', 'month'
        ValueError: If activity doesn't exist in the data
        
    Example:
        >>> df = pd.DataFrame({
        ...     'timestamp': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-02']),
        ...     'date': [date(2024, 1, 1), date(2024, 1, 1), date(2024, 1, 2)],
        ...     'activity': ['Water', 'Water', 'Water'],
        ...     'quantity': [500, 300, 600]
        ... })
        >>> timeline = get_activity_timeline(df, 'Water', 'day')
        >>> timeline['quantity'].tolist()
        [800.0, 600.0]
    """
    # Validate activity exists
    if activity not in df['activity'].values:
        raise ValueError(f"Activity '{activity}' not found in data")
        
    activity_df = df[df['activity'] == activity].copy()
    
    if group_by == 'day':
        timeline = activity_df.groupby('date')['quantity'].sum().reset_index()
    elif group_by == 'week':
        activity_df['week'] = activity_df['timestamp'].dt.to_period('W')
        timeline = activity_df.groupby('week')['quantity'].sum().reset_index()
    elif group_by == 'month':
        activity_df['month'] = activity_df['timestamp'].dt.to_period('M')
        timeline = activity_df.groupby('month')['quantity'].sum().reset_index()
    else:
        raise ValueError("group_by must be 'day', 'week', or 'month'")
    
    return timeline


# --- VISUALIZATION HELPER FUNCTIONS ---

def create_totals_chart_data(df: pd.DataFrame) -> Tuple[List[str], List[float]]:
    """
    Prepares data for totals bar chart.
    
    Extracts and formats total quantities per activity for visualization.
    Returns parallel lists suitable for plotting libraries like matplotlib
    or web charting libraries.
    
    Args:
        df: DataFrame with activity data, must contain 'activity' and 'quantity' columns
        
    Returns:
        Tuple[List[str], List[float]]: Two parallel lists:
                                       - activity_names: List of activity types
                                       - quantities: Corresponding total quantities
                                       Both lists have same length and matching indices
                                       
    Example:
        >>> df = pd.DataFrame({
        ...     'activity': ['Water', 'Walk', 'Water'],
        ...     'quantity': [500, 2, 750]
        ... })
        >>> names, quantities = create_totals_chart_data(df)
        >>> names
        ['Walk', 'Water']
        >>> quantities
        [2.0, 1250.0]
    """
    totals = get_totals(df)
    return totals.index.tolist(), totals.values.tolist()


def create_timeline_chart_data(df: pd.DataFrame, activity: str) -> Tuple[List[date], List[float]]:
    """
    Prepares data for timeline chart.
    
    Extracts daily timeline data for a specific activity formatted for
    time-series visualization. Returns parallel lists of dates and quantities.
    
    Args:
        df: DataFrame with activity data
        activity: Activity name to extract timeline for
        
    Returns:
        Tuple[List[date], List[float]]: Two parallel lists:
                                        - dates: List of date objects
                                        - quantities: Daily totals for the activity
                                        Both sorted chronologically
                                        
    Example:
        >>> df = pd.DataFrame({
        ...     'timestamp': pd.to_datetime(['2024-01-01', '2024-01-02']),
        ...     'date': [date(2024, 1, 1), date(2024, 1, 2)],
        ...     'activity': ['Water', 'Water'],
        ...     'quantity': [500, 750]
        ... })
        >>> dates, quantities = create_timeline_chart_data(df, 'Water')
        >>> dates[0].isoformat()
        '2024-01-01'
        >>> quantities
        [500.0, 750.0]
    """
    timeline = get_activity_timeline(df, activity)
    return timeline['date'].tolist(), timeline['quantity'].tolist()


# --- MATPLOTLIB VISUALIZATION FUNCTIONS (for CLI) ---

def show_totals_graph(df: pd.DataFrame) -> None:
    """
    Displays a bar chart of total quantities for each activity.
    
    Creates a horizontal bar chart showing cumulative quantities for all
    activities. Uses seaborn styling for professional appearance. Chart
    is displayed using matplotlib's interactive window.
    
    Args:
        df: DataFrame with activity data, must contain 'activity' and 'quantity' columns
        
    Side Effects:
        - Displays matplotlib figure window
        - May block execution until window is closed (depending on backend)
        
    Visual Properties:
        - Figure size: 10x6 inches
        - Style: Seaborn whitegrid
        - Color palette: Viridis
        - Horizontal bars sorted by activity name
        
    Example:
        >>> df = load_data()
        >>> show_totals_graph(df)  # Opens interactive chart window
    """
    sns.set_theme(style="whitegrid")
    totals = df.groupby('activity')['quantity'].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.barplot(x='quantity', y='activity', data=totals, palette='viridis')
    plt.title('Total Quantity per Activity', fontsize=16)
    plt.xlabel('Total Quantity')
    plt.ylabel('Activity')
    plt.tight_layout()
    plt.show()


def show_timeline_graph(df: pd.DataFrame, activity: Optional[str] = None) -> None:
    """
    Displays a line chart of activity over time.
    
    Creates a time-series line chart showing daily activity quantities.
    If no activity is specified, presents an interactive menu for selection.
    Uses seaborn styling with markers for each data point.
    
    Args:
        df: DataFrame with activity data
        activity: Optional activity name to plot. If None, user selects interactively
        
    Side Effects:
        - May prompt user for input if activity not specified
        - Displays matplotlib figure window
        - Prints activity menu to console when interactive
        
    Visual Properties:
        - Figure size: 12x6 inches
        - Style: Seaborn whitegrid
        - Line plot with circular markers
        - X-axis labels rotated 45 degrees for readability
        - Shows daily aggregated quantities
        
    Example:
        >>> df = load_data()
        >>> # Direct activity specification
        >>> show_timeline_graph(df, 'Water')
        
        >>> # Interactive selection
        >>> show_timeline_graph(df)
        Available activities:
        1. Water
        2. Walk
        3. Food
        Choose an activity (number) to see its timeline: 1
    """
    if activity is None:
        activities = df['activity'].unique()
        print("\nAvailable activities:")
        for i, act in enumerate(activities):
            print(f"{i + 1}. {act}")
        try:
            choice = int(input("Choose an activity (number) to see its timeline: "))
            activity = activities[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            return

    timeline_data = get_activity_timeline(df, activity)
    
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='quantity', data=timeline_data, marker='o')
    plt.title(f'Timeline for "{activity}"', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Total Quantity')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# --- UTILITY FUNCTIONS ---

def validate_api_key() -> bool:
    """
    Validates that the API key is set and has a valid format.
    
    Checks if an API key is available from either the config file or environment
    variable, and validates its basic format. This validation is critical before
    making any API calls to prevent authentication errors.
    
    Returns:
        bool: True if API key is set and appears valid, False otherwise
        
    Validation Criteria:
        - Key is not empty
        - Key starts with expected prefix ('sk-or-' or 'sk-')
        - Key has minimum expected length (20 characters)
        
    Example:
        >>> # With valid API key
        >>> set_api_key('sk-or-v1-valid-key-example')
        >>> validate_api_key()
        True
        
        >>> # With invalid API key
        >>> set_api_key('invalid-key')
        >>> validate_api_key()
        False
        
        >>> # Without API key
        >>> set_api_key('')
        >>> validate_api_key()
        False
    """
    api_key = get_api_key()
    if not api_key or not api_key.strip():
        return False
    
    # Basic format validation for OpenRouter API keys
    if not api_key.startswith(('sk-or-', 'sk-')):
        return False
    
    # Minimum length check
    if len(api_key) < 20:
        return False
    
    return True


def get_available_activities(df: pd.DataFrame) -> List[str]:
    """
    Returns list of unique activities in the dataset.
    
    Extracts all unique activity types that have been logged in the data.
    Useful for generating activity selection menus and validating user input.
    
    Args:
        df: DataFrame with activity data, must contain 'activity' column
        
    Returns:
        List[str]: Sorted list of unique activity names, empty list if DataFrame is empty
        
    Example:
        >>> data = pd.DataFrame({
        ...     'activity': ['Water', 'Walk', 'Water', 'Food'],
        ...     'quantity': [500, 2, 300, 1]
        ... })
        >>> get_available_activities(data)
        ['Food', 'Walk', 'Water']
        
        >>> empty_df = pd.DataFrame()
        >>> get_available_activities(empty_df)
        []
    """
    return sorted(df['activity'].unique().tolist()) if not df.empty else []


def format_activity_summary(activities: List[Dict]) -> str:
    """
    Formats a list of today's activities into a human-readable string.
    
    Args:
        activities: A list of activity dictionaries (e.g., from df.to_dict('records')).
                    Each dict should have 'activity', 'quantity', 'unit'.
                    
    Returns:
        str: A formatted string summarizing the activities.
             Example: "- Water: 1.0 liter\\n- Walk: 2.5 km"
             Returns "No activities logged yet." if the list is empty.
    """
    if not activities:
        return "No activities logged yet."

    summary_parts = []
    for activity_data in activities:
        # Ensure quantity is float for consistent formatting
        try:
            quantity = float(activity_data['quantity'])
        except (ValueError, TypeError):
            quantity = 0.0 # Default if conversion fails

        unit = activity_data.get('unit', '') # Get unit, default to empty string if missing
        
        # Format quantity to one decimal place
        formatted_quantity = "{:.1f}".format(quantity)
        
        summary_parts.append(f"- {activity_data['activity']}: {formatted_quantity} {unit}".strip())
        
    return "\\n".join(summary_parts) 