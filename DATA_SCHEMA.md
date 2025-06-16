# Data Schema Documentation

## Overview

Personal Life Tracker uses a simple CSV format for data storage, making it portable, human-readable, and easy to backup or analyze with external tools.

## File Location

- **Default filename**: `livslogg.csv`
- **Location**: Project root directory
- **Encoding**: UTF-8
- **Format**: Standard CSV with headers

## Schema Definition

### Columns

| Column Name | Data Type | Format | Required | Description |
|-------------|-----------|---------|----------|-------------|
| `timestamp` | string | ISO 8601 | Yes | When the activity was logged |
| `activity` | string | Text | Yes | Type of activity from predefined categories |
| `quantity` | float | Number | Yes | Amount/quantity of the activity |
| `unit` | string | Text | Yes | Unit of measurement |

### Example Data

```csv
timestamp,activity,quantity,unit
2024-01-15T08:30:00.123456,Water,500,ml
2024-01-15T09:15:00.789012,Walk,2.5,km
2024-01-15T10:00:00.345678,Cannabis,1,unit
2024-01-15T12:30:00.901234,Food,1,meal
2024-01-15T14:00:00.567890,Water,250,ml
```

## Field Details

### timestamp
- **Format**: ISO 8601 datetime string with microseconds
- **Example**: `2024-01-15T08:30:00.123456`
- **Generated**: Automatically when activity is logged
- **Timezone**: Local system time (not timezone-aware)
- **Purpose**: Precise temporal ordering and filtering

### activity
- **Type**: String from predefined categories
- **Valid Values**: 
  - `Water` - Hydration tracking
  - `Cannabis` - Cannabis consumption
  - `Cigarette` - Cigarette smoking
  - `Alcohol` - Alcoholic beverage consumption
  - `Sex` - Sexual activity
  - `Walk` - Walking/exercise
  - `Food` - Food consumption
- **Case Sensitive**: Yes
- **Validation**: Must match exactly one of the categories

### quantity
- **Type**: Floating point number
- **Range**: Any positive number (0 excluded in practice)
- **Precision**: Up to 2 decimal places recommended
- **Examples**:
  - `500` (500ml of water)
  - `2.5` (2.5km walk)
  - `1` (1 cigarette)
  - `0.5` (half a meal)

### unit
- **Type**: Free-form string
- **Common Units by Activity**:
  - **Water**: `ml`, `liters`, `glasses`, `cups`
  - **Walk**: `km`, `miles`, `steps`, `minutes`
  - **Cannabis**: `unit`, `joints`, `grams`
  - **Cigarette**: `unit`, `cigarettes`, `packs`
  - **Alcohol**: `ml`, `drinks`, `glasses`, `beers`
  - **Sex**: `unit`, `sessions`, `minutes`
  - **Food**: `meal`, `calories`, `portions`
- **Flexibility**: AI can parse various unit formats

## Data Processing

### On Write (Saving)
1. AI parses natural language input
2. Extracts activity, quantity, and unit
3. Adds current timestamp
4. Appends to CSV file

### On Read (Loading)
1. Parse CSV into DataFrame
2. Convert timestamp to datetime object
3. Convert quantity to numeric (float)
4. Drop invalid rows (NaN values)
5. Add derived `date` column for filtering

## Derived Fields

When data is loaded, additional fields are computed:

| Field | Type | Description |
|-------|------|-------------|
| `date` | date | Date portion of timestamp for daily aggregations |
| `week` | period | Week number for weekly aggregations (when needed) |
| `month` | period | Month for monthly aggregations (when needed) |

## Data Integrity

### Validation Rules
1. **Timestamp**: Must be valid ISO 8601 format
2. **Activity**: Must be from predefined categories
3. **Quantity**: Must be numeric and positive
4. **Unit**: Cannot be empty

### Error Handling
- Invalid rows are skipped during loading
- Malformed timestamps are treated as NaT (Not a Time)
- Non-numeric quantities are treated as NaN
- Rows with NaN values are dropped

## Migration Notes

### From Norwegian Version
If migrating from the original Norwegian version:
- `tidspunkt` → `timestamp`
- `aktivitet` → `activity`
- `mengde` → `quantity`
- `enhet` → `unit`

Activity name mappings:
- `Vann` → `Water`
- `Gåtur` → `Walk`
- `Sigarett` → `Cigarette`
- `Mat` → `Food`

## Backup Recommendations

1. **Regular Backups**: Copy `livslogg.csv` to a backup location
2. **Version Control**: Consider adding to git (if not sensitive)
3. **Cloud Sync**: Can be synced with cloud storage services
4. **Export Options**: Can be opened in Excel, Google Sheets, etc.

## Advanced Usage

### Manual Editing
The CSV can be edited manually with:
- Text editors (VS Code, Notepad++)
- Spreadsheet software (Excel, LibreOffice Calc)
- Command-line tools (csvkit, pandas)

### Data Analysis
Compatible with:
- Pandas for Python analysis
- R for statistical analysis
- SQL databases (after import)
- Business intelligence tools

### Custom Queries

Example using pandas:
```python
import pandas as pd

# Load data
df = pd.read_csv('livslogg.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Get water intake for January 2024
water_jan = df[(df['activity'] == 'Water') & 
               (df['timestamp'].dt.month == 1) & 
               (df['timestamp'].dt.year == 2024)]

# Calculate daily averages
daily_avg = df.groupby([df['timestamp'].dt.date, 'activity'])['quantity'].sum()
```

## Future Considerations

### Potential Schema Extensions
- `location`: GPS or place name
- `mood`: Emotional state (1-10 scale)
- `notes`: Free-form text notes
- `tags`: Multiple tags for categorization
- `source`: Manual entry vs automatic

### Performance Optimization
- For datasets > 100,000 rows, consider:
  - SQLite database
  - Parquet format
  - Monthly CSV files
  - Indexed storage

## Data Privacy

- All data is stored locally
- No cloud sync by default
- No analytics or tracking
- User has full control over their data
- Can be encrypted at filesystem level