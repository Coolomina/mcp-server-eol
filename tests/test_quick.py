#!/usr/bin/env python3
"""
Quick smoke test for MCP Server EOL.
Tests basic connectivity and one tool to ensure server is working.
"""

import asyncio
import json
from pathlib import Path


async def test_quick():
    """Quick smoke test - just verify server is working."""
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError:
        print("❌ MCP client library not available")
        return False
    
    print("⚡ Quick Smoke Test - MCP Server EOL")
    print("=" * 40)
    
    server_params = StdioServerParameters(
        command="pdm",
        args=["run", "python", "-m", "mcp_server_eol.server"],
        cwd=str(Path(__file__).parent.parent)
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ Server connection established")
                
                # List available tools
                tools = await session.list_tools()
                print(f"✅ Found {len(tools.tools)} tools available")
                
                # Test one simple tool
                print("🔍 Testing search functionality...")
                result = await session.call_tool("eol_search_products", {"query": "python"})
                search_data = json.loads(result.content[0].text)
                print(f"✅ Search works: found {search_data['count']} Python-related products")
                
                print("\n🎉 Quick test PASSED - Server is working!")
                return True
                
    except Exception as e:
        print(f"❌ Quick test FAILED: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_quick())
    exit(0 if success else 1)
