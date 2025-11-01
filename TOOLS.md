# MCP Tools Documentation

This document provides comprehensive documentation for all Model Context Protocol (MCP) tools, resources, and prompts available in the Cursor Background Agent MCP Server.

## Table of Contents

- [Overview](#overview)
- [Agent Management Tools](#agent-management-tools)
- [Agent Interaction Tools](#agent-interaction-tools)
- [System Information Tools](#system-information-tools)
- [MCP Resources](#mcp-resources)
- [MCP Prompts](#mcp-prompts)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

---

## Overview

The Cursor Background Agent MCP Server provides a complete set of tools for creating, managing, and monitoring autonomous coding agents. These agents work independently on GitHub repositories, implementing features, fixing bugs, and performing various development tasks.

### Key Concepts

- **Background Agents**: Autonomous AI agents that work on repositories without continuous supervision
- **Agent Status**: Current state of an agent (RUNNING, COMPLETED, FAILED, STOPPED)
- **Agent Progress**: Detailed information about what the agent is currently doing
- **Follow-up Instructions**: Additional guidance you can provide to running agents

---

## Agent Management Tools

### `cursor_create_background_agent`

Creates a new autonomous coding agent that will work on a specified repository.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `repository_url` | string | Yes | - | GitHub repository URL where the agent will work |
| `prompt` | string | Yes | - | Detailed instructions for what the agent should accomplish |
| `branch` | string | No | `"main"` | Git branch to work on |
| `model` | string | No | `"claude-3-5-sonnet"` | AI model to use. Options: `"claude-3-5-sonnet"`, `"gpt-4o"`, `"claude-3-haiku"` |
| `max_iterations` | integer | No | `10` | Maximum number of iterations (1-50) |

#### Response Structure

```json
{
  "success": true,
  "agent_id": "agent-1234567890",
  "status": "CREATING",
  "repository_url": "https://github.com/owner/repo",
  "branch": "feature/new-feature",
  "model": "claude-3-5-sonnet",
  "created_at": "2025-01-15T10:30:00Z",
  "message": "Background agent created successfully..."
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/web-app",
    "prompt": "Implement user authentication with JWT tokens, including login, registration, and password reset functionality",
    "branch": "feature/auth-system",
    "model": "claude-3-5-sonnet",
    "max_iterations": 20
})
```

#### Best Practices

- **Be Specific**: Provide detailed, clear instructions. Include acceptance criteria when possible.
- **Include Context**: Mention relevant files, patterns, or conventions the agent should follow.
- **Set Realistic Iterations**: Complex tasks may need 20-30 iterations, simple tasks can work with 5-10.
- **Choose Appropriate Model**: Use `claude-3-5-sonnet` for most tasks, `gpt-4o` for maximum capability, `claude-3-haiku` for speed.

---

### `cursor_list_background_agents`

Lists all background agents with optional filtering by status or repository.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status_filter` | string | No | Filter by status: `"running"`, `"completed"`, `"failed"`, `"stopped"` |
| `repository_filter` | string | No | Filter by repository URL |
| `limit` | integer | No | Maximum number of agents to return |
| `cursor` | string | No | Pagination cursor for next page |

#### Response Structure

```json
{
  "success": true,
  "total_agents": 5,
  "agents": [
    {
      "agent_id": "agent-123",
      "status": "running",
      "repository_url": "https://github.com/owner/repo",
      "prompt": "Add user authentication...",
      "branch": "feature/auth",
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
    "repository_filter": "https://github.com/mycompany/web-app"
})
```

---

### `cursor_get_agent_status`

Gets the current status and detailed progress information for a specific agent.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | ID of the background agent to check |

#### Response Structure

```json
{
  "success": true,
  "agent_id": "agent-123",
  "status": "running",
  "progress": {
    "current_step": "Implementing authentication middleware",
    "completed_steps": 3,
    "total_estimated_steps": 8,
    "files_modified": ["src/auth/middleware.js", "src/routes/auth.js"],
    "commits_made": 2,
    "completion_percentage": 37.5
  },
  "repository_url": "https://github.com/owner/repo",
  "branch": "feature/auth-system",
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
- `COMPLETED`: Agent has finished successfully
- `FAILED`: Agent encountered an error
- `STOPPED`: Agent was manually stopped

#### Example Usage

```python
result = await client.call_tool("cursor_get_agent_status", {
    "agent_id": "agent-1234567890"
})

if result["success"]:
    print(f"Status: {result['status']}")
    print(f"Progress: {result['progress']['completion_percentage']}%")
    print(f"Current Step: {result['progress']['current_step']}")
```

---

### `cursor_stop_background_agent`

Stops a running background agent. Use this to halt an agent's work if needed.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | ID of the background agent to stop |

#### Response Structure

```json
{
  "success": true,
  "agent_id": "agent-123",
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

#### When to Stop an Agent

- The task requirements have changed significantly
- The agent is going in the wrong direction
- You need to free up resources
- The agent is stuck in an error loop

---

## Agent Interaction Tools

### `cursor_add_followup_instruction`

Sends additional instructions or clarifications to a running agent. This is useful for course correction or adding new requirements while the agent is working.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | ID of the background agent |
| `instruction` | string | Yes | Additional instruction or clarification |

#### Response Structure

```json
{
  "success": true,
  "agent_id": "agent-123",
  "instruction_added": "Please also ensure the feature works on mobile devices",
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
    """
})
```

#### Best Practices for Follow-ups

- **Be Specific**: Clearly state what you want changed or added
- **Provide Context**: Reference existing code or patterns when relevant
- **Use Examples**: Show code examples if you want specific implementations
- **Timing Matters**: Send follow-ups early if possible, before the agent has completed related work
- **One Focus**: Keep each follow-up focused on a single concern when possible

#### Common Follow-up Scenarios

1. **Clarification**: "Use TypeScript instead of JavaScript for this component"
2. **Additional Requirements**: "Also add email verification for new users"
3. **Style Guidance**: "Follow the existing error handling patterns in the auth module"
4. **Bug Fix**: "The API endpoint URL should be '/api/v2/users' not '/api/users'"
5. **Architecture Change**: "Switch from REST to GraphQL for this feature"

---

## System Information Tools

### `cursor_get_api_usage`

Retrieves current API usage statistics, limits, and billing information.

#### Parameters

No parameters required.

#### Response Structure

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

if result["success"]:
    usage = result["usage"]
    limits = result["limits"]
    
    print(f"Active Agents: {usage['active_agents']}/{limits['max_active_agents']}")
    print(f"Monthly Usage: {usage['agents_created_this_month']}/{limits['monthly_agent_limit']}")
    print(f"Remaining: {result['remaining_quota']['agents']} agents this month")
```

---

### `cursor_list_available_models`

Gets a list of all available AI models that can be used for background agents.

#### Parameters

No parameters required.

#### Response Structure

```json
{
  "success": true,
  "models": [
    {
      "id": "claude-3-5-sonnet",
      "name": "Claude 3.5 Sonnet",
      "description": "Best overall performance (recommended)",
      "capabilities": ["code", "reasoning", "long_context"]
    },
    {
      "id": "gpt-4o",
      "name": "GPT-4o",
      "description": "Maximum capability for complex tasks",
      "capabilities": ["code", "reasoning"]
    }
  ],
  "total_models": 3,
  "recommended": {
    "id": "claude-3-5-sonnet",
    "name": "Claude 3.5 Sonnet"
  },
  "message": "Retrieved 3 available models"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_list_available_models", {})

if result["success"]:
    print("Available Models:")
    for model in result["models"]:
        print(f"  - {model['id']}: {model['description']}")
    
    recommended = result["recommended"]
    print(f"\nRecommended: {recommended['id']}")
```

#### Model Selection Guide

- **claude-3-5-sonnet**: Best overall choice for most tasks. Good balance of speed and capability.
- **gpt-4o**: Maximum capability for very complex tasks requiring advanced reasoning.
- **claude-3-haiku**: Fastest option, suitable for simpler tasks.

---

### `cursor_list_repositories`

Lists all GitHub repositories accessible to your API key.

#### Parameters

No parameters required.

#### Response Structure

```json
{
  "success": true,
  "repositories": [
    {
      "url": "https://github.com/owner/repo1",
      "name": "repo1",
      "owner": "owner",
      "private": false,
      "description": "Main application"
    }
  ],
  "total_repositories": 10,
  "message": "Retrieved 10 accessible repositories"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_list_repositories", {})

if result["success"]:
    print(f"Found {result['total_repositories']} repositories:")
    for repo in result["repositories"]:
        print(f"  - {repo['url']}: {repo.get('description', 'No description')}")
```

#### Notes

- Repositories are cached for 5 minutes to reduce API calls
- Only repositories you have access to will be returned
- Private repositories require proper authentication

---

### `cursor_list_repository_branches`

Gets a list of all branches for a specific GitHub repository.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `repository_url` | string | Yes | - | GitHub repository URL (e.g., `https://github.com/owner/repo`) |
| `force_refresh` | boolean | No | `false` | Force refresh the branch list from GitHub API |

#### Response Structure

```json
{
  "success": true,
  "repository": "https://github.com/owner/repo",
  "owner": "owner",
  "repo": "repo",
  "branches": ["main", "develop", "feature/auth", "feature/payment"],
  "total_branches": 4,
  "message": "Retrieved 4 branches for owner/repo"
}
```

#### Example Usage

```python
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": "https://github.com/mycompany/web-app",
    "force_refresh": False
})

if result["success"]:
    print(f"Branches for {result['repository']}:")
    for branch in result["branches"]:
        print(f"  - {branch}")
```

#### Notes

- Branch data is cached per repository for 5 minutes
- Use `force_refresh: true` to bypass cache and get latest branches
- If repository access fails, common branch names (`main`, `master`, `develop`) are returned as fallback
- Private repositories may require a `GITHUB_TOKEN` environment variable

---

## MCP Resources

MCP resources provide read-only access to server state and configuration information.

### `mcp://cursor-agent/api-config`

Current API configuration and server settings.

#### Example Usage

```python
config_data = await client.read_resource("mcp://cursor-agent/api-config")
config = json.loads(config_data)

print(f"API Base URL: {config['base_url']}")
print(f"Timeout: {config['timeout']}s")
print(f"API Key Configured: {config['api_key_configured']}")
print(f"Session Active: {config['session_active']}")
```

#### Response Structure

```json
{
  "base_url": "https://api.cursor.com",
  "timeout": 30,
  "max_retries": 3,
  "api_key_configured": true,
  "session_active": true
}
```

---

### `mcp://cursor-agent/agents-summary`

Summary of all background agents with status breakdown.

#### Example Usage

```python
summary_data = await client.read_resource("mcp://cursor-agent/agents-summary")
summary = json.loads(summary_data)

print(f"Total Agents: {summary['total_agents']}")
print("Status Breakdown:")
for status, count in summary["agents_by_status"].items():
    print(f"  {status}: {count}")
```

#### Response Structure

```json
{
  "total_agents": 5,
  "agents_by_status": {
    "running": 2,
    "completed": 2,
    "failed": 1
  },
  "agents": [
    {
      "agent_id": "agent-123",
      "status": "running",
      "repository_url": "https://github.com/owner/repo",
      "created_at": "2025-01-15T10:30:00Z",
      "branch": "feature/auth"
    }
  ]
}
```

---

### `mcp://cursor-agent/usage-metrics`

API usage statistics and performance metrics (same as `cursor_get_api_usage`).

#### Example Usage

```python
metrics_data = await client.read_resource("mcp://cursor-agent/usage-metrics")
metrics = json.loads(metrics_data)

print(f"Active Agents: {metrics['usage']['active_agents']}")
print(f"Monthly Usage: {metrics['usage']['agents_created_this_month']}")
```

---

## MCP Prompts

MCP prompts provide templated guidance for creating effective agent tasks and follow-up instructions.

### `cursor_agent_task_template`

Generates a structured task template based on task type and complexity.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_type` | string | Yes | Type of task: `"feature"`, `"bugfix"`, `"refactor"`, `"test"`, `"docs"` |
| `complexity` | string | No | Task complexity: `"simple"`, `"medium"`, `"complex"` |

#### Example Usage

```python
template = await client.get_prompt("cursor_agent_task_template", {
    "task_type": "feature",
    "complexity": "medium"
})

# Use the template to create a well-structured prompt
prompt = template.messages[0].content.text
```

#### Available Templates

- **Feature (simple/medium/complex)**: Templates for implementing new features
- **Bugfix (simple/medium/complex)**: Templates for fixing bugs with appropriate investigation depth

Each template includes:
- Clear objective statement
- Detailed requirements
- Acceptance criteria
- Implementation approach
- Notes and considerations

---

### `cursor_agent_followup_guide`

Provides guidance on creating effective follow-up instructions based on agent status.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `current_status` | string | Yes | Current agent status (`"running"`, `"stuck"`, etc.) |
| `issue_type` | string | No | Type of issue (`"clarification"`, `"issue"`) |

#### Example Usage

```python
guide = await client.get_prompt("cursor_agent_followup_guide", {
    "current_status": "running",
    "issue_type": "clarification"
})

# Use the guide to craft effective follow-up instructions
guidance = guide.messages[0].content.text
```

---

## Usage Examples

### Complete Workflow Example

```python
import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

async def complete_agent_workflow():
    """Complete example of creating and managing an agent"""
    
    # Connect to MCP server
    async with stdio_client(["python3", "cursor_agent_mcp_server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 1. List available models
            models_result = await session.call_tool(
                "cursor_list_available_models",
                {}
            )
            print(f"Available models: {models_result.content[0].text}")
            
            # 2. List repositories
            repos_result = await session.call_tool(
                "cursor_list_repositories",
                {}
            )
            print(f"Repositories: {repos_result.content[0].text}")
            
            # 3. Create an agent
            create_result = await session.call_tool(
                "cursor_create_background_agent",
                {
                    "repository_url": "https://github.com/mycompany/app",
                    "prompt": "Add user authentication with JWT tokens",
                    "branch": "feature/auth",
                    "model": "claude-3-5-sonnet",
                    "max_iterations": 20
                }
            )
            agent_data = json.loads(create_result.content[0].text)
            agent_id = agent_data["agent_id"]
            print(f"Created agent: {agent_id}")
            
            # 4. Monitor agent progress
            for _ in range(10):
                status_result = await session.call_tool(
                    "cursor_get_agent_status",
                    {"agent_id": agent_id}
                )
                status_data = json.loads(status_result.content[0].text)
                
                if status_data["status"] in ["completed", "failed", "stopped"]:
                    break
                
                progress = status_data.get("progress", {})
                print(f"Progress: {progress.get('completion_percentage', 0)}%")
                await asyncio.sleep(30)  # Check every 30 seconds
            
            # 5. Add follow-up if needed
            await session.call_tool(
                "cursor_add_followup_instruction",
                {
                    "agent_id": agent_id,
                    "instruction": "Also add two-factor authentication support"
                }
            )
            
            # 6. List all agents
            list_result = await session.call_tool(
                "cursor_list_background_agents",
                {}
            )
            print(f"All agents: {list_result.content[0].text}")

asyncio.run(complete_agent_workflow())
```

### Real-World Scenarios

#### Scenario 1: Security Audit and Fixes

```python
await session.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/company/project",
    "prompt": """
    Perform comprehensive security audit and implement fixes:
    
    Areas to review:
    - Input validation and sanitization
    - SQL injection prevention
    - XSS protection
    - Authentication vulnerabilities
    - Authorization checks
    - Sensitive data exposure
    - Rate limiting implementation
    
    For each issue found:
    1. Document the vulnerability
    2. Implement the fix
    3. Add tests to prevent regression
    4. Update security documentation
    """,
    "model": "claude-3-5-sonnet",
    "max_iterations": 30
})
```

#### Scenario 2: Mobile Responsive Redesign

```python
await session.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/company/web-app",
    "prompt": """
    Redesign the application for mobile responsiveness:
    
    Requirements:
    - Audit all pages for mobile compatibility
    - Implement responsive navigation
    - Optimize images and media
    - Ensure touch-friendly interactions
    - Test across different screen sizes
    - Maintain accessibility standards
    
    Use CSS Grid/Flexbox and follow mobile-first approach.
    """,
    "model": "claude-3-5-sonnet",
    "max_iterations": 25
})
```

#### Scenario 3: Test Coverage Enhancement

```python
await session.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/company/project",
    "prompt": """
    Increase test coverage to 90%+ across the application:
    
    Tasks:
    - Analyze current test coverage
    - Identify untested code paths
    - Write unit tests for all functions
    - Add integration tests for critical flows
    - Create end-to-end tests for user journeys
    - Set up test automation in CI/CD
    
    Focus on business-critical functionality first.
    """,
    "model": "claude-3-5-sonnet",
    "max_iterations": 30
})
```

---

## Error Handling

### Common Error Scenarios

#### Authentication Errors

```json
{
  "success": false,
  "error": "Authentication failed. Check your Cursor API key.",
  "tool": "cursor_create_background_agent",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Resolution**: Ensure `CURSOR_API_KEY` environment variable is set correctly.

#### Repository Access Errors

```json
{
  "success": false,
  "error": "Repository not found or not accessible",
  "repository": "https://github.com/owner/repo"
}
```

**Resolution**: 
- Verify repository URL is correct
- Ensure API key has access to the repository
- For private repos, check GitHub token permissions

#### Rate Limiting

```json
{
  "success": false,
  "error": "API request failed: 429 - Rate limit exceeded"
}
```

**Resolution**: 
- Implement exponential backoff
- Cache results when possible
- Reduce API call frequency

### Error Response Format

All tools return errors in a consistent format:

```json
{
  "success": false,
  "error": "Error description",
  "tool": "tool_name",
  "timestamp": "ISO-8601 timestamp",
  "message": "User-friendly error message"
}
```

### Handling Errors in Code

```python
result = await session.call_tool("cursor_create_background_agent", {...})
data = json.loads(result.content[0].text)

if not data.get("success"):
    error = data.get("error", "Unknown error")
    message = data.get("message", "Operation failed")
    
    print(f"Error: {error}")
    print(f"Details: {message}")
    
    # Handle specific error types
    if "Authentication" in error:
        print("Check your API key configuration")
    elif "Repository" in error:
        print("Verify repository URL and access permissions")
    else:
        print("Retry the operation or check logs for details")
```

---

## Best Practices

### Writing Effective Prompts

1. **Be Specific and Detailed**
   - ? "Add authentication"
   - ? "Implement JWT-based authentication with login, registration, password reset, and session management. Use bcrypt for password hashing and follow the existing error handling patterns."

2. **Include Acceptance Criteria**
   ```
   Acceptance Criteria:
   - [ ] Users can register with email and password
   - [ ] Passwords are hashed before storage
   - [ ] JWT tokens expire after 24 hours
   - [ ] All auth endpoints have rate limiting
   ```

3. **Provide Context**
   - Reference existing files or patterns
   - Mention coding conventions
   - Specify technology choices
   - Include business requirements

4. **Set Realistic Scope**
   - Break large tasks into smaller agents if needed
   - Consider complexity when setting `max_iterations`
   - Be clear about what's in scope vs out of scope

### Agent Monitoring

1. **Regular Status Checks**: Poll agent status every 30-60 seconds for active monitoring
2. **Progress Tracking**: Monitor `completion_percentage` and `current_step` to understand progress
3. **Log Review**: Check `logs` array for detailed activity information
4. **Early Intervention**: Send follow-up instructions early if you notice issues

### Resource Management

1. **Use Caching**: Leverage built-in caching for models, repositories, and branches
2. **Batch Operations**: Group related operations when possible
3. **Limit Active Agents**: Monitor `cursor_get_api_usage` to stay within limits
4. **Clean Up**: Stop unnecessary agents to free up resources

### Security Considerations

1. **API Key Protection**: Never commit API keys to version control
2. **Repository Access**: Only grant agents access to repositories they need
3. **Branch Strategy**: Use feature branches, not main/master for agent work
4. **Code Review**: Always review agent-generated code before merging

### Performance Optimization

1. **Model Selection**: Use faster models (haiku) for simple tasks, powerful models (sonnet/opus) for complex tasks
2. **Iteration Limits**: Set appropriate `max_iterations` - too high wastes resources, too low may not complete
3. **Parallel Agents**: Run multiple agents simultaneously for different repositories or tasks
4. **Cache Results**: Use `force_refresh: false` when fresh data isn't critical

---

## Tool Reference Summary

| Tool Name | Purpose | Key Parameters |
|-----------|---------|----------------|
| `cursor_create_background_agent` | Create new agent | `repository_url`, `prompt`, `branch`, `model` |
| `cursor_get_agent_status` | Check agent progress | `agent_id` |
| `cursor_list_background_agents` | List all agents | `status_filter`, `repository_filter` |
| `cursor_stop_background_agent` | Stop an agent | `agent_id` |
| `cursor_add_followup_instruction` | Send additional instructions | `agent_id`, `instruction` |
| `cursor_get_api_usage` | Check usage/limits | None |
| `cursor_list_available_models` | List AI models | None |
| `cursor_list_repositories` | List repositories | None |
| `cursor_list_repository_branches` | List repo branches | `repository_url` |

---

## Additional Resources

- [Cursor Background Agent API Documentation](https://docs.cursor.com/en/background-agent/api/overview)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [Project README](./README.md) - General project documentation
- [Example Client Code](./example_cursor_mcp_client.py) - Working code examples

---

## Support

For issues, questions, or contributions:

1. Check the error messages and this documentation
2. Review the example code in `example_cursor_mcp_client.py`
3. Verify your API key and permissions
4. Check agent status and logs for detailed error information

---

*Last updated: January 2025*
