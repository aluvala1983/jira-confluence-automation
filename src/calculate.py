#!/usr/bin/env python3
import asyncio
import math

from mcp import types
from mcp.server.lowlevel.server import Server
from mcp.server.stdio import stdio_server

OPERATIONS = ("add", "subtract", "multiply", "divide")


async def handle_list_tools(ctx, params):
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="calculate",
                description="Performs basic arithmetic on two numbers.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": list(OPERATIONS),
                            "description": "The arithmetic operation to perform.",
                        },
                        "a": {
                            "type": "number",
                            "description": "The first number.",
                        },
                        "b": {
                            "type": "number",
                            "description": "The second number.",
                        },
                    },
                    "required": ["operation", "a", "b"],
                    "additionalProperties": False,
                },
            )
        ]
    )


async def handle_call_tool(ctx, params):
    if params.name != "calculate":
        raise ValueError(f"Unknown tool: {params.name}")

    arguments = params.arguments or {}
    operation = arguments.get("operation")
    a = arguments.get("a")
    b = arguments.get("b")

    if operation not in OPERATIONS:
        raise ValueError(f"Unsupported operation: {operation}")
    if isinstance(a, bool) or not isinstance(a, (int, float)) or not math.isfinite(a):
        raise ValueError("'a' must be a finite number")
    if isinstance(b, bool) or not isinstance(b, (int, float)) or not math.isfinite(b):
        raise ValueError("'b' must be a finite number")

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    else:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b

    if not math.isfinite(result):
        raise ValueError("The calculation result is outside the supported numeric range")

    return types.CallToolResult(
        content=[types.TextContent(type="text", text=str(result))]
    )


server = Server(
    "calculate",
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
