# MCP Tools Documentation

This document provides comprehensive documentation for all MCP tools available in the Cursor Background Agent MCP Server. Each tool includes detailed descriptions, parameter specifications, return values, and practical usage examples.

## Table of Contents

- [Agent Management Tools](#agent-management-tools)
  - [cursor_create_background_agent](#cursor_create_background_agent)
  - [cursor_get_agent_status](#cursor_get_agent_status)
  - [cursor_list_background_agents](#cursor_list_background_agents)
  - [cursor_stop_background_agent](#cursor_stop_background_agent)
- [Agent Interaction Tools](#agent-interaction-tools)
  - [cursor_add_followup_instruction](#cursor_add_followup_instruction)
- [System Information Tools](#system-information-tools)
  - [cursor_get_api_usage](#cursor_get_api_usage)
  - [cursor_list_available_models](#cursor_list_available_models)
  - [cursor_list_repositories](#cursor_list_repositories)
  - [cursor_list_repository_branches](#cursor_list_repository_branches)

---

## Agent Management Tools

### cursor_create_background_agent

Create a new Cursor background agent for autonomous coding tasks. The agent will work independently on your repository, writing code, making commits, and creating pull requests.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `repository_url` | string | ? Yes | - | GitHub repository URL where the agent will work (e.g., `https://github.com/owner/repo`) |
| `prompt` | string | ? Yes | - | Detailed instructions for what the agent should accomplish |
| `branch` | string | ? No | `"main"` | Git branch to work on |
| `model` | string | ? No | `"claude-3-5-sonnet"` | AI model to use. Options: `claude-3-5-sonnet`, `gpt-4o`, `claude-3-haiku` |
| `max_iterations` | integer | ? No | `10` | Maximum number of iterations (1-50) |

#### Return Value

```json
{
  "success": true,
  "agent_id": "agent-12345",
  "status": "CREATING",
  "repository_url": "https://github.com/owner/repo",
  "branch": "feature/new-feature",
  "model": "claude-3-5-sonnet",
  "created_at": "2025-01-15T10:30:00Z",
  "message": "Background agent created successfully. Agent will work autonomously on 'Add user authentication system'"
}
```

#### Usage Examples

##### Example 1: Basic Feature Development

```python
# Python MCP Client
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/web-app",
    "prompt": "Add a user profile page with avatar upload and bio editing functionality. Include form validation and error handling.",
    "branch": "feature/user-profile",
    "model": "claude-3-5-sonnet"
})

print(f"Agent created: {result['agent_id']}")
```

##### Example 2: Complex Refactoring Task

```python
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/api-service",
    "prompt": """Refactor the legacy authentication system to use modern patterns:
    
    Current issues:
    - Mixed authentication methods (sessions + JWT)
    - No proper error handling
    - Security vulnerabilities
    
    Refactoring goals:
    - Standardize on JWT with refresh tokens
    - Add comprehensive error handling
    - Implement proper middleware
    - Add unit and integration tests
    - Update documentation""",
    "branch": "refactor/auth-modernization",
    "model": "gpt-4o",
    "max_iterations": 25
})
```

##### Example 3: Bug Fix with Fast Model

```python
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/mobile-app",
    "prompt": """Fix the memory leak in the shopping cart component.
    
    Problem: Users report the page becomes slow after adding/removing items
    Location: components/ShoppingCart.tsx
    
    Investigation needed:
    1. Check for event listener cleanup
    2. Review useEffect dependencies
    3. Look for state update loops
    4. Add proper component unmounting""",
    "branch": "bugfix/cart-memory-leak",
    "model": "claude-3-haiku",  # Faster, cheaper model for simple fixes
    "max_iterations": 10
})
```

##### Example 4: Test Coverage Enhancement

```python
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/service",
    "prompt": """Increase test coverage to 90%+ across the application:
    
    Tasks:
    - Analyze current test coverage
    - Identify untested code paths
    - Write unit tests for all functions
    - Add integration tests for critical flows
    - Create end-to-end tests for user journeys
    - Set up test automation in CI/CD
    
    Focus on business-critical functionality first.
    Include edge cases and error scenarios.""",
    "model": "claude-3-5-sonnet",
    "max_iterations": 20
})
```

##### Example 5: Using via Web API

```javascript
// JavaScript/Fetch API
const response = await fetch('http://localhost:8080/api/create-agent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        repository_url: 'https://github.com/mycompany/web-app',
        prompt: 'Add dark mode toggle functionality',
        branch: 'feature/dark-mode',
        model: 'claude-3-5-sonnet'
    })
});

const result = await response.json();
console.log('Agent created:', result.agent_id);
```

##### Example 6: Using via cURL

```bash
curl -X POST http://localhost:8080/api/create-agent \
  -H "Content-Type: application/json" \
  -d '{
    "repository_url": "https://github.com/mycompany/web-app",
    "prompt": "Implement user authentication with JWT tokens",
    "branch": "feature/auth",
    "model": "claude-3-5-sonnet",
    "max_iterations": 15
  }'
```

#### Best Practices

- **Clear Prompts**: Write detailed, specific prompts with clear requirements and acceptance criteria
- **Branch Strategy**: Use descriptive branch names like `feature/feature-name`, `bugfix/issue-description`
- **Model Selection**: 
  - Use `claude-3-5-sonnet` for most tasks (best balance)
  - Use `gpt-4o` for complex architectural decisions
  - Use `claude-3-haiku` for simple fixes and tasks
- **Iterations**: 
  - Simple tasks: 5-10 iterations
  - Medium tasks: 10-20 iterations
  - Complex tasks: 20-50 iterations

---

### cursor_get_agent_status

Get the current status and progress of a background agent. Use this to monitor agent progress, check completion percentage, view modified files, and see recent activity logs.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | ? Yes | ID of the background agent to check |

#### Return Value

```json
{
  "success": true,
  "agent_id": "agent-12345",
  "status": "running",
  "progress": {
    "current_step": "Implementing authentication middleware",
    "completed_steps": 3,
    "total_estimated_steps": 8,
    "files_modified": [
      "src/auth/middleware.js",
      "src/routes/auth.js"
    ],
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
    "Implementing JWT token validation",
    "Adding password hashing utilities"
  ]
}
```

#### Status Values

- `CREATING` - Agent is being initialized
- `running` - Agent is actively working on the task
- `completed` - Agent has finished successfully
- `failed` - Agent encountered an error and stopped
- `stopped` - Agent was manually stopped

#### Usage Examples

##### Example 1: Check Agent Status

```python
result = await client.call_tool("cursor_get_agent_status", {
    "agent_id": "agent-12345"
})

if result["success"]:
    status = result["status"]
    progress = result["progress"]
    
    print(f"Status: {status}")
    print(f"Progress: {progress['completed_steps']}/{progress['total_estimated_steps']} steps")
    print(f"Completion: {progress['completion_percentage']}%")
    print(f"Current step: {progress['current_step']}")
    print(f"Files modified: {', '.join(progress['files_modified'])}")
```

##### Example 2: Monitor Agent Progress Loop

```python
import asyncio
import time

async def monitor_agent(agent_id):
    """Monitor agent until completion"""
    while True:
        result = await client.call_tool("cursor_get_agent_status", {
            "agent_id": agent_id
        })
        
        if not result["success"]:
            print(f"Error: {result.get('error')}")
            break
        
        status = result["status"]
        progress = result.get("progress", {})
        
        print(f"\n[{status.upper()}] {progress.get('completion_percentage', 0)}% complete")
        print(f"Current: {progress.get('current_step', 'N/A')}")
        
        if status in ["completed", "failed", "stopped"]:
            print(f"\nAgent finished with status: {status}")
            break
        
        await asyncio.sleep(30)  # Check every 30 seconds

# Usage
await monitor_agent("agent-12345")
```

##### Example 3: Get Status with Error Handling

```python
try:
    result = await client.call_tool("cursor_get_agent_status", {
        "agent_id": "agent-12345"
    })
    
    if result["success"]:
        if result["status"] == "completed":
            print("? Agent completed successfully!")
            # Check for pull request link, commits, etc.
        elif result["status"] == "failed":
            print(f"? Agent failed: {result.get('error', 'Unknown error')}")
        elif result["status"] == "running":
            print(f"?? Agent is still working... {result['progress']['completion_percentage']}% complete")
    else:
        print(f"Error: {result.get('error')}")
        
except Exception as e:
    print(f"Failed to get agent status: {e}")
```

##### Example 4: Check Status via Web API

```javascript
const response = await fetch('http://localhost:8080/api/agent-status/agent-12345');
const result = await response.json();

if (result.success) {
    console.log(`Status: ${result.status}`);
    console.log(`Progress: ${result.progress.completion_percentage}%`);
    console.log(`Current step: ${result.progress.current_step}`);
}
```

---

### cursor_list_background_agents

List all background agents with optional filtering by status or repository. Useful for monitoring multiple agents or finding specific agents.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status_filter` | string | ? No | Filter agents by status. Options: `"running"`, `"completed"`, `"failed"`, `"stopped"` |
| `repository_filter` | string | ? No | Filter agents by repository URL |

#### Return Value

```json
{
  "success": true,
  "total_agents": 3,
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
    },
    {
      "agent_id": "agent-003",
      "status": "failed",
      "repository_url": "https://github.com/company/mobile",
      "prompt": "Add push notification support",
      "branch": "feature/push-notifications",
      "created_at": "2025-01-15T08:15:00Z",
      "error": "Repository access denied"
    }
  ],
  "filters_applied": {
    "status": null,
    "repository": null
  }
}
```

#### Usage Examples

##### Example 1: List All Agents

```python
result = await client.call_tool("cursor_list_background_agents", {})

if result["success"]:
    print(f"Total agents: {result['total_agents']}")
    
    for agent in result["agents"]:
        status_emoji = {
            "completed": "?",
            "running": "??",
            "failed": "?",
            "stopped": "??"
        }.get(agent["status"], "?")
        
        print(f"{status_emoji} {agent['agent_id']}: {agent['status']}")
        print(f"   ?? {agent['repository_url']}")
        print(f"   ?? {agent['branch']}")
        print(f"   ?? {agent['prompt'][:60]}...")
```

##### Example 2: Filter by Status

```python
# Get only running agents
result = await client.call_tool("cursor_list_background_agents", {
    "status_filter": "running"
})

if result["success"]:
    print(f"Running agents: {result['total_agents']}")
    for agent in result["agents"]:
        print(f"- {agent['agent_id']} on {agent['repository_url']}")
```

##### Example 3: Filter by Repository

```python
# Get agents for a specific repository
result = await client.call_tool("cursor_list_background_agents", {
    "repository_filter": "https://github.com/mycompany/web-app"
})

if result["success"]:
    print(f"Agents for repository: {result['total_agents']}")
    for agent in result["agents"]:
        print(f"- {agent['agent_id']}: {agent['status']} ({agent['branch']})")
```

##### Example 4: Combined Filtering and Status Check

```python
# Get completed agents for a specific repo
result = await client.call_tool("cursor_list_background_agents", {
    "status_filter": "completed",
    "repository_filter": "https://github.com/mycompany/api"
})

if result["success"]:
    completed_agents = result["agents"]
    print(f"Found {len(completed_agents)} completed agents:")
    
    for agent in completed_agents:
        print(f"\n? {agent['agent_id']}")
        print(f"   Branch: {agent['branch']}")
        print(f"   Task: {agent['prompt']}")
        print(f"   Created: {agent['created_at']}")
```

##### Example 5: List Agents via Web API

```javascript
// Get all agents
const response = await fetch('http://localhost:8080/api/agents');
const result = await response.json();

// Get running agents only
const runningResponse = await fetch(
    'http://localhost:8080/api/agents?status=running'
);
const runningAgents = await runningResponse.json();

console.log(`Total agents: ${result.total_agents}`);
console.log(`Running agents: ${runningAgents.total_agents}`);
```

---

### cursor_stop_background_agent

Stop a running background agent. This will halt the agent's work immediately and prevent it from making further changes.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | ? Yes | ID of the background agent to stop |

#### Return Value

```json
{
  "success": true,
  "agent_id": "agent-12345",
  "status": "stopped",
  "message": "Background agent stopped successfully"
}
```

#### Usage Examples

##### Example 1: Stop a Running Agent

```python
result = await client.call_tool("cursor_stop_background_agent", {
    "agent_id": "agent-12345"
})

if result["success"]:
    print(f"? Agent {result['agent_id']} stopped successfully")
else:
    print(f"? Failed to stop agent: {result.get('error')}")
```

##### Example 2: Stop All Running Agents

```python
# First, get all running agents
list_result = await client.call_tool("cursor_list_background_agents", {
    "status_filter": "running"
})

if list_result["success"]:
    running_agents = list_result["agents"]
    
    for agent in running_agents:
        stop_result = await client.call_tool("cursor_stop_background_agent", {
            "agent_id": agent["agent_id"]
        })
        
        if stop_result["success"]:
            print(f"? Stopped {agent['agent_id']}")
        else:
            print(f"? Failed to stop {agent['agent_id']}: {stop_result.get('error')}")
```

##### Example 3: Stop Agent with Confirmation

```python
agent_id = "agent-12345"

# First check the agent status
status_result = await client.call_tool("cursor_get_agent_status", {
    "agent_id": agent_id
})

if status_result["success"]:
    if status_result["status"] == "running":
        # Confirm before stopping
        confirm = input(f"Stop agent {agent_id}? (yes/no): ")
        
        if confirm.lower() == "yes":
            stop_result = await client.call_tool("cursor_stop_background_agent", {
                "agent_id": agent_id
            })
            print(f"Agent stopped: {stop_result['success']}")
        else:
            print("Cancelled")
    else:
        print(f"Agent is not running (status: {status_result['status']})")
```

##### Example 4: Stop Agent via Web API

```javascript
const response = await fetch('http://localhost:8080/api/agent/agent-12345', {
    method: 'DELETE'
});

const result = await response.json();

if (result.success) {
    console.log(`Agent ${result.agent_id} stopped successfully`);
} else {
    console.error(`Failed to stop agent: ${result.error}`);
}
```

---

## Agent Interaction Tools

### cursor_add_followup_instruction

Add a follow-up instruction to a running background agent. Use this to provide clarifications, add requirements, or redirect the agent's work.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | ? Yes | ID of the background agent |
| `instruction` | string | ? Yes | Additional instruction or clarification for the agent |

#### Return Value

```json
{
  "success": true,
  "agent_id": "agent-12345",
  "instruction_added": "Please also add two-factor authentication support",
  "status": "updated",
  "message": "Follow-up instruction added successfully"
}
```

#### Usage Examples

##### Example 1: Add Clarification

```python
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-12345",
    "instruction": "Please use TypeScript instead of JavaScript for this component, and follow the existing patterns in src/components/auth/"
})

if result["success"]:
    print("? Follow-up instruction added")
```

##### Example 2: Add New Requirements

```python
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-12345",
    "instruction": """Please also add the following enhancements:
    - Two-factor authentication (2FA) support
    - Social login options (Google, GitHub)
    - Remember me functionality
    - Account lockout after failed attempts
    
    Make sure to maintain backward compatibility and add proper documentation."""
})

if result["success"]:
    print("? Additional requirements sent to agent")
```

##### Example 3: Fix Issue or Redirect

```python
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-12345",
    "instruction": """The API endpoint URL should be '/api/v2/users' not '/api/users'.
    Please update the fetch calls in the authentication service to use the correct endpoint."""
})

if result["success"]:
    print("? Correction sent to agent")
```

##### Example 4: Provide Context or Examples

```python
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-12345",
    "instruction": """Look at how user authentication is handled in src/auth/AuthProvider.tsx for the pattern to follow.
    Also check src/components/Login.tsx for the form structure we use. 
    Ensure the new component follows the same styling and error handling patterns."""
})

if result["success"]:
    print("? Context and examples provided to agent")
```

##### Example 5: Stop Current Work and Redirect

```python
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-12345",
    "instruction": """Please pause the current implementation. Instead, focus on:
    1. First, add comprehensive unit tests for existing authentication code
    2. Then proceed with the new feature implementation
    3. Ensure all tests pass before making changes"""
})

