# API Reference

## Core Module: `logic.py`

The `logic.py` module contains all core business logic for the Personal Life Tracker. This centralized approach ensures consistency across different interfaces.

### Constants

```python
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-flash-1.5"
CSV_FILENAME = "livslogg.csv"
ACTIVITY_CATEGORIES = ['Water', 'Cannabis', 'Cigarette', 'Alcohol', 'Sex', 'Walk', 'Food']
```

### Logging Functions

#### `log_activity(user_input: str) -> bool`
Main entry point for logging activities.

**Parameters:**
- `user_input` (str): Natural language description of activities

**Returns:**
- `bool`: True if successful, False otherwise

**Raises:**
- `ValueError`: If API key is not set
- `Exception`: If analysis or saving fails

**Example:**
```python
success = log_activity("drank 500ml of water and walked 2km")
```

#### `analyze_with_ai(user_input: str) -> List[Dict]`
Sends user input to AI for parsing into structured data.

**Parameters:**
- `user_input` (str): Natural language text to analyze

**Returns:**
- `List[Dict]`: List of activity dictionaries with keys:
  - `activity` (str): Activity type from ACTIVITY_CATEGORIES
  - `quantity` (float): Amount of the activity
  - `unit` (str): Unit of measurement

**Raises:**
- `Exception`: If API call fails or response parsing fails

**Example:**
```python
activities = analyze_with_ai("walked 5km and drank 2 glasses of water")
# Returns: [
#   {"activity": "Walk", "quantity": 5, "unit": "km"},
#   {"activity": "Water", "quantity": 2, "unit": "glasses"}
# ]
```

#### `save_to_csv(activities: List[Dict]) -> bool`
Saves parsed activities to the CSV file.

**Parameters:**
- `activities` (List[Dict]): List of activity dictionaries

**Returns:**
- `bool`: True if successful, False otherwise

**Raises:**
- `Exception`: If file operation fails

### Data Loading Functions

#### `load_data() -> Optional[pd.DataFrame]`
Loads and cleans data from the CSV file.

**Returns:**
- `pd.DataFrame`: DataFrame with columns: timestamp, activity, quantity, unit, date
- `None`: If file doesn't exist

**Raises:**
- `Exception`: If loading or parsing fails

**Data Processing:**
- Converts timestamp to datetime
- Converts quantity to numeric
- Drops rows with invalid data
- Adds date column for easier filtering

#### `get_data_summary(df: pd.DataFrame) -> Dict`
Returns comprehensive statistics about the dataset.

**Parameters:**
- `df` (pd.DataFrame): Activity data

**Returns:**
- `Dict`: Summary with keys:
  - `total_activities` (int): Total number of logged activities
  - `unique_activities` (int): Number of unique activity types
  - `date_range` (Dict): First/last entry dates and days tracked
  - `activity_counts` (Dict): Count of each activity type
  - `total_quantities` (Dict): Sum of quantities per activity

### Analysis Functions

#### `get_totals(df: pd.DataFrame) -> pd.Series`
Calculates total quantities for each activity type.

**Parameters:**
- `df` (pd.DataFrame): Activity data

**Returns:**
- `pd.Series`: Index=activity names, Values=total quantities

**Example:**
```python
totals = get_totals(df)
# Returns: Series with index=['Water', 'Walk', ...] and values=[1500.0, 25.5, ...]
```

#### `get_today_activities(df: pd.DataFrame) -> pd.DataFrame`
Filters activities logged today.

**Parameters:**
- `df` (pd.DataFrame): Activity data

**Returns:**
- `pd.DataFrame`: Today's activities sorted by timestamp

#### `get_date_range_activities(df: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame`
Filters activities within a date range.

**Parameters:**
- `df` (pd.DataFrame): Activity data
- `start_date` (date): Start date (inclusive)
- `end_date` (date): End date (inclusive)

**Returns:**
- `pd.DataFrame`: Filtered activities

#### `get_activity_timeline(df: pd.DataFrame, activity: str, group_by: str = 'day') -> pd.DataFrame`
Aggregates activity data over time periods.

**Parameters:**
- `df` (pd.DataFrame): Activity data
- `activity` (str): Activity name to filter
- `group_by` (str): Aggregation period ('day', 'week', 'month')

