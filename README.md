# MCP Server for endoflife.date API

A modern Model Context Protocol (MCP) server that provides access to the endoflife.date API for checking end-of-life dates and support status of various software products. Built with robust typing, comprehensive testing, and automated CI/CD.

## ✨ Features

- 🔍 **Product Discovery**: Get list of all tracked products and search by name
- 📋 **Version Information**: Get detailed version/cycle information for specific products  
- ⏰ **Support Status**: Check if specific versions are still supported
- 🐳 **Docker Ready**: Multi-architecture Docker images with automated builds

## 🚀 Quick Start

### MCP Client Configuration

Add this to your MCP client configuration:

```json
{
  "servers": {
    "endoflife": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm", 
        "ghcr.io/coolomina/mcp-server-eol:latest"
      ]
    }
  }
}
```

### Using PDM (Development)

For local development:

```json
{
  "servers": {
    "endoflife": {
      "command": "pdm",
      "args": [
        "run",
        "python",
        "-m", 
        "mcp_server_eol.server"
      ],
      "cwd": "/path/to/mcp-server-eol"
    }
  }
}
```

## 💬 Useful Prompts

Here are some helpful prompts to get the most out of this MCP server:

```
"Generate a report of end-of-life dates for this repository languages"
"What programming languages and frameworks are tracked by endoflife.date?"
"Show me all the Python versions and their support status"
"Check if any of these technologies are approaching end-of-life: Python 3.9, Node.js 16, Ubuntu 20.04"
"When does support end for Node.js 18 and what should I upgrade to?"
"Which Ubuntu LTS versions are still supported?"
"Compare the support timelines of Node.js 18 vs 20 vs 22"
"What versions of PostgreSQL are still receiving full support vs security-only?"
"Show me products that will reach end-of-life in the next 6 months"
"Search for all products related to 'docker' and show their support status"
```

## Using PDM (Development)

For development or custom setups, use PDM:

```bash
# Install PDM if needed
pip install --user pdm

# Clone and setup
git clone https://github.com/Coolomina/mcp-server-eol.git
cd mcp-server-eol
chmod +x setup.sh && ./setup.sh

# Run the server
pdm run python -m mcp_server_eol.server
```

## 🛠️ Available Tools

The server provides these MCP tools for querying end-of-life information:

- **`eol_get_all_products`** - Get a list of all products tracked by endoflife.date
- **`eol_get_product_versions`** - Get all versions/cycles for a specific product  
- **`eol_get_cycle_details`** - Get detailed information about a specific product cycle
- **`eol_search_products`** - Search for products by name (case-insensitive)
- **`eol_check_support_status`** - Check if a specific product version is still supported


## 🧪 Testing

The project includes a comprehensive, temporal-aware test suite:

```bash
# Quick smoke test (recommended for development)
make test-quick

# Full comprehensive test suite with API validation
make test-all

# Test specific components
python tests/test_api_client.py      # API client tests
python tests/test_comprehensive.py   # End-to-end tests  
python tests/test_temporal.py        # Time-sensitive tests
```

**Note**: Tests are designed to be temporal-aware and will continue working as products reach end-of-life by dynamically checking current status rather than using hardcoded expectations.

## 🐳 Docker

### Multi-Architecture Support

Docker images are automatically built for multiple architectures:
- `linux/amd64` (Intel/AMD x64)
- `linux/arm64` (Apple Silicon, ARM servers)

### Available Tags

- `latest` - Latest stable release
- `main` - Latest commit on main branch  

### Building Locally

```bash
# Build local image
make docker-build

# Run locally built image
make docker-run
```

## 🚀 Development

### Development Setup

```bash
# Install development dependencies
pdm install -G dev

# Run tests
make test

# Format code
make format

# Type checking
make lint
```

## 💡 Example Usage

```python
# Query all available products
eol_get_all_products()

# Get all Node.js versions
eol_get_product_versions(product="nodejs")

# Get detailed info for a specific version
eol_get_cycle_details(product="python", cycle="3.11")

# Check if Python 3.8 is still supported
eol_check_support_status(product="python", version="3.8")

# Search for products containing "ubuntu"
eol_search_products(query="ubuntu")
```

### Real-world Examples

```bash
# Check if your Python version is still supported
eol_check_support_status(product="python", version="3.11")
# Returns: {"supported": true, "eol_date": "2027-10-31"}

# Find when Ubuntu 22.04 reaches end-of-life
eol_get_cycle_details(product="ubuntu", cycle="22.04")
# Returns detailed timeline including support phases

# See all available Node.js versions
eol_get_product_versions(product="nodejs") 
# Returns list of all Node.js releases with support status
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with tests: `make test`
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 🔗 Links

- **Repository**: https://github.com/Coolomina/mcp-server-eol
- **Docker Images**: https://github.com/Coolomina/mcp-server-eol/pkgs/container/mcp-server-eol
- **endoflife.date API**: https://endoflife.date/docs/api
- **Model Context Protocol**: https://modelcontextprotocol.io
