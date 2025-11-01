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

##### Basic Example

```python
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/web-app",
    "prompt": "Implement user authentication with JWT tokens, including login, registration, and password reset functionality",
    "branch": "feature/auth-system",
    "model": "claude-3-5-sonnet",
    "max_iterations": 20
})

if result.get("success"):
    agent_id = result["agent_id"]
    print(f"? Agent created: {agent_id}")
    print(f"?? Repository: {result['repository_url']}")
    print(f"?? Branch: {result['branch']}")
else:
    print(f"? Failed: {result.get('error')}")
```

##### Feature Implementation Example

```python
# Creating an agent for a new feature
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/company/ecommerce-platform",
    "prompt": """
    Implement a shopping cart feature with the following requirements:
    
    1. Add/remove items from cart
    2. Update item quantities
    3. Calculate total price with tax and shipping
    4. Persist cart to local storage
    5. Display cart summary in header
    6. Create checkout flow
    
    Technical Requirements:
    - Use React hooks for state management
    - Follow existing component patterns in src/components/
    - Add TypeScript types for cart items
    - Implement cart persistence using localStorage
    - Add unit tests for cart utilities
    - Ensure responsive design
    
    Acceptance Criteria:
    - [ ] Cart persists across page refreshes
    - [ ] Cart updates in real-time across tabs
    - [ ] All prices display in USD format
    - [ ] Tax calculation matches business rules
    - [ ] Mobile-responsive cart dropdown
    """,
    "branch": "feature/shopping-cart",
    "model": "claude-3-5-sonnet",
    "max_iterations": 25
})
```

##### Bug Fix Example

```python
# Creating an agent to fix a specific bug
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/company/api-server",
    "prompt": """
    Fix the user authentication bug where sessions expire prematurely.
    
    Issue Description:
    Users are being logged out after 15 minutes instead of the configured 2 hours.
    
    Investigation Required:
    1. Check JWT token expiration logic in auth/middleware.js
    2. Review session storage implementation in auth/session.js
    3. Verify refresh token logic
    4. Check for timezone or clock synchronization issues
    
    Expected Behavior:
    - Sessions should last 2 hours (120 minutes)
    - Refresh tokens should extend session automatically
    - Logout should only happen on explicit logout or after 2 hours of inactivity
    
    Requirements:
    - Fix the expiration logic
    - Add logging for debugging
    - Add unit tests for session expiration
    - Update API documentation
    """,
    "branch": "bugfix/session-expiration",
    "model": "claude-3-5-sonnet",
    "max_iterations": 15
})
```

##### Simple Task Example (Using Fast Model)

```python
# Quick task using the faster haiku model
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/company/docs-site",
    "prompt": "Add API documentation for the /api/users endpoint including request/response examples",
    "branch": "docs/api-endpoints",
    "model": "claude-3-haiku",  # Fast model for simple task
    "max_iterations": 5  # Simple task needs fewer iterations
})
```

##### Complex Refactoring Example

```python
# Large refactoring task with maximum iterations
result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/company/legacy-app",
    "prompt": """
    Refactor the authentication module to use a modern architecture:
    
    Current State:
    - Monolithic auth.js file (2000+ lines)
    - Mixed responsibilities (auth, validation, session management)
    - No dependency injection
    - Tightly coupled to database
    
    Target Architecture:
    1. Separate concerns into modules:
       - auth/strategies/ (local, OAuth, SSO)
       - auth/middleware/ (auth, roles, permissions)
       - auth/services/ (token, session, password)
       - auth/validators/ (input validation)
    
    2. Implement dependency injection pattern
    3. Add interface abstractions for database layer
    4. Create unit tests with >80% coverage
    5. Maintain backward compatibility with existing API
    
    Migration Strategy:
    - Keep old endpoints working during transition
    - Add feature flag to switch between old/new implementation
    - Update API documentation
    - Create migration guide for other developers
    """,
    "branch": "refactor/auth-module",
    "model": "claude-3-5-sonnet",
    "max_iterations": 40  # Complex task needs more iterations
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

##### List All Agents

```python
# List all agents
result = await client.call_tool("cursor_list_background_agents", {})

