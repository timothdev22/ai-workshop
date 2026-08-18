"""MCP server exposing the research agent and the PDF converter to any MCP host.

    mcp dev server.py          # MCP Inspector, no editor needed
    python server.py           # stdio, for Cline / Claude Code / Claude Desktop

Two tools, deliberately different in kind:
  research_topic  -> runs an agent loop. Costs money. Makes decisions.
  md_to_pdf       -> runs a function. Costs nothing. Makes none.

The docstring on each tool IS the prompt the host's model reads to decide
whether to call it. Vague docstring, unused tool.

STDOUT BELONGS TO THE PROTOCOL. Anything printed there breaks the transport.
"""

from pathlib import Path

import anyio
from mcp.server.fastmcp import Context, FastMCP

from agent import MAX_STEPS, research_to_file
from md2pdf import md_to_pdf as convert_to_pdf

REPORTS = Path(__file__).parent / "reports"

mcp = FastMCP("research-reports")


@mcp.tool()
async def research_topic(topic: str, ctx: Context) -> str:
    """Research a topic on the web and save a Markdown report.

    Use for open questions needing current sources. Returns the path to the .md file,
    which can then be passed to md_to_pdf. Takes 30-60 seconds.
    """
    await ctx.info(f"Researching {topic!r} (up to {MAX_STEPS} steps)")
    try:
        # The agent loop is blocking HTTP. Run it off the event loop or the
        # whole server stalls while it works.
        path = await anyio.to_thread.run_sync(research_to_file, topic)
    except Exception as exc:
        return f"Research failed: {type(exc).__name__}: {exc}"
    return f"Saved report to {path}"


@mcp.tool()
def md_to_pdf(md_path: str) -> str:
    """Convert an existing Markdown report to PDF. Returns the path to the .pdf file.

    md_path must be a report inside the reports/ directory.
    """
    try:
        return f"Saved PDF to {convert_to_pdf(md_path)}"
    except Exception as exc:
        return f"Conversion failed: {type(exc).__name__}: {exc}"


@mcp.resource("reports://list")
def list_reports() -> str:
    """Every report on disk. A resource is data the host reads; a tool is an action it runs."""
    REPORTS.mkdir(exist_ok=True)
    files = sorted(p.name for p in REPORTS.iterdir() if p.suffix in {".md", ".pdf"})
    return "\n".join(files) or "(no reports yet)"


if __name__ == "__main__":
    mcp.run(transport="stdio")
