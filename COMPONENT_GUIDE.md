# Component Guide - Personal Life Tracker

## Architecture Overview

The Personal Life Tracker follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐     ┌─────────────────┐
│   CLI Interface │     │  Web Interface  │
│    (cli.py)     │     │(streamlit_app.py)│
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
              ┌──────▼──────┐
              │ Core Logic  │
              │ (logic.py)  │
              └──────┬──────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
    ┌─────────┐           ┌─────────────┐
    │   CSV   │           │ OpenRouter  │
    │  Files  │           │     API     │
    └─────────┘           └─────────────┘
```

## Core Components

### 1. logic.py - Business Logic Core

The heart of the application containing all data processing and analysis functions.

**Key Functions**:

#### Activity Logging
- `log_activity(user_input: str) -> bool`: Main entry point for logging
- `analyze_with_ai(user_input: str) -> List[Dict]`: AI text analysis
- `save_to_csv(activities: List[Dict]) -> bool`: Data persistence

#### Data Loading
- `load_data() -> Optional[pd.DataFrame]`: Load and clean CSV data
- `get_data_summary(df: pd.DataFrame) -> Dict`: Generate statistics

#### Analysis Functions
- `get_totals(df: pd.DataFrame) -> pd.Series`: Aggregate totals
- `get_today_activities(df: pd.DataFrame) -> pd.DataFrame`: Today's filter
- `get_date_range_activities(df, start, end) -> pd.DataFrame`: Date filtering
- `get_activity_timeline(df, activity, group_by) -> pd.DataFrame`: Time series

#### Visualization Helpers
- `create_totals_chart_data(df) -> Tuple[List, List]`: Bar chart data
- `create_timeline_chart_data(df, activity) -> Tuple[List, List]`: Line chart data
- `show_totals_graph(df) -> None`: Matplotlib bar chart
- `show_timeline_graph(df, activity) -> None`: Matplotlib line chart

#### Utilities
- `validate_api_key() -> bool`: Check API key configuration
- `get_available_activities(df) -> List[str]`: List unique activities
- `format_activity_summary(activities) -> str`: Format for display

### 2. cli.py - Command Line Interface

Provides a user-friendly command-line interface for all functionality.

**Commands**:

```bash
# Log new activity
python cli.py log "drank 500ml of water"

# View analysis
python cli.py analyze --totals      # Total quantities
python cli.py analyze --today       # Today's activities
python cli.py analyze --graph-totals    # Bar chart
python cli.py analyze --graph-timeline  # Time series chart
```

**Key Functions**:
- `handle_log_command(text: str) -> None`: Process log commands
- `handle_analyze_command(args) -> None`: Process analysis commands
- `main()`: Argument parser and command router

### 3. streamlit_app.py - Web Interface

Modern web interface with real-time updates and interactive visualizations.

**Features**:
- Sidebar for activity logging
- Multi-tab analysis views
- Interactive date filtering
- Real-time chart updates

**Key Sections**:
- **Sidebar**: Natural language input with AI analysis
- **Overview Tab**: Summary metrics and distribution charts
- **Today Tab**: Chronological activity list
- **Totals Tab**: Aggregate bar charts
- **Timeline Tab**: Time series visualizations

**Configuration Constants**:
```python
LAYOUT_CONFIG = {
    "metrics_columns": 4,
    "filter_columns": 3,
    "chart_height": 400,
    "timeline_height": 500
}

DATE_FILTER_OPTIONS = [
    "All", "Today", "Last 7 days", 
    "Last 30 days", "Custom"
]
```

## Data Flow

### 1. Activity Logging Flow

```
User Input → AI Analysis → Structured Data → CSV Storage
     ↓             ↓              ↓              ↓
"drank water" → Gemini AI → {activity: "Water", quantity: 500, unit: "ml"} → livslogg.csv
```

### 2. Data Analysis Flow

```
CSV File → DataFrame → Filtering → Aggregation → Visualization
    ↓          ↓           ↓           ↓             ↓
