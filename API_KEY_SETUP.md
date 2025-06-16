# 🔑 API Key Setup Guide

The Personal Life Tracker now supports **persistent API key storage** with multiple configuration methods. No more environment variables needed!

## 🚀 Quick Setup Methods

### Method 1: CLI Configuration (Recommended)

```bash
# Interactive setup with hidden input
python cli.py config --set-api-key

# View current configuration
python cli.py config --show
```

### Method 2: Web Interface

1. Start the web app: `streamlit run streamlit_app.py`
2. Open the **Settings** section in the sidebar
3. Enter your API key in the secure form
4. Click **Save Key**

### Method 3: Environment Variable (Legacy)

```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
```

## 🔒 Security Features

- **Hidden Input**: API keys are masked during CLI entry
- **Masked Display**: Stored keys show as `sk-or-v1-xxx...xxx` 
- **Local Storage**: Keys saved in local `config.json` file only
- **Validation**: Format validation before saving
- **Gitignored**: `config.json` is automatically ignored by git

## 📁 Configuration File

The system creates a `config.json` file with this structure:

```json
{
  "api_key": "your-actual-key-here",
  "api_url": "https://openrouter.ai/api/v1/chat/completions", 
  "model": "google/gemini-flash-1.5",
  "csv_filename": "livslogg.csv"
}
```

## 🔄 Priority Order

The system checks for API keys in this order:

1. **config.json** file (highest priority)
2. **OPENROUTER_API_KEY** environment variable (fallback)

## 🛠️ Troubleshooting

### "API key not configured"
- Run: `python cli.py config --set-api-key`
- Or use the web interface Settings section

### "API key validation failed"
- Ensure your key starts with `sk-or-v1-` (OpenRouter format)
- Check key length (minimum 20 characters)
- Verify key is valid at https://openrouter.ai/

### "Failed to save API key"
- Check file permissions in current directory
- Ensure you have write access
- Try running from project root directory

### Config file corrupted
- Delete `config.json` and reconfigure
- The system will recreate with defaults

## 💡 Benefits

### For Users:
- **One-time setup**: Set once, works everywhere
- **No environment hassle**: No need to set variables
- **Persistent**: Survives computer restarts
- **Secure**: Local storage only, not in code

### For Developers:
- **Backwards compatible**: Still works with env vars
- **Easy testing**: Quick key switching
- **Configuration management**: Extensible for future settings
- **Clean separation**: Config logic isolated from business logic

## 🔧 Technical Details

### Functions Added:
- `load_config()` - Load configuration from file
- `save_config()` - Save configuration to file
- `get_api_key()` - Get API key with fallback priority
- `set_api_key()` - Set and validate API key
- `get_config_value()` - Get any config value
- `set_config_value()` - Set any config value

### CLI Commands Added:
- `python cli.py config --show` - Display configuration
- `python cli.py config --set-api-key` - Set API key interactively

### Web Interface Features:
- Settings expander in sidebar
- Secure password input form
- Masked key display
- Real-time validation
- Success/error feedback

## 🎯 Example Workflow

1. **First time setup:**
   ```bash
   pip install -r requirements.txt
   python cli.py config --set-api-key
   # Enter your key securely
   ```

2. **Start using:**
   ```bash
   python cli.py log "drank 500ml of water"
   # or
   streamlit run streamlit_app.py
   ```

3. **Check configuration anytime:**
   ```bash
   python cli.py config --show
   ```

That's it! Your API key is now saved and will work across all interfaces without any environment variable setup. 