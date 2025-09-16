#!/usr/bin/env python3
"""
Cursor Background Agent API - MCP Server

This MCP server provides tools to interact with the Cursor Background Agent API,
allowing AI agents to programmatically create and manage background agents
that work autonomously on repositories.

Features:
- Create background agents for autonomous coding tasks
- Monitor agent status and progress
- Follow up with additional instructions
- Manage agent lifecycle
- Repository integration

Based on Cursor Background Agents API documentation:
https://docs.cursor.com/en/background-agent/api/overview
"""

import os
import json
import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path

# MCP imports
import mcp.types as types
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

# HTTP client for Cursor API
import aiohttp
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cursor-agent-mcp")

@dataclass
class CursorApiConfig:
    """Configuration for Cursor Background Agent API"""
    api_key: str
    base_url: str = "https://api.cursor.com"
    timeout: int = 30
    max_retries: int = 3

@dataclass
class BackgroundAgent:
    """Represents a Cursor Background Agent"""
    agent_id: str
    status: str
    repository_url: str
    prompt: str
    branch: Optional[str] = None
    model: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    progress: Optional[Dict[str, Any]] = None

class CursorAgentMCPServer:
    """MCP Server for Cursor Background Agent API integration"""
    
    def __init__(self, config: CursorApiConfig):
        self.config = config
        self.server = Server("cursor-background-agent-mcp")
        self.session: Optional[aiohttp.ClientSession] = None
        self.agents: Dict[str, BackgroundAgent] = {}
        
        # Cache for models and repositories to avoid repeated API calls
        self._models_cache = None
        self._repositories_cache = None
        self._branches_cache = {}  # Cache branches per repository
        self._models_cache_timestamp = None
        self._repositories_cache_timestamp = None
        self._branches_cache_timestamp = {}  # Cache timestamps per repository
        self._cache_duration = 300  # 5 minutes cache duration
        
        # Setup MCP server handlers
        self._setup_mcp_handlers()
    
    def _is_cache_valid(self, cache_timestamp: Optional[float]) -> bool:
        """Check if cache is still valid based on timestamp"""
        if cache_timestamp is None:
            return False
        return (time.time() - cache_timestamp) < self._cache_duration
    
    def clear_cache(self):
        """Clear all cached data"""
        self._models_cache = None
        self._repositories_cache = None
        self._branches_cache = {}
        self._models_cache_timestamp = None
        self._repositories_cache_timestamp = None
        self._branches_cache_timestamp = {}
        logger.info("Cache cleared")
    
    def _extract_repo_info(self, repository_url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL"""
        try:
            # Handle different GitHub URL formats
            if "github.com" in repository_url:
                parts = repository_url.replace("https://github.com/", "").replace("http://github.com/", "").rstrip("/")
                if "/" in parts:
                    owner, repo = parts.split("/", 1)
                    return owner, repo
            raise ValueError(f"Invalid GitHub URL format: {repository_url}")
        except Exception as e:
            logger.error(f"Failed to extract repo info from {repository_url}: {e}")
            raise ValueError(f"Invalid repository URL: {repository_url}")
    
    async def _list_repository_branches(self, repository_url: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Get list of branches for a specific repository"""
        try:
            owner, repo = self._extract_repo_info(repository_url)
            cache_key = f"{owner}/{repo}"
            
            # Check cache first unless force refresh is requested
            if not force_refresh and self._is_cache_valid(self._branches_cache_timestamp.get(cache_key)) and cache_key in self._branches_cache:
                logger.info(f"Returning cached branches data for {cache_key}")
                return self._branches_cache[cache_key]
            
            # Fetch branches from GitHub API
            github_url = f"https://api.github.com/repos/{owner}/{repo}/branches"
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Cursor-MCP-Server"
            }
            
            # Add GitHub token if available (for private repos)
            github_token = os.getenv("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"
            
            async with self.session.get(github_url, headers=headers) as response:
                if response.status == 200:
                    branches_data = await response.json()
                    branches = [branch["name"] for branch in branches_data]
                    
                    result = {
                        "success": True,
                        "repository": repository_url,
                        "owner": owner,
                        "repo": repo,
                        "branches": branches,
                        "total_branches": len(branches),
                        "message": f"Retrieved {len(branches)} branches for {owner}/{repo}"
                    }
                    
                    # Cache the result
                    self._branches_cache[cache_key] = result
                    self._branches_cache_timestamp[cache_key] = time.time()
                    logger.info(f"Cached {len(branches)} branches for {cache_key} for {self._cache_duration} seconds")
                    
                    return result
                    
                elif response.status == 404:
                    return {
                        "success": False,
                        "error": "Repository not found or not accessible",
                        "repository": repository_url,
                        "branches": ["main", "master", "develop"],
                        "message": f"Repository {owner}/{repo} not found or not accessible. Using common branch names."
                    }
                elif response.status == 401:
                    return {
                        "success": False,
                        "error": "Authentication required for private repository",
                        "repository": repository_url,
                        "branches": ["main", "master", "develop", "feature/new-feature"],
                        "message": f"Private repository {owner}/{repo} requires GitHub token. Using common branch names."
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"GitHub API error: {response.status}",
                        "repository": repository_url,
                        "branches": ["main", "master", "develop", "feature/new-feature"],
                        "message": f"Failed to fetch branches: {error_text}. Using common branch names."
                    }
                    
        except Exception as e:
            logger.error(f"Failed to get branches for {repository_url}: {e}")
            # Return cached data if available, otherwise fallback
            try:
                owner, repo = self._extract_repo_info(repository_url)
                cache_key = f"{owner}/{repo}"
                if cache_key in self._branches_cache:
                    logger.info(f"Returning cached branches data due to API error for {cache_key}")
                    return self._branches_cache[cache_key]
            except:
                pass
            
            return {
                "success": False,
                "error": str(e),
                "repository": repository_url,
                "branches": ["main", "master", "develop"],  # Common fallback branches
                "message": f"Failed to fetch branches: {str(e)}"
            }
    
    def _setup_mcp_handlers(self):
        """Setup MCP server request handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available Cursor Agent tools"""
            return [
                types.Tool(
                    name="cursor_create_background_agent",
                    description="Create a new Cursor background agent for autonomous coding tasks",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repository_url": {
                                "type": "string",
                                "description": "GitHub repository URL where the agent will work"
                            },
                            "prompt": {
                                "type": "string",
                                "description": "Detailed instructions for what the agent should accomplish"
                            },
                            "branch": {
                                "type": "string",
                                "description": "Git branch to work on (optional, defaults to main)",
                                "default": "main"
                            },
                            "model": {
                                "type": "string",
                                "description": "AI model to use (optional, defaults to claude-3-5-sonnet)",
                                "enum": ["claude-3-5-sonnet", "gpt-4o", "claude-3-haiku"],
                                "default": "claude-3-5-sonnet"
                            },
                            "max_iterations": {
                                "type": "integer",
                                "description": "Maximum number of iterations (optional, defaults to 10)",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 50
                            }
                        },
                        "required": ["repository_url", "prompt"]
                    }
                ),
                types.Tool(
                    name="cursor_get_agent_status",
                    description="Get the current status and progress of a background agent",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_id": {
                                "type": "string",
                                "description": "ID of the background agent to check"
                            }
                        },
                        "required": ["agent_id"]
                    }
                ),
                types.Tool(
                    name="cursor_add_followup_instruction",
                    description="Add a follow-up instruction to a running background agent",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_id": {
                                "type": "string",
                                "description": "ID of the background agent"
                            },
                            "instruction": {
                                "type": "string",
                                "description": "Additional instruction or clarification for the agent"
                            }
                        },
                        "required": ["agent_id", "instruction"]
                    }
                ),
                types.Tool(
                    name="cursor_stop_background_agent",
                    description="Stop a running background agent",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_id": {
                                "type": "string",
                                "description": "ID of the background agent to stop"
                            }
                        },
                        "required": ["agent_id"]
                    }
                ),
                types.Tool(
                    name="cursor_list_background_agents",
                    description="List all background agents and their current status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status_filter": {
                                "type": "string",
                                "description": "Filter agents by status (optional)",
                                "enum": ["running", "completed", "failed", "stopped"]
                            },
                            "repository_filter": {
                                "type": "string",
                                "description": "Filter agents by repository URL (optional)"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="cursor_get_api_usage",
                    description="Get current API usage and limits for Cursor Background Agents",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="cursor_list_available_models",
                    description="Get list of available AI models for background agents",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="cursor_list_repositories",
                    description="Get list of accessible GitHub repositories",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="cursor_list_repository_branches",
                    description="Get list of branches for a specific GitHub repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repository_url": {
                                "type": "string",
                                "description": "GitHub repository URL (e.g., https://github.com/owner/repo)"
                            },
                            "force_refresh": {
                                "type": "boolean",
                                "description": "Force refresh the branch list from GitHub API",
                                "default": False
                            }
                        },
                        "required": ["repository_url"],
                        "additionalProperties": False
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Handle MCP tool calls"""
            try:
                if name == "cursor_create_background_agent":
                    result = await self._create_background_agent(arguments)
                elif name == "cursor_get_agent_status":
                    result = await self._get_agent_status(arguments)
                elif name == "cursor_add_followup_instruction":
                    result = await self._add_followup_instruction(arguments)
                elif name == "cursor_stop_background_agent":
                    result = await self._stop_background_agent(arguments)
                elif name == "cursor_list_background_agents":
                    result = await self._list_background_agents(arguments)
                elif name == "cursor_get_api_usage":
                    result = await self._get_api_usage()
                elif name == "cursor_list_available_models":
                    result = await self._list_available_models()
                elif name == "cursor_list_repositories":
                    result = await self._list_repositories()
                elif name == "cursor_list_repository_branches":
                    repository_url = arguments.get("repository_url")
                    force_refresh = arguments.get("force_refresh", False)
                    if not repository_url:
                        raise ValueError("repository_url is required")
                    result = await self._list_repository_branches(repository_url, force_refresh)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": str(e),
                        "tool": name,
                        "timestamp": datetime.utcnow().isoformat()
                    }, indent=2)
                )]
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[types.Resource]:
            """List available MCP resources"""
            return [
                types.Resource(
                    uri="mcp://cursor-agent/api-config",
                    name="API Configuration",
                    description="Current Cursor API configuration and settings",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri="mcp://cursor-agent/agents-summary",
                    name="Agents Summary",
                    description="Summary of all background agents and their status",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri="mcp://cursor-agent/usage-metrics",
                    name="Usage Metrics",
                    description="API usage statistics and performance metrics",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Handle MCP resource reads"""
            try:
                if uri == "mcp://cursor-agent/api-config":
                    config_data = {
                        "base_url": self.config.base_url,
                        "timeout": self.config.timeout,
                        "max_retries": self.config.max_retries,
                        "api_key_configured": bool(self.config.api_key),
                        "session_active": self.session is not None
                    }
                    return json.dumps(config_data, indent=2)
                
                elif uri == "mcp://cursor-agent/agents-summary":
                    summary = {
                        "total_agents": len(self.agents),
                        "agents_by_status": {},
                        "agents": []
                    }
                    
                    for agent in self.agents.values():
                        status = agent.status
                        summary["agents_by_status"][status] = summary["agents_by_status"].get(status, 0) + 1
                        summary["agents"].append({
                            "agent_id": agent.agent_id,
                            "status": agent.status,
                            "repository_url": agent.repository_url,
                            "created_at": agent.created_at,
                            "branch": agent.branch
                        })
                    
                    return json.dumps(summary, indent=2)
                
                elif uri == "mcp://cursor-agent/usage-metrics":
                    usage_data = await self._get_api_usage()
                    return json.dumps(usage_data, indent=2)
                
                else:
                    raise ValueError(f"Unknown resource: {uri}")
                    
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {e}")
                return json.dumps({"error": str(e)}, indent=2)
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> List[types.Prompt]:
            """List available MCP prompts"""
            return [
                types.Prompt(
                    name="cursor_agent_task_template",
                    description="Template for creating effective background agent tasks",
                    arguments=[
                        types.PromptArgument(
                            name="task_type",
                            description="Type of task (feature, bugfix, refactor, test, docs)",
                            required=True
                        ),
                        types.PromptArgument(
                            name="complexity",
                            description="Task complexity (simple, medium, complex)",
                            required=False
                        )
                    ]
                ),
                types.Prompt(
                    name="cursor_agent_followup_guide",
                    description="Guide for effective follow-up instructions to background agents",
                    arguments=[
                        types.PromptArgument(
                            name="current_status",
                            description="Current status of the agent",
                            required=True
                        ),
                        types.PromptArgument(
                            name="issue_type",
                            description="Type of issue or clarification needed",
                            required=False
                        )
                    ]
                )
            ]
        
        @self.server.get_prompt()
        async def handle_get_prompt(name: str, arguments: Dict[str, str]) -> types.GetPromptResult:
            """Handle MCP prompt requests"""
            if name == "cursor_agent_task_template":
                task_type = arguments.get("task_type", "feature")
                complexity = arguments.get("complexity", "medium")
                
                template = self._generate_task_template(task_type, complexity)
                
                return types.GetPromptResult(
                    description=f"Template for {task_type} task with {complexity} complexity",
                    messages=[
                        types.PromptMessage(
                            role="user",
                            content=types.TextContent(type="text", text=template)
                        )
                    ]
                )
            
            elif name == "cursor_agent_followup_guide":
                current_status = arguments.get("current_status", "running")
                issue_type = arguments.get("issue_type", "clarification")
                
                guide = self._generate_followup_guide(current_status, issue_type)
                
                return types.GetPromptResult(
                    description=f"Follow-up guide for {current_status} agent with {issue_type}",
                    messages=[
                        types.PromptMessage(
                            role="user", 
                            content=types.TextContent(type="text", text=guide)
                        )
                    ]
                )
            
            else:
                raise ValueError(f"Unknown prompt: {name}")
    
    async def _ensure_session(self):
        """Ensure HTTP session is active"""
        if self.session is None:
            # Create SSL context that doesn't verify certificates for development
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "Cursor-Agent-MCP-Server/1.0.0"
                }
            )
    
    async def _make_api_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make authenticated request to Cursor API"""
        await self._ensure_session()
        
        url = f"{self.config.base_url}{endpoint}"
        
        for attempt in range(self.config.max_retries):
            try:
                async with self.session.request(method, url, json=data) as response:
                    response_data = await response.json()
                    
                    if response.status == 200 or response.status == 201:
                        return response_data
                    elif response.status == 401:
                        raise Exception("Authentication failed. Check your Cursor API key.")
                    elif response.status == 429:
                        # Rate limited - wait and retry
                        wait_time = 2 ** attempt
                        logger.warning(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{self.config.max_retries}")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        raise Exception(f"API request failed: {response.status} - {response_data}")
                        
            except aiohttp.ClientError as e:
                if attempt == self.config.max_retries - 1:
                    raise Exception(f"Network error after {self.config.max_retries} attempts: {e}")
                await asyncio.sleep(2 ** attempt)
        
        raise Exception(f"Failed to complete request after {self.config.max_retries} attempts")
    
    async def _create_background_agent(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Cursor background agent"""
        try:
            # Prepare the request payload according to Cursor API spec
            payload = {
                "prompt": {
                    "text": args["prompt"]
                },
                "source": {
                    "repository": args["repository_url"],
                    "ref": args.get("branch", "main")
                },
                "model": args.get("model", "claude-3-5-sonnet"),
                "target": {
                    "autoCreatePr": True
                }
            }
            
            
            # Add webhook if configured
            if hasattr(self.config, 'webhook_url') and self.config.webhook_url:
                payload["webhook"] = {
                    "url": self.config.webhook_url
                }
            
            # Make API request to create agent
            response = await self._make_api_request("POST", "/v0/agents", payload)
            
            # Create agent object from API response
            agent = BackgroundAgent(
                agent_id=response.get("id", f"agent-{datetime.utcnow().timestamp()}"),
                status=response.get("status", "CREATING"),
                repository_url=args["repository_url"],
                prompt=args["prompt"],
                branch=args.get("branch", "main"),
                model=args.get("model", "claude-3-5-sonnet"),
                created_at=response.get("createdAt", datetime.utcnow().isoformat())
            )
            
            # Store agent locally
            self.agents[agent.agent_id] = agent
            
            logger.info(f"Created background agent {agent.agent_id} for {args['repository_url']}")
            
            return {
                "success": True,
                "agent_id": agent.agent_id,
                "status": agent.status,
                "repository_url": agent.repository_url,
                "branch": agent.branch,
                "model": agent.model,
                "created_at": agent.created_at,
                "message": f"Background agent created successfully. Agent will work autonomously on '{args['prompt']}'"
            }
            
        except Exception as e:
            logger.error(f"Failed to create background agent: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create background agent. Check your API key and repository access."
            }
    
    async def _get_agent_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get the status of a background agent"""
        try:
            agent_id = args["agent_id"]
            
            # Get status from API
            response = await self._make_api_request("GET", f"/v0/agents/{agent_id}")
            
            # Update local agent if it exists
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.status = response.get("status", agent.status)
                agent.progress = response.get("progress", agent.progress)
                agent.updated_at = datetime.utcnow().isoformat()
            
            return {
                "success": True,
                "agent_id": agent_id,
                "status": response.get("status", "unknown"),
                "progress": response.get("progress", {}),
                "repository_url": response.get("repository_url"),
                "branch": response.get("branch"),
                "created_at": response.get("created_at"),
                "updated_at": response.get("updated_at"),
                "logs": response.get("logs", [])
            }
            
        except Exception as e:
            logger.error(f"Failed to get agent status: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get status for agent {args.get('agent_id')}"
            }
    
    async def _add_followup_instruction(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a follow-up instruction to a running agent"""
        try:
            agent_id = args["agent_id"]
            instruction = args["instruction"]
            
            payload = {"instruction": instruction}
            
            # Send follow-up instruction via API (based on Cursor docs)
            response = await self._make_api_request("POST", f"/v0/agents/{agent_id}/followup", payload)
            
            return {
                "success": True,
                "agent_id": agent_id,
                "instruction_added": instruction,
                "status": response.get("status", "updated"),
                "message": "Follow-up instruction added successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to add follow-up instruction: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to add instruction to agent {args.get('agent_id')}"
            }
    
    async def _stop_background_agent(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Stop a running background agent"""
        try:
            agent_id = args["agent_id"]
            
            # Delete/stop agent via API
            response = await self._make_api_request("DELETE", f"/v0/agents/{agent_id}")
            
            # Update local agent
            if agent_id in self.agents:
                self.agents[agent_id].status = "stopped"
                self.agents[agent_id].updated_at = datetime.utcnow().isoformat()
            
            return {
                "success": True,
                "agent_id": agent_id,
                "status": "stopped",
                "message": "Background agent stopped successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to stop background agent: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to stop agent {args.get('agent_id')}"
            }
    
    async def _list_background_agents(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List all background agents with optional filtering"""
        try:
            # Get agents from API
            params = {}
            if args.get("status_filter"):
                params["status"] = args["status_filter"]
            if args.get("repository_filter"):
                params["repository"] = args["repository_filter"]
            
            # Build query string for Cursor API
            query_params = []
            if args.get("limit"):
                query_params.append(f"limit={args['limit']}")
            if args.get("cursor"):
                query_params.append(f"cursor={args['cursor']}")
            
            query_string = "&".join(query_params)
            endpoint = f"/v0/agents?{query_string}" if query_string else "/v0/agents"
            
            response = await self._make_api_request("GET", endpoint)
            
            agents = response.get("agents", [])
            
            # Update local agent storage
            for agent_data in agents:
                agent_id = agent_data.get("agent_id")
                if agent_id:
                    if agent_id in self.agents:
                        # Update existing agent
                        agent = self.agents[agent_id]
                        agent.status = agent_data.get("status", agent.status)
                        agent.updated_at = datetime.utcnow().isoformat()
                    else:
                        # Add new agent
                        agent = BackgroundAgent(
                            agent_id=agent_id,
                            status=agent_data.get("status", "unknown"),
                            repository_url=agent_data.get("repository_url", ""),
                            prompt=agent_data.get("prompt", ""),
                            branch=agent_data.get("branch"),
                            model=agent_data.get("model"),
                            created_at=agent_data.get("created_at")
                        )
                        self.agents[agent_id] = agent
            
            return {
                "success": True,
                "total_agents": len(agents),
                "agents": agents,
                "filters_applied": {
                    "status": args.get("status_filter"),
                    "repository": args.get("repository_filter")
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to list background agents: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list background agents"
            }
    
    async def _get_api_usage(self) -> Dict[str, Any]:
        """Get current API usage and limits"""
        try:
            response = await self._make_api_request("GET", "/v0/api-key-info")
            
            return {
                "success": True,
                "usage": response.get("usage", {}),
                "limits": response.get("limits", {}),
                "billing_period": response.get("billing_period", {}),
                "remaining_quota": response.get("remaining_quota", {}),
                "reset_date": response.get("reset_date")
            }
            
        except Exception as e:
            logger.error(f"Failed to get API usage: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get API usage information",
                "usage": {
                    "active_agents": len([a for a in self.agents.values() if a.status == "running"]),
                    "total_agents_created": len(self.agents)
                }
            }
    
    async def _list_available_models(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get list of available AI models for background agents"""
        # Check cache first unless force refresh is requested
        if not force_refresh and self._is_cache_valid(self._models_cache_timestamp) and self._models_cache:
            logger.info("Returning cached models data")
            return self._models_cache
        
        try:
            response = await self._make_api_request("GET", "/v0/models")
            
            models = response.get("models", [])
            
            result = {
                "success": True,
                "models": models,
                "total_models": len(models),
                "recommended": models[0] if models else None,
                "message": f"Retrieved {len(models)} available models"
            }
            
            # Cache the result
            self._models_cache = result
            self._models_cache_timestamp = time.time()
            logger.info(f"Cached {len(models)} models for {self._cache_duration} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get available models: {e}")
            # Return cached data if available, otherwise fallback
            if self._models_cache:
                logger.info("Returning cached models data due to API error")
                return self._models_cache
            
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get available models",
                "models": [
                    "claude-4-sonnet-thinking",
                    "o3", 
                    "claude-4-opus-thinking"
                ]
            }
    
    async def _list_repositories(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Get list of accessible GitHub repositories"""
        # Check cache first unless force refresh is requested
        if not force_refresh and self._is_cache_valid(self._repositories_cache_timestamp) and self._repositories_cache:
            logger.info("Returning cached repositories data")
            return self._repositories_cache
        
        try:
            response = await self._make_api_request("GET", "/v0/repositories")
            
            repositories = response.get("repositories", [])
            
            result = {
                "success": True,
                "repositories": repositories,
                "total_repositories": len(repositories),
                "message": f"Retrieved {len(repositories)} accessible repositories"
            }
            
            # Cache the result
            self._repositories_cache = result
            self._repositories_cache_timestamp = time.time()
            logger.info(f"Cached {len(repositories)} repositories for {self._cache_duration} seconds")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get repositories: {e}")
            # Return cached data if available, otherwise fallback
            if self._repositories_cache:
                logger.info("Returning cached repositories data due to API error")
                return self._repositories_cache
            
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get accessible repositories",
                "repositories": []
            }
    
    def _generate_task_template(self, task_type: str, complexity: str) -> str:
        """Generate a task template for background agents"""
        templates = {
            "feature": {
                "simple": """
# Feature Implementation Task

## Objective
Implement a simple {feature_name} feature.

## Requirements
- Create the basic functionality
- Add appropriate error handling
- Include basic tests
- Update documentation

## Acceptance Criteria
- [ ] Feature works as described
- [ ] Code follows project conventions
- [ ] Tests pass
- [ ] Documentation updated

## Notes
Keep the implementation simple and focused. Ask for clarification if requirements are unclear.
""",
                "medium": """
# Feature Implementation Task

## Objective
Implement a {feature_name} feature with moderate complexity.

## Requirements
- Design and implement the core functionality
- Handle edge cases and error scenarios
- Create comprehensive tests (unit + integration)
- Update documentation and examples
- Consider performance implications

## Acceptance Criteria
- [ ] Feature fully implemented according to specs
- [ ] Comprehensive error handling
- [ ] Test coverage > 80%
- [ ] Performance meets requirements
- [ ] Documentation includes examples

## Implementation Approach
1. Analyze existing codebase patterns
2. Design the feature architecture
3. Implement core functionality
4. Add error handling and validation
5. Create tests
6. Update documentation

## Notes
This is a moderate complexity task. Break it down into smaller commits and ask for feedback if you encounter design decisions.
""",
                "complex": """
# Complex Feature Implementation Task

## Objective
Implement a complex {feature_name} feature requiring significant architectural changes.

## Requirements
- Design scalable architecture
- Implement robust error handling and recovery
- Create comprehensive test suite
- Ensure backward compatibility
- Performance optimization
- Security considerations
- Documentation and migration guides

## Acceptance Criteria
- [ ] Feature fully implemented with scalable design
- [ ] Comprehensive error handling and recovery
- [ ] Test coverage > 90% with integration tests
- [ ] Performance benchmarks met
- [ ] Security review passed
- [ ] Migration path documented

## Implementation Approach
1. Research and design phase
2. Create architectural proposal
3. Implement in phases with reviews
4. Comprehensive testing
5. Performance optimization
6. Security audit
7. Documentation

## Notes
This is a complex task requiring careful planning. Create design documents, seek architectural review, and implement incrementally.
"""
            },
            "bugfix": {
                "simple": """
# Bug Fix Task

## Objective
Fix a simple bug: {bug_description}

## Requirements
- Identify root cause
- Implement minimal fix
- Add regression test
- Verify fix works

## Acceptance Criteria
- [ ] Bug is fixed
- [ ] Root cause identified
- [ ] Regression test added
- [ ] No side effects

## Notes
Focus on minimal, targeted fix. Don't over-engineer the solution.
""",
                "medium": """
# Bug Fix Task

## Objective
Fix a moderate complexity bug: {bug_description}

## Requirements
- Thorough investigation of root cause
- Implement robust fix
- Add comprehensive tests
- Consider related edge cases
- Update documentation if needed

## Acceptance Criteria
- [ ] Bug completely resolved
- [ ] Root cause analysis documented
- [ ] Comprehensive test coverage
- [ ] Related issues addressed
- [ ] Documentation updated

## Investigation Steps
1. Reproduce the bug consistently
2. Analyze logs and error traces
3. Identify root cause
4. Design fix approach
5. Implement and test
6. Verify no regressions

## Notes
This may involve deeper investigation. Document your findings and reasoning for the fix approach.
""",
                "complex": """
# Complex Bug Fix Task

## Objective
Fix a complex, system-wide bug: {bug_description}

## Requirements
- Deep system analysis
- Consider architectural implications
- Implement comprehensive solution
- Extensive testing across systems
- Performance impact analysis
- Migration strategy if needed

## Acceptance Criteria
- [ ] Bug fully resolved across all systems
- [ ] No performance degradation
- [ ] Comprehensive test coverage
- [ ] System stability maintained
- [ ] Migration plan documented

## Investigation Process
1. System-wide impact analysis
2. Root cause deep dive
3. Solution architecture design
4. Implementation with monitoring
5. Comprehensive testing
6. Performance validation
7. Rollback planning

## Notes
This is a critical bug requiring careful analysis. Document everything and consider system-wide implications.
"""
            }
        }
        
        return templates.get(task_type, {}).get(complexity, "Custom task template - please provide specific requirements.")
    
    def _generate_followup_guide(self, current_status: str, issue_type: str) -> str:
        """Generate follow-up instruction guide"""
        guides = {
            "running": {
                "clarification": """
# Follow-up Instruction for Running Agent

The agent is currently working. If you need to provide clarification:

## Good Follow-up Examples:
- "Please also ensure the feature works on mobile devices"
- "Add validation for email format in the user input"
- "Use TypeScript instead of JavaScript for this component"
- "Follow the existing error handling patterns in the auth module"

## Instructions Format:
Be specific and actionable. The agent will integrate this into its current work.

## Timing:
Send follow-ups early if possible, as the agent may have already started on related work.
""",
                "issue": """
# Follow-up for Issue Resolution

The agent is running but may need help with an issue:

## Troubleshooting Follow-ups:
- "Check the logs in the console for detailed error messages"
- "The API endpoint URL should be '/api/v2/users' not '/api/users'"
- "Import the utility function from '../utils/helpers'"
- "The database schema was updated yesterday, check the migration files"

## Debugging Tips:
- Provide specific file paths
- Share error messages if you have them
- Point to existing code examples
- Clarify external dependencies
"""
            },
            "stuck": {
                "clarification": """
# Help for Stuck Agent

The agent needs additional guidance:

## Effective Unsticking Strategies:
- Break down the task into smaller steps
- Provide specific code examples
- Point to similar implementations in the codebase
- Clarify requirements that may be ambiguous
- Share domain knowledge or business context

## Example:
"Look at how user authentication is handled in src/auth/AuthProvider.tsx for the pattern to follow"
"""
            }
        }
        
        return guides.get(current_status, {}).get(issue_type, "Provide clear, specific instructions to help the agent continue.")
    
    async def initialize(self):
        """Initialize the MCP server"""
        logger.info("Initializing Cursor Agent MCP Server")
        await self._ensure_session()
        logger.info(f"MCP Server ready with Cursor API at {self.config.base_url}")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        logger.info("Cursor Agent MCP Server cleaned up")

async def main():
    """Main entry point for the MCP server"""
    # Get configuration from environment
    api_key = os.getenv("CURSOR_API_KEY")
    if not api_key:
        logger.error("CURSOR_API_KEY environment variable is required")
        return
    
    # Create configuration
    config = CursorApiConfig(api_key=api_key)
    
    # Create and initialize server
    server_instance = CursorAgentMCPServer(config)
    await server_instance.initialize()
    
    # Run MCP server
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cursor-background-agent-mcp",
                server_version="1.0.0",
                capabilities=server_instance.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    # Setup logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Cursor Agent MCP Server stopped by user")
    except Exception as e:
        logger.error(f"Cursor Agent MCP Server error: {e}")
