# MCP Tools Documentation

This document provides comprehensive documentation for all Model Context Protocol (MCP) tools available in the Cursor Background Agent MCP Server.

## Table of Contents

- [Overview](#overview)
- [Agent Management Tools](#agent-management-tools)
- [System Information Tools](#system-information-tools)
- [MCP Resources](#mcp-resources)
- [MCP Prompts](#mcp-prompts)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## Overview

The Cursor Background Agent MCP Server provides 9 tools that enable programmatic interaction with the Cursor Background Agent API. These tools allow you to create, manage, and monitor autonomous coding agents that work independently on your repositories.

### Tool Categories

- **Agent Management**: Create, monitor, and control background agents
- **System Information**: Query available models, repositories, branches, and API usage

---

## Agent Management Tools

### `cursor_create_background_agent`

Create a new autonomous coding agent that will work independently on a repository.

#### Description
Creates a background agent that analyzes your repository, creates a feature branch, implements the specified task, makes commits, and creates a pull request automatically.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|--------|-------------|
| `repository_url` | string | Yes | - | GitHub repository URL (e.g., `https://github.com/owner/repo`) |
| `prompt` | string | Yes | - | Detailed instructions for what the agent should accomplish |
| `branch` | string | No | `"main"` | Git branch to work on (defaults to main) |
| `model` | string | No | `"claude-3-5-sonnet"` | AI model to use. Options: `claude-3-5-sonnet`, `gpt-4o`, `claude-3-haiku` |
| `max_iterations` | integer | No | `10` | Maximum number of iterations (1-50) |

#### Response

```json
{
  "success": true,
  "agent_id": "agent-1234567890",
  "status": "CREATING",
  "repository_url": "https://github.com/owner/repo",
  "branch": "feature/new-feature",
  "model": "claude-3-5-sonnet",
  "created_at": "2025-01-15T10:30:00Z",
  "message": "Background agent created successfully. Agent will work autonomously on 'Add user authentication...'"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/web-app",
    "prompt": "Implement comprehensive user authentication system with JWT tokens, password reset, and email verification",
    "branch": "feature/authentication",
    "model": "claude-3-5-sonnet",
    "max_iterations": 20
})
```

#### Best Practices

- Provide clear, detailed prompts with specific requirements
- Specify acceptance criteria when possible
- Use appropriate models for task complexity:
  - `claude-3-haiku`: Simple fixes, quick tasks
  - `claude-3-5-sonnet`: Most features (recommended)
  - `gpt-4o`: Complex architectural changes
- Set `max_iterations` based on task complexity:
  - Simple: 5-10
  - Medium: 10-20
  - Complex: 20-50

---

### `cursor_get_agent_status`

Get the current status, progress, and details of a background agent.

#### Description
Retrieves real-time information about an agent's status, including progress, current step, files modified, commits made, and activity logs.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | ID of the background agent to check |

#### Response

```json
{
  "success": true,
  "agent_id": "agent-1234567890",
  "status": "RUNNING",
  "progress": {
    "current_step": "Implementing authentication middleware",
    "completed_steps": 3,
    "total_estimated_steps": 8,
    "files_modified": ["src/auth/middleware.js", "src/routes/auth.js"],
    "commits_made": 2,
    "completion_percentage": 37.5
  },
  "repository_url": "https://github.com/owner/repo",
  "branch": "feature/authentication",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:45:00Z",
  "logs": [
    "Started authentication implementation...",
    "Created auth middleware structure",
    "Implementing JWT token validation"
  ]
}
```

#### Status Values

- `CREATING`: Agent is being initialized
- `RUNNING`: Agent is actively working
- `COMPLETED`: Agent finished successfully
- `FAILED`: Agent encountered an error
- `STOPPED`: Agent was manually stopped

#### Example Usage

```python
result = await client.call_tool("cursor_get_agent_status", {
    "agent_id": "agent-1234567890"
})

if result["status"] == "RUNNING":
    print(f"Progress: {result['progress']['completion_percentage']}%")
    print(f"Current step: {result['progress']['current_step']}")
```

---

### `cursor_add_followup_instruction`

Send additional instructions or clarifications to a running background agent.

#### Description
Allows you to guide an agent that's already working by providing follow-up instructions, clarifications, or additional requirements.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | ID of the background agent |
| `instruction` | string | Yes | Additional instruction or clarification for the agent |

#### Response

```json
{
  "success": true,
  "agent_id": "agent-1234567890",
  "instruction_added": "Please also add two-factor authentication support",
  "status": "updated",
  "message": "Follow-up instruction added successfully"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-1234567890",
    "instruction": """
    Please also add the following enhancements:
    - Two-factor authentication (2FA) support
    - Social login options (Google, GitHub)
    - Remember me functionality
    - Admin panel for user management
    """
})
```

#### Best Practices

- Send follow-ups early in the agent's execution
- Be specific and actionable
- Provide code examples or references to existing implementations when helpful
- Avoid conflicting instructions

---

### `cursor_stop_background_agent`

Stop a running background agent and clean up its resources.

#### Description
Terminates an active agent, preventing it from making further changes. Useful when an agent is working incorrectly or you need to change direction.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | ID of the background agent to stop |

#### Response

```json
{
  "success": true,
  "agent_id": "agent-1234567890",
  "status": "stopped",
  "message": "Background agent stopped successfully"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_stop_background_agent", {
    "agent_id": "agent-1234567890"
})
```

---

### `cursor_list_background_agents`

List all background agents with optional filtering by status or repository.

#### Description
Retrieves a list of all your background agents, allowing you to see their status, repositories, branches, and creation dates. Supports filtering for easier management.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status_filter` | string | No | Filter by status: `running`, `completed`, `failed`, `stopped` |
| `repository_filter` | string | No | Filter by repository URL |

#### Response

```json
{
  "success": true,
  "total_agents": 5,
  "agents": [
    {
      "agent_id": "agent-001",
      "status": "completed",
      "repository_url": "https://github.com/company/frontend",
      "prompt": "Add dark mode toggle functionality",
      "branch": "feature/dark-mode",
      "created_at": "2025-01-15T09:00:00Z",
      "completed_at": "2025-01-15T09:45:00Z"
    },
    {
      "agent_id": "agent-002",
      "status": "running",
      "repository_url": "https://github.com/company/api",
      "prompt": "Implement user authentication system",
      "branch": "feature/auth-system",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "filters_applied": {
    "status": null,
    "repository": null
  }
}
```

#### Example Usage

```python
# List all agents
result = await client.call_tool("cursor_list_background_agents", {})

# List only running agents
result = await client.call_tool("cursor_list_background_agents", {
    "status_filter": "running"
})

# List agents for a specific repository
result = await client.call_tool("cursor_list_background_agents", {
    "repository_filter": "https://github.com/company/api"
})
```

---

## System Information Tools

### `cursor_list_available_models`

Get a list of available AI models that can be used for background agents.

#### Description
Returns all AI models available for background agents, helping you choose the right model for your task.

#### Parameters

None

#### Response

```json
{
  "success": true,
  "models": [
    "claude-4-sonnet-thinking",
    "o3",
    "claude-4-opus-thinking",
    "claude-3-5-sonnet",
    "gpt-4o",
    "claude-3-haiku"
  ],
  "total_models": 6,
  "recommended": "claude-4-sonnet-thinking",
  "message": "Retrieved 6 available models"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_list_available_models", {})

print("Available models:")
for model in result["models"]:
    print(f"  - {model}")
```

#### Model Recommendations

- **Simple tasks**: `claude-3-haiku` (fast, cost-effective)
- **Most features**: `claude-3-5-sonnet` or `claude-4-sonnet-thinking` (recommended)
- **Complex tasks**: `claude-4-opus-thinking` or `o3` (maximum capability)
- **Architectural changes**: `gpt-4o` or `o3` (deep reasoning)

---

### `cursor_list_repositories`

Get a list of GitHub repositories accessible with your Cursor API key.

#### Description
Retrieves all repositories you have access to through the Cursor API, making it easy to select the correct repository for agent creation.

#### Parameters

None

#### Response

```json
{
  "success": true,
  "repositories": [
    "https://github.com/company/frontend",
    "https://github.com/company/api",
    "https://github.com/company/mobile",
    "https://github.com/username/personal-project"
  ],
  "total_repositories": 4,
  "message": "Retrieved 4 accessible repositories"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_list_repositories", {})

print("Your repositories:")
for repo in result["repositories"]:
    print(f"  - {repo}")
```

---

### `cursor_list_repository_branches`

Get a list of branches for a specific GitHub repository.

#### Description
Retrieves all branches available in a repository, helping you select or specify the correct branch for agent operations. Includes caching for efficient API usage.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repository_url` | string | Yes | GitHub repository URL (e.g., `https://github.com/owner/repo`) |
| `force_refresh` | boolean | No | `false` | Force refresh from GitHub API (bypasses cache) |

#### Response

```json
{
  "success": true,
  "repository": "https://github.com/owner/repo",
  "owner": "owner",
  "repo": "repo",
  "branches": [
    "main",
    "develop",
    "feature/user-auth",
    "feature/payment-system"
  ],
  "total_branches": 4,
  "message": "Retrieved 4 branches for owner/repo"
}
```

#### Example Usage

```python
# Get branches (uses cache if available)
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": "https://github.com/company/api"
})

# Force refresh from GitHub
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": "https://github.com/company/api",
    "force_refresh": True
})
```

#### Notes

- Results are cached for 5 minutes to reduce API calls
- For private repositories, set `GITHUB_TOKEN` environment variable
- Falls back to common branch names if GitHub API is unavailable

---

### `cursor_get_api_usage`

Get current API usage statistics and limits for your Cursor API key.

#### Description
Returns information about your API usage, remaining quotas, billing period, and rate limits. Useful for monitoring usage and planning agent creation.

#### Parameters

None

#### Response

```json
{
  "success": true,
  "usage": {
    "agents_created_this_month": 47,
    "active_agents": 2,
    "api_calls_today": 156,
    "tokens_used_today": 45000
  },
  "limits": {
    "max_active_agents": 256,
    "monthly_agent_limit": 1000,
    "daily_api_calls": 10000,
    "rate_limit_per_minute": 60
  },
  "billing_period": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31",
    "days_remaining": 16
  },
  "remaining_quota": {
    "agents": 953,
    "api_calls": 9844
  },
  "reset_date": "2025-02-01T00:00:00Z"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_get_api_usage", {})

usage = result["usage"]
limits = result["limits"]

print(f"Active agents: {usage['active_agents']}/{limits['max_active_agents']}")
print(f"Remaining agents this month: {result['remaining_quota']['agents']}")
```

---

## MCP Resources

The server also provides MCP resources for accessing structured data:

### `mcp://cursor-agent/api-config`

Returns current API configuration settings including base URL, timeout, retry settings, and session status.

**Example Response:**
```json
{
  "base_url": "https://api.cursor.com",
  "timeout": 30,
  "max_retries": 3,
  "api_key_configured": true,
  "session_active": true
}
```

### `mcp://cursor-agent/agents-summary`

Returns a summary of all agents with status distribution and quick overview.

**Example Response:**
```json
{
  "total_agents": 5,
  "agents_by_status": {
    "completed": 2,
    "running": 2,
    "failed": 1
  },
  "agents": [
    {
      "agent_id": "agent-001",
      "status": "completed",
      "repository_url": "https://github.com/company/repo",
      "created_at": "2025-01-15T10:30:00Z",
      "branch": "feature/new-feature"
    }
  ]
}
```

### `mcp://cursor-agent/usage-metrics`

Returns API usage statistics and performance metrics (same as `cursor_get_api_usage` tool).

---

## MCP Prompts

The server provides prompt templates to help generate effective agent instructions:

### `cursor_agent_task_template`

Template for creating effective background agent task descriptions.

**Arguments:**
- `task_type` (required): Type of task - `feature`, `bugfix`, `refactor`, `test`, `docs`
- `complexity` (optional): Task complexity - `simple`, `medium`, `complex`

**Example Usage:**
```python
prompt = await client.get_prompt("cursor_agent_task_template", {
    "task_type": "feature",
    "complexity": "medium"
})
```

### `cursor_agent_followup_guide`

Guide for writing effective follow-up instructions to running agents.

**Arguments:**
- `current_status` (required): Current agent status
- `issue_type` (optional): Type of issue or clarification needed

**Example Usage:**
```python
guide = await client.get_prompt("cursor_agent_followup_guide", {
    "current_status": "running",
    "issue_type": "clarification"
})
```

---

## Usage Examples

### Complete Workflow Example

```python
import asyncio
from cursor_agent_mcp_server import CursorAgentMCPServer, CursorApiConfig

async def complete_workflow():
    # Initialize server
    config = CursorApiConfig(api_key=os.getenv("CURSOR_API_KEY"))
    server = CursorAgentMCPServer(config)
    await server.initialize()
    
    # 1. Check available models
    models = await server._list_available_models()
    print(f"Available models: {models['models']}")
    
    # 2. List repositories
    repos = await server._list_repositories()
    print(f"Accessible repositories: {repos['repositories']}")
    
    # 3. Get branches for a repository
    branches = await server._list_repository_branches(
        "https://github.com/company/api"
    )
    print(f"Available branches: {branches['branches']}")
    
    # 4. Create an agent
    agent = await server._create_background_agent({
        "repository_url": "https://github.com/company/api",
        "prompt": "Add REST API endpoint for user profile management",
        "branch": "feature/user-profile-api",
        "model": "claude-3-5-sonnet",
        "max_iterations": 15
    })
    
    agent_id = agent["agent_id"]
    print(f"Created agent: {agent_id}")
    
    # 5. Monitor progress
    while True:
        status = await server._get_agent_status({"agent_id": agent_id})
        print(f"Status: {status['status']}, Progress: {status.get('progress', {})}")
        
        if status["status"] in ["COMPLETED", "FAILED", "STOPPED"]:
            break
        
        await asyncio.sleep(30)  # Check every 30 seconds
    
    # 6. Check API usage
    usage = await server._get_api_usage()
    print(f"API Usage: {usage['usage']}")
    
    await server.cleanup()

asyncio.run(complete_workflow())
```

### Batch Agent Creation

```python
async def create_multiple_agents():
    server = await initialize_server()
    
    tasks = [
        {
            "repository_url": "https://github.com/company/frontend",
            "prompt": "Add dark mode toggle",
            "branch": "feature/dark-mode"
        },
        {
            "repository_url": "https://github.com/company/api",
            "prompt": "Implement rate limiting middleware",
            "branch": "feature/rate-limiting"
        },
        {
            "repository_url": "https://github.com/company/docs",
            "prompt": "Update API documentation",
            "branch": "docs/api-updates"
        }
    ]
    
    agents = []
    for task in tasks:
        result = await server._create_background_agent({
            **task,
            "model": "claude-3-5-sonnet",
            "max_iterations": 10
        })
        agents.append(result["agent_id"])
    
    print(f"Created {len(agents)} agents")
    return agents
```

### Monitoring Multiple Agents

```python
async def monitor_all_agents():
    server = await initialize_server()
    
    # List all running agents
    all_agents = await server._list_background_agents({
        "status_filter": "running"
    })
    
    print(f"Monitoring {all_agents['total_agents']} running agents")
    
    for agent in all_agents["agents"]:
        agent_id = agent["agent_id"]
        status = await server._get_agent_status({"agent_id": agent_id})
        
        print(f"\nAgent {agent_id}:")
        print(f"  Repository: {status['repository_url']}")
        print(f"  Branch: {status['branch']}")
        print(f"  Status: {status['status']}")
        
        if "progress" in status:
            progress = status["progress"]
            print(f"  Progress: {progress.get('completion_percentage', 0)}%")
            print(f"  Current step: {progress.get('current_step', 'N/A')}")
```

---

## Error Handling

### Common Errors

#### Authentication Errors

```json
{
  "success": false,
  "error": "Authentication failed. Check your Cursor API key.",
  "tool": "cursor_create_background_agent"
}
```

**Solution**: Verify your `CURSOR_API_KEY` environment variable is set correctly.

#### Repository Access Errors

```json
{
  "success": false,
  "error": "Repository not found or not accessible",
  "message": "Repository owner/repo not found or not accessible"
}
```

**Solution**: Ensure the repository URL is correct and you have access through your Cursor API key.

#### Rate Limiting

```json
{
  "success": false,
  "error": "API request failed: 429 - Rate limit exceeded"
}
```

**Solution**: The server automatically retries with exponential backoff. Wait a few minutes before creating more agents.

#### Invalid Parameters

```json
{
  "success": false,
  "error": "repository_url is required"
}
```

**Solution**: Ensure all required parameters are provided with correct types.

### Error Response Format

All tools return errors in a consistent format:

```json
{
  "success": false,
  "error": "Error message description",
  "tool": "tool_name",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

## Best Practices

### 1. Agent Creation

- **Write clear prompts**: Include specific requirements, acceptance criteria, and technical constraints
- **Choose appropriate models**: Match model capability to task complexity
- **Set realistic iterations**: Too few may result in incomplete work; too many increases cost
- **Use feature branches**: Always specify a branch name for easier code review

### 2. Monitoring

- **Check status regularly**: Monitor agent progress to catch issues early
- **Use follow-ups proactively**: Send clarifications early rather than waiting for completion
- **Review logs**: Check agent logs to understand what it's doing

### 3. Resource Management

- **Monitor API usage**: Regularly check `cursor_get_api_usage` to track quotas
- **Clean up stopped agents**: Stop agents that are no longer needed
- **Cache branch lists**: Use caching to reduce API calls when listing branches

### 4. Error Handling

- **Always check `success` field**: Verify operations completed successfully
- **Handle rate limits**: Implement retry logic with exponential backoff
- **Validate inputs**: Ensure repository URLs and other parameters are correct before calling tools

### 5. Security

- **Protect API keys**: Never commit API keys to version control
- **Use environment variables**: Store credentials in `.env` files
- **Review agent changes**: Always review PRs created by agents before merging

### 6. Performance

- **Use caching**: Branch and repository lists are cached for 5 minutes
- **Batch operations**: Create multiple agents sequentially rather than in parallel if hitting rate limits
- **Monitor usage**: Track API usage to optimize costs

---

## Tool Summary Table

| Tool Name | Category | Purpose | Key Parameters |
|-----------|----------|---------|----------------|
| `cursor_create_background_agent` | Management | Create autonomous coding agent | `repository_url`, `prompt` |
| `cursor_get_agent_status` | Management | Monitor agent progress | `agent_id` |
| `cursor_add_followup_instruction` | Management | Guide running agent | `agent_id`, `instruction` |
| `cursor_stop_background_agent` | Management | Terminate agent | `agent_id` |
| `cursor_list_background_agents` | Management | List all agents | `status_filter`, `repository_filter` |
| `cursor_list_available_models` | System | Get AI models | None |
| `cursor_list_repositories` | System | Get accessible repos | None |
| `cursor_list_repository_branches` | System | Get repo branches | `repository_url` |
| `cursor_get_api_usage` | System | Check API usage/limits | None |

---

## Additional Resources

- [Main README](README.md) - Project overview and setup instructions
- [Cursor Background Agent API Docs](https://docs.cursor.com/en/background-agent/api/overview) - Official API documentation
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification

---

## Support

For issues, questions, or contributions:

1. Check the [README.md](README.md) for setup instructions
2. Review error messages and check API key configuration
3. Consult the Cursor API documentation for API-specific questions
4. Check agent status and logs for debugging agent behavior

---

**Last Updated**: January 2025
**MCP Server Version**: 1.0.0