if result["success"]:
    print("? Work direction updated")
```

##### Example 6: Add Follow-up via Web API

```javascript
const response = await fetch('http://localhost:8080/api/agent/agent-12345/followup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        instruction: 'Please also ensure the feature works on mobile devices'
    })
});

const result = await response.json();

if (result.success) {
    console.log('Follow-up instruction added successfully');
}
```

#### Best Practices for Follow-up Instructions

- **Be Specific**: Provide clear, actionable instructions
- **Include Context**: Reference existing code or patterns when possible
- **Break Down Complex Requests**: Split multiple changes into separate instructions if needed
- **Provide Examples**: Show the agent similar code or patterns to follow
- **Timing**: Send follow-ups early if possible, before the agent completes related work

---

## System Information Tools

### cursor_get_api_usage

Get current API usage and limits for Cursor Background Agents. Monitor your quota, track usage, and plan your agent creation accordingly.

#### Parameters

This tool takes no parameters.

#### Return Value

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

#### Usage Examples

##### Example 1: Check API Usage

```python
result = await client.call_tool("cursor_get_api_usage", {})

if result["success"]:
    usage = result["usage"]
    limits = result["limits"]
    
    print("?? Current Usage:")
    print(f"   ?? Active Agents: {usage['active_agents']}/{limits['max_active_agents']}")
    print(f"   ?? Agents This Month: {usage['agents_created_this_month']}/{limits['monthly_agent_limit']}")
    print(f"   ?? API Calls Today: {usage['api_calls_today']}/{limits['daily_api_calls']}")
    print(f"   ?? Tokens Used Today: {usage['tokens_used_today']:,}")
    
    print("\n?? Remaining Quota:")
    print(f"   ?? Agents: {result['remaining_quota']['agents']:,}")
    print(f"   ?? API Calls: {result['remaining_quota']['api_calls']:,}")
