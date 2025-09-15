#!/usr/bin/env python3
"""
Example client for Cursor Background Agent MCP Server

This demonstrates how to interact with the Cursor MCP server to create
and manage autonomous coding agents.
"""

import os
import json
import asyncio
from typing import Dict, Any

# For a real implementation, you would use the MCP client
# from mcp.client.session import ClientSession
# from mcp.client.stdio import stdio_client

class MockMCPClient:
    """Mock MCP client for demonstration purposes"""
    
    def __init__(self, server_command: list):
        self.server_command = server_command
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Mock tool call - in real implementation this would use MCP protocol"""
        print(f"🔧 Calling tool: {name}")
        print(f"📋 Arguments: {json.dumps(arguments, indent=2)}")
        
        # Mock responses based on tool name
        if name == "cursor_create_background_agent":
            return {
                "success": True,
                "agent_id": f"agent-{int(asyncio.get_event_loop().time())}",
                "status": "starting",
                "repository_url": arguments["repository_url"],
                "branch": arguments.get("branch", "main"),
                "model": arguments.get("model", "claude-3-5-sonnet"),
                "created_at": "2025-01-15T10:30:00Z",
                "message": f"Background agent created successfully. Agent will work autonomously on '{arguments['prompt'][:50]}...'"
            }
        
        elif name == "cursor_get_agent_status":
            return {
                "success": True,
                "agent_id": arguments["agent_id"],
                "status": "running",
                "progress": {
                    "current_step": "Implementing authentication middleware",
                    "completed_steps": 3,
                    "total_estimated_steps": 8,
                    "files_modified": ["src/auth/middleware.js", "src/routes/auth.js"],
                    "commits_made": 2,
                    "completion_percentage": 37.5
                },
                "repository_url": "https://github.com/company/repo",
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
        
        elif name == "cursor_list_background_agents":
            return {
                "success": True,
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
                ]
            }
        
        elif name == "cursor_get_api_usage":
            return {
                "success": True,
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
                }
            }
        
        else:
            return {
                "success": False,
                "error": f"Unknown tool: {name}"
            }
    
    async def read_resource(self, uri: str) -> str:
        """Mock resource read"""
        print(f"📖 Reading resource: {uri}")
        
        if uri == "mcp://cursor-agent/agents-summary":
            summary = {
                "total_agents": 3,
                "agents_by_status": {
                    "completed": 1,
                    "running": 1,
                    "failed": 1
                },
                "agents": [
                    {"agent_id": "agent-001", "status": "completed"},
                    {"agent_id": "agent-002", "status": "running"},
                    {"agent_id": "agent-003", "status": "failed"}
                ]
            }
            return json.dumps(summary, indent=2)
        
        return json.dumps({"error": f"Unknown resource: {uri}"}, indent=2)

async def demonstrate_cursor_mcp():
    """Demonstrate the Cursor MCP server capabilities"""
    
    print("🚀 Cursor Background Agent MCP Server Demonstration")
    print("=" * 60)
    
    # Create mock client (in real usage, this would connect to the MCP server)
    client = MockMCPClient(["python3", "cursor_agent_mcp_server.py"])
    
    print("\n1️⃣ Creating a Background Agent for Feature Development")
    print("-" * 50)
    
    # Create an agent for implementing authentication
    create_result = await client.call_tool("cursor_create_background_agent", {
        "repository_url": "https://github.com/mycompany/web-app",
        "prompt": """
        Implement comprehensive user authentication system:
        
        Features needed:
        - User registration with email verification
        - Login with email/password
        - Password reset functionality
        - JWT token-based sessions
        - Protected route middleware
        - User profile management
        
        Technical requirements:
        - Use bcrypt for password hashing
        - Implement proper error handling
        - Add input validation
        - Create responsive forms
        - Follow existing code patterns
        - Add comprehensive tests
        
        Security considerations:
        - Secure password storage
        - Rate limiting for auth endpoints
        - Proper session management
        - CSRF protection
        """,
        "branch": "feature/authentication-system",
        "model": "claude-3-5-sonnet",
        "max_iterations": 20
    })
    
    if create_result["success"]:
        agent_id = create_result["agent_id"]
        print(f"✅ Agent created successfully!")
        print(f"🔗 Agent ID: {agent_id}")
        print(f"📂 Repository: {create_result['repository_url']}")
        print(f"🌿 Branch: {create_result['branch']}")
        print(f"🤖 Model: {create_result['model']}")
    else:
        print(f"❌ Failed to create agent: {create_result.get('error')}")
        return
    
    print("\n2️⃣ Monitoring Agent Progress")
    print("-" * 50)
    
    # Check agent status
    status_result = await client.call_tool("cursor_get_agent_status", {
        "agent_id": agent_id
    })
    
    if status_result["success"]:
        print(f"📊 Status: {status_result['status']}")
        print(f"🔄 Current Step: {status_result['progress']['current_step']}")
        print(f"📈 Progress: {status_result['progress']['completed_steps']}/{status_result['progress']['total_estimated_steps']} steps ({status_result['progress']['completion_percentage']}%)")
        print(f"📁 Files Modified: {', '.join(status_result['progress']['files_modified'])}")
        print(f"💾 Commits Made: {status_result['progress']['commits_made']}")
        
        print("\n📋 Recent Activity:")
        for log in status_result['logs'][-3:]:  # Show last 3 log entries
            print(f"   • {log}")
    
    print("\n3️⃣ Adding Follow-up Instructions")
    print("-" * 50)
    
    # Add follow-up instruction
    followup_result = await client.call_tool("cursor_add_followup_instruction", {
        "agent_id": agent_id,
        "instruction": """
        Please also add the following enhancements:
        - Two-factor authentication (2FA) support
        - Social login options (Google, GitHub)
        - Remember me functionality
        - Account lockout after failed attempts
        - Admin panel for user management
        
        Make sure to maintain backward compatibility and add proper documentation.
        """
    })
    
    if followup_result["success"]:
        print("✅ Follow-up instruction added successfully!")
        print("🔄 Agent will integrate these requirements into current work")
    
    print("\n4️⃣ Viewing All Background Agents")
    print("-" * 50)
    
    # List all agents
    list_result = await client.call_tool("cursor_list_background_agents", {})
    
    if list_result["success"]:
        print(f"📊 Total Agents: {list_result['total_agents']}")
        print("\n🤖 Agent Overview:")
        
        for agent in list_result["agents"]:
            status_emoji = {
                "completed": "✅",
                "running": "🔄", 
                "failed": "❌",
                "stopped": "⏹️"
            }.get(agent["status"], "❓")
            
            print(f"   {status_emoji} {agent['agent_id']}: {agent['status']}")
            print(f"      📂 {agent['repository_url']}")
            print(f"      🌿 {agent['branch']}")
            print(f"      📝 {agent['prompt'][:60]}...")
            if agent.get("error"):
                print(f"      ⚠️  Error: {agent['error']}")
            print()
    
    print("\n5️⃣ Checking API Usage and Limits")
    print("-" * 50)
    
    # Get API usage
    usage_result = await client.call_tool("cursor_get_api_usage", {})
    
    if usage_result["success"]:
        usage = usage_result["usage"]
        limits = usage_result["limits"]
        
        print("📊 Current Usage:")
        print(f"   🤖 Active Agents: {usage['active_agents']}/{limits['max_active_agents']}")
        print(f"   📅 Agents This Month: {usage['agents_created_this_month']}/{limits['monthly_agent_limit']}")
        print(f"   🔄 API Calls Today: {usage['api_calls_today']}/{limits['daily_api_calls']}")
        print(f"   🧠 Tokens Used Today: {usage['tokens_used_today']:,}")
        
        print("\n💰 Remaining Quota:")
        print(f"   🤖 Agents: {usage_result['remaining_quota']['agents']:,}")
        print(f"   🔄 API Calls: {usage_result['remaining_quota']['api_calls']:,}")
        
        billing = usage_result["billing_period"]
        print(f"\n📅 Billing Period: {billing['start_date']} to {billing['end_date']}")
        print(f"   ⏰ Days Remaining: {billing['days_remaining']}")
    
    print("\n6️⃣ Accessing MCP Resources")
    print("-" * 50)
    
    # Read agents summary resource
    summary_resource = await client.read_resource("mcp://cursor-agent/agents-summary")
    summary_data = json.loads(summary_resource)
    
    print("📊 Agents Summary Resource:")
    print(f"   📈 Total Agents: {summary_data['total_agents']}")
    print("   📊 Status Distribution:")
    for status, count in summary_data["agents_by_status"].items():
        print(f"      {status}: {count}")
    
    print("\n🎉 Demonstration Complete!")
    print("=" * 60)
    print("This MCP server provides powerful autonomous coding capabilities:")
    print("• 🤖 Create agents for any coding task")
    print("• 📊 Monitor progress in real-time") 
    print("• 🔄 Send follow-up instructions")
    print("• 📈 Track usage and performance")
    print("• 🔗 Integrate with existing workflows")
    print("\n🚀 Ready to revolutionize your development process!")

def demonstrate_real_world_scenarios():
    """Show real-world usage scenarios"""
    
    print("\n" + "=" * 60)
    print("🌟 REAL-WORLD USAGE SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        {
            "title": "🔐 Security Audit & Fixes",
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
            "use_case": "Monthly security reviews and automated vulnerability fixing"
        },
        {
            "title": "📱 Mobile Responsive Redesign",
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
            Ensure performance remains optimal on mobile devices.
            """,
            "use_case": "Modernizing legacy applications for mobile users"
        },
        {
            "title": "🧪 Test Coverage Enhancement",
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
            Include edge cases and error scenarios.
            """,
            "use_case": "Improving code quality and reducing production bugs"
        },
        {
            "title": "⚡ Performance Optimization",
            "prompt": """
            Optimize application performance for 50% faster load times:
            
            Areas to optimize:
            - Database query optimization
            - Caching strategies implementation
            - Bundle size reduction
            - Image and asset optimization
            - Lazy loading implementation
            - API response optimization
            
            Measure before/after metrics and document improvements.
            Ensure optimizations don't break functionality.
            """,
            "use_case": "Improving user experience and reducing server costs"
        },
        {
            "title": "🔄 API Modernization",
            "prompt": """
            Modernize REST API to GraphQL with backward compatibility:
            
            Migration plan:
            - Design GraphQL schema
            - Implement resolvers
            - Add authentication to GraphQL
            - Create migration guide
            - Maintain REST endpoints during transition
            - Update client applications gradually
            
            Ensure zero downtime during migration.
            Provide comprehensive documentation.
            """,
            "use_case": "Technology stack modernization"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}️⃣ {scenario['title']}")
        print("-" * 40)
        print(f"💡 Use Case: {scenario['use_case']}")
        print(f"📝 Prompt Preview: {scenario['prompt'][:150]}...")
        print(f"🎯 Agent Command:")
        print(f"   cursor_create_background_agent(")
        print(f"       repository_url='https://github.com/company/project',")
        print(f"       prompt='''{scenario['prompt']}''',")
        print(f"       model='claude-3-5-sonnet',")
        print(f"       max_iterations=25")
        print(f"   )")

if __name__ == "__main__":
    print("🔧 Cursor Background Agent MCP Server - Example Client")
    print("📖 This demonstrates how to use the MCP server with autonomous coding agents")
    print()
    
    try:
        # Run the main demonstration
        asyncio.run(demonstrate_cursor_mcp())
        
        # Show real-world scenarios
        demonstrate_real_world_scenarios()
        
    except KeyboardInterrupt:
        print("\n👋 Demonstration stopped by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("💡 This is a mock demonstration. For real usage, ensure:")
        print("   • Cursor API key is configured")
        print("   • MCP server dependencies are installed") 
        print("   • Repository access is properly set up")
