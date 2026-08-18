"""A research agent: a bounded tool loop over any OpenAI-compatible chat API.

    export OPENROUTER_API_KEY=sk-or-...
    python agent.py "what is retrieval-augmented generation"

The agent is the for-loop in run_agent(). Everything else is plumbing.

Logs go to STDERR on purpose. This module is imported by an MCP server, where
stdout carries the JSON-RPC protocol — one stray print() there desyncs the client.
"""

import json
import os
import re
import sys
from pathlib import Path

import requests
from ddgs import DDGS

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openrouter/free"   # auto-routes to a free model that supports tool calling
MAX_STEPS = 6               # an agent that cannot stop is a bill, not a feature
REPORTS = Path(__file__).parent / "reports"

def load_key() -> str:
    """Read the key from the environment, falling back to a .env file beside this script.

    The MCP Inspector gives child processes a sanitised environment and does NOT
    forward your shell exports, so a .env is the only thing that works everywhere:
    Inspector, Cline, and a plain terminal.
    """
    if "OPENROUTER_API_KEY" not in os.environ:
        env_file = Path(__file__).parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                key, _, value = line.partition("=")
                if key.strip() == "OPENROUTER_API_KEY":
                    os.environ["OPENROUTER_API_KEY"] = value.strip().strip("\"'")
    try:
        return os.environ["OPENROUTER_API_KEY"]
    except KeyError:
        raise RuntimeError(
            "No OPENROUTER_API_KEY. Export it, or put it in a .env file next to agent.py."
        ) from None


SYSTEM = """You are a research assistant.

Search the web until you can answer, then write the final report as Markdown:

# <Title>
## Findings
- one bullet per claim
## Sources
- one URL per line

Rules:
- Never state a fact you did not find in a search result.
- If sources disagree, say so.
- Stop searching once you can answer. Do not pad.
- Your last message must be the report itself, nothing else."""

TOOLS = [{
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web. Returns the top 5 results as title, URL and snippet.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "The search query."}},
            "required": ["query"],
        },
    },
}]


def web_search(query: str) -> str:
    """The one tool. Plain Python — no model inside it."""
    hits = DDGS().text(query, max_results=5)
    if not hits:
        return f"No results for '{query}'."
    return "\n".join(f"{h['title']} — {h['href']}\n{h['body']}" for h in hits)


def run_tool(name: str, args: dict) -> str:
    """Tools return strings and never raise: an error the model can read is one it can retry."""
    try:
        return web_search(**args) if name == "web_search" else f"Unknown tool: {name}"
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def call_model(messages: list[dict]) -> dict:
    resp = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {load_key()}"},
        json={"model": MODEL, "messages": messages, "tools": TOOLS},
        timeout=120,   # never a naked post
    )
    resp.raise_for_status()
    body = resp.json()
    # "openrouter/free" is a router, not a model — this is who actually answered.
    print(f"    model={body.get('model')}", file=sys.stderr)
    return body["choices"][0]["message"]


def run_agent(topic: str) -> str:
    """The agent. Send, read, run tools, repeat — until it stops asking or runs out of steps."""
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": topic}]

    for step in range(1, MAX_STEPS + 1):
        message = call_model(messages)
        messages.append(message)
        calls = message.get("tool_calls") or []
        print(f"[step {step}] tools={[c['function']['name'] for c in calls]}", file=sys.stderr)

        # No tool calls means the model is done talking to us: this is the report.
        if not calls:
            return message.get("content") or "[empty response]"

        for call in calls:
            # arguments arrives as a JSON *string*, not a dict. Forgetting this is
            # the most common bug in the OpenAI tool-calling format.
            args = json.loads(call["function"]["arguments"] or "{}")
            result = run_tool(call["function"]["name"], args)
            print(f"    -> {call['function']['name']}({args}) => {len(result)} chars", file=sys.stderr)
            # One message per call, each tagged with its id. Not batched.
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": result})

    return f"[stopped: hit MAX_STEPS={MAX_STEPS} without a final report]"


def research_to_file(topic: str) -> Path:
    """Run the agent and save the report. Returns the path to the .md file."""
    report = run_agent(topic)
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:60] or "report"
    REPORTS.mkdir(exist_ok=True)
    path = REPORTS / f"{slug}.md"
    path.write_text(report, encoding="utf-8")
    return path


if __name__ == "__main__":
    topic = " ".join(sys.argv[1:]) or "what is retrieval-augmented generation"
    print(research_to_file(topic))
