# MCP Server for endoflife.date - Usage Guide

## ✅ Working MCP Server

Your MCP server is working correctly! Here's how to use it:

## 🚀 Quick Test

Run this to verify everything works:
```bash
pdm run python simple_test.py
```

## 🔧 Configuration for Claude Desktop

Add this to your Claude Desktop config file:
**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "endoflife": {
      "command": "pdm",
      "args": ["run", "python", "-m", "mcp_server_eol.server"],
      "cwd": "/Users/ale/repos/personal/mcp-server-eol"
    }
  }
}
```

## 🛠️ Available Tools

1. **eol_get_all_products** - Get all 385+ tracked products
2. **eol_search_products** - Search products by name
3. **eol_get_product_versions** - Get versions for a specific product
4. **eol_get_cycle_details** - Get detailed info for a specific version
5. **eol_check_support_status** - Check if a version is still supported

## 💬 Example Claude Conversations

Once configured, you can ask Claude:

- "What Python versions are still supported?"
- "When does Ubuntu 22.04 reach end of life?"
- "Show me all Node.js versions and their support status"
- "Is Java 11 still supported?"
- "What's the latest version of PostgreSQL?"

## 🔍 Manual Testing

Test individual tools:
```bash
# Test the API client directly
pdm run python test_client.py

# Test the MCP server
pdm run python simple_test.py

# Run comprehensive demos
pdm run python test_mcp_client.py
```

## 📊 Tool Examples

### Search for products:
```json
{
  "tool": "eol_search_products",
  "args": {"query": "python"}
}
```

### Get Python versions:
```json
{
  "tool": "eol_get_product_versions", 
  "args": {"product": "python"}
}
```

### Check if Python 3.9 is supported:
```json
{
  "tool": "eol_check_support_status",
  "args": {"product": "python", "version": "3.9"}
}
```

### Get Node.js 18 details:
```json
{
  "tool": "eol_get_cycle_details",
  "args": {"product": "nodejs", "cycle": "18"}
}
```

## 🐛 Troubleshooting

If something doesn't work:

1. **Check dependencies**: `pdm install`
2. **Test API client**: `pdm run python test_client.py`
3. **Test MCP server**: `pdm run python simple_test.py`
4. **Check logs**: Look for error messages in terminal output

## 🎉 Success!

Your MCP server is ready to use! Add it to Claude Desktop and start asking about end-of-life dates for your technology stack.