if result.get("success"):
    agents = result["agents"]
    print(f"Total agents: {result['total_agents']}")
    
    for agent in agents:
        status_icon = {
            "running": "??",
            "completed": "?",
            "failed": "?",
            "stopped": "??"
        }.get(agent["status"], "?")
        
        print(f"{status_icon} {agent['agent_id']}: {agent['status']}")
        print(f"   ?? {agent['repository_url']}")
        print(f"   ?? {agent.get('branch', 'N/A')}")
```

##### Filter by Status

```python
# List only running agents
result = await client.call_tool("cursor_list_background_agents", {
    "status_filter": "running"
})

if result.get("success"):
    running_agents = result["agents"]
    print(f"Active agents: {len(running_agents)}")
    
    for agent in running_agents:
        print(f"?? {agent['agent_id']} - {agent.get('prompt', '')[:50]}...")
```

##### Filter by Repository

```python
# List agents for a specific repository
result = await client.call_tool("cursor_list_background_agents", {
    "repository_filter": "https://github.com/mycompany/web-app"
})

if result.get("success"):
    repo_agents = result["agents"]
    print(f"Agents for web-app: {len(repo_agents)}")
    
    # Group by status
    by_status = {}
    for agent in repo_agents:
        status = agent["status"]
        by_status[status] = by_status.get(status, 0) + 1
    
    print("Status breakdown:")
    for status, count in by_status.items():
        print(f"  {status}: {count}")
```

##### Pagination Example

```python
# List agents with pagination
cursor = None
all_agents = []

while True:
    params = {"limit": 20}
    if cursor:
        params["cursor"] = cursor
    
    result = await client.call_tool("cursor_list_background_agents", params)
    
    if not result.get("success"):
        break
    
    agents = result.get("agents", [])
    all_agents.extend(agents)
    
    # Check if there are more pages
    if len(agents) < 20 or "next_cursor" not in result:
        break
    
    cursor = result["next_cursor"]

print(f"Retrieved {len(all_agents)} total agents")
```

##### Monitor Multiple Agents

```python
async def monitor_active_agents():
    """Monitor all active agents and display their progress"""
    result = await client.call_tool("cursor_list_background_agents", {
        "status_filter": "running"
    })
    
    if not result.get("success"):
        return
    
    for agent in result["agents"]:
        agent_id = agent["agent_id"]
        
        # Get detailed status
        status_result = await client.call_tool("cursor_get_agent_status", {
            "agent_id": agent_id
        })
        
        if status_result.get("success"):
            progress = status_result.get("progress", {})
            print(f"\n?? Agent: {agent_id}")
            print(f"   Status: {status_result['status']}")
            print(f"   Progress: {progress.get('completion_percentage', 0)}%")
            print(f"   Current: {progress.get('current_step', 'N/A')}")
            print(f"   Files: {len(progress.get('files_modified', []))}")

await monitor_active_agents()
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

##### Basic Status Check

```python
result = await client.call_tool("cursor_get_agent_status", {
    "agent_id": "agent-1234567890"
})

if result.get("success"):
    print(f"Status: {result['status']}")
    print(f"Progress: {result['progress']['completion_percentage']}%")
    print(f"Current Step: {result['progress']['current_step']}")
```

##### Detailed Progress Monitoring

```python
async def monitor_agent_progress(agent_id: str):
    """Monitor agent with detailed progress information"""
    result = await client.call_tool("cursor_get_agent_status", {
        "agent_id": agent_id
    })
    
    if not result.get("success"):
        print(f"? Failed to get status: {result.get('error')}")
        return
    
    status = result["status"]
    progress = result.get("progress", {})
    
    print(f"\n{'='*60}")
    print(f"Agent ID: {agent_id}")
    print(f"Status: {status}")
    print(f"{'='*60}")
    
    if progress:
        print(f"\n?? Progress: {progress.get('completion_percentage', 0)}%")
        print(f"?? Current Step: {progress.get('current_step', 'N/A')}")
        print(f"? Completed: {progress.get('completed_steps', 0)}/{progress.get('total_estimated_steps', 0)} steps")
        print(f"?? Files Modified: {len(progress.get('files_modified', []))}")
        print(f"?? Commits Made: {progress.get('commits_made', 0)}")
        
        if progress.get('files_modified'):
            print(f"\n?? Modified Files:")
            for file in progress['files_modified']:
                print(f"   ? {file}")
    
    # Show recent logs
    logs = result.get("logs", [])
    if logs:
        print(f"\n?? Recent Activity:")
        for log in logs[-5:]:  # Show last 5 log entries
            print(f"   ? {log}")
    
    # Show timestamps
    print(f"\n? Created: {result.get('created_at', 'N/A')}")
    print(f"? Updated: {result.get('updated_at', 'N/A')}")

await monitor_agent_progress("agent-1234567890")
```

