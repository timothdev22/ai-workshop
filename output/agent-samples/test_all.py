"""Full test suite. Runs the agent loop against a local stub of the OpenAI
chat-completions endpoint, so requests/headers/parsing/message-shaping are all real.
Only the model's judgment is simulated."""
import json, os, sys, threading, traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("OPENROUTER_API_KEY", "stub-key")

import agent, md2pdf

PASS, FAIL = [], []
def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("  PASS " if cond else "  FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))

# ---- stub server -----------------------------------------------------------
SCRIPT, REQUESTS = [], []

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        REQUESTS.append({"body": body, "auth": self.headers.get("Authorization")})
        reply = SCRIPT.pop(0) if SCRIPT else {"status": 200, "message": {"role": "assistant", "content": "done"}}
        self.send_response(reply.get("status", 200))
        self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(json.dumps({"choices": [{"message": reply.get("message", {})}]}).encode())

srv = HTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
agent.API_URL = f"http://127.0.0.1:{srv.server_port}/v1/chat/completions"

def tool_call(cid, name, args):
    return {"id": cid, "type": "function", "function": {"name": name, "arguments": json.dumps(args)}}

def reset(script):
    SCRIPT.clear(); SCRIPT.extend(script); REQUESTS.clear()

# ---- A. md2pdf -------------------------------------------------------------
print("\nA. md2pdf.py")
REPORTS = Path(agent.__file__).parent / "reports"
REPORTS.mkdir(exist_ok=True)
(REPORTS / "t_basic.md").write_text("# T\n\n## Findings\n- a\n\n| x | y |\n|---|---|\n| 1 | 2 |\n")
out = md2pdf.md_to_pdf(REPORTS / "t_basic.md")
check("converts markdown to a real PDF", out.exists() and out.read_bytes()[:4] == b"%PDF", str(out))

(REPORTS / "t_uni.md").write_text("# T\n\n- em—dash, curly “quotes”, café, 中文\n")
try:
    md2pdf.md_to_pdf(REPORTS / "t_uni.md"); ok = True; err = ""
except Exception as e: ok, err = False, repr(e)
check("survives non-latin-1 characters", ok, err)

for bad in ["/etc/passwd", str(REPORTS / ".." / ".." / "CLAUDE.md")]:
    try: md2pdf.md_to_pdf(bad); blocked = False
    except ValueError: blocked = True
    except Exception: blocked = False
    check(f"rejects path outside reports/: {bad}", blocked)

try: md2pdf.md_to_pdf(REPORTS / "nope.md"); raised = False
except FileNotFoundError: raised = True
except Exception: raised = False
check("missing file raises FileNotFoundError (server catches it)", raised)

# ---- B. tool layer ---------------------------------------------------------
print("\nB. tool layer")
check("run_tool: unknown tool returns string", "Unknown tool" in agent.run_tool("nope", {}))
_orig = agent.web_search
agent.web_search = lambda query: (_ for _ in ()).throw(ValueError("rate limited"))
r = agent.run_tool("web_search", {"query": "x"})
check("run_tool: exception becomes a string, never raises", r == "ValueError: rate limited", r)
agent.web_search = lambda query: f"RESULTS for {query}"

# ---- C. the loop -----------------------------------------------------------
print("\nC. agent loop")
reset([{"message": {"role": "assistant", "tool_calls": [tool_call("c1", "web_search", {"query": "rag"})]}},
       {"message": {"role": "assistant", "content": "# RAG\n## Findings\n- ok\n## Sources\n- u"}}])
res = agent.run_agent("rag")
check("tool call then final report", res.startswith("# RAG"), res[:40])
check("made exactly 2 API calls", len(REQUESTS) == 2, str(len(REQUESTS)))
sent = REQUESTS[1]["body"]["messages"]
check("auth header sent", REQUESTS[0]["auth"] == "Bearer stub-key", str(REQUESTS[0]["auth"]))
check("tools declared in request", REQUESTS[0]["body"]["tools"][0]["function"]["name"] == "web_search")
check("message order: system,user,assistant,tool",
      [m["role"] for m in sent] == ["system", "user", "assistant", "tool"], str([m["role"] for m in sent]))
check("tool message carries tool_call_id", sent[3].get("tool_call_id") == "c1", str(sent[3]))
check("tool result content passed through", "RESULTS for rag" in sent[3]["content"])

reset([{"message": {"role": "assistant", "tool_calls": [
          tool_call("a", "web_search", {"query": "one"}), tool_call("b", "web_search", {"query": "two"})]}},
       {"message": {"role": "assistant", "content": "final"}}])
agent.run_agent("x")
sent = REQUESTS[1]["body"]["messages"]
tool_msgs = [m for m in sent if m["role"] == "tool"]
check("parallel calls -> one message per call", len(tool_msgs) == 2, str(len(tool_msgs)))
check("each has its own id", {m["tool_call_id"] for m in tool_msgs} == {"a", "b"})

reset([{"message": {"role": "assistant", "tool_calls": [tool_call(f"c{i}", "web_search", {"query": "q"})]}}
       for i in range(agent.MAX_STEPS + 2)])
res = agent.run_agent("loop forever")
check("MAX_STEPS bound stops the loop", res.startswith("[stopped:"), res)
check("bound honoured exactly", len(REQUESTS) == agent.MAX_STEPS, str(len(REQUESTS)))

reset([{"message": {"role": "assistant", "tool_calls": [
    {"id": "z", "type": "function", "function": {"name": "web_search", "arguments": ""}}]}},
    {"message": {"role": "assistant", "content": "ok"}}])
try: agent.run_agent("empty args"); ok = True; err = ""
except Exception as e: ok, err = False, repr(e)
check("empty arguments string handled", ok, err)

reset([{"status": 500, "message": {}}])
try: agent.run_agent("boom"); raised = False
except Exception: raised = True
check("HTTP 500 propagates out of the loop", raised)

reset([{"message": {"role": "assistant", "content": None}}])
check("null content does not crash", agent.run_agent("x") == "[empty response]")

# ---- D. research_to_file ---------------------------------------------------
print("\nD. research_to_file")
reset([{"message": {"role": "assistant", "content": "# Report\n- body"}}])
p = agent.research_to_file("What is RAG, really?")
check("slugified filename", p.name == "what-is-rag-really.md", p.name)
check("file written under reports/", p.parent == REPORTS and p.read_text().startswith("# Report"))

agent.web_search = _orig
print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL: print("FAILED:", FAIL); sys.exit(1)
