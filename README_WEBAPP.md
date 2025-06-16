# Personal Life Tracker - Web Application

## Quick Start

1. **Make sure you have your API key set:**
   ```bash
   export OPENROUTER_API_KEY='your-api-key-here'
   ```

2. **Run the web app:**
   ```bash
   ./run_webapp.sh
   ```
   
   Or directly with:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open your browser** to http://localhost:8501

## Features

### 📝 Logging Interface
- Natural language input (e.g., "I drank 500ml of water and walked 2km")
- Instant feedback with success animations
- Automatic parsing using AI

### 📊 Analysis Dashboard

#### Overview Tab
- Key metrics: Total activities, unique activities, days tracked
- Activity distribution pie chart
- Quick stats at a glance

#### Today Tab
- Chronological list of today's activities
- Daily summary with totals

#### Totals Tab
- Bar charts showing cumulative quantities
- Sortable data table
- Group by activity type and unit

#### Timeline Tab
- Interactive line charts with trends
- Date range selector
- Compare multiple activities
- Zoom and pan capabilities

### ⚙️ Filters & Configuration
- Date range filters (Today, Last 7/30 days, Custom)
- Activity type filters
- All filters apply across all tabs

## Tips

1. **Mobile Friendly**: The app works great on phones and tablets
2. **Interactive Charts**: Click legend items to show/hide data
3. **Export Charts**: Use the camera icon on charts to save images
4. **Keyboard Shortcut**: Press Enter after typing to save quickly

## Comparison with CLI

| Feature | CLI (`python main.py`) | Web App |
|---------|------------------------|----------|
| Logging | Command line args | Text input box |
| Visualization | Static matplotlib | Interactive Plotly |
| Filtering | Limited | Full date/activity filters |
| Interface | Terminal only | Browser-based |
| Mobile | No | Yes |

Both versions use the same `livslogg.csv` file, so you can switch between them anytime!

## Troubleshooting

- **"API key not found"**: Make sure to export your OPENROUTER_API_KEY
- **Port already in use**: Change port with `--server.port 8502`
- **Can't connect**: Check firewall settings for port 8501