##### Continuous Monitoring Loop

```python
import asyncio
import json

async def continuously_monitor_agent(agent_id: str, check_interval: int = 30):
    """Continuously monitor an agent until completion"""
    print(f"?? Starting continuous monitoring for agent: {agent_id}")
    print(f"??  Check interval: {check_interval} seconds\n")
    
    while True:
        result = await client.call_tool("cursor_get_agent_status", {
            "agent_id": agent_id
        })
        
        if not result.get("success"):
            print(f"? Error: {result.get('error')}")
            break
        
        status = result["status"]
        progress = result.get("progress", {})
        percentage = progress.get("completion_percentage", 0)
        current_step = progress.get("current_step", "N/A")
        
        # Clear line and update progress
        print(f"\r?? Status: {status} | Progress: {percentage}% | {current_step[:50]}", end="", flush=True)
        
        # Check if agent is done
        if status in ["completed", "failed", "stopped"]:
            print(f"\n\n{'?' if status == 'completed' else '?'} Agent finished with status: {status}")
            break
        
        # Wait before next check
        await asyncio.sleep(check_interval)
    
    # Final status report
    final_result = await client.call_tool("cursor_get_agent_status", {
        "agent_id": agent_id
    })
    
    if final_result.get("success"):
        print(json.dumps(final_result, indent=2))

# Monitor an agent every 30 seconds
asyncio.run(continuously_monitor_agent("agent-1234567890", check_interval=30))
```

##### Status with Error Handling

```python
async def safe_get_agent_status(agent_id: str):
    """Get agent status with comprehensive error handling"""
    try:
        result = await client.call_tool("cursor_get_agent_status", {
            "agent_id": agent_id
        })
        
        data = json.loads(result.content[0].text) if hasattr(result, 'content') else result
        
        if not data.get("success"):
            error = data.get("error", "Unknown error")
            
            if "not found" in error.lower():
                print(f"? Agent {agent_id} not found")
                return None
            elif "authentication" in error.lower():
                print(f"? Authentication error. Check your API key")
                return None
            else:
                print(f"? Error: {error}")
                return None
        
        return data
        
    except Exception as e:
        print(f"? Exception occurred: {e}")
        return None

status = await safe_get_agent_status("agent-1234567890")
if status:
    print(f"? Agent status retrieved successfully")
    print(f"   Status: {status['status']}")
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

##### Basic Stop

```python
result = await client.call_tool("cursor_stop_background_agent", {
    "agent_id": "agent-1234567890"
})

if result.get("success"):
    print(f"? Agent {result['agent_id']} stopped successfully")
else:
    print(f"? Failed to stop agent: {result.get('error')}")
```

##### Stop with Verification

```python
async def stop_agent_safely(agent_id: str):
    """Stop an agent and verify it was stopped"""
    # First, check current status
    status_result = await client.call_tool("cursor_get_agent_status", {
        "agent_id": agent_id
    })
    
    if not status_result.get("success"):
        print(f"? Cannot get agent status: {status_result.get('error')}")
        return False
    
    current_status = status_result["status"]
    
    if current_status in ["completed", "failed", "stopped"]:
        print(f"??  Agent is already {current_status}")
        return True
    
    print(f"?? Stopping agent (current status: {current_status})...")
    
    # Stop the agent
    stop_result = await client.call_tool("cursor_stop_background_agent", {
        "agent_id": agent_id
    })
    
    if not stop_result.get("success"):
        print(f"? Failed to stop agent: {stop_result.get('error')}")
        return False
    
    # Verify it was stopped
    await asyncio.sleep(2)  # Wait a moment for status update
    
    verify_result = await client.call_tool("cursor_get_agent_status", {
        "agent_id": agent_id
    })
    
    if verify_result.get("status") == "stopped":
        print(f"? Agent stopped and verified")
        return True
    else:
        print(f"??  Agent status is {verify_result.get('status')}, may still be stopping")
        return False

