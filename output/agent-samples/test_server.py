"""Server tests over real MCP stdio. No editor, no host."""
import anyio, os, sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = Path(__file__).parent
PASS, FAIL = [], []
def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("  PASS " if cond else "  FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))

FIXTURE = HERE / "reports" / "t_fixture.md"

async def main():
    (HERE / "reports").mkdir(exist_ok=True)
    FIXTURE.write_text("# Fixture\n\n## Findings\n- a claim\n")
    py = str(HERE / ".venv" / "bin" / "python")
    # Deliberately NO key: research_topic must fail as a STRING, not a crash.
    env = {k: v for k, v in os.environ.items() if k != "OPENROUTER_API_KEY"}
    params = StdioServerParameters(command=py, args=[str(HERE / "server.py")], env=env, cwd=str(HERE))
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            check("initialize handshake", init.serverInfo.name == "research-reports", init.serverInfo.name)

            tools = {t.name: t for t in (await s.list_tools()).tools}
            check("both tools listed", set(tools) == {"research_topic", "md_to_pdf"}, str(set(tools)))
            check("ctx excluded from schema", set(tools["research_topic"].inputSchema["properties"]) == {"topic"},
                  str(set(tools["research_topic"].inputSchema["properties"])))
            check("docstring became the tool description",
                  "Research a topic" in (tools["research_topic"].description or ""))
            check("md_to_pdf schema", set(tools["md_to_pdf"].inputSchema["properties"]) == {"md_path"})

            res = {str(x.uri) for x in (await s.list_resources()).resources}
            check("resource listed", res == {"reports://list"}, str(res))
            body = (await s.read_resource("reports://list")).contents[0].text
            check("resource returns report names", FIXTURE.name in body, body[:60])

            ok = await s.call_tool("md_to_pdf", {"md_path": f"reports/{FIXTURE.name}"})
            check("md_to_pdf succeeds through MCP", "Saved PDF" in ok.content[0].text, ok.content[0].text)

            bad = await s.call_tool("md_to_pdf", {"md_path": "/etc/passwd"})
            check("path traversal blocked through MCP", "refusing to touch" in bad.content[0].text, bad.content[0].text)

            gone = await s.call_tool("md_to_pdf", {"md_path": "reports/missing.md"})
            check("missing file -> error string, not a crash",
                  gone.content[0].text.startswith("Conversion failed"), gone.content[0].text)

            # No API key in env: the agent will raise KeyError inside the thread.
            nokey = await s.call_tool("research_topic", {"topic": "anything"})
            check("research_topic failure returns a string, server survives",
                  nokey.content[0].text.startswith("Research failed"), nokey.content[0].text)

            still = await s.call_tool("md_to_pdf", {"md_path": f"reports/{FIXTURE.name}"})
            check("server still alive after a tool failure", "Saved PDF" in still.content[0].text)

anyio.run(main)
for f in (HERE / "reports").glob("t_fixture.*"):
    f.unlink()
print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL: print("FAILED:", FAIL); sys.exit(1)