livslogg.csv → pandas → date/activity → sum/group → charts
```

## Integration Patterns

### Using Core Logic in New Interfaces

```python
from logic import (
    log_activity,
    load_data,
    get_totals,
    validate_api_key
)

# Check API key before operations
if not validate_api_key():
    handle_api_key_error()

# Log new activity
success = log_activity("your activity text")

# Load and analyze data
df = load_data()
if df is not None:
    totals = get_totals(df)
    display_results(totals)
```

### Adding New Activity Categories

1. Update `ACTIVITY_CATEGORIES` in logic.py
2. Update AI prompt in `analyze_with_ai()`
3. Update documentation

### Creating Custom Visualizations

```python
# Use the helper functions to get data
from logic import create_timeline_chart_data

dates, quantities = create_timeline_chart_data(df, 'Water')

# Create your own visualization
your_custom_chart(dates, quantities)
```

## Best Practices

### 1. Error Handling

Always wrap API calls and file operations:

```python
try:
    activities = analyze_with_ai(user_input)
except Exception as e:
    handle_error(f"Analysis failed: {e}")
```

### 2. Data Validation

Validate data after loading:

```python
df = load_data()
if df is None:
    print("No data file found")
elif df.empty:
    print("Data file is empty")
else:
    # Process data
```

### 3. User Feedback

Provide clear feedback for all operations:

```python
# CLI
print("✅ Successfully logged activities")
print("❌ Failed to save data")

# Web
st.success("Activities saved!")
st.error("Failed to analyze input")
```

## Extending the System

### Adding a New Interface

1. Create new interface file (e.g., `mobile_api.py`)
2. Import required functions from `logic.py`
3. Implement interface-specific presentation
4. Handle user input/output appropriately

Example structure:

```python
from logic import log_activity, load_data, get_totals

def handle_api_request(request):
    # Validate request
    if not request.data:
        return error_response("No data provided")
    
    # Use core logic
    success = log_activity(request.data['text'])
    
    # Return appropriate response
    return json_response({"success": success})
```

### Adding New Analysis Functions

1. Add function to logic.py following existing patterns
2. Add appropriate type hints and documentation
3. Update interfaces to expose new functionality
4. Add tests for new functions

Example:

```python
def get_weekly_average(df: pd.DataFrame, activity: str) -> float:
    """
    Calculate weekly average for an activity.
    
    Args:
        df: Activity data
        activity: Activity type to analyze
        
    Returns:
        float: Average quantity per week
    """
    # Implementation here
```

## Testing Components

### Unit Testing Core Logic

```python
import pytest
from logic import analyze_with_ai, format_activity_summary

def test_format_activity_summary():
    activities = [
        {"activity": "Water", "quantity": 500, "unit": "ml"}
    ]
    result = format_activity_summary(activities)
    assert "Water: 500 ml" in result
```

### Integration Testing

Test the full flow from input to storage:

```python
def test_full_logging_flow():
    # Mock API response
    with mock.patch('logic.analyze_with_ai') as mock_ai:
        mock_ai.return_value = [
            {"activity": "Water", "quantity": 500, "unit": "ml"}
        ]
        
        # Test logging
        success = log_activity("test input")
        assert success
        
        # Verify data saved
        df = load_data()
        assert len(df) > 0
```

## Common Issues and Solutions

### Issue: "No module named logic"

**Solution**: Ensure you're running from the project directory:
```bash
cd /path/to/tracker
python cli.py log "activity"
```

### Issue: Charts not displaying

**Solution**: Install visualization dependencies:
```bash
pip install matplotlib seaborn plotly
```

### Issue: API key not recognized

**Solution**: Check both environment variable and config.json:
```bash
export OPENROUTER_API_KEY='your-key'
# OR save in config.json
```

## Performance Considerations

1. **Large CSV Files**: Consider implementing pagination or date-based filtering
2. **API Rate Limits**: Implement caching for repeated queries
3. **Memory Usage**: Use chunking for very large datasets
4. **Startup Time**: Lazy load heavy dependencies