await stop_agent_safely("agent-1234567890")
```

##### Stop Multiple Agents

```python
async def stop_all_running_agents():
    """Stop all currently running agents"""
    # Get all running agents
    list_result = await client.call_tool("cursor_list_background_agents", {
        "status_filter": "running"
    })
    
    if not list_result.get("success"):
        print(f"? Failed to list agents: {list_result.get('error')}")
        return
    
    running_agents = list_result.get("agents", [])
    
    if not running_agents:
        print("??  No running agents found")
        return
    
    print(f"?? Stopping {len(running_agents)} running agents...")
    
    stopped_count = 0
    for agent in running_agents:
        agent_id = agent["agent_id"]
        print(f"   Stopping {agent_id}...")
        
        stop_result = await client.call_tool("cursor_stop_background_agent", {
            "agent_id": agent_id
        })
        
        if stop_result.get("success"):
            stopped_count += 1
            print(f"   ? {agent_id} stopped")
        else:
            print(f"   ? Failed to stop {agent_id}: {stop_result.get('error')}")
    
    print(f"\n? Stopped {stopped_count}/{len(running_agents)} agents")

await stop_all_running_agents()
```

##### Stop Agents by Repository

```python
async def stop_agents_for_repository(repo_url: str):
    """Stop all agents working on a specific repository"""
    # Get agents for this repository
    list_result = await client.call_tool("cursor_list_background_agents", {
        "repository_filter": repo_url
    })
    
    if not list_result.get("success"):
        print(f"? Failed to list agents: {list_result.get('error')}")
        return
    
    agents = list_result.get("agents", [])
    running_agents = [a for a in agents if a["status"] == "running"]
    
    if not running_agents:
        print(f"??  No running agents found for {repo_url}")
        return
    
    print(f"?? Stopping {len(running_agents)} agents for repository...")
    
    for agent in running_agents:
        await client.call_tool("cursor_stop_background_agent", {
            "agent_id": agent["agent_id"]
        })
    
    print(f"? All agents stopped for {repo_url}")

await stop_agents_for_repository("https://github.com/mycompany/web-app")
```

#### When to Stop an Agent

- The task requirements have changed significantly
- The agent is going in the wrong direction
- You need to free up resources
- The agent is stuck in an error loop
- You need to modify the prompt and restart with new instructions

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

##### Basic Follow-up

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

if result.get("success"):
    print(f"? Follow-up instruction added to agent {result['agent_id']}")
else:
    print(f"? Failed: {result.get('error')}")
```

##### Corrective Follow-up

```python
# Agent is going in wrong direction - provide correction
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-1234567890",
    "instruction": """
    Please correct the following:
    
    1. The API endpoint should be '/api/v2/users' not '/api/users'
       - Update src/routes/api.js
       - Update frontend API calls in src/services/api.js
    
    2. Use TypeScript instead of JavaScript for new components
       - Follow the pattern in src/components/AuthForm.tsx
    
    3. Password validation should require:
       - Minimum 12 characters
       - At least one uppercase letter
       - At least one number
       - At least one special character
    
    Please update the implementation accordingly.
    """
})
```

##### Additional Requirements Follow-up

```python
# Adding requirements while agent is working
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-1234567890",
    "instruction": """
    Please also implement:
    
    1. Email verification flow:
       - Send verification email on registration
       - Add verification endpoint
       - Prevent login until email is verified
    
    2. Account lockout after 5 failed login attempts:
       - Lock account for 15 minutes
       - Log security events
       - Send notification email
    
    3. Password strength indicator:
       - Real-time feedback in registration form
       - Visual indicator (weak/medium/strong)
       - Use the same validation rules as password reset
    
    Reference the existing email service in src/services/email.js
    """
})
```

