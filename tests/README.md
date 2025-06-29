# Test Suite for MCP Server EOL

This directory contains organized tests for the MCP Server EOL project.

## Test Files

### 🚀 **test_comprehensive.py**
- **Purpose**: Complete test suite covering all MCP server functionality
- **Use when**: Running full validation or CI/CD pipelines
- **Tests**: All 5 MCP tools, error handling, and edge cases
- **Runtime**: ~30-60 seconds

### ⚡ **test_quick.py** 
- **Purpose**: Fast smoke test for basic functionality
- **Use when**: Quick verification that server is working
- **Tests**: Server connection and one simple tool
- **Runtime**: ~5-10 seconds

### 🌐 **test_api_client.py**
- **Purpose**: Direct API client testing (bypasses MCP protocol)
- **Use when**: Debugging API connectivity issues
- **Tests**: Raw endoflife.date API client functionality
- **Runtime**: ~10-15 seconds

## Running Tests

```bash
# Quick smoke test (recommended for development)
python tests/test_quick.py

# Full comprehensive test suite
python tests/test_comprehensive.py  

# Test direct API client (troubleshooting)
python tests/test_api_client.py

# Run all tests
python -m pytest tests/ -v
```

## Test Requirements

- PDM environment set up (`pdm install`)
- Internet connection (for endoflife.date API)
- MCP client library available in environment

## Expected Output

All tests provide clear pass/fail indicators:
- ✅ = Success
- ❌ = Failure  
- ⚠️ = Warning/Partial success

## Troubleshooting

If tests fail:
1. Run `test_api_client.py` first to verify API connectivity
2. Check that `pdm install` was run successfully
3. Ensure you're in the project root directory
4. Verify internet connection for API access
