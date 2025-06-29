"""MCP Server for endoflife.date API."""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.server.stdio
from mcp.server.models import InitializationOptions

from .client import EndOfLifeClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-server-eol")

app = Server("mcp-server-eol")

# Global client instance
eol_client: Optional[EndOfLifeClient] = None


@app.list_resources()
async def handle_list_resources() -> List[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="eol://products",
            name="All Products",
            description="List of all products tracked by endoflife.date",
            mimeType="application/json"
        ),
        Resource(
            uri="eol://search",
            name="Product Search",
            description="Search for products by name",
            mimeType="application/json"
        )
    ]


@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a specific resource."""
    global eol_client
    if not eol_client:
        raise RuntimeError("Client not initialized")
    
    if uri == "eol://products":
        products = await eol_client.get_all_products()
        return json.dumps({
            "products": products,
            "count": len(products),
            "description": "All products tracked by endoflife.date"
        }, indent=2)
    elif uri.startswith("eol://search?q="):
        query = uri.split("q=", 1)[1]
        results = await eol_client.search_products(query)
        return json.dumps({
            "query": query,
            "results": results,
            "count": len(results)
        }, indent=2)
    else:
        raise ValueError(f"Unknown resource URI: {uri}")


@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="eol_get_all_products",
            description="Get a list of all products tracked by endoflife.date",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="eol_get_product_versions",
            description="Get all versions/cycles for a specific product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "The product name (e.g., 'nodejs', 'python', 'ubuntu')"
                    }
                },
                "required": ["product"]
            }
        ),
        Tool(
            name="eol_get_cycle_details",
            description="Get detailed information about a specific product cycle/version",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "The product name"
                    },
                    "cycle": {
                        "type": "string",
                        "description": "The cycle/version identifier"
                    }
                },
                "required": ["product", "cycle"]
            }
        ),
        Tool(
            name="eol_search_products",
            description="Search for products by name (case-insensitive partial match)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find products"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="eol_check_support_status",
            description="Check if a specific product version is still supported",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "The product name"
                    },
                    "version": {
                        "type": "string",
                        "description": "The version to check"
                    }
                },
                "required": ["product", "version"]
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    global eol_client
    if not eol_client:
        raise RuntimeError("Client not initialized")
    
    try:
        if name == "eol_get_all_products":
            result = await eol_client.get_all_products()
            return [
                TextContent(
                    type="text",
                    text=result.model_dump_json(indent=2)
                )
            ]
        
        elif name == "eol_get_product_versions":
            product = arguments.get("product")
            if not product:
                raise ValueError("Product name is required")
            
            result = await eol_client.get_product_versions(product)
            return [
                TextContent(
                    type="text",
                    text=result.model_dump_json(indent=2)
                )
            ]
        
        elif name == "eol_get_cycle_details":
            product = arguments.get("product")
            cycle = arguments.get("cycle")
            if not product or not cycle:
                raise ValueError("Both product and cycle are required")
            
            details = await eol_client.get_cycle_details(product, cycle)
            return [
                TextContent(
                    type="text",
                    text=details.model_dump_json(indent=2)
                )
            ]
        
        elif name == "eol_search_products":
            query = arguments.get("query")
            if not query:
                raise ValueError("Search query is required")
            
            result = await eol_client.search_products(query)
            return [
                TextContent(
                    type="text",
                    text=result.model_dump_json(indent=2)
                )
            ]
        
        elif name == "eol_check_support_status":
            product = arguments.get("product")
            version = arguments.get("version")
            if not product or not version:
                raise ValueError("Both product and version are required")
            
            result = await eol_client.check_support_status(product, version)
            return [
                TextContent(
                    type="text",
                    text=result.model_dump_json(indent=2)
                )
            ]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "error": str(e),
                    "tool": name,
                    "arguments": arguments
                }, indent=2)
            )
        ]


async def main():
    """Main entry point for the server."""
    global eol_client
    
    # Initialize the client
    eol_client = EndOfLifeClient()
    
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-server-eol",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
