# Scope and success measures

## Deliberate scope exclusions

To protect completion and career impact, do not spend core workshop time on:

- transformer mathematics beyond useful intuition
- training a large foundation model
- fine-tuning `gpt-oss-120b` in Colab
- a student-run fine-tuning lab; the workflow is demonstrated and the decision is assessed, and the notebook goes home
- multi-agent swarms or role-play demos without measured need
- implementing MCP's JSON-RPC protocol manually
- production OAuth implementation for remote MCP
- MCP beyond a thin adapter over already-tested services
- many interchangeable frameworks
- independent student-chosen domains requiring separate instructor support
- an open-ended hackathon before students complete the common core
- coding-assistant use before students can recognise correct code for this system
- polished UI work before the evaluation set passes
- generic enterprise case-study presentations
- resume generation unsupported by a real project
- legal claims that have not been verified for the relevant jurisdiction and date

## Workshop definition of success

The workshop succeeds when most pairs can demonstrate all core items and explain them without reading generated text:

```text
[ ] Calls gpt-oss-120b through the configured Nscale service
[ ] Retrieves and cites supporting evidence
[ ] Admits when evidence is missing
[ ] Uses or avoids the expected tool on representative cases
[ ] Stops safely and validates tool inputs
[ ] Exposes a tested capability through a local MCP server
[ ] Explains when fine-tuning would be the right tool here and why it was not used
[ ] Runs a 15-case evaluation set through a harness the pair built and can explain
[ ] Shows a before/after results comparison for one improvement driven by that evidence
[ ] States what a coding assistant generated, what was rejected, and how the rest was verified
[ ] Demonstrates one security or Responsible AI control
[ ] Runs locally and has a deployment path
[ ] Contains no committed secrets
[ ] Includes README, architecture, evaluation, and limitations
[ ] Contains an honest contribution statement and resume bullet
[ ] Both partners can give a short technical explanation
[ ] Each student states how they would build the next version independently
```

Attendance alone is not the desired result. A working screen alone is also not the desired result. The intended result is a student who can build, verify, communicate, and continue learning.

