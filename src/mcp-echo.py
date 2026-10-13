#!/usr/bin/env python3
import asyncio

from mcp import types
from mcp.server.lowlevel.server import Server
from mcp.server.stdio import stdio_server


async def handle_list_tools(ctx, params):
    """List available tools provided by this server."""
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="echo",
                description="Echoes back the input message.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to echo back",
                        }
                    },
                    "required": ["message"],
                },
            )
        ]
    )


async def handle_call_tool(ctx, params):
    """Handle tool execution requests."""
    if params.name != "echo":
        raise ValueError(f"Unknown tool: {params.name}")

    arguments = params.arguments or {}
    message = arguments.get("message")
    if message is None:
        raise ValueError("Missing required argument: 'message'")

    return types.CallToolResult(
        content=[types.TextContent(type="text", text=f"Echo: {message}")]
    )


server = Server(
    "mcp-echo",
    on_list_tools=handle_list_tools,
    on_call_tool=handle_call_tool,
)


async def main():
    """Run the server using standard input/output streams (stdio)."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