##### Architecture Guidance Follow-up

```python
# Providing architectural guidance
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-1234567890",
    "instruction": """
    Please refactor to follow microservices pattern:
    
    1. Separate authentication into its own service
       - Create auth-service directory
       - Move all auth-related code there
       - Keep API gateway pattern in mind
    
    2. Use dependency injection:
       - Create interfaces for database and email services
       - Inject dependencies through constructor
       - Follow the pattern in src/core/di.ts
    
    3. Add proper error handling:
       - Create custom error classes
       - Use error middleware pattern from src/middleware/error.ts
       - Return consistent error format
    
    4. Update API documentation to reflect new structure
    """
})
```

##### Code Style Follow-up

```python
# Ensuring code follows style guidelines
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-1234567890",
    "instruction": """
    Please ensure code follows our style guidelines:
    
    - Use ESLint configuration from .eslintrc.json
    - Follow Prettier formatting (check .prettierrc)
    - Use TypeScript strict mode
    - Add JSDoc comments to all exported functions
    - Use async/await instead of promises
    - Follow naming conventions: camelCase for variables, PascalCase for classes
    - Maximum line length: 100 characters
    
    Run 'npm run lint' and fix any issues before committing.
    """
})
```

##### Context-Specific Follow-up

```python
# Providing context about existing codebase
result = await client.call_tool("cursor_add_followup_instruction", {
    "agent_id": "agent-1234567890",
    "instruction": """
    Please note these important details:
    
    1. Database schema: Check migrations in db/migrations/ for the exact user table structure
       - Column names are snake_case, not camelCase
       - Use the ORM models from src/models/User.ts
    
    2. Authentication pattern: Follow the JWT implementation in src/auth/jwt.ts
       - Use the same secret key from environment variable
       - Token expiration is handled in middleware
    
    3. Error handling: Use the ErrorHandler utility from src/utils/ErrorHandler.ts
       - It automatically formats errors for API responses
       - Includes proper HTTP status codes
    
    4. Testing: Add tests following the pattern in tests/auth.test.ts
       - Use Jest and Supertest
       - Mock external dependencies
    """
})
```

##### Sequential Follow-ups

```python
async def send_multiple_followups(agent_id: str):
    """Send multiple follow-up instructions in sequence"""
    
    followups = [
        "Please use React hooks (useState, useEffect) instead of class components",
        "Add loading states for all async operations",
        "Implement error boundaries for better error handling",
        "Add unit tests with >80% code coverage"
    ]
    
    for i, instruction in enumerate(followups, 1):
        print(f"Sending follow-up {i}/{len(followups)}...")
        
        result = await client.call_tool("cursor_add_followup_instruction", {
            "agent_id": agent_id,
            "instruction": instruction
        })
        
        if result.get("success"):
            print(f"? Follow-up {i} added")
            await asyncio.sleep(2)  # Small delay between follow-ups
        else:
            print(f"? Failed to add follow-up {i}: {result.get('error')}")
            break

await send_multiple_followups("agent-1234567890")
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

##### Basic Usage Check

```python
result = await client.call_tool("cursor_get_api_usage", {})

if result.get("success"):
    usage = result["usage"]
    limits = result["limits"]
    
    print(f"Active Agents: {usage['active_agents']}/{limits['max_active_agents']}")
    print(f"Monthly Usage: {usage['agents_created_this_month']}/{limits['monthly_agent_limit']}")
    print(f"Remaining: {result['remaining_quota']['agents']} agents this month")
