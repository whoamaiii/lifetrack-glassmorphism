# CLAUDE.md - Personal Life Tracker

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal Life Tracker is a Python-based application that uses AI to parse natural language input and track daily activities. It features a clean architecture with separation of concerns, multiple interfaces (CLI and Web), and comprehensive data analysis capabilities.

**Tech Stack:**
- **Python 3.8+** - Core language
- **Streamlit** - Web interface framework
- **Pandas** - Data analysis and manipulation
- **Matplotlib/Seaborn** - CLI visualizations
- **Plotly** - Interactive web charts
- **OpenRouter API** - AI service (Google Gemini Flash 1.5)
- **CSV** - Simple, portable data storage

## Architecture

The project follows a modular architecture with clear separation of concerns:

```
tracker/
├── logic.py           # Core business logic (single source of truth)
├── cli.py            # Command-line interface (presentation only)
├── streamlit_app.py  # Web interface (presentation only)
├── livslogg.csv      # Data storage (CSV format)
│
├── [DEPRECATED FILES - Do not use]
├── main.py           # Original combined implementation
├── tracker.py        # Original Norwegian version (SECURITY RISK: hardcoded API key!)
└── analyser.py       # Original Norwegian analysis tool
```

### Design Principles

1. **Separation of Concerns**: Business logic isolated in `logic.py`
2. **DRY (Don't Repeat Yourself)**: No code duplication between interfaces
3. **Type Safety**: Type hints throughout for better IDE support
4. **Backward Compatibility**: Supports old Norwegian data format
5. **Security First**: No hardcoded API keys, environment variables only

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (required)
export OPENROUTER_API_KEY='your-key-here'

# Command-line interface
python cli.py log "drank 500ml of water"
python cli.py analyze --totals
python cli.py analyze --today
python cli.py analyze --graph-totals
python cli.py analyze --graph-timeline

# Web interface
./run_webapp.sh
# or
streamlit run streamlit_app.py

# Run on custom port
./run_webapp.sh 8502

# Allow network access (careful!)
./run_webapp.sh --network
```

## Key Functions in logic.py

### Core Logging
- `log_activity(user_input: str) -> bool` - Main entry point for logging
- `analyze_with_ai(user_input: str) -> List[Dict]` - AI parsing
- `save_to_csv(activities: List[Dict]) -> bool` - Data persistence

### Data Loading
- `load_data() -> Optional[pd.DataFrame]` - Load and clean CSV data
- `get_data_summary(df: pd.DataFrame) -> Dict` - Statistical overview

### Analysis
- `get_totals(df: pd.DataFrame) -> pd.Series` - Activity totals
- `get_today_activities(df: pd.DataFrame) -> pd.DataFrame` - Today's data
- `get_date_range_activities(df, start_date, end_date) -> pd.DataFrame` - Date filtering
- `get_activity_timeline(df, activity, group_by) -> pd.DataFrame` - Time series

### Utilities
- `validate_api_key() -> bool` - Check API configuration
- `format_activity_summary(activities: List[Dict]) -> str` - Human-readable formatting

## Data Schema

CSV format with columns:
- `timestamp` (ISO 8601): When activity was logged
- `activity` (string): Category from ACTIVITY_CATEGORIES
- `quantity` (float): Amount
- `unit` (string): Unit of measurement

Supported activities: Water, Cannabis, Cigarette, Alcohol, Sex, Walk, Food

## Environment Variables

Required:
- `OPENROUTER_API_KEY` - Your OpenRouter API key

Optional (future use):
- `TRACKER_CSV_FILE` - Custom CSV filename
- `TRACKER_AI_MODEL` - Different AI model
- `STREAMLIT_SERVER_PORT` - Custom web port

## Security Considerations

1. **NEVER commit API keys** - Use environment variables only
2. **Avoid tracker.py** - Contains hardcoded API key (security risk)
3. **Local data storage** - No cloud sync by default
4. **Input validation** - AI responses validated before storage
5. **File permissions** - Consider restricting CSV file access

## Common Tasks

### Adding a New Activity Type
1. Update `ACTIVITY_CATEGORIES` in `logic.py`
2. Update AI prompt in `analyze_with_ai()`
3. Update documentation
4. Test with various phrasings

### Adding a New Analysis Feature
1. Add function to `logic.py`
2. Add CLI argument in `cli.py` if needed
3. Add UI component in `streamlit_app.py` if needed
4. Update API documentation

### Debugging API Issues
1. Check API key is set: `echo $OPENROUTER_API_KEY`
2. Verify API balance at OpenRouter
3. Check network connectivity
4. Enable debug logging if implemented

## Migration from Old Versions

### From Norwegian Version (tracker.py/analyser.py)
- Data in `livslogg.csv` is automatically compatible
- Column names auto-translate (tidspunkt→timestamp, etc.)
- Use `cli.py` instead of `tracker.py`
- Use `cli.py analyze` instead of `analyser.py`

### From Combined Version (main.py)
- Same commands work with `cli.py`
- All functionality preserved
- Better error handling and messages

## Testing Approach

While no formal tests exist yet, when testing:
1. Test core logic functions in isolation
2. Test with various natural language inputs
3. Test edge cases (empty data, invalid input)
4. Test both interfaces with same operations

## Performance Considerations

- CSV format is simple but may slow with >100k rows
- Consider SQLite for large datasets
- Matplotlib graphs may be slow with many data points
- Web interface has better performance for visualizations

## Future Enhancements

Potential improvements maintaining current architecture:
1. Add authentication to web interface
2. Implement data export (JSON, Excel)
3. Add more activity categories
4. Support for multiple users
5. Data encryption for sensitive information
6. REST API for third-party integrations
7. Mobile app using the same `logic.py`

## Important Notes

- **Deprecated Files**: Don't use `main.py`, `tracker.py`, or `analyser.py`
- **Security**: Remove/ignore `tracker.py` due to hardcoded API key
- **Data Format**: English column names are standard, Norwegian supported for compatibility
- **Error Handling**: All functions include try/except with descriptive messages
- **Type Hints**: Use throughout for better IDE support and documentation