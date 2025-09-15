#!/usr/bin/env python3
"""
Quick example of how to create a Cursor background agent
with specific repository and model settings.
"""

import asyncio
import json
from cursor_agent_mcp_server import CursorAgentMCPServer, CursorApiConfig
import os

async def create_agent_example():
    """Example of creating an agent with specific repo and model"""
    
    # Get API key from environment
    api_key = os.getenv("CURSOR_API_KEY")
    if not api_key:
        print("❌ Please set CURSOR_API_KEY in your .env file")
        return
    
    print("🚀 Creating Background Agent Example")
    print("=" * 50)
    
    # Create the MCP server instance
    config = CursorApiConfig(api_key=api_key)
    server = CursorAgentMCPServer(config)
    
    try:
        await server.initialize()
        
        # Example 1: Basic feature development
        print("\n📝 Example 1: Feature Development")
        print("-" * 30)
        
        agent_args = {
            "repository_url": "https://github.com/YOUR_USERNAME/YOUR_REPO",  # 👈 YOUR REPO HERE
            "prompt": "Add a user profile page with avatar upload and bio editing",
            "branch": "feature/user-profile",  # Optional: specify branch
            "model": "claude-3-5-sonnet",     # 👈 MODEL CHOICE HERE
            "max_iterations": 15              # Optional: iteration limit
        }
        
        print("🔧 Tool Call:")
        print(f"   cursor_create_background_agent({json.dumps(agent_args, indent=4)})")
        
        result = await server._create_background_agent(agent_args)
        print(f"\n✅ Result: {json.dumps(result, indent=2)}")
        
        # Example 2: Bug fix with different model
        print("\n\n🐛 Example 2: Bug Fix")
        print("-" * 30)
        
        bug_fix_args = {
            "repository_url": "https://github.com/YOUR_USERNAME/YOUR_REPO",
            "prompt": """
            Fix the memory leak in the shopping cart component:
            
            Problem: Users report the page becomes slow after adding/removing items
            Location: components/ShoppingCart.tsx
            
            Investigation needed:
            1. Check for event listener cleanup
            2. Review useEffect dependencies  
            3. Look for state update loops
            4. Add proper component unmounting
            """,
            "branch": "bugfix/cart-memory-leak",
            "model": "claude-3-haiku",  # 👈 Faster, cheaper model for simple fixes
            "max_iterations": 10
        }
        
        print("🔧 Tool Call:")
        print(f"   cursor_create_background_agent({json.dumps(bug_fix_args, indent=4)})")
        
        result2 = await server._create_background_agent(bug_fix_args)
        print(f"\n✅ Result: {json.dumps(result2, indent=2)}")
        
        # Example 3: Complex refactoring with GPT-4
        print("\n\n🔄 Example 3: Complex Refactoring")
        print("-" * 30)
        
        refactor_args = {
            "repository_url": "https://github.com/YOUR_USERNAME/YOUR_REPO",
            "prompt": """
            Refactor the legacy authentication system to use modern patterns:
            
            Current issues:
            - Mixed authentication methods (sessions + JWT)
            - No proper error handling
            - Security vulnerabilities
            - Hard to test and maintain
            
            Refactoring goals:
            - Standardize on JWT with refresh tokens
            - Add comprehensive error handling
            - Implement proper middleware
            - Add unit and integration tests
            - Update documentation
            """,
            "branch": "refactor/auth-modernization",
            "model": "gpt-4o",  # 👈 Most capable model for complex tasks
            "max_iterations": 25
        }
        
        print("🔧 Tool Call:")
        print(f"   cursor_create_background_agent({json.dumps(refactor_args, indent=4)})")
        
        result3 = await server._create_background_agent(refactor_args)
        print(f"\n✅ Result: {json.dumps(result3, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await server.cleanup()

def show_available_options():
    """Show all available repository and model options"""
    
    print("\n" + "=" * 60)
    print("🎯 CONFIGURATION OPTIONS")
    print("=" * 60)
    
    print("\n📂 Repository URL:")
    print("   • Any GitHub repository you have access to")
    print("   • Format: https://github.com/username/repository")
    print("   • Examples:")
    print("     - https://github.com/mycompany/web-app")
    print("     - https://github.com/username/personal-project")
    print("     - https://github.com/organization/api-service")
    
    print("\n🤖 Available Models:")
    print("   • claude-3-5-sonnet (Recommended)")
    print("     - Best overall performance")
    print("     - Great for complex features")
    print("     - Good reasoning capabilities")
    print("   • claude-3-haiku")
    print("     - Fastest and most cost-effective") 
    print("     - Good for simple fixes and tasks")
    print("     - Lower resource usage")
    print("   • gpt-4o")
    print("     - Most capable for complex reasoning")
    print("     - Best for architectural decisions")
    print("     - Higher cost but highest quality")
    
    print("\n🌿 Branch Options:")
    print("   • Default: 'main' (if not specified)")
    print("   • Feature branches: 'feature/feature-name'")
    print("   • Bug fixes: 'bugfix/issue-description'")
    print("   • Refactoring: 'refactor/component-name'")
    print("   • Experiments: 'experiment/new-approach'")
    
    print("\n🔄 Max Iterations:")
    print("   • Default: 10")
    print("   • Simple tasks: 5-10 iterations")
    print("   • Medium tasks: 10-20 iterations")
    print("   • Complex tasks: 20-50 iterations")
    print("   • Note: Higher iterations = more thorough but more expensive")

if __name__ == "__main__":
    print("🔧 Cursor Background Agent - Repository & Model Configuration")
    print("📖 This shows how to specify which repository and model to use")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Show configuration options
    show_available_options()
    
    # Run the examples
    print("\n🚀 Running Examples...")
    try:
        asyncio.run(create_agent_example())
    except KeyboardInterrupt:
        print("\n👋 Examples stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure your CURSOR_API_KEY is set in .env")
        print("💡 Replace 'YOUR_USERNAME/YOUR_REPO' with actual repository URLs")