```

##### Detailed Usage Report

```python
async def print_detailed_usage_report():
    """Print a comprehensive usage report"""
    result = await client.call_tool("cursor_get_api_usage", {})
    
    if not result.get("success"):
        print(f"? Failed to get usage: {result.get('error')}")
        return
    
    usage = result["usage"]
    limits = result["limits"]
    quota = result["remaining_quota"]
    billing = result.get("billing_period", {})
    
    print("=" * 60)
    print("?? API USAGE REPORT")
    print("=" * 60)
    
    # Agent Usage
    print(f"\n?? Agents:")
    print(f"   Active: {usage['active_agents']}/{limits['max_active_agents']}")
    print(f"   Created This Month: {usage['agents_created_this_month']}/{limits['monthly_agent_limit']}")
    print(f"   Remaining: {quota.get('agents', 0)}")
    
    # API Calls
    print(f"\n?? API Calls:")
    print(f"   Today: {usage['api_calls_today']}/{limits['daily_api_calls']}")
    print(f"   Remaining: {quota.get('api_calls', 0)}")
    print(f"   Rate Limit: {limits['rate_limit_per_minute']}/minute")
    
    # Token Usage
    if usage.get('tokens_used_today'):
        print(f"\n?? Tokens:")
        print(f"   Used Today: {usage['tokens_used_today']:,}")
    
    # Billing Period
    if billing:
        print(f"\n?? Billing Period:")
        print(f"   Start: {billing.get('start_date', 'N/A')}")
        print(f"   End: {billing.get('end_date', 'N/A')}")
        print(f"   Days Remaining: {billing.get('days_remaining', 'N/A')}")
    
    # Usage Warnings
    print(f"\n??  Warnings:")
    agent_percent = (usage['active_agents'] / limits['max_active_agents']) * 100
    if agent_percent > 80:
        print(f"   ??  Active agents at {agent_percent:.1f}% of limit!")
    
    monthly_percent = (usage['agents_created_this_month'] / limits['monthly_agent_limit']) * 100
    if monthly_percent > 80:
        print(f"   ??  Monthly usage at {monthly_percent:.1f}% of limit!")
    
    daily_percent = (usage['api_calls_today'] / limits['daily_api_calls']) * 100
    if daily_percent > 80:
        print(f"   ??  Daily API calls at {daily_percent:.1f}% of limit!")
    
    if agent_percent < 80 and monthly_percent < 80 and daily_percent < 80:
        print(f"   ? All usage within safe limits")

await print_detailed_usage_report()
```

##### Usage Monitoring Function

```python
async def check_usage_before_creating_agent():
    """Check if we have enough quota before creating a new agent"""
    result = await client.call_tool("cursor_get_api_usage", {})
    
    if not result.get("success"):
        print("??  Could not check usage, proceeding anyway...")
        return True
    
    usage = result["usage"]
    limits = result["limits"]
    quota = result["remaining_quota"]
    
    # Check active agents limit
    if usage['active_agents'] >= limits['max_active_agents']:
        print(f"? Cannot create agent: Active agents limit reached ({usage['active_agents']}/{limits['max_active_agents']})")
        print(f"   Please stop some agents or wait for others to complete")
        return False
    
    # Check monthly limit
    if usage['agents_created_this_month'] >= limits['monthly_agent_limit']:
        print(f"? Cannot create agent: Monthly limit reached ({usage['agents_created_this_month']}/{limits['monthly_agent_limit']})")
        return False
    
    # Check daily API calls
    if usage['api_calls_today'] >= limits['daily_api_calls']:
        print(f"??  Daily API call limit reached. Agent creation may be rate limited")
        return False
    
    print(f"? Quota available:")
    print(f"   Active agents: {usage['active_agents']}/{limits['max_active_agents']}")
    print(f"   Monthly: {usage['agents_created_this_month']}/{limits['monthly_agent_limit']} ({quota.get('agents', 0)} remaining)")
    return True

# Use before creating agent
if await check_usage_before_creating_agent():
    # Safe to create agent
    await client.call_tool("cursor_create_background_agent", {...})
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

##### Basic Repository List

```python
result = await client.call_tool("cursor_list_repositories", {})

if result.get("success"):
    print(f"Found {result['total_repositories']} repositories:")
    for repo in result["repositories"]:
        print(f"  - {repo['url']}: {repo.get('description', 'No description')}")
```

##### Filter and Search Repositories

