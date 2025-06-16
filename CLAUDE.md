# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Personal Life Tracker** - A comprehensive activity tracking application with natural language processing capabilities. Users can log daily activities using natural language, and the system uses AI to parse and store structured data for analysis and visualization.

**Tech Stack:**
- **Python 3.8+** - Core programming language
- **Pandas** - Data manipulation and analysis
- **Streamlit** - Web interface framework
- **Matplotlib/Seaborn** - CLI visualizations
- **Plotly** - Web visualizations
- **OpenRouter API** - AI text analysis (Google Gemini Flash 1.5)
- **CSV** - Data storage format

## Architecture

The project follows a modular architecture with clear separation of concerns:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLI       │     │   Web App   │     │   Future    │
│  (cli.py)   │     │(streamlit.py)│     │ Interfaces  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                            │
                    ┌───────▼────────┐
                    │   Core Logic   │
                    │   (logic.py)   │
                    └───────┬────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────┐               ┌──────────────┐
       │ CSV File │               │ OpenRouter   │
       │Storage   │               │     API      │
       └──────────┘               └──────────────┘
```

## Development Commands

### Command Line Interface
```bash
# Log activities
python cli.py log "drank 500ml of water and walked 2km"

# View analysis
python cli.py analyze --totals        # Show total quantities
python cli.py analyze --today         # Show today's activities
python cli.py analyze --graph-totals  # Display bar chart
python cli.py analyze --graph-timeline # Display timeline chart
```

### Web Interface
```bash
# Start web app
streamlit run streamlit_app.py

# Or use the launcher script
./run_webapp.sh               # Default port 8501
./run_webapp.sh 8502          # Custom port
./run_webapp.sh --network     # Network access (careful!)
```

## Code Documentation Standards

All code is extensively documented with:

1. **Module Docstrings**: Overview, architecture, and usage examples
2. **Function Docstrings**: 
   - Description and purpose
   - Args with types and descriptions
   - Returns with types and descriptions
   - Raises for error conditions
   - Examples for complex functions
3. **Inline Comments**: For complex logic and business rules
4. **Type Hints**: Throughout all function signatures

## Key Files

### Core Logic (logic.py)
- `log_activity()`: Main entry point for logging
- `analyze_with_ai()`: AI text analysis
- `save_to_csv()`: Data persistence
- `load_data()`: Data loading with cleaning
- `get_totals()`, `get_today_activities()`: Analysis functions
- `show_totals_graph()`, `show_timeline_graph()`: Visualizations

### Interfaces
- `cli.py`: Command-line interface with argparse
- `streamlit_app.py`: Web interface with real-time updates

### Configuration
- API key management via config.json or environment variable
- `OPENROUTER_API_KEY` environment variable
- Activity categories: Water, Cannabis, Cigarette, Alcohol, Sex, Walk, Food

## Data Format

CSV file (`livslogg.csv`) with columns:
- `timestamp`: ISO format datetime
- `activity`: Category from predefined list
- `quantity`: Numeric amount
- `unit`: Measurement unit

Supports both English and Norwegian column names for backward compatibility.

## API Integration

### OpenRouter Configuration
- Endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Model: `google/gemini-flash-1.5`
- Authentication: Bearer token
- Response format: JSON

### Error Handling
- API key validation before requests
- Timeout handling (30 seconds)
- Graceful error messages for users
- Exception propagation with context

## Testing Guidelines

### Unit Tests
- Test core logic functions independently
- Mock external dependencies (API calls, file I/O)
- Use pytest for test organization

### Integration Tests
- Test full flow from input to storage
- Verify data persistence
- Check visualization generation

## Security Considerations

1. **API Keys**:
   - Never hardcode in source
   - Use environment variables or secure config
   - Validate format before use

2. **Data Privacy**:
   - No personal identifiers in logs
   - Local CSV storage only
   - User controls all data

## Common Tasks

### Adding New Activity Categories
1. Update `ACTIVITY_CATEGORIES` in logic.py
2. Update AI prompt in `analyze_with_ai()`
3. Update documentation

### Creating New Interface
1. Import required functions from logic.py
2. Handle user input/output
3. Implement interface-specific features
4. Maintain consistent error handling

### Debugging
- Enable verbose logging with environment variables
- Check CSV file for data integrity
- Verify API key configuration
- Test with simple inputs first

## Performance Optimization

- Lazy loading of visualization libraries
- Efficient pandas operations for large datasets
- Caching for repeated API queries (future)
- Pagination for data display (future)

## Future Enhancements

1. **Data Management**:
   - Database backend option
   - Data export/import features
   - Backup automation

2. **Analytics**:
   - Advanced statistical analysis
   - Predictive insights
   - Goal setting and tracking

3. **User Experience**:
   - Mobile app interface
   - Voice input support
   - Real-time notifications

4. **Integration**:
   - Health app connections
   - Wearable device support
   - Social sharing features