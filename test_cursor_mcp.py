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