```python
async def find_repository_by_name(search_term: str):
    """Find repositories matching a search term"""
    result = await client.call_tool("cursor_list_repositories", {})
    
    if not result.get("success"):
        print(f"? Failed to list repositories: {result.get('error')}")
        return None
    
    repositories = result.get("repositories", [])
    
    # Search in name, description, or URL
    matches = []
    search_lower = search_term.lower()
    
    for repo in repositories:
        name = repo.get("name", "").lower()
        description = repo.get("description", "").lower()
        url = repo.get("url", "").lower()
        
        if search_lower in name or search_lower in description or search_lower in url:
            matches.append(repo)
    
    return matches

# Find repositories
matches = await find_repository_by_name("web-app")
if matches:
    print(f"Found {len(matches)} matching repositories:")
    for repo in matches:
        print(f"  ? {repo['url']}")
```

##### Repository Selection Menu

```python
async def select_repository_interactive():
    """Display repositories in a selectable format"""
    result = await client.call_tool("cursor_list_repositories", {})
    
    if not result.get("success"):
        print(f"? Failed to list repositories")
        return None
    
    repositories = result.get("repositories", [])
    
    if not repositories:
        print("??  No repositories found")
        return None
    
    print(f"\n?? Available Repositories ({len(repositories)}):")
    print("=" * 60)
    
    for i, repo in enumerate(repositories, 1):
        name = repo.get("name", "Unknown")
        owner = repo.get("owner", "Unknown")
        private = "??" if repo.get("private", False) else "??"
        description = repo.get("description", "No description")
        
        print(f"\n{i}. {private} {owner}/{name}")
        print(f"   URL: {repo.get('url', 'N/A')}")
        print(f"   Description: {description[:60]}...")
    
    # In a real interactive app, you'd prompt for selection
    # For this example, return the first one
    return repositories[0] if repositories else None

selected_repo = await select_repository_interactive()
if selected_repo:
    print(f"\n? Selected: {selected_repo['url']}")
```

##### Repository Statistics

```python
async def repository_statistics():
    """Display statistics about accessible repositories"""
    result = await client.call_tool("cursor_list_repositories", {})
    
    if not result.get("success"):
        print(f"? Failed to get repositories")
        return
    
    repositories = result.get("repositories", [])
    
    if not repositories:
        print("??  No repositories found")
        return
    
    # Calculate statistics
    total = len(repositories)
    private_count = sum(1 for r in repositories if r.get("private", False))
    public_count = total - private_count
    
    # Group by owner
    by_owner = {}
    for repo in repositories:
        owner = repo.get("owner", "unknown")
        by_owner[owner] = by_owner.get(owner, 0) + 1
    
    print("=" * 60)
    print("?? REPOSITORY STATISTICS")
    print("=" * 60)
    print(f"\nTotal Repositories: {total}")
    print(f"   ?? Public: {public_count}")
    print(f"   ?? Private: {private_count}")
    
    print(f"\n?? By Owner:")
    for owner, count in sorted(by_owner.items(), key=lambda x: x[1], reverse=True):
        print(f"   ? {owner}: {count} repositories")

await repository_statistics()
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

##### Basic Branch List

```python
result = await client.call_tool("cursor_list_repository_branches", {
    "repository_url": "https://github.com/mycompany/web-app",
    "force_refresh": False
})

if result.get("success"):
    print(f"Branches for {result['repository']}:")
    for branch in result["branches"]:
        print(f"  - {branch}")
else:
    print(f"??  {result.get('message', 'Failed to get branches')}")
    # Fallback branches are still available
    print(f"Using fallback branches: {result.get('branches', [])}")
```

##### Select Branch for Agent

```python
async def select_or_create_branch(repo_url: str, desired_branch: str):
    """Select existing branch or use default if branch doesn't exist"""
    # Get all branches
    result = await client.call_tool("cursor_list_repository_branches", {
        "repository_url": repo_url,
        "force_refresh": True  # Get latest branches
    })
    
    if not result.get("success"):
        print(f"??  Could not fetch branches: {result.get('error')}")
        return "main"  # Default fallback
    
    branches = result.get("branches", [])
    
    # Check if desired branch exists
    if desired_branch in branches:
        print(f"? Branch '{desired_branch}' exists")
        return desired_branch
    
    # Branch doesn't exist - agent will create it
    print(f"??  Branch '{desired_branch}' doesn't exist yet")
    print(f"   Agent will create it automatically")
    
    # Show available branches for reference
    print(f"\nAvailable branches:")
    for branch in branches[:10]:  # Show first 10
        print(f"   ? {branch}")
    
    return desired_branch  # Return desired branch name

