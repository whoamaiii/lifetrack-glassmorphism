#!/bin/bash

# Personal Life Tracker - Web App Launcher
# ========================================
# This script starts the Streamlit web interface with proper error handling
# and environment checks.
#
# Usage:
#   ./run_webapp.sh              # Start on default port 8501
#   ./run_webapp.sh 8502         # Start on custom port
#   ./run_webapp.sh --network    # Allow network access (careful!)
#
# Requirements:
#   - Python 3.8 or higher
#   - OPENROUTER_API_KEY environment variable
#   - Dependencies from requirements.txt

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🎯 Starting Personal Life Tracker Web Interface..."
echo "================================================"

# Check Python version
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo -e "${RED}❌ Error: Python 3.8 or higher is required${NC}"
    exit 1
fi

# Check for API key
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  Warning: OPENROUTER_API_KEY not set${NC}"
    echo "You won't be able to log activities without it."
    echo "Set it with: export OPENROUTER_API_KEY='your-key-here'"
    echo ""
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}📦 Streamlit not found. Installing...${NC}"
    python3 -m pip install streamlit plotly pandas
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        echo "Try running: pip install -r requirements.txt"
        exit 1
    fi
fi

# Parse command line arguments
PORT=8501
NETWORK_FLAG=""

if [ "$1" == "--network" ]; then
    NETWORK_FLAG="--server.address 0.0.0.0"
    echo -e "${YELLOW}⚠️  WARNING: App will be accessible from network!${NC}"
    echo "Anyone on your network can access your data."
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
elif [ -n "$1" ] && [ "$1" -eq "$1" ] 2>/dev/null; then
    PORT=$1
fi

echo -e "${GREEN}✅ Starting app on port $PORT${NC}"
echo "The app will open in your browser at http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Streamlit app with error handling
exec streamlit run streamlit_app.py \
    --server.port $PORT \
    $NETWORK_FLAG \
    --server.headless true \
    2>&1 | while read line; do
        # Filter out noisy Streamlit logs
        if [[ ! "$line" =~ "Stopping..." ]] && \
           [[ ! "$line" =~ "Shutting down" ]]; then
            echo "$line"
        fi
    done

# This will only run if streamlit fails to start
echo -e "${RED}❌ Failed to start Streamlit${NC}"
exit 1