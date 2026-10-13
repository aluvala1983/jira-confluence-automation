#!/usr/bin/env python3
import asyncio
from datetime import datetime, timezone

from mcp import types
from mcp.server.lowlevel.server import Server
from mcp.server.stdio import stdio_server


async def handle_list_tools(ctx, params):
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="get_time",
                description="Returns the current timestamp in UTC.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            )
        ]
    )


async def handle_call_tool(ctx, params):
    if params.name != "get_time":
        raise ValueError(f"Unknown tool: {params.name}")

    timestamp = datetime.now(timezone.utc).isoformat()
    return types.CallToolResult(
        content=[types.TextContent(type="text", text=timestamp)]
    )


server = Server(
    "get-time",
    on_list_tools=handle_list_tools,
    on_call_tool=handle_call_tool,
)


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
