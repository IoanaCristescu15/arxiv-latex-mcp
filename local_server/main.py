#!/usr/bin/env python3
"""Local STDIO launcher for the Smithery FastMCP server."""

from __future__ import annotations

import asyncio
import logging

from mcp.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from arxiv_latex_mcp.server import create_server

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Run the FastMCP server over stdio for local development."""
    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=server.name,
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