# Use in agent creation
branch = await select_or_create_branch(
    "https://github.com/mycompany/web-app",
    "feature/new-authentication"
)

result = await client.call_tool("cursor_create_background_agent", {
    "repository_url": "https://github.com/mycompany/web-app",
    "branch": branch,
    "prompt": "..."
})
```

##### Validate Repository Access

```python
async def validate_repository_access(repo_url: str):
    """Check if we can access a repository by fetching its branches"""
    result = await client.call_tool("cursor_list_repository_branches", {
        "repository_url": repo_url,
        "force_refresh": True
    })
    
    if not result.get("success"):
        error = result.get("error", "")
        
        if "not found" in error.lower() or "404" in error:
            print(f"? Repository not found: {repo_url}")
            print(f"   Check the URL or repository access permissions")
            return False
        elif "authentication" in error.lower() or "401" in error:
            print(f"? Authentication required for private repository")
            print(f"   Set GITHUB_TOKEN environment variable")
            return False
        else:
            print(f"??  Warning: {error}")
            print(f"   Using fallback branches: {result.get('branches', [])}")
            return True  # Still usable with fallback
    
    branches = result.get("branches", [])
    print(f"? Repository accessible")
    print(f"   Found {len(branches)} branches")
    
    # Check for common branches
    common_branches = ["main", "master", "develop"]
    found_common = [b for b in common_branches if b in branches]
    
    if found_common:
        print(f"   Default branches available: {', '.join(found_common)}")
    else:
        print(f"   ??  No common default branches found")
        print(f"   Available branches: {', '.join(branches[:5])}")
    
    return True

# Validate before creating agent
if await validate_repository_access("https://github.com/mycompany/web-app"):
    # Safe to create agent
    await client.call_tool("cursor_create_background_agent", {...})
```

##### Branch Information Display

```python
async def display_branch_information(repo_url: str):
    """Display detailed branch information"""
    result = await client.call_tool("cursor_list_repository_branches", {
        "repository_url": repo_url,
        "force_refresh": False
    })
    
    if not result.get("success"):
        print(f"? Error: {result.get('error')}")
        return
    
    owner = result.get("owner", "unknown")
    repo = result.get("repo", "unknown")
    branches = result.get("branches", [])
    
    print(f"\n?? Repository: {owner}/{repo}")
    print(f"?? URL: {repo_url}")
    print(f"?? Total Branches: {len(branches)}")
    print(f"\nBranch List:")
    
    # Categorize branches
    main_branches = [b for b in branches if b in ["main", "master"]]
    develop_branches = [b for b in branches if "develop" in b.lower() or "dev" in b.lower()]
    feature_branches = [b for b in branches if "feature" in b.lower()]
    release_branches = [b for b in branches if "release" in b.lower() or "rel" in b.lower()]
    other_branches = [b for b in branches if b not in main_branches + develop_branches + feature_branches + release_branches]
    
    if main_branches:
        print(f"\n   ?? Main Branches:")
        for branch in main_branches:
            print(f"      ? {branch}")
    
    if develop_branches:
        print(f"\n   ?? Development Branches:")
        for branch in develop_branches[:5]:  # Limit to 5
            print(f"      ? {branch}")
    
    if feature_branches:
        print(f"\n   ? Feature Branches ({len(feature_branches)}):")
        for branch in feature_branches[:10]:  # Show first 10
            print(f"      ? {branch}")
    
    if release_branches:
        print(f"\n   ?? Release Branches:")
        for branch in release_branches[:5]:
            print(f"      ? {branch}")
    
    if other_branches:
        print(f"\n   ?? Other Branches:")
        for branch in other_branches[:5]:
            print(f"      ? {branch}")

await display_branch_information("https://github.com/mycompany/web-app")
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
