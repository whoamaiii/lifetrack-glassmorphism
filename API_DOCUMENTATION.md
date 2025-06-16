# API Documentation - Personal Life Tracker

## Overview

The Personal Life Tracker uses the OpenRouter API to analyze natural language input and extract structured activity data. This document covers all API-related functionality and integration points.

## External API Integration

### OpenRouter API

**Endpoint**: `https://openrouter.ai/api/v1/chat/completions`  
**Model**: Google Gemini Flash 1.5 (`google/gemini-flash-1.5`)  
**Authentication**: Bearer token via `OPENROUTER_API_KEY` environment variable

### API Configuration

```python
# Environment variable required
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

# Configuration in logic.py
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-flash-1.5"
```

## Core API Functions

### `analyze_with_ai(user_input: str) -> List[Dict]`

Analyzes natural language text and extracts structured activity data.

**Location**: `logic.py:104`

**Parameters**:
- `user_input` (str): Natural language description of activities

**Returns**:
- List[Dict]: Parsed activities with structure:
  ```python
  {
      "activity": str,  # Category: Water, Walk, etc.
      "quantity": float,  # Numeric amount
      "unit": str  # Unit of measurement
  }
  ```

**API Request Format**:
```json
{
    "model": "google/gemini-flash-1.5",
    "messages": [
        {"role": "system", "content": "<system_prompt>"},
        {"role": "user", "content": "<user_input>"}
    ],
    "response_format": {"type": "json_object"}
}
```

**Error Handling**:
- Network errors raise `requests.exceptions.RequestException`
- JSON parsing errors raise `json.JSONDecodeError`
- API errors raise generic `Exception` with details

### `validate_api_key() -> bool`

Validates that the API key environment variable is set.

**Location**: `logic.py:418`

**Returns**:
- `True` if API key exists and is not empty
- `False` otherwise

## Activity Categories

The AI is trained to recognize these activity categories:

| Category | Examples | Common Units |
|----------|----------|--------------|
| Water | "drank water", "had a glass of water" | ml, cups, glasses |
| Cannabis | "smoked a joint", "used cannabis" | unit, gram |
| Cigarette | "smoked a cigarette" | unit, pack |
| Alcohol | "had a beer", "drank wine" | unit, ml, glass |
| Sex | "had sex", "intimate time" | unit, times |
| Walk | "went for a walk", "walked" | km, minutes, steps |
| Food | "ate lunch", "had a snack" | unit, serving |

## Example API Interactions

### Successful Analysis

**Input**: "drank 500ml of water and walked 2km"

**API Response**:
```json
[
    {"activity": "Water", "quantity": 500, "unit": "ml"},
    {"activity": "Walk", "quantity": 2, "unit": "km"}
]
```

### Quantity Inference

**Input**: "had a coffee and smoked"

**API Response**:
```json
[
    {"activity": "Food", "quantity": 1, "unit": "unit"},
    {"activity": "Cigarette", "quantity": 1, "unit": "unit"}
]
```

## Rate Limits and Best Practices

1. **Timeout**: All API calls have a 30-second timeout
2. **Error Recovery**: Failed API calls should be retried with exponential backoff
3. **Caching**: Consider caching similar queries to reduce API calls
4. **Batch Processing**: Group multiple activities in one natural language input

## Security Considerations

1. **API Key Storage**:
   - Never hardcode API keys in source code
   - Use environment variables or secure key management
   - Rotate keys regularly

2. **Data Privacy**:
   - User input is sent to OpenRouter/Google
   - No personal identifiers should be included in activity descriptions
   - Consider data retention policies

## Integration Points

### CLI Integration (`cli.py`)

```python
def handle_log_command(text: str) -> None:
    if not validate_api_key():
        print("❌ ERROR: OPENROUTER_API_KEY not set")
        return
    
    activities = analyze_with_ai(text)
    if activities:
        save_to_csv(activities)
```

### Web App Integration (`streamlit_app.py`)

```python
with st.spinner("Analyzing with AI..."):
    activities = analyze_with_ai(user_input)
if activities:
    save_to_csv(activities)
    st.success("✅ Saved!")
```

## Troubleshooting

### Common Issues

1. **"API key not found"**
   - Solution: Set `OPENROUTER_API_KEY` environment variable

2. **"Failed to parse AI response"**
   - Cause: AI returned non-JSON or unexpected format
   - Solution: Check API status, retry request

3. **"Request timeout"**
   - Cause: Network issues or API overload
   - Solution: Retry with exponential backoff

### Debug Mode

Enable detailed logging by setting:
```bash
export DEBUG=true
```

This will log:
- Full API requests and responses
- Parsing steps
- Error details

## Future Enhancements

1. **Multi-language Support**: Extend beyond English/Norwegian
2. **Custom Categories**: Allow users to define their own activity types
3. **Batch Analysis**: Process multiple entries in one API call
4. **Offline Mode**: Cache common patterns for offline use
5. **Alternative Models**: Support for different AI providers