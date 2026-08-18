# Run it

## 1. Install

```bash
cd output/agent-samples
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 2. Key

Create `.env` next to `agent.py`:

```
OPENROUTER_API_KEY=sk-or-...
```

```bash
chmod 600 .env
```

Needed because editors do not pass your shell exports to the server.

## 3. Test without any editor

```bash
.venv/bin/python md2pdf.py reports/sample.md        # PDF, no key needed
.venv/bin/python agent.py "what is RAG"             # agent loop, writes reports/*.md
```

## 4. Antigravity

Config file: `~/.gemini/antigravity/mcp_config.json`
(or open it from the UI: **…** menu → **MCP Servers** → **Manage MCP Servers** → **View raw config**)

```json
{
  "mcpServers": {
    "research-reports": {
      "command": "/ABS/PATH/output/agent-samples/.venv/bin/python",
      "args": ["/ABS/PATH/output/agent-samples/server.py"]
    }
  }
}
```

Absolute paths. Must be `.venv/bin/python`, not system python.

Reload MCP servers in Antigravity, then ask:

> research retrieval-augmented generation and give me a PDF

Antigravity calls `research_topic`, gets back a `.md` path, then calls `md_to_pdf` on it. Output lands in `reports/`.

## Execution order

```
Antigravity (its model, free)
  └─ research_topic(topic)      → agent.py loop, up to MAX_STEPS=6 calls on YOUR key
       └─ web_search            → ddgs, free
     returns "Saved report to reports/x.md"
  └─ md_to_pdf("reports/x.md")  → no LLM
     returns "Saved PDF to reports/x.pdf"
```

Antigravity chains the two because `research_topic`'s docstring names `md_to_pdf` and its return value contains a real path.

## Other clients

```bash
npx -y @modelcontextprotocol/inspector .venv/bin/python server.py     # Inspector UI
```

Cline: same JSON, in `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

Do not use `mcp dev` — needs `uv`, fails with `spawn uv ENOENT`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Server not listed | use absolute paths and `.venv/bin/python` |
| `Research failed: KeyError` | key not reaching it — use `.env` |
| `Research failed: HTTPError 401` | wrong or expired key |
| `[stopped: hit MAX_STEPS=6]` | free model kept searching, never wrote — rerun or pin a better model |
| PDF step never runs | docstring or return value stopped naming a path |