**Returns:**
- `pd.DataFrame`: Timeline data with date/period and quantity columns

**Raises:**
- `ValueError`: If group_by is not valid

### Visualization Helper Functions

#### `create_totals_chart_data(df: pd.DataFrame) -> Tuple[List[str], List[float]]`
Prepares data for totals bar chart.

**Parameters:**
- `df` (pd.DataFrame): Activity data

**Returns:**
- `Tuple[List[str], List[float]]`: (activity_names, quantities)

#### `create_timeline_chart_data(df: pd.DataFrame, activity: str) -> Tuple[List[date], List[float]]`
Prepares data for timeline chart.

**Parameters:**
- `df` (pd.DataFrame): Activity data
- `activity` (str): Activity name

**Returns:**
- `Tuple[List[date], List[float]]`: (dates, quantities)

### Matplotlib Visualization Functions

#### `show_totals_graph(df: pd.DataFrame) -> None`
Displays a horizontal bar chart of total quantities.

**Parameters:**
- `df` (pd.DataFrame): Activity data

**Side Effects:**
- Shows matplotlib plot window

#### `show_timeline_graph(df: pd.DataFrame, activity: Optional[str] = None) -> None`
Displays a line chart of activity over time.

**Parameters:**
- `df` (pd.DataFrame): Activity data
- `activity` (Optional[str]): Activity name. If None, prompts user to choose

**Side Effects:**
- Shows matplotlib plot window
- May prompt for user input if activity not specified

### Utility Functions

#### `validate_api_key() -> bool`
Checks if API key is configured.

**Returns:**
- `bool`: True if API key is set and non-empty

#### `get_available_activities(df: pd.DataFrame) -> List[str]`
Returns unique activity names in the dataset.

**Parameters:**
- `df` (pd.DataFrame): Activity data

**Returns:**
- `List[str]`: Unique activity names

#### `format_activity_summary(activities: List[Dict]) -> str`
Formats activities into human-readable text.

**Parameters:**
- `activities` (List[Dict]): List of activity dictionaries

**Returns:**
- `str`: Formatted summary with bullet points

**Example:**
```python
summary = format_activity_summary([
    {"activity": "Water", "quantity": 500, "unit": "ml"},
    {"activity": "Walk", "quantity": 2, "unit": "km"}
])
# Returns:
# - Water: 500 ml
# - Walk: 2 km
```

## CLI Module: `cli.py`

### Functions

#### `handle_log_command(text: str) -> None`
Processes the log command from CLI.

**Parameters:**
- `text` (str): Activity description

**Side Effects:**
- Prints success/error messages
- Saves data to CSV file

#### `handle_analyze_command(args) -> None`
Processes analyze command with various options.

**Parameters:**
- `args`: Argparse namespace with flags (totals, today, graph_totals, graph_timeline)

**Side Effects:**
- Prints analysis results
- May show matplotlib graphs

#### `main() -> None`
CLI entry point with argument parsing.

**Command Structure:**
```bash
cli.py log <text>
cli.py analyze [--totals] [--today] [--graph-totals] [--graph-timeline]
```

## Web Module: `streamlit_app.py`

### Functions

#### `main() -> None`
Streamlit application entry point.

**Features:**
- Sidebar for activity logging
- Tabbed interface for different views
- Date and activity filtering
- Interactive Plotly charts

**UI Components:**
- Log input area with AI analysis
- Overview tab with metrics and pie chart
- Today tab with chronological view
- Totals tab with bar chart
- Timeline tab with line charts

## Error Handling

All functions use exception handling with descriptive error messages. Common exceptions:

- `ValueError`: Invalid input or missing configuration
- `FileNotFoundError`: Data file doesn't exist
- `requests.RequestException`: API call failures
- `json.JSONDecodeError`: Invalid API response
- `pd.errors.ParserError`: Corrupted CSV data

## Best Practices

1. **Always validate API key** before making AI calls
2. **Check for empty DataFrames** before analysis
3. **Use type hints** for better IDE support
4. **Handle exceptions gracefully** with user-friendly messages
5. **Centralize business logic** in logic.py
6. **Keep interfaces thin** - presentation only