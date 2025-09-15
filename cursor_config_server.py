#!/usr/bin/env python3
"""
Cursor Configuration Web Server

A simple web server that provides a frontend for configuring
Cursor background agents and saves the configuration.
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from cursor_agent_mcp_server import CursorAgentMCPServer, CursorApiConfig

# Create FastAPI app
app = FastAPI(
    title="Cursor Agent Configuration Server",
    description="Web interface for configuring Cursor background agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class AgentConfig(BaseModel):
    repository_url: str
    prompt: str
    branch: str = "main"
    model: str = "claude-3-5-sonnet"
    max_iterations: int = 15
    task_type: str = "feature"

class AgentResponse(BaseModel):
    success: bool
    agent_id: str = None
    message: str
    config: Dict[str, Any] = None
    error: str = None

# Global MCP server instance
mcp_server: CursorAgentMCPServer = None

def get_mcp_server():
    """Get or create MCP server instance"""
    global mcp_server
    
    if mcp_server is None:
        api_key = os.getenv("CURSOR_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="CURSOR_API_KEY not configured")
        
        config = CursorApiConfig(api_key=api_key)
        mcp_server = CursorAgentMCPServer(config)
    
    return mcp_server

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main configuration frontend"""
    try:
        with open("cursor_config_web.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend file not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "api_key_configured": bool(os.getenv("CURSOR_API_KEY")),
        "mcp_server_ready": mcp_server is not None
    }

@app.post("/api/create-agent", response_model=AgentResponse)
async def create_background_agent(config: AgentConfig):
    """Create a new background agent with the specified configuration"""
    try:
        server = get_mcp_server()
        
        # Initialize server if needed
        if not hasattr(server, '_initialized') or not server._initialized:
            await server.initialize()
        
        # Prepare agent arguments
        agent_args = {
            "repository_url": config.repository_url,
            "prompt": config.prompt,
            "branch": config.branch,
            "model": config.model,
            "max_iterations": config.max_iterations
        }
        
        # Create the agent
        result = await server._create_background_agent(agent_args)
        
        if result.get("success"):
            # Save successful configuration
            await save_config(config.dict())
            
            return AgentResponse(
                success=True,
                agent_id=result.get("agent_id"),
                message=f"Background agent created successfully for {config.repository_url}",
                config=agent_args
            )
        else:
            return AgentResponse(
                success=False,
                message="Failed to create background agent",
                error=result.get("error", "Unknown error"),
                config=agent_args
            )
            
    except Exception as e:
        return AgentResponse(
            success=False,
            message="Server error while creating agent",
            error=str(e)
        )

@app.get("/api/saved-configs")
async def get_saved_configs():
    """Get previously saved configurations"""
    try:
        config_file = Path("saved_configs.json")
        if config_file.exists():
            with open(config_file, "r") as f:
                configs = json.load(f)
                return {"configs": configs}
        else:
            return {"configs": []}
    except Exception as e:
        return {"configs": [], "error": str(e)}

@app.post("/api/save-config")
async def save_configuration(config: AgentConfig):
    """Save a configuration for later use"""
    try:
        await save_config(config.dict())
        return {
            "success": True,
            "message": "Configuration saved successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/agent-status/{agent_id}")
async def get_agent_status(agent_id: str):
    """Get the status of a specific agent"""
    try:
        server = get_mcp_server()
        
        if not hasattr(server, '_initialized') or not server._initialized:
            await server.initialize()
        
        result = await server._get_agent_status({"agent_id": agent_id})
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/list-agents")
async def list_all_agents():
    """List all background agents"""
    try:
        server = get_mcp_server()
        
        if not hasattr(server, '_initialized') or not server._initialized:
            await server.initialize()
        
        result = await server._list_background_agents({})
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/agent/{agent_id}/followup")
async def add_followup_instruction(agent_id: str, instruction: dict):
    """Add a follow-up instruction to an agent"""
    try:
        server = get_mcp_server()
        
        if not hasattr(server, '_initialized') or not server._initialized:
            await server.initialize()
        
        result = await server._add_followup_instruction({
            "agent_id": agent_id,
            "instruction": instruction.get("instruction", "")
        })
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/agent/{agent_id}/stop")
async def stop_agent(agent_id: str):
    """Stop a running agent"""
    try:
        server = get_mcp_server()
        
        if not hasattr(server, '_initialized') or not server._initialized:
            await server.initialize()
        
        result = await server._stop_background_agent({"agent_id": agent_id})
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/models")
async def list_available_models():
    """Get list of available AI models"""
    try:
        server = get_mcp_server()
        
        if not hasattr(server, '_initialized') or not server._initialized:
            await server.initialize()
        
        result = await server._list_available_models()
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "models": [
                "claude-4-sonnet-thinking",
                "o3", 
                "claude-4-opus-thinking"
            ]
        }

@app.get("/api/repositories")
async def list_repositories():
    """Get list of accessible repositories"""
    try:
        server = get_mcp_server()
        
        if not hasattr(server, '_initialized') or not server._initialized:
            await server.initialize()
        
        result = await server._list_repositories()
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "repositories": []
        }

async def save_config(config_data: Dict[str, Any]):
    """Save configuration to file"""
    try:
        config_file = Path("saved_configs.json")
        
        # Load existing configs
        if config_file.exists():
            with open(config_file, "r") as f:
                configs = json.load(f)
        else:
            configs = []
        
        # Add timestamp and save
        config_data["saved_at"] = datetime.utcnow().isoformat()
        config_data["id"] = f"config-{int(datetime.utcnow().timestamp())}"
        
        configs.append(config_data)
        
        # Keep only last 50 configs
        configs = configs[-50:]
        
        # Save back to file
        with open(config_file, "w") as f:
            json.dump(configs, f, indent=2)
            
    except Exception as e:
        print(f"Error saving config: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize the server on startup"""
    print("🚀 Cursor Configuration Server starting...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("CURSOR_API_KEY")
    if api_key:
        print("✅ Cursor API key loaded")
    else:
        print("⚠️  Cursor API key not found - some features may not work")
    
    print("🌐 Server ready at http://localhost:8080")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global mcp_server
    if mcp_server:
        await mcp_server.cleanup()
    print("👋 Cursor Configuration Server stopped")

if __name__ == "__main__":
    import sys
    
    print("🔧 Cursor Background Agent Configuration Server")
    print("=" * 50)
    print("🌐 Starting web server at http://localhost:8080")
    print("📖 Open your browser and navigate to the URL above")
    print("⚠️  Make sure CURSOR_API_KEY is set in your .env file")
    print("🔑 Get your API key from: https://cursor.com/integrations")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "cursor_config_server:app",
            host="0.0.0.0",
            port=8080,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)