```

##### Example 2: Check if Can Create More Agents

```python
result = await client.call_tool("cursor_get_api_usage", {})

if result["success"]:
    remaining = result["remaining_quota"]["agents"]
    active = result["usage"]["active_agents"]
    max_active = result["limits"]["max_active_agents"]
    
    if remaining > 0 and active < max_active:
        print(f"? Can create agents (remaining: {remaining}, active: {active}/{max_active})")
    else:
        print(f"? Cannot create more agents")
        print(f"   Remaining quota: {remaining}")
        print(f"   Active agents: {active}/{max_active}")
```

##### Example 3: Monitor Usage Over Time

```python
import asyncio
from datetime import datetime

async def monitor_usage():
    """Monitor API usage periodically"""
    while True:
        result = await client.call_tool("cursor_get_api_usage", {})
        
        if result["success"]:
            usage = result["usage"]
            remaining = result["remaining_quota"]
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Active: {usage['active_agents']}, "
                  f"Today: {usage['api_calls_today']} calls, "
                  f"Remaining: {remaining['agents']} agents")
        
        await asyncio.sleep(300)  # Check every 5 minutes

# Usage
await monitor_usage()
```

##### Example 4: Get Usage via Web API

```javascript
const response = await fetch('http://localhost:8080/api/api-usage');
const result = await response.json();

