#!/bin/bash

# Cursor MCP Server Startup Script

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Check if API key is set
if [ -z "$CURSOR_API_KEY" ]; then
    echo "❌ CURSOR_API_KEY not set. Please set it in .env file or environment"
    echo "📖 Get your API key from: https://cursor.com/integrations"
    exit 1
fi

# Activate virtual environment
source cursor_mcp_venv/bin/activate

# Start the MCP server
echo "🚀 Starting Cursor Background Agent MCP Server..."
echo "📡 API Key: ${CURSOR_API_KEY:0:8}..."
echo "🔗 Base URL: ${CURSOR_API_BASE_URL:-https://api.cursor.com}"

python3 cursor_agent_mcp_server.py
