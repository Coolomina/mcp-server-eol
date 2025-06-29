#!/usr/bin/env python3
"""
Test runner for MCP Server EOL.
Runs tests in order from quick to comprehensive.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tests.test_quick import test_quick
from tests.test_api_client import test_api_client
from tests.test_comprehensive import test_comprehensive
from tests.test_temporal import test_temporal_validation


async def run_all_tests():
    """Run all tests in sequence."""
    print("🧪 MCP Server EOL - Test Runner")
    print("=" * 50)
    
    tests = [
        ("Quick Smoke Test", test_quick),
        ("API Client Test", test_api_client), 
        ("Comprehensive Test", test_comprehensive),
        ("Temporal Validation", test_temporal_validation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running {test_name}...")
        print("-" * 30)
        
        try:
            success = await test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"💥 {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("-" * 30)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    exit(0 if success else 1)
