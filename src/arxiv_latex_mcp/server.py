"""Smithery-compatible FastMCP server definition for arXiv LaTeX processing."""

from __future__ import annotations

import asyncio
import logging

from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery

from arxiv_to_prompt import process_latex_source

_LOGGER = logging.getLogger("arxiv-latex-mcp")
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO)

_RENDERING_INSTRUCTIONS = (
    "\n\nIMPORTANT INSTRUCTIONS FOR RENDERING:\n"
    "When discussing this paper, please use dollar sign notation ($...$) for inline equations "
    "and double dollar signs ($$...$$) for display equations when providing responses that "
    "include LaTeX mathematical expressions.\n"
)


@smithery.server()
def create_server() -> FastMCP:
    """Create and return the FastMCP server instance expected by Smithery."""
    server = FastMCP("arxiv-latex-mcp")

    @server.tool(
        name="get_paper_prompt",
        description=(
            "Get a flattened LaTeX code of a paper from arXiv ID for precise interpretation "
            "of mathematical expressions"
        ),
    )
    async def get_paper_prompt(arxiv_id: str) -> str:
        """Fetch and flatten LaTeX for the requested arXiv paper."""
        if not arxiv_id:
            raise ValueError("Missing required argument: arxiv_id")

        _LOGGER.info("Processing arXiv paper: %s", arxiv_id)

        try:
            prompt = await asyncio.to_thread(process_latex_source, arxiv_id)
            result = f"{prompt}{_RENDERING_INSTRUCTIONS}"
            _LOGGER.info("Successfully processed arXiv paper: %s", arxiv_id)
            return result
        except Exception as exc:  # noqa: BLE001 - we return the error to the client
            error_msg = f"Error processing arXiv paper {arxiv_id}: {exc}"
            _LOGGER.error(error_msg)
            return error_msg

    return server


__all__ = ["create_server"]
