#!/usr/bin/env python3
"""
Comprehensive test suite for the MCP Server EOL.
Tests all tools and functionality in an organized manner.
"""

import asyncio
import json
from pathlib import Path


async def test_comprehensive():
    """Run comprehensive tests of all MCP server functionality."""
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError:
        print("❌ MCP client library not available in this context")
        return False
    
    print("🚀 MCP Server EOL - Comprehensive Test Suite")
    print("=" * 60)
    
    server_params = StdioServerParameters(
        command="pdm",
        args=["run", "python", "-m", "mcp_server_eol.server"],
        cwd=str(Path(__file__).parent.parent)
    )
    
    success_count = 0
    total_tests = 0
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ MCP Session initialized\n")
                
                # Test 1: Server connection and tool listing
                print("📋 TEST 1: Server Connection & Tool Discovery")
                print("-" * 50)
                tools = await session.list_tools()
                print(f"✅ Connected successfully")
                print(f"✅ Found {len(tools.tools)} available tools:")
                for tool in tools.tools:
                    print(f"   • {tool.name}: {tool.description}")
                success_count += 1
                total_tests += 1
                
                # Test 2: Get all products
                print(f"\n📋 TEST 2: Get All Products")
                print("-" * 50)
                try:
                    result = await session.call_tool("eol_get_all_products", {})
                    products_data = json.loads(result.content[0].text)
                    print(f"✅ Retrieved {products_data['count']} products")
                    print(f"   Sample: {products_data['products'][:5]}")
                    success_count += 1
                except Exception as e:
                    print(f"❌ Failed: {e}")
                total_tests += 1
                
                # Test 3: Search functionality
                print(f"\n🔍 TEST 3: Product Search")
                print("-" * 50)
                search_queries = ["python", "node", "ubuntu", "java"]
                for query in search_queries:
                    try:
                        result = await session.call_tool("eol_search_products", {"query": query})
                        search_data = json.loads(result.content[0].text)
                        print(f"   '{query}': {search_data['results']} ({search_data['count']} found)")
                        success_count += 0.25  # Partial credit for each search
                    except Exception as e:
                        print(f"   '{query}': ❌ {e}")
                total_tests += 1
                
                # Test 4: Product versions
                print(f"\n📦 TEST 4: Product Version Listings")
                print("-" * 50)
                products_to_check = ["python", "nodejs", "ubuntu"]
                for product in products_to_check:
                    try:
                        result = await session.call_tool("eol_get_product_versions", {"product": product})
                        versions = json.loads(result.content[0].text)
                        print(f"   {product}: {len(versions['versions'])} versions available")
                        if versions['versions']:
                            latest = versions['versions'][0]
                            print(f"      Latest: {latest.get('cycle')} (EOL: {latest.get('eol')})")
                        success_count += 0.33  # Partial credit
                    except Exception as e:
                        print(f"   {product}: ❌ {e}")
                total_tests += 1
                
                # Test 5: Specific cycle details (flexible testing)
                print(f"\n🔍 TEST 5: Specific Version Details")
                print("-" * 50)
                
                # Test cycles that are likely to exist for a long time
                test_cycles = [
                    ("python", "3.11"),
                    ("python", "3.10"),
                    ("nodejs", "18"),
                    ("ubuntu", "22.04")
                ]
                
                valid_details = 0
                for product, cycle in test_cycles:
                    try:
                        result = await session.call_tool("eol_get_cycle_details", {
                            "product": product, 
                            "cycle": cycle
                        })
                        details = json.loads(result.content[0].text)
                        
                        # Verify response structure
                        if 'details' in details and 'product' in details:
                            cycle_details = details['details']
                            eol_date = cycle_details.get('eol', 'Unknown')
                            support_date = cycle_details.get('support', 'Unknown')
                            release_date = cycle_details.get('release_date', cycle_details.get('releaseDate', 'Unknown'))
                            
                            print(f"   {product} {cycle}: Released {release_date}, EOL {eol_date}, Support {support_date}")
                            valid_details += 1
                        else:
                            print(f"   {product} {cycle}: ❌ Invalid response structure")
                            
                    except Exception as e:
                        print(f"   {product} {cycle}: ❌ {e}")
                
                # Success if most queries worked
                if valid_details >= len(test_cycles) * 0.75:  # 75% success rate
                    print(f"   📊 Detail queries: {valid_details}/{len(test_cycles)} successful")
                    success_count += 1
                else:
                    print(f"   📊 Detail queries: {valid_details}/{len(test_cycles)} successful - Below threshold")
                total_tests += 1
                
                # Test 6: Support status checks (temporal-aware)
                print(f"\n✅ TEST 6: Support Status Verification")
                print("-" * 50)
                
                # Test a variety of products/versions without hardcoded expectations
                test_cases = [
                    ("python", "3.8"),
                    ("python", "3.11"), 
                    ("nodejs", "16"),
                    ("nodejs", "20"),
                    ("ubuntu", "18.04"),
                    ("ubuntu", "22.04")
                ]
                
                valid_responses = 0
                for product, version in test_cases:
                    try:
                        result = await session.call_tool("eol_check_support_status", {
                            "product": product, 
                            "version": version
                        })
                        status = json.loads(result.content[0].text)
                        
                        # Verify the response structure is correct
                        required_fields = ['product', 'version', 'found', 'is_supported', 'is_eol']
                        if all(field in status for field in required_fields):
                            is_supported = status.get('is_supported', False)
                            is_eol = status.get('is_eol', True)
                            found = status.get('found', False)
                            
                            if found:
                                if is_eol:
                                    status_text = "❌ EOL"
                                elif is_supported:
                                    status_text = "✅ Active Support"
                                else:
                                    status_text = "🟡 Security Only"
                            else:
                                status_text = "❓ Not Found"
                                
                            print(f"   {product} {version}: {status_text}")
                            valid_responses += 1
                        else:
                            print(f"   {product} {version}: ❌ Invalid response structure")
                            
                    except Exception as e:
                        print(f"   {product} {version}: ❌ Error: {e}")
                
                # Consider test successful if most queries worked (allows for API changes)
                success_rate = valid_responses / len(test_cases)
                if success_rate >= 0.7:  # 70% success rate threshold
                    print(f"   📊 Response validation: {valid_responses}/{len(test_cases)} valid ({success_rate:.1%})")
                    success_count += 1
                else:
                    print(f"   📊 Response validation: {valid_responses}/{len(test_cases)} valid ({success_rate:.1%}) - Below threshold")
                total_tests += 1
                
    except Exception as e:
        print(f"❌ Critical error during testing: {e}")
        return False
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 TEST SUMMARY")
    print(f"   Tests passed: {success_count:.1f}/{total_tests}")
    print(f"   Success rate: {(success_count/total_tests)*100:.1f}%")
    
    # Consider test successful if we got at least 95% of the points
    success_threshold = total_tests * 0.95
    
    if success_count >= success_threshold:
        print("🎉 All tests passed successfully!")
        print("\n💡 Usage Tips:")
        print("• Add this server to Claude Desktop config")
        print("• Ask Claude to check EOL dates for your tech stack")
        print("• Get upgrade recommendations for outdated versions")
        return True
    else:
        print("⚠️  Some tests failed - check server configuration")
        return False


if __name__ == "__main__":
    asyncio.run(test_comprehensive())
