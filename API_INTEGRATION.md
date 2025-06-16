# 🤖 API Integration Documentation

> **Understanding the AI-powered natural language processing**

This document explains how the Personal Life Tracker integrates with OpenRouter AI to parse natural language input into structured data.

## 📋 Table of Contents

1. [Overview](#overview)
2. [OpenRouter Setup](#openrouter-setup)
3. [AI Processing Flow](#ai-processing-flow)
4. [Prompt Engineering](#prompt-engineering)
5. [Response Handling](#response-handling)
6. [Error Handling](#error-handling)
7. [Rate Limits & Costs](#rate-limits--costs)
8. [Testing & Debugging](#testing--debugging)
9. [Alternative Providers](#alternative-providers)
10. [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

### Purpose
The AI integration transforms natural language input like "drank 500ml water and walked 2km" into structured data that can be stored and analyzed.

### Provider
- **Service**: OpenRouter
- **Website**: https://openrouter.ai/
- **Model**: `google/gemini-flash-1.5` (default)
- **API Version**: v1

### Key Benefits
- **Natural Language**: Users can input activities conversationally
- **Multi-Activity**: Single input can contain multiple activities
- **Standardization**: AI normalizes activity names and units
- **Multilingual**: Supports various languages, outputs in English

---

## 🔧 OpenRouter Setup

### Account Creation
1. Visit https://openrouter.ai/
2. Sign up for an account
3. Navigate to "API Keys" in your dashboard
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-...`)

### Environment Configuration
```bash
# In your .env file
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### Verification
```python
# Test API key validity
from logic import validate_api_key
print(validate_api_key())  # Should return True
```

### API Endpoint
- **Base URL**: `https://openrouter.ai/api/v1/chat/completions`
- **Method**: POST
- **Content-Type**: `application/json`

---

## 🔄 AI Processing Flow

### Complete Flow Diagram
```
┌─────────────────┐
│   User Input    │
│ "Natural Text"  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Input Validation│
│ (length, chars) │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  API Request    │
│  (OpenRouter)   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  AI Processing  │
│ (Gemini Flash)  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ JSON Response   │
│   Validation    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Data Extraction │
│ & Normalization │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  CSV Storage    │
│ (with timestamp)│
└─────────────────┘
```

### Processing Steps
1. **Input Validation**: Check text length and basic format
2. **API Request**: Send to OpenRouter with system prompt
3. **AI Processing**: Model analyzes and structures the input
4. **Response Validation**: Verify JSON format and required fields
5. **Data Normalization**: Standardize activity names and units
6. **Storage**: Add timestamp and save to CSV

---

## 📝 Prompt Engineering

### System Prompt Structure
The AI receives a carefully crafted system prompt to ensure consistent output:

```python
system_prompt = """
Du er en assistent som konverterer brukerens dagboknotater til strukturerte data.
Analyser teksten og identifiser alle sporbare aktiviteter.
Svar med gyldig JSON som inneholder en array av aktiviteter.

Forventede kategorier:
- Water (drikking av vann)
- Cannabis (røyking/inntak av cannabis) 
- Cigarette (røyking av sigaretter)
- Alcohol (drikking av alkohol)
- Sex (seksuell aktivitet)
- Walk (gåturer/gange)
- Food (spising av mat)

Format: {"activities": [{"activity": "...", "quantity": ..., "unit": "..."}]}

Eksempel input: "drakk 500ml vann og røyka en sigg"
Eksempel output: {"activities": [{"activity": "Water", "quantity": 500, "unit": "ml"}, {"activity": "Cigarette", "quantity": 1, "unit": "cigarette"}]}

Viktig: Svar kun med gyldig JSON, ingen ekstra tekst.
"""
```

### Prompt Design Principles
1. **Clear Instructions**: Specific about expected output format
2. **Category Guidance**: Lists expected activity types
3. **Examples**: Shows input/output patterns
4. **JSON-Only**: Ensures clean, parseable responses
5. **Multilingual**: Accepts Norwegian, outputs English

### Model Configuration
```python
# API request configuration
payload = {
    "model": "google/gemini-flash-1.5",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ],
    "max_tokens": 1000,
    "temperature": 0.1,  # Low temperature for consistent output
    "top_p": 0.9
}
```

---

## 🔍 Response Handling

### Expected Response Format
```json
{
  "activities": [
    {
      "activity": "Water",
      "quantity": 500,
      "unit": "ml"
    },
    {
      "activity": "Walk", 
      "quantity": 2.5,
      "unit": "km"
    }
  ]
}
```

### Response Processing Code
```python
def analyze_with_ai(user_input: str) -> List[Dict]:
    """Process user input through AI and return structured activities."""
    
    # Send request to OpenRouter
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Extract and parse JSON
    ai_response = response.json()['choices'][0]['message']['content']
    
    try:
        # Parse JSON response
        parsed_data = json.loads(ai_response)
        activities = parsed_data.get('activities', [])
        
        # Validate each activity
        validated_activities = []
        for activity in activities:
            if validate_activity(activity):
                validated_activities.append(activity)
                
        return validated_activities
        
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON response: {ai_response}")
        return []
```

### Activity Validation
```python
def validate_activity(activity: Dict) -> bool:
    """Validate that an activity has required fields and valid data."""
    required_fields = ['activity', 'quantity', 'unit']
    
    # Check required fields exist
    if not all(field in activity for field in required_fields):
        return False
    
    # Validate data types
    if not isinstance(activity['activity'], str):
        return False
    if not isinstance(activity['quantity'], (int, float)):
        return False
    if not isinstance(activity['unit'], str):
        return False
        
    # Validate values
    if activity['quantity'] <= 0:
        return False
    if not activity['activity'].strip():
        return False
    if not activity['unit'].strip():
        return False
        
    return True
```

---

## ⚠️ Error Handling

### API Error Types
1. **Authentication Errors** (401): Invalid API key
2. **Rate Limit Errors** (429): Too many requests
3. **Server Errors** (500+): OpenRouter service issues
4. **Network Errors**: Connection timeouts
5. **JSON Parse Errors**: Invalid AI response format

### Error Handling Strategy
```python
def analyze_with_ai(user_input: str) -> List[Dict]:
    """Robust AI analysis with comprehensive error handling."""
    
    if not validate_api_key():
        logger.error("API key not configured")
        return []
        
    try:
        response = requests.post(
            API_URL, 
            headers=headers, 
            json=payload,
            timeout=30  # 30-second timeout
        )
        
        # Handle HTTP errors
        if response.status_code == 401:
            logger.error("Invalid API key")
            return []
        elif response.status_code == 429:
            logger.error("Rate limit exceeded")
            return []
        elif response.status_code >= 500:
            logger.error(f"Server error: {response.status_code}")
            return []
            
        response.raise_for_status()
        
        # Process successful response
        return process_ai_response(response.json())
        
    except requests.exceptions.ConnectionError:
        logger.error("Network connection error")
        return []
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []
```

### Fallback Strategies
1. **Graceful Degradation**: Continue without AI if API fails
2. **User Feedback**: Clear error messages for users
3. **Retry Logic**: Automatic retries for transient errors
4. **Logging**: Detailed logs for debugging

---

## 💰 Rate Limits & Costs

### OpenRouter Pricing (as of 2025)
- **google/gemini-flash-1.5**:
  - Input: ~$0.075 per 1M tokens
  - Output: ~$0.30 per 1M tokens
- **Typical Usage**: ~100-200 tokens per request
- **Estimated Cost**: <$0.01 per activity logging session

### Rate Limits
- **Default**: ~60 requests per minute
- **Burst**: Higher limits for short periods
- **Monitoring**: Track usage in OpenRouter dashboard

### Cost Optimization
1. **Efficient Prompts**: Minimize token usage
2. **Batch Processing**: Process multiple activities at once
3. **Caching**: Cache common patterns (future enhancement)
4. **Model Selection**: Use cost-effective models when appropriate

### Usage Monitoring
```python
# Track API usage (implement as needed)
def log_api_usage(tokens_used: int, cost_estimate: float):
    """Log API usage for monitoring costs."""
    logger.info(f"API usage: {tokens_used} tokens, ~${cost_estimate:.4f}")
```

---

## 🧪 Testing & Debugging

### Manual Testing
```python
# Test AI parsing directly
from logic import analyze_with_ai

# Test various inputs
test_inputs = [
    "drank 500ml water",
    "walked 2km and smoked a cigarette",
    "hade sex två gånger",  # Swedish input
    "spiste en banan og drakk kaffe"  # Norwegian input
]

for input_text in test_inputs:
    result = analyze_with_ai(input_text)
    print(f"Input: {input_text}")
    print(f"Output: {result}")
    print("---")
```

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test with debug output
result = analyze_with_ai("test input")
```

### API Response Inspection
```python
# Inspect raw API responses
def debug_analyze_with_ai(user_input: str):
    """Debug version that shows raw API response."""
    response = requests.post(API_URL, headers=headers, json=payload)
    
    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)
    
    try:
        ai_response = response.json()['choices'][0]['message']['content']
        print("AI Content:", ai_response)
        
        parsed = json.loads(ai_response)
        print("Parsed JSON:", parsed)
        
    except Exception as e:
        print("Parse Error:", e)
```

---

## 🔄 Alternative Providers

### Backup Options
If OpenRouter becomes unavailable, consider these alternatives:

#### 1. Direct OpenAI API
```python
# OpenAI configuration
API_URL = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
```

#### 2. Anthropic Claude
```python
# Claude configuration
API_URL = "https://api.anthropic.com/v1/messages"
headers = {
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}
```

#### 3. Local Models (Ollama)
```python
# Ollama local deployment
API_URL = "http://localhost:11434/api/generate"
# No API key required for local models
```

### Provider Switching
```python
# Configuration-driven provider selection
def get_ai_provider():
    """Return active AI provider configuration."""
    provider = os.getenv('AI_PROVIDER', 'openrouter')
    
    if provider == 'openrouter':
        return OpenRouterProvider()
    elif provider == 'openai':
        return OpenAIProvider()
    elif provider == 'anthropic':
        return AnthropicProvider()
    else:
        raise ValueError(f"Unknown provider: {provider}")
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "API key not found"
**Symptoms**: 401 Unauthorized errors
**Solutions**:
```bash
# Check environment variable
echo $OPENROUTER_API_KEY

# Verify .env file
cat .env | grep OPENROUTER

# Test in Python
python3 -c "import os; print(os.getenv('OPENROUTER_API_KEY'))"
```

#### 2. "Invalid JSON response"
**Symptoms**: JSON parsing errors
**Solutions**:
- Check system prompt clarity
- Verify model responses with debug mode
- Implement retry logic for malformed responses

#### 3. "Rate limit exceeded"
**Symptoms**: 429 errors
**Solutions**:
- Implement exponential backoff
- Monitor usage in OpenRouter dashboard
- Consider upgrading plan or switching models

#### 4. "Connection timeout"
**Symptoms**: Network timeouts
**Solutions**:
- Increase timeout values
- Check internet connectivity
- Verify OpenRouter service status

#### 5. "Empty activity list"
**Symptoms**: No activities extracted from valid input
**Solutions**:
- Review system prompt for clarity
- Check activity validation logic
- Test with simpler input patterns

### Debug Checklist
1. ✅ API key is set and valid
2. ✅ Network connection is working
3. ✅ Input text is reasonable length
4. ✅ System prompt is properly formatted
5. ✅ Model is available and responding
6. ✅ JSON parsing is handling edge cases
7. ✅ Activity validation is not too strict

---

## 📊 Performance Monitoring

### Key Metrics
- **Response Time**: API call latency
- **Success Rate**: Successful parsing percentage
- **Cost Tracking**: Token usage and expenses
- **Error Rates**: Failed requests by type

### Monitoring Implementation
```python
import time
from functools import wraps

def monitor_api_call(func):
    """Decorator to monitor API call performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"API call successful: {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"API call failed: {duration:.2f}s, {e}")
            raise
    return wrapper

@monitor_api_call
def analyze_with_ai(user_input: str) -> List[Dict]:
    # Implementation here
    pass
```

---

*This API integration documentation ensures the AI-powered features remain reliable, cost-effective, and easy to maintain as the application scales.* 