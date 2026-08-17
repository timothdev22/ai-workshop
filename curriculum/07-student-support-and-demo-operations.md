# Student support and demo operations

## Fast pairs: depth, not a second project

**Every pair builds the common project.** There is no independent-domain track.

An earlier version of this curriculum allowed strong pairs to propose their own domain behind an approval gate. That was dropped deliberately. With 30 pairs, one lead instructor, and two assistants who may not materialise, a variant track creates a second curriculum to support—separate data problems, separate failure modes, separate debugging—consuming the scarcest resource in the room on behalf of the students who need it least. It also rewards ambition with a higher chance of finishing Day 3 with nothing demonstrable.

Fast pairs are redirected into **depth on the same system**, which costs no additional instructor surface and produces better interview evidence than a shallower second project would.

### Stretch tracks

Offered only after a pair is green on the current checkpoint. A pair may work through several.

**Retrieval depth**

- Implement hybrid retrieval—keyword plus semantic—and measure whether it helps on identifier-heavy queries.
- Compare two chunking strategies on the same case file and explain the difference in the results, not just report it.
- Add a reranking step and measure whether it earns its latency cost.
- Build a case the current pipeline cannot answer, and explain precisely why.

**Evaluation depth**

- Expand the case file past 25 cases with genuinely hard examples rather than easy ones.
- Add a second scorer and measure agreement with the first on the same cases.
- Add regression detection so the harness fails when a previously passing case breaks.
- Chart metric movement across the pair's own commits.

**Adversarial depth**

- Write three new prompt-injection payloads that defeat the pair's current mitigation, then fix them.
- Attack a neighbouring pair's system and file the finding as a reproducible report.
- Test excessive-agency paths: can the assistant be persuaded to skip the approval boundary?
- Probe the MCP surface for capabilities that should not be exposed.

**Engineering depth**

- Add unit tests for tool schema validation and error behavior.
- Compare ambiguous and precise tool descriptions and measure the routing difference.
- Deploy the MCP server over Streamable HTTP through Coolify, with authentication, HTTPS, origin validation, and least privilege.
- Complete the fine-tuning notebook end to end from the take-home package.

Cross-pair attack exercises are the highest-value stretch task in the list: they occupy strong pairs productively, generate real findings for the pairs being attacked, and turn into the best answers to the "how could this be attacked?" interview question.

### Domain variation, kept cheap

Pairs who want their work to feel like their own may swap the **document corpus** while keeping the architecture, tools, evaluation harness, and safety boundaries identical. Instructor-approved corpora only, prepared in advance:

- healthcare administrative-policy assistant, explicitly non-diagnostic
- electronics manual and troubleshooting assistant
- sales enablement and product-knowledge assistant
- software repository/runbook assistant
- college policy assistant

This gives portfolio differentiation at near-zero support cost, because every failure mode remains one the instructor has already seen thirty times.

## Participation and demonstration model

There is no grade. Use checkpoint evidence to keep all pairs moving.

### Pair checkpoint board

Track each pair after the major labs:

```text
Grey   = not started
Red    = blocked after documented attempts
Amber  = runs but acceptance check fails
Green  = acceptance check passes and both students can explain it
Blue   = stretch task, only after green
```

Green requires explanation by either partner, not merely a successful screen.

### Help protocol for 30 pairs

Before calling the instructor, a pair should:

1. Read the error and record the exact failing command/case.
2. Check the relevant troubleshooting card.
3. Compare with the last checkpoint output.
4. Ask the neighboring pair in its five-pair pod.
5. Add a concise blocker to the shared issue board.

This prevents the instructor from solving the same setup issue 15 times and teaches good bug reporting.

### Demo carousel

Organize six pods of five pairs. All pods demonstrate simultaneously.

Each pair gets three minutes:

- 30 seconds: problem and intended user
- 60 seconds: evidence-backed question and citation
- 30 seconds: tool or MCP call
- 30 seconds: one failure, evaluation result, and improvement
- 30 seconds: contribution and next step

Peers use a completion checklist, not a score. The instructor rotates, then selects several spotlight demonstrations for the room if time permits. Each pair also submits a short saved demo or screenshots so participation evidence does not depend only on what the instructor happened to observe.

