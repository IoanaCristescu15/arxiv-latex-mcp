"""Smithery deployment package for the arXiv LaTeX MCP server."""

from .server import create_server

__all__ = ["create_server"]
