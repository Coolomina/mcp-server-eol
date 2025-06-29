#!/usr/bin/env python3
"""
Direct API client test (no MCP protocol).
Tests the underlying endoflife.date API client functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path for local imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_eol.client import EndOfLifeClient


async def test_api_client():
    """Test the direct API client functionality."""
    print("🌐 Testing Direct API Client")
    print("=" * 40)
    
    client = EndOfLifeClient()
    
    try:
        # Test basic connectivity
        print("1. Testing API connectivity...")
        products_result = await client.get_all_products()
        print(f"✅ Connected to endoflife.date API")
        print(f"   Found {products_result.count} tracked products")
        
        # Test search functionality  
        print("\n2. Testing product search...")
        python_results = await client.search_products("python")
        print(f"✅ Search works: {python_results.results}")
        
        # Test version lookup
        print("\n3. Testing version information...")
        python_versions = await client.get_product_versions("python")
        print(f"✅ Version lookup works: {python_versions.count} Python versions")
        
        # Test specific version details
        print("\n4. Testing specific version details...")
        python311 = await client.get_cycle_details("python", "3.11")
        print(f"✅ Details lookup works:")
        print(f"   Python 3.11 EOL: {python311.details.eol}")
        print(f"   Support until: {python311.details.support}")
        
        print("\n🎉 API Client test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ API Client test FAILED: {e}")
        return False
    finally:
        await client.close()


if __name__ == "__main__":
    success = asyncio.run(test_api_client())
    exit(0 if success else 1)
