# 🎯 Personal Life Tracker - Professional Architecture

A comprehensive system for tracking and analyzing your daily activities using natural language input and AI-powered parsing.

## 🏗️ Architecture Overview 

This project follows professional software engineering practices with **separation of concerns**:

```
📁 Personal Life Tracker/
├── 🧠 logic.py          # Core business logic (WHAT the app does)
├── 📱 cli.py            # Command-line interface (HOW it looks in terminal)
├── 🌐 streamlit_app.py  # Web interface (HOW it looks in browser)
├── 📊 livslogg.csv      # Data storage
├── 📋 requirements.txt  # Dependencies
└── 🚀 run_webapp.sh     # Quick launcher
```

### Why This Architecture?

- **🔄 DRY Principle**: All logic is in one place - no code duplication
- **🔧 Easy Maintenance**: Fix bugs once, and both interfaces benefit
- **📈 Scalable**: Adding new interfaces (mobile app, API, etc.) is simple
- **🧪 Testable**: Core logic can be tested independently
- **👥 Team-Friendly**: Clear separation makes collaboration easier

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up your API key

**Option A: Using the CLI (Recommended)**
```bash
python cli.py config --set-api-key
```

**Option B: Using the Web Interface**
- Start the web app and use the Settings section in the sidebar

**Option C: Environment Variable (Legacy)**
```bash
export OPENROUTER_API_KEY='your-api-key-here'
```

### 3. Choose your interface:

**Option A: Web Interface (Recommended)**
```bash
./run_webapp.sh
# or directly: streamlit run streamlit_app.py
```

**Option B: Command Line Interface**
```bash
python cli.py log "drank 500ml of water and walked 2km"
python cli.py analyze --totals
```

## 📱 CLI Interface (`cli.py`)

Perfect for quick logging and automation.

### Commands:
```bash
# Configuration
python cli.py config --set-api-key  # Set your API key
python cli.py config --show         # View current settings

# Log activities
python cli.py log "your activity description"

# View analysis
python cli.py analyze --totals      # Show total quantities
python cli.py analyze --today       # Show today's activities  
python cli.py analyze --graph-totals    # Bar chart of totals
python cli.py analyze --graph-timeline  # Timeline for specific activity
```

### Examples:
```bash
python cli.py log "drank 3 glasses of water, smoked 2 cigarettes"
python cli.py log "walked 5km and ate a healthy salad"
python cli.py analyze --totals
```

## 🌐 Web Interface (`streamlit_app.py`)

Modern, interactive web application with rich visualizations.

### Features:
- **📝 Smart Logging**: Natural language input with instant AI analysis for activities.
- **📊 Interactive Charts**: Visualizations for activity trends.
- **🔍 Advanced Filtering**: Date ranges, activity types for analysis.
- **📱 Mobile Friendly**: Responsive design for all devices.
- **🎨 Professional UI**: Clean, modern interface.
- ✅ **Task Management**: Add, edit, and track your to-dos with due dates and priorities.
- 💬 **AI Assistant**: Interact with the AI health coach for advice and support.

### Tabs:
1. **🏠 Home / Overview**: Key metrics and quick actions.
2. **📊 Analysis**: Detailed charts and statistical views for activities.
3. **✍️ Log**: Log new activities and quick-add tasks.
4. **✅ Tasks**: Manage your to-do list with due dates and priorities.
5. **💬 Chat**: Interact with the AI health coach.
6. **⚙️ Settings**: Configure API keys and application preferences.

## 🧠 Core Logic (`logic.py`)

The heart of the application - contains all business functions:

### Key Functions:
- `log_activity()` - AI analysis and data saving
- `load_data()` - Data loading and cleaning
- `get_totals()` - Activity quantity summaries
- `get_today_activities()` - Today's activity filtering
- `get_data_summary()` - Statistical overview
- And many more...

## 📊 Supported Activities

The AI recognizes these activity categories:
- 💧 **Water** (ml, glasses, etc.)
- 🌿 **Cannabis** (joints, grams, etc.)
- 🚬 **Cigarette** (cigarettes, packs, etc.)
- 🍷 **Alcohol** (drinks, ml, etc.)
- ❤️ **Sex** (sessions, minutes, etc.)
- 🚶‍♂️ **Walk** (km, steps, minutes, etc.)
- 🍎 **Food** (meals, calories, etc.)

## 💡 Usage Examples

### Natural Language Input:
- "drank 500ml of water"
- "smoked 2 cigarettes and walked 3km"  
- "had 2 glasses of wine with dinner"
- "30 minute walk in the park"

### The AI automatically:
- Identifies multiple activities in one sentence
- Extracts quantities and units
- Categorizes activities correctly
- Handles various phrasings and units

## 🔧 Technical Details

### Dependencies:
- **Core**: `pandas`, `requests`, `python-dateutil`
- **Web UI**: `streamlit`, `plotly`
- **CLI Charts**: `matplotlib`, `seaborn`
- **AI Integration**: OpenRouter API (Gemini Flash 1.5)

### Data Format:
```csv
timestamp,activity,quantity,unit
2024-01-01T10:00:00,Water,500,ml
2024-01-01T10:30:00,Walk,2,km
```

## 🚀 Development 

### Adding New Features:
1. **Add business logic** to `logic.py`
2. **Update CLI** in `cli.py` if needed  
3. **Update web UI** in `streamlit_app.py` if needed
4. Both interfaces automatically benefit from core improvements!

### Adding New Interfaces:
Want a mobile app? Discord bot? REST API? Just import from `logic.py`:

```python
from logic import log_activity, load_data, get_totals
# Build any interface you want!
```

## 🔄 Data Compatibility

All your existing data in `livslogg.csv` remains fully compatible with this version!
The modern architecture uses the same data format, ensuring seamless continuity. 

## 🛠️ Troubleshooting

- **"API key not found"**: `export OPENROUTER_API_KEY='your-key'`
- **"Port already in use"**: `streamlit run streamlit_app.py --server.port 8502`
- **Import errors**: `pip install -r requirements.txt`
- **Data issues**: Check that `livslogg.csv` exists and has proper headers

## 🎉 What's New in v3.0

✅ **Professional Architecture**: Separation of concerns  
✅ **Unified Data Model**: Consistent English column names  
✅ **Enhanced Error Handling**: Better user feedback  
✅ **Improved Performance**: Optimized data processing  
✅ **Better Documentation**: Clear code and comments  
✅ **Future-Proof Design**: Easy to extend and maintain  

---

*Personal Life Tracker v3.0 - Professional Architecture*  
*Built with ❤️ using Python, Streamlit, and AI*