#!/bin/bash

# Cursor Configuration Web Interface Startup Script

echo "🌐 Starting Cursor Configuration Web Interface..."
echo "=" * 60

# Load environment variables if .env exists
if [ -f ".env" ]; then
    echo "📋 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  .env file not found - creating one..."
    cat > .env << 'EOF'
# Cursor API Configuration
CURSOR_API_KEY=your_cursor_api_key_here

# Optional: Custom API base URL
# CURSOR_API_BASE_URL=https://api.cursor.com

# Logging Level
LOG_LEVEL=INFO
EOF
    echo "📝 Created .env file - please edit it with your Cursor API key"
fi

# Check if API key is set
if [ -z "$CURSOR_API_KEY" ] || [ "$CURSOR_API_KEY" = "your_cursor_api_key_here" ]; then
    echo "⚠️  WARNING: CURSOR_API_KEY not set or using placeholder"
    echo "🔑 Get your API key from: https://cursor.com/integrations"
    echo "📝 Edit .env file and set: CURSOR_API_KEY=your_actual_api_key"
    echo ""
    echo "❓ Continue anyway? (y/n)"
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "👋 Startup cancelled. Please set your API key first."
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "cursor_mcp_venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   ./setup_cursor_mcp.sh"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source cursor_mcp_venv/bin/activate

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing FastAPI..."
    pip install fastapi uvicorn python-multipart
fi

# Start the web server
echo "🚀 Starting web server..."
echo "🌐 Open your browser and go to: http://localhost:8080"
echo "📱 Mobile-friendly interface included"
echo "🔧 Configure repositories, models, and create agents"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=" * 60

# Run the server
python cursor_config_server.py