if (result.success) {
    const usage = result.usage;
    const limits = result.limits;
    
    console.log(`Active agents: ${usage.active_agents}/${limits.max_active_agents}`);
    console.log(`Agents this month: ${usage.agents_created_this_month}/${limits.monthly_agent_limit}`);
    console.log(`Remaining quota: ${result.remaining_quota.agents} agents`);
}
```

---

### cursor_list_available_models

Get a list of available AI models for background agents. This helps you choose the right model for your task.

#### Parameters

This tool takes no parameters.

#### Return Value

```json
{
  "success": true,
  "models": [
    {
      "id": "claude-3-5-sonnet",
      "name": "Claude 3.5 Sonnet",
      "description": "Best overall performance for most tasks",
      "capabilities": ["reasoning", "code", "analysis"],
      "recommended": true
    },
    {
      "id": "gpt-4o",
      "name": "GPT-4 Optimized",
      "description": "Most capable model for complex reasoning",
      "capabilities": ["reasoning", "code", "analysis", "architecture"]
    },
    {
      "id": "claude-3-haiku",
      "name": "Claude 3 Haiku",
      "description": "Fastest and most cost-effective",
      "capabilities": ["code", "simple_tasks"]
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

#### Usage Examples

##### Example 1: List All Available Models

```python
result = await client.call_tool("cursor_list_available_models", {})

if result["success"]:
    print(f"Available models: {result['total_models']}")
    
    for model in result["models"]:
        recommended = "?" if model.get("recommended") else "  "
        print(f"{recommended} {model['id']}: {model['name']}")
        print(f"     {model['description']}")
```

##### Example 2: Choose Model Based on Task Complexity

```python
result = await client.call_tool("cursor_list_available_models", {})

if result["success"]:
    models = result["models"]
    
    # For simple task, use faster model
    simple_task_model = next(
        (m for m in models if "haiku" in m["id"].lower()),
        models[0]
    )
    
    # For complex task, use most capable model
    complex_task_model = next(
        (m for m in models if "gpt-4" in m["id"].lower() or m.get("recommended")),
        models[-1]
    )
    
    print(f"Simple task model: {simple_task_model['id']}")
    print(f"Complex task model: {complex_task_model['id']}")
```

##### Example 3: Get Recommended Model

```python
result = await client.call_tool("cursor_list_available_models", {})

if result["success"]:
    recommended = result.get("recommended")
    if recommended:
        print(f"? Recommended model: {recommended['id']} - {recommended['name']}")
        # Use this model for agent creation
        model_to_use = recommended["id"]
    else:
        # Fallback to first model
        model_to_use = result["models"][0]["id"]
```

##### Example 4: List Models via Web API

```javascript
const response = await fetch('http://localhost:8080/api/models');
const result = await response.json();

if (result.success) {
    result.models.forEach(model => {
        console.log(`${model.id}: ${model.name}`);
        console.log(`  ${model.description}`);
    });
    
    if (result.recommended) {
        console.log(`\n? Recommended: ${result.recommended.id}`);
    }
}
```

---

### cursor_list_repositories

Get a list of accessible GitHub repositories. This helps you find the correct repository URL when creating agents.

#### Parameters

This tool takes no parameters.

#### Return Value

```json
{
  "success": true,
  "repositories": [
    {
      "url": "https://github.com/mycompany/web-app",
      "name": "web-app",
      "owner": "mycompany",
      "full_name": "mycompany/web-app",
      "private": false,
      "description": "Main web application",
      "default_branch": "main"
    },
    {
      "url": "https://github.com/mycompany/api-service",
      "name": "api-service",
      "owner": "mycompany",
      "full_name": "mycompany/api-service",
      "private": true,
      "description": "Backend API service",
      "default_branch": "main"
    }
  ],
  "total_repositories": 2,
  "message": "Retrieved 2 accessible repositories"
}
```

#### Usage Examples

##### Example 1: List All Repositories

```python
result = await client.call_tool("cursor_list_repositories", {})

if result["success"]:
    print(f"Accessible repositories: {result['total_repositories']}")
    
    for repo in result["repositories"]:
        privacy = "??" if repo["private"] else "??"
        print(f"{privacy} {repo['full_name']}")
        print(f"   {repo['url']}")
        if repo.get("description"):
            print(f"   {repo['description']}")
```

##### Example 2: Find Repository by Name

```python
result = await client.call_tool("cursor_list_repositories", {})

if result["success"]:
    search_term = "web-app"
    
    matching_repos = [
        repo for repo in result["repositories"]
        if search_term.lower() in repo["name"].lower()
    ]
    
    if matching_repos:
        repo = matching_repos[0]
        print(f"Found: {repo['full_name']}")
        print(f"URL: {repo['url']}")
        # Use this URL for agent creation
        repository_url = repo["url"]
    else:
        print(f"No repository found matching '{search_term}'")
```

##### Example 3: Filter Repositories

```python
result = await client.call_tool("cursor_list_repositories", {})

if result["success"]:
    # Get only public repositories
    public_repos = [repo for repo in result["repositories"] if not repo["private"]]
    
    # Get only private repositories
    private_repos = [repo for repo in result["repositories"] if repo["private"]]
    
    print(f"Public repos: {len(public_repos)}")
    print(f"Private repos: {len(private_repos)}")
```

##### Example 4: List Repositories via Web API

```javascript
const response = await fetch('http://localhost:8080/api/repositories');
const result = await response.json();

if (result.success) {
    result.repositories.forEach(repo => {
        const icon = repo.private ? '??' : '??';
        console.log(`${icon} ${repo.full_name}`);
        console.log(`   ${repo.url}`);
    });
}
```

---

### cursor_list_repository_branches

Get a list of branches for a specific GitHub repository. Useful for finding the correct branch name or confirming a branch exists.

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `repository_url` | string | ? Yes | GitHub repository URL (e.g., `https://github.com/owner/repo`) |
| `force_refresh` | boolean | ? No | Force refresh the branch list from GitHub API (default: `false`) |

#### Return Value

```json
{
  "success": true,
  "repository": "https://github.com/mycompany/web-app",
  "owner": "mycompany",
  "repo": "web-app",
  "branches": [
    "main",
    "develop",
    "feature/user-auth",
    "feature/dark-mode",
    "bugfix/login-issue",
    "release/v1.2.0"
  ],
  "total_branches": 6,
  "message": "Retrieved 6 branches for mycompany/web-app"
}
```

#### Usage Examples

##### Example 1: List All Branches for a Repository

```python
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": "https://github.com/mycompany/web-app"
})

if result["success"]:
    print(f"Branches for {result['repo']}:")
    for branch in result["branches"]:
        print(f"  ?? {branch}")
else:
    print(f"Error: {result.get('error')}")
    # Fallback branches are still provided
    print(f"Fallback branches: {result.get('branches', [])}")
```

##### Example 2: Check if Branch Exists Before Creating Agent

```python
repository_url = "https://github.com/mycompany/web-app"
desired_branch = "feature/new-feature"

# Get branches
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": repository_url
})

if result["success"]:
    branches = result["branches"]
    
    if desired_branch in branches:
        print(f"? Branch '{desired_branch}' exists")
        # Use this branch for agent
        branch_to_use = desired_branch
    else:
        print(f"??  Branch '{desired_branch}' not found")
        print(f"Available branches: {', '.join(branches)}")
        # Ask user or use default branch
        branch_to_use = "main"
```

##### Example 3: Find Feature Branches

```python
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": "https://github.com/mycompany/web-app"
})

if result["success"]:
    branches = result["branches"]
    
    # Filter feature branches
    feature_branches = [b for b in branches if b.startswith("feature/")]
    bugfix_branches = [b for b in branches if b.startswith("bugfix/")]
    
    print(f"Feature branches: {len(feature_branches)}")
    for branch in feature_branches:
        print(f"  ?? {branch}")
    
    print(f"\nBugfix branches: {len(bugfix_branches)}")
    for branch in bugfix_branches:
        print(f"  ?? {branch}")
```

##### Example 4: Force Refresh Branch List

```python
# Force refresh to get latest branches from GitHub
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": "https://github.com/mycompany/web-app",
    "force_refresh": True  # Bypass cache and fetch fresh data
})

if result["success"]:
    print(f"Refreshed branch list: {result['total_branches']} branches")
    for branch in result["branches"]:
        print(f"  {branch}")
```

##### Example 5: List Branches via Web API

```javascript
const repositoryUrl = encodeURIComponent('https://github.com/mycompany/web-app');
const response = await fetch(`http://localhost:8080/api/branches?repository=${repositoryUrl}`);

const result = await response.json();

if (result.success) {
    console.log(`Branches for ${result.repo}:`);
    result.branches.forEach(branch => {
        console.log(`  ${branch}`);
    });
}
```

---

## Complete Workflow Example

Here's a complete example showing how to use multiple tools together:

```python
import asyncio

async def complete_agent_workflow():
    """Complete workflow: check usage, list repos, create agent, monitor, add follow-up"""
    
    # 1. Check API usage and limits
    usage_result = await client.call_tool("cursor_get_api_usage", {})
    if usage_result["success"]:
        remaining = usage_result["remaining_quota"]["agents"]
        if remaining <= 0:
            print("? No agent quota remaining")
            return
    
    # 2. List available repositories
    repos_result = await client.call_tool("cursor_list_repositories", {})
    if not repos_result["success"]:
        print("? Failed to list repositories")
        return
    
    # Find the target repository
    target_repo = next(
        (r for r in repos_result["repositories"] if "web-app" in r["name"]),
        None
    )
    if not target_repo:
        print("? Repository not found")
        return
    
    # 3. Get branches for the repository
    branches_result = await client.call_tool("cursor_list_repository_branches", {
        "repository_url": target_repo["url"]
    })
    
    # 4. Create agent
    create_result = await client.call_tool("cursor_create_background_agent", {
        "repository_url": target_repo["url"],
        "prompt": "Add user authentication with JWT tokens",
        "branch": "feature/auth-system",
        "model": "claude-3-5-sonnet",
        "max_iterations": 15
    })
    
    if not create_result["success"]:
        print(f"? Failed to create agent: {create_result.get('error')}")
        return
    
    agent_id = create_result["agent_id"]
    print(f"? Agent created: {agent_id}")
    
    # 5. Monitor agent progress
    for _ in range(10):  # Check 10 times
        await asyncio.sleep(30)  # Wait 30 seconds between checks
        
        status_result = await client.call_tool("cursor_get_agent_status", {
            "agent_id": agent_id
        })
        
        if status_result["success"]:
            status = status_result["status"]
            progress = status_result.get("progress", {})
            
            print(f"[{status}] {progress.get('completion_percentage', 0)}% - "
                  f"{progress.get('current_step', 'N/A')}")
            
            if status in ["completed", "failed", "stopped"]:
                break
    
    # 6. Add follow-up instruction if still running
    status_result = await client.call_tool("cursor_get_agent_status", {
        "agent_id": agent_id
    })
    
    if status_result["success"] and status_result["status"] == "running":
        followup_result = await client.call_tool("cursor_add_followup_instruction", {
            "agent_id": agent_id,
            "instruction": "Please also add two-factor authentication support"
        })
        print(f"? Follow-up added: {followup_result['success']}")
    
    # 7. List all agents to see final state
    list_result = await client.call_tool("cursor_list_background_agents", {})
    if list_result["success"]:
        print(f"\n?? Total agents: {list_result['total_agents']}")

# Run the workflow
asyncio.run(complete_agent_workflow())
```

---

## Error Handling

All tools return a `success` field indicating whether the operation succeeded. Always check this field before processing results:

```python
result = await client.call_tool("cursor_create_background_agent", {...})

if result["success"]:
    # Process successful result
    agent_id = result["agent_id"]
else:
    # Handle error
    error_message = result.get("error", "Unknown error")
    print(f"Error: {error_message}")
```

### Common Error Scenarios

1. **Authentication Errors**: Check your `CURSOR_API_KEY` environment variable
2. **Repository Access**: Ensure you have access to the repository
3. **Invalid Branch**: Verify the branch exists using `cursor_list_repository_branches`
4. **Quota Exceeded**: Check usage with `cursor_get_api_usage` before creating agents
5. **Agent Not Found**: Verify the agent ID is correct when checking status

---

## Best Practices Summary

1. **Always check `success` field** in tool responses
2. **Use appropriate models** for task complexity
3. **Monitor agent progress** regularly with `cursor_get_agent_status`
4. **Provide detailed prompts** when creating agents
5. **Check API usage** before creating multiple agents
6. **Verify repository access** and branch names before agent creation
7. **Use follow-up instructions** to guide running agents
8. **Filter agent lists** to find specific agents efficiently
9. **Handle errors gracefully** with appropriate error messages
10. **Cache repository and branch lists** when possible to reduce API calls

---

For more information, see the [README.md](README.md) file or the [Cursor Background Agents API documentation](https://docs.cursor.com/en/background-agent/api/overview).
