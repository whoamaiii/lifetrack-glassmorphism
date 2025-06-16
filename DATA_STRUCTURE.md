# 📊 Data Structure Documentation

> **Understanding the Personal Life Tracker data format**

This document explains the data structure, CSV format, and data flow in the Personal Life Tracker application.

## 📋 Table of Contents

1. [CSV File Structure](#csv-file-structure)
2. [Data Types](#data-types)
3. [Column Mapping](#column-mapping)
4. [Data Validation](#data-validation)
5. [AI Processing](#ai-processing)
6. [Data Flow](#data-flow)
7. [Backward Compatibility](#backward-compatibility)
8. [Common Issues](#common-issues)

---

## 📁 CSV File Structure

### File Location
- **Filename**: `livslogg.csv`
- **Location**: Project root directory
- **Encoding**: UTF-8

### Column Structure
The CSV file contains the following columns (English format):

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `timestamp` | DateTime | ISO format timestamp | `2025-01-15T14:30:25.123456` |
| `activity` | String | Activity name | `"Water"`, `"Walk"`, `"Cannabis"` |
| `quantity` | Float | Numeric amount | `500.0`, `2.5`, `1.0` |
| `unit` | String | Unit of measurement | `"ml"`, `"km"`, `"puff"` |

### Example CSV Content
```csv
timestamp,activity,quantity,unit
2025-01-15T14:30:25.123456,Water,500.0,ml
2025-01-15T15:45:10.987654,Walk,2.5,km
2025-01-15T16:20:00.000000,Cannabis,1.0,puff
```

---

## 🔢 Data Types

### Timestamp
- **Format**: ISO 8601 format (`YYYY-MM-DDTHH:MM:SS.ffffff`)
- **Timezone**: Local time (no timezone info stored)
- **Generated**: Automatically when logging activities
- **Example**: `2025-01-15T14:30:25.123456`

### Activity
- **Type**: String
- **Case**: Standardized by AI (e.g., "water" → "Water")
- **Languages**: Supports multiple languages, normalized to English
- **Examples**: 
  - `"Water"` (drinking water)
  - `"Cannabis"` (smoking/consuming cannabis)
  - `"Cigarette"` (smoking cigarettes)
  - `"Walk"` (walking exercise)
  - `"Food"` (eating)
  - `"Sex"` (sexual activity)
  - `"Alcohol"` (drinking alcohol)

### Quantity
- **Type**: Float (numeric)
- **Precision**: Up to 2 decimal places typically
- **Validation**: Must be positive number
- **Examples**: `500.0`, `2.5`, `1.0`

### Unit
- **Type**: String
- **Standardization**: AI normalizes units
- **Common Units**:
  - Volume: `"ml"`, `"l"`, `"cl"`
  - Distance: `"km"`, `"m"`, `"steps"`
  - Count: `"puff"`, `"cigarette"`, `"glass"`
  - Time: `"min"`, `"hour"`
  - Weight: `"g"`, `"mg"`

---

## 🔄 Column Mapping

### Norwegian ↔ English Mapping
The application supports backward compatibility with Norwegian column names:

| Norwegian | English |
|-----------|---------|
| `tidspunkt` | `timestamp` |
| `aktivitet` | `activity` |
| `mengde` | `quantity` |
| `enhet` | `unit` |

### Automatic Conversion
The `load_data()` function automatically detects and converts column names:

```python
# Automatic column mapping in logic.py
if 'tidspunkt' in df.columns:
    df = df.rename(columns={
        'tidspunkt': 'timestamp',
        'aktivitet': 'activity', 
        'mengde': 'quantity',
        'enhet': 'unit'
    })
```

---

## ✅ Data Validation

### Input Validation
1. **Timestamp**: Must be valid datetime format
2. **Activity**: Must be non-empty string
3. **Quantity**: Must be positive numeric value
4. **Unit**: Must be non-empty string

### Data Cleaning Process
```python
# Data cleaning in load_data() function
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df = df.dropna(subset=['timestamp', 'quantity'])
```

### Validation Rules
- **Invalid timestamps** → Row dropped
- **Invalid quantities** → Row dropped  
- **Missing activity/unit** → Row dropped
- **Negative quantities** → Row dropped

---

## 🤖 AI Processing

### Input Processing Flow
```
Natural Language Input → AI Analysis → Structured Data → Validation → CSV Storage
```

### AI Prompt Structure
The AI receives this system prompt for parsing:
```
You are an assistant that converts user diary entries to structured data.
Analyze the text and identify all trackable activities.
Respond with valid JSON containing an array of activities.

Expected categories: Water, Cannabis, Cigarette, Alcohol, Sex, Walk, Food

Format: {"activities": [{"activity": "...", "quantity": ..., "unit": "..."}]}
```

### AI Response Processing
1. **JSON Parsing**: Extract activities array
2. **Data Validation**: Check required fields
3. **Standardization**: Normalize activity names and units
4. **Timestamp Addition**: Add current timestamp
5. **CSV Append**: Save to file

### Example AI Processing
```
Input: "drank 500ml water and walked 2km"
AI Response: {
  "activities": [
    {"activity": "Water", "quantity": 500, "unit": "ml"},
    {"activity": "Walk", "quantity": 2, "unit": "km"}
  ]
}
Result: Two CSV rows with timestamps added
```

---

## 🔄 Data Flow

### Complete Data Flow Diagram
```
┌─────────────────┐
│   User Input    │
│ "Natural Lang"  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  AI Processing  │
│  (OpenRouter)   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Data Extraction │
│ & Validation    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  CSV Storage    │
│  livslogg.csv   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Data Loading   │
│ (load_data())   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Column Mapping  │
│ NO → EN names   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Analysis &    │
│ Visualization   │
└─────────────────┘
```

### Data Transformation Steps
1. **Input**: Natural language text
2. **AI Parsing**: Structured JSON extraction
3. **Validation**: Data type and business rule validation
4. **Storage**: Append to CSV with timestamp
5. **Loading**: Read CSV with column mapping
6. **Processing**: Clean and prepare for analysis
7. **Output**: Charts, tables, summaries

---

## 🔄 Backward Compatibility

### Legacy Support
The application maintains compatibility with:
- **Norwegian column names** (older CSV files)
- **Mixed language data** (Norwegian + English entries)
- **Different timestamp formats** (handled by pandas)

### Migration Strategy
No explicit migration needed:
1. Existing CSV files work automatically
2. Column mapping happens at runtime
3. New data uses English column names
4. Old data remains unchanged

### Gradual Transition
```
Old CSV: tidspunkt,aktivitet,mengde,enhet
         ↓ (load_data() function)
Memory:  timestamp,activity,quantity,unit
         ↓ (save_to_csv() function)
New CSV: timestamp,activity,quantity,unit
```

---

## 🚨 Common Issues

### Issue 1: "Failed to load data: 'timestamp'"
**Cause**: Column name mismatch
**Solution**: Automatic column mapping handles this
**Prevention**: Use `load_data()` function consistently

### Issue 2: Invalid data types
**Cause**: Corrupted CSV data
**Solution**: Data cleaning removes invalid rows
**Prevention**: Always validate before manual CSV edits

### Issue 3: Missing timestamps
**Cause**: Manual CSV editing without timestamps
**Solution**: Add proper ISO format timestamps
**Example**: `2025-01-15T14:30:25.123456`

### Issue 4: Duplicate entries
**Cause**: Multiple logging of same activity
**Solution**: This is by design (allows tracking frequency)
**Analysis**: Use aggregation functions for totals

### Issue 5: Large CSV files
**Cause**: Long-term usage
**Solution**: Performance handled by pandas
**Future**: Consider database migration if >100MB

---

## 🛠️ Maintenance Tips

### Regular Maintenance
- **Backup CSV files** regularly
- **Monitor file size** for performance
- **Validate data integrity** periodically
- **Update AI prompts** if needed

### Data Quality Checks
```python
# Check for data quality issues
df = load_data()

# Check for missing data
print(df.isnull().sum())

# Check for invalid quantities
print(df[df['quantity'] <= 0])

# Check timestamp range
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")

# Check unique activities
print(f"Unique activities: {df['activity'].unique()}")
```

### Performance Monitoring
- Monitor CSV file size
- Check load times for large datasets
- Profile memory usage with big files
- Consider database migration thresholds

---

## 📈 Analytics Considerations

### Time-based Analysis
- **Daily trends**: Group by date
- **Hourly patterns**: Extract hour from timestamp
- **Weekly/Monthly**: Use pandas time grouping

### Activity Analysis
- **Totals**: Sum quantities by activity
- **Frequency**: Count occurrences
- **Patterns**: Time-based activity correlation

### Data Aggregation Examples
```python
# Daily totals
daily_totals = df.groupby(['date', 'activity'])['quantity'].sum()

# Hourly patterns
df['hour'] = df['timestamp'].dt.hour
hourly_patterns = df.groupby(['hour', 'activity'])['quantity'].mean()

# Activity frequency
activity_frequency = df['activity'].value_counts()
```

---

*This data structure documentation ensures the Personal Life Tracker data remains consistent, accessible, and easy to maintain as the application evolves.* 