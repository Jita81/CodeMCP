#!/bin/bash

# Cursor Background Agent MCP Server Setup Script
# This script sets up the MCP server for Cursor Background Agent API integration

set -e

echo "🚀 Setting up Cursor Background Agent MCP Server..."

# Check if Python 3.8+ is available
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1-2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version $python_version is compatible"

# Create virtual environment if it doesn't exist
if [ ! -d "cursor_mcp_venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv cursor_mcp_venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source cursor_mcp_venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r cursor_mcp_requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating environment configuration..."
    cat > .env << EOF
# Cursor API Configuration
CURSOR_API_KEY=your_cursor_api_key_here

# Optional: Custom API base URL
# CURSOR_API_BASE_URL=https://api.cursor.com

# Logging Level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# MCP Server Configuration
MCP_SERVER_NAME=cursor-background-agent-mcp
MCP_SERVER_VERSION=1.0.0
EOF
    echo "📝 Created .env file. Please edit it with your Cursor API key."
else
    echo "✅ .env file already exists"
fi

# Make the MCP server executable
echo "🔧 Making MCP server executable..."
chmod +x cursor_agent_mcp_server.py

# Create a startup script
echo "📜 Creating startup script..."
cat > start_cursor_mcp.sh << 'EOF'
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
EOF

chmod +x start_cursor_mcp.sh

# Create a test script
echo "🧪 Creating test script..."
cat > test_cursor_mcp.py << 'EOF'
#!/usr/bin/env python3
"""
Test script for Cursor Background Agent MCP Server
"""

import os
import json
import asyncio
from cursor_agent_mcp_server import CursorAgentMCPServer, CursorApiConfig

async def test_mcp_server():
    """Test the MCP server functionality"""
    
    # Get API key from environment
    api_key = os.getenv("CURSOR_API_KEY")
    if not api_key:
        print("❌ CURSOR_API_KEY not set")
        return False
    
    print("🧪 Testing Cursor Agent MCP Server...")
    
    # Create server instance
    config = CursorApiConfig(api_key=api_key)
    server = CursorAgentMCPServer(config)
    
    try:
        # Initialize server
        await server.initialize()
        print("✅ Server initialization successful")
        
        # Test API configuration
        usage_data = await server._get_api_usage()
        if usage_data.get("success"):
            print("✅ API connection successful")
            print(f"📊 Usage data: {json.dumps(usage_data, indent=2)}")
        else:
            print("⚠️  API connection test inconclusive")
            print(f"📊 Response: {json.dumps(usage_data, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        await server.cleanup()

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    success = asyncio.run(test_mcp_server())
    exit(0 if success else 1)
EOF

chmod +x test_cursor_mcp.py

echo ""
echo "🎉 Cursor Background Agent MCP Server setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file and add your Cursor API key:"
echo "   CURSOR_API_KEY=your_actual_api_key"
echo ""
echo "2. Get your API key from: https://cursor.com/integrations"
echo ""
echo "3. Test the setup:"
echo "   ./test_cursor_mcp.py"
echo ""
echo "4. Start the MCP server:"
echo "   ./start_cursor_mcp.sh"
echo ""
echo "📖 Available MCP Tools:"
echo "   - cursor_create_background_agent"
echo "   - cursor_get_agent_status"
echo "   - cursor_add_followup_instruction"
echo "   - cursor_stop_background_agent"
echo "   - cursor_list_background_agents"
echo "   - cursor_get_api_usage"
echo ""
echo "🔗 Documentation: https://docs.cursor.com/en/background-agent/api/overview"
echo ""

# Check if in git repository and offer to commit
if [ -d ".git" ]; then
    echo "📝 Git repository detected. Add files to git?"
    read -p "Add new MCP server files to git? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add cursor_agent_mcp_server.py
        git add cursor_mcp_requirements.txt
        git add cursor_mcp_config.json
        git add setup_cursor_mcp.sh
        git add start_cursor_mcp.sh
        git add test_cursor_mcp.py
        echo "✅ Files added to git staging"
        echo "💡 Don't forget to commit: git commit -m 'Add Cursor Background Agent MCP Server'"
    fi
fi

echo "🚀 Setup complete! Happy autonomous coding!"
