# Day 2 (Alternate Plan) — AI-Assisted Development + Computer Vision

Two halves:

- **Morning:** AI-assisted development end to end planning, coding, debugging, testing, documentation —> building one project: an **Astro.js + React portfolio site**.
- **Afternoon:** build a **computer-vision hand-gesture controller with MediaPipe**, using the AI-assist workflow learned in the morning.

**Core** for the whole day: Students must be able to say the specification/working logic and know what they accepted, and what they rejected.

---

## Day 2 outcomes

By 17:00 every pair should have:

- a written `PLAN.md` they wrote **before** touching the assistant
- an `ASSISTANT_LOG.md` recording one accepted suggestion, one rejected suggestion, one bug the assistant misdiagnosed
- a working `.agents/` config in their repo (one rule, one workflow, one subagent)
- a portfolio site running locally, deployed to a public URL, in their own GitHub repo/Cloudflare Pages.
- a webcam hand-gesture demo that changes something visible on screen

---

## Schedule

| Time | Mode | Session | Student evidence |
|---|---|---|---|
| 09:00–09:30 | Explain | Before AI: what "development" actually is & Need of AI in coding, When to use AI, when not to | Repo created, first commit pushed |
| 09:30–10:00 | Explain | Things to know: tokens, context window, hallucinations, prompting & File structure of Ai Agent(claude/antigravity) | Token count of own prompt; one hallucination caught |
| 10:10–10:30 | Explain + activity | Create first plan.md manually. Enhance it with AI.   | They should be able to describe the problem |
| 10:30–10:45 | Break | — | — |
| 10:45–11:20 | Demo | AI-assisted workflow on live code: spec → plan → challenge → diff review → test → debug → document ( portfolio sample) | Notes on the one suggestion instructor rejected |
| 11:20–12:45 | Guided build | **Lab A: portfolio site (steps 1–5)** — Astro + React, assistant-driven, reviewed | Site running locally, sections rendered |
| 12:45–13:30 | Lunch | — | — |
| 13:30–14:00 | Explain + demo | Agents: How agents work? How subagents works? Can We build Own agents? | One workflow and one subagent working in own repo |
| 14:00–14:20 | Demo | MediaPipe: what a landmark is, how a "model" here is 21 points, not deep learning homework | Predicted landmark IDs before running |
| 14:20–15:50 | Guided build | **Lab B: hand-gesture controller (steps 1–6)** | Webcam → landmarks → gesture → visible action |
| 15:50–16:05 | Break | — | — |
| 16:05–16:45 | Guided build | **Lab A continued (steps 6–8)**: embed CV demo, deploy portfolio, README | Live URL, deployed site with demo |
| 16:45–17:00 | Checkpoint | Commits both project. | Day 2 commit and checkpoint record |

Approximate balance: ~1h50m explanation, ~1h15m demo, ~3h55m student build.

---

# Part 1 — Before AI-assisted development

## 1.1 Understand plain development first

An assistant that writes code you cannot read is a liability. Ten minutes on the unglamorous loop:

```text
edit file → run it → read error → change one thing → run again
```

**Everything the assistant does is this loop, faster. If a student cannot do the loop by hand, they cannot review the loop done for them.**

Minimum floor before any AI tool opens:

- open a folder in VS Code, create a file, run it in the integrated terminal

**Start point (VS Code + GitHub, ≤10 min, no accounts blocked):** create repo on GitHub → clone → edit `README.md` → commit → push → see it on github.com. Everyone finishes this. It is the first rung of the ladder and the repo every later step grows into.

## 1.2 Things to know before prompting

### Token

A token is the unit the model reads and bills. Roughly **1 token ≈ 4 characters ≈ 0.75 English words**; code tokenizes worse than prose (indentation, symbols, long identifiers all cost).

Why it matters:

- **Cost** is per token, input and output.
- **Speed** is per output token.
- **Limits** are counted in tokens, not files.

Practical rule: pasting a whole 2,000-line file to fix a 5-line function is paying for 2,000 lines of distraction.

*Activity (5 min):* paste a prompt into any tokenizer viewer, then paste the same text as code. Note the difference.

### Context window

The context window is everything the model can see at once: system prompt + rules files + conversation + files read + tool output + its own replies. It is not memory. When the window relevant material is dropped or summarized this leads an assistant to "forgets" the decision made 40 minutes ago.

Approximate windows (verify at the freeze check before delivery — these change often):

| Model family | Approx. input context |
|---|---|
| Gemini (Pro tier, Antigravity default) | ~1M tokens |
| Claude (Opus/Sonnet tiers) | ~200K standard, 1M on some tiers |
| GPT (frontier tiers) | ~400K |
| Local/open models (7B–14B class) | 8K–128K depending on build |

Teaching points:

- A big window is not free: more context = slower, costlier, and often *worse* attention on the part that matters.
- "Context rot": accuracy degrades as irrelevant material accumulates. Long chats get dumber.
- Fix: start a new session per task; give files deliberately, not by dumping the repo.

### Hallucination

The model predicts plausible next tokens. Plausible ≠ true. It will confidently invent:

- npm packages that do not exist
- function/props names that "should" exist in a library
- config keys, CLI flags, API endpoints
- citations and version numbers

It hallucinates hardest where it has least training signal: brand-new frameworks, your private code, exact version-specific APIs, precise numbers.

Defense: **anything the assistant asserts about the outside world must be executed or checked, not read and believed.** 

*Demo (must be live):* ask for a MediaPipe or Astro API detail with a slightly wrong premise and let it agree. Show the failure, then show the same question asked with docs supplied.

### How to prompt

Prompt structure that works for code:

```text
CONTEXT: what the project is, what file, what stack/version
GOAL:    the one change wanted
CONSTRAINTS: what must not change; style; libraries allowed
OUTPUT:  a plan / a diff / one file — say which
CHECK:   how we will know it worked
```

Rules of thumb:

- One task per prompt. Two tasks = two half-done tasks.
- Ask for a **plan before code** on anything over ~30 lines.
- Give the error text verbatim; never paraphrase an error.
- Say what you already tried, so it stops suggesting that.
- "Make it better" produces noise. "Reduce re-renders on the project list" produces a diff.
- Ask for the **smallest** change that satisfies the check.

Anti-patterns to name out loud: dumping the whole repo, accepting a 400-line diff, arguing with the model instead of restarting the session, asking the model why it lied.

## 1.3 When to use AI

| Use it for | Why it is safe |
|---|---|
| Boilerplate code | High-volume, low-judgment, instantly verifiable (config, scaffolds, CRUD, forms, test fixtures) |
| Learning new syntax/frameworks | Faster than doc-hunting; you verify by running it |
| Refactoring | You already know the correct behavior, so you can spot a wrong rename |
| Commenting / docstrings | Cheap, reviewable, improves the repo |
| Stuck on a syntax error | Machine reads the parser message better than a tired student at 4pm |

Add: translating between languages, writing regex, generating test cases, explaining unfamiliar code, writing commit messages and README sections.

## 1.4 When NOT to use AI

| Avoid for | Why |
|---|---|
| Security-related code | Auth, crypto, session, input sanitizing. Trained on years of insecure Stack Overflow answers. Wrong here = exploitable, and it looks fine. |
| Secrets / API keys | Never paste keys into a prompt. They land in logs, provider history, and sometimes in generated files committed to git. |
| Complex logic | Business rules, edge cases, concurrency, money math. Assistants produce code that *runs*, not code that is *right*. |
| Domain you don't know | You cannot review what you cannot evaluate. Generating medical/finance/legal logic blind is generating liability. |
| System architecture design | Ask for options and trade-offs; do not adopt a proposal you cannot defend. It optimizes for common, not for your constraints. |

---

# Part 2 — Agents and the assistant workflow

## 2.1 The workflow (demo, then repeated in every lab)

1. Write the requirement and acceptance criteria **with the assistant closed**.
3. Ask for a **plan, no code**.
4. Challenge at least one assumption; require a revision.
5. Approve **one** step.
6. Review the diff line by line; reject anything unexplained.
7. Run it. Reproduce the failure.
8. Hand over evidence (error text, input, output), not a guess.
9. Apply the smallest fix.
10. Update the docs with what you actually verified.

The instructor demo must include one suggestion rejected out loud, with the reason.

## 2.2 Agents — Antigravity as the reference tool

Agentic assistants (Antigravity, Claude Code, Copilot agent mode, Cursor) are the **same shape**: a model in a loop with tools, permission gates, and a project scope. Learn one properly; the rest map over.

**Antigravity concepts to demo:**

- **Projects** define the folders/repos an agent can touch.
- **Agent Manager vs Editor** — manage several agents working in parallel, or stay in the file view. Agents can run in a **worktree** so a bad run does not wreck the working copy.
- **Artifacts** — the agent produces a **task list**, an **implementation plan**, and a **walkthrough** with screenshots. Review the *plan artifact*, not the diff, when the change is big.
- **Browser control** (`/browser`) — the agent drives Chrome to verify the UI it just wrote. This is why the portfolio is a good target.

**File structure (workspace root):**

```text
your-repo/
├── .agents/
│   ├── rules/        # always-on / glob-scoped conventions (12k char limit per file)
│   ├── workflows/    # step sequences, invoked as /workflow-name (12k char limit)
│   ├── skills/       # on-demand knowledge; each is a folder with SKILL.md
│   └── agents/       # subagent definitions: <name>.md with YAML frontmatter
└── AGENTS.md         # project-level instructions
```

Global equivalents live under `~/.gemini/` (`GEMINI.md` for global rules, `config/agents/` for global subagents). The older `.agent/` folder name still works.


**Subagents.** A subagent is a separate agent with its own clean context, invoked by the main agent, running in parallel. Point: **context hygiene** — a codebase search or a test run should not fill the main agent's window with noise.

Definition format — `.agents/agents/<name>.md`:

```markdown
---
name: test-runner
description: Runs the test suite and reports only failures with file:line.
tools: [view_file, run_command]
model: flash
---
Run the project's tests. Report only failing tests: name, file:line, and the
assertion message. Do not fix anything. Do not summarize passing tests.
```

`description` is what the planner uses to decide delegation — write it as a trigger, not as a title. Built-in subagents include `research` (codebase exploration), `browser` (sandboxed web testing), and `self`. Nesting is capped at 10 levels; subagents inherit the parent's permissions and sandbox settings.

**Tool mapping (same concepts, different names):**

| Concept | Antigravity | Claude Code | GitHub Copilot |
|---|---|---|---|
| Project instructions | `AGENTS.md`, `.agents/rules/` | `CLAUDE.md` | `.github/copilot-instructions.md` |
| Custom slash command | `.agents/workflows/*.md` | `.claude/commands/*.md` | prompt files / `.github/prompts` |
| Subagent | `.agents/agents/*.md`, `invoke_subagent` | `.claude/agents/*.md`, Task tool | agent mode delegation |
| On-demand knowledge | `.agents/skills/<name>/SKILL.md` | Skills | — |
| External tools | MCP | MCP | MCP |
| Isolation | worktree mode | worktrees | branches |

Say plainly: **conceptually Claude Code looks the same.** 

---

# Part 3 — Lab A: Astro.js + React portfolio (AI-assisted, reviewed)


**Why Astro + React:** Astro ships zero JS by default and gives fast static pages; React `islands` are added only where interactivity is genuinely needed. That contrast is itself the teachable point — students see *why* a framework choice matters instead of being told.

Acceptance criterion, stated up front:

> A public URL showing your name, three project cards, an interactive filter, and your Day 2 gesture demo — from a repo whose every file you can explain.

### Step 1 — Scaffold (10 min, no assistant)

```bash
npm create astro@latest my-portfolio   # choose: empty / minimal, TypeScript optional
cd my-portfolio && npm install && npm run dev
```

Open `localhost:4321`. Commit. **Everyone reaches a running site inside 10 minutes.** No credentials, no API keys.

Self-check: page loads, edit `src/pages/index.astro`, see hot reload.

### Step 2 — Write the spec by hand (10 min, assistant closed)

Create `PLAN.md`:

```text
Goal:       personal portfolio, one page, deployed
Sections:   hero (name, one line, links) | projects (3 cards) | about | contact
Data:       projects live in src/data/projects.json — not hardcoded in markup
Interactive: tag filter on the project list (React island)
Must:       mobile-readable, no secrets in repo, builds with `npm run build`
Done when:  public URL loads and the filter works
```

This file is graded. A pair that lets the assistant write the spec has skipped the lesson.

### Step 3 — Plan, then challenge (15 min)

Ask the agent to read the repo and propose an implementation plan **with no code changes**. Then challenge one assumption and require a revision. Typical honest challenges:

- "Why is the whole page a React component? Astro renders static HTML — which part actually needs to be an island?"
- "Why Tailwind? Add the cost of that decision to the plan or drop it."
- "You planned 6 files. Do it in 3."

Record the challenge and the outcome in `ASSISTANT_LOG.md`.

### Step 4 — Build static sections React  (20 min)

Add a tag filter as a React component, mounted with a `client:` directive:

```astro
---
import ProjectFilter from '../components/ProjectFilter.jsx';
import projects from '../data/projects.json';
---
<ProjectFilter client:load projects={projects} />
```


### Step 6 — Break it, then debug with the assistant (20 min, after lunch block)

Instructor injects one bug per pair (swap `props`, break a key, wrong import path). Rule: **give the assistant the error and the reproduction, not a theory.** Log whether its first diagnosis was right. It often is not — that data point is the lesson.

### Step 7 — Embed the CV demo (15 min)

Add the afternoon gesture demo to `projects.json` with the screenshot/GIF produced in Lab B. Same artifact, grown again.

### Step 8 — Deploy + document (25 min)

```bash
npm run build      # must pass before deploying
```

Deploy the static output (Netlify drop, Vercel, GitHub Pages, or Cloudflare Pages — pick whichever the room's network tolerates). Then have the assistant draft the README and **cut everything untrue from it**. Deleting the assistant's exaggerations is part of the exercise.

`README.md` must contain: what it is, stack, how to run locally, live URL, screenshot, what you would do next.

**Required artifact — `ASSISTANT_LOG.md`:**

```text
What I specified before prompting:
What the assistant planned:
The assumption I challenged, and what changed:
What I accepted unchanged:
What I rejected or rewrote, and why:
A bug the assistant misdiagnosed first:
What I verified by running, not by reading:
What I still do not fully understand in this code:
```

The last line is graded as honesty. It is usually the best interview answer a student takes home.

**Stretch (fast finishers only, after the checkpoint):** add a blog collection with Astro content collections; add dark mode; write a `.agents/workflows/new-project-card.md` workflow and invoke it as `/new-project-card`; add a `test-runner` subagent; run Lighthouse and fix the two worst scores.

---

# Part 4 — Lab B: hand-gesture controller with MediaPipe

**Framing:** this is computer vision without a GPU, without a dataset, and without training. MediaPipe hand tracking gives **21 landmarks per hand**, each with x, y, z. Once you have 21 points, "gesture recognition" is ordinary geometry — distances and comparisons. That is the demystification.

```text
webcam frame → MediaPipe Hands → 21 landmarks → your rule/classifier → action
```

Setup (test on the actual room laptops the day before):

```bash
pip install mediapipe opencv-python
```

If a laptop has no webcam or the install fails, fall back to a supplied video file — the same pipeline runs on `cv2.VideoCapture("hand.mp4")`.

### Step 1 — Webcam window (10 min)

Read frames, show the window, quit on `q`. Nothing else. Everyone gets a window on screen fast.

Self-check: your face on screen, `q` closes it cleanly.

### Step 2 — Draw landmarks (15 min)

Run MediaPipe Hands, draw the 21 points and the connections. Payoff is immediate and it is the moment the room wakes up.

```python
import cv2, mediapipe as mp

mp_hands, mp_draw = mp.solutions.hands, mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok: break
        frame = cv2.flip(frame, 1)
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if result.multi_hand_landmarks:
            for lm in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
        cv2.imshow("hand", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
cap.release(); cv2.destroyAllWindows()
```

Landmark indices needed later (given, so difficulty comes from thinking, not from hunting): wrist `0`, thumb tip `4`, index tip `8`, middle tip `12`, ring tip `16`, pinky tip `20`, index MCP `5`.

Self-check: move your hand, points follow. Note that x, y are **normalized 0–1**, not pixels — multiply by frame width/height.

### Step 3 — Count fingers (20 min)

Rule: a finger is "up" when its tip landmark is above its PIP joint (smaller y). The thumb needs an x comparison instead — ask students *why* before telling them.

Print the count on the frame with `cv2.putText`. A number that moves when they move: the visible payout.

Self-check: open palm → 5, fist → 0, peace sign → 2.

### Step 4 — Gestures from geometry (20 min)

Define three gestures from the finger-count and one distance:

| Gesture | Rule |
|---|---|
| Open palm | 5 fingers up |
| Fist | 0 fingers up |
| Pinch | euclidean distance(landmark 4, landmark 8) < threshold |

Threshold problem is deliberate: a fixed pixel threshold breaks when the hand moves closer to the camera. Correct fix is normalizing by hand size (e.g. distance 0→5). Let them hit the bug first, then fix it — a diagnosed bug is a step payout.

### Step 5 — Make it control something (20 min)

Pick one, all visible:

- pinch distance → volume or on-screen slider value
- open palm / fist → play/pause a video or toggle a colored rectangle
- index-finger tip → draw a trail on the frame (air-drawing)

Acceptance criterion: **a stranger walking past can tell it is working without being told.**

### Step 6 — Stabilize, then record (15 min)

Raw per-frame classification flickers. Fix with a small deque and majority vote over the last N frames — that is temporal smoothing, and it is the same idea used in real deployed CV. Then record a short screen capture / GIF for the portfolio.

Self-check: label stops flickering; recording saved into the portfolio repo.

**Where AI-assist belongs here (and where it does not):**

- Use it for: OpenCV boilerplate, `putText` arguments, the deque smoothing, refactoring gesture rules into a function.
- Do it yourself: the gesture rules and thresholds. That is the judgment part, and it is what a viva will ask about.

**Stretch:** two-hand support; collect ~50 landmark samples per gesture and train a small `sklearn` classifier, comparing it against the rules (this is where "rules vs learned model" becomes concrete); serve results to the portfolio page over a small FastAPI endpoint; measure FPS and speed it up.

---

## Checkpoint (16:45–17:00)

Each pair, in 90 seconds:

1. Show the deployed portfolio URL.
2. Show the gesture demo running.
3. Point at one file and explain it line by line (instructor picks the file).
4. Read out the "rejected or rewrote" line from `ASSISTANT_LOG.md`.

Traffic light: green = deployed + demo works, amber = both run locally, red = blocked (record the blocker; it becomes the first thing fixed on Day 3).

A pair who cannot explain their own portfolio code has not finished the lab, regardless of how good the site looks.

---

## Instructor preparation

- Reference implementations finished and working offline: portfolio repo + gesture script.
- Node LTS, Python 3.11+, `mediapipe`, `opencv-python` pre-installed or wheels cached; MediaPipe model files pre-downloaded.
- `npm create astro` cache warmed, or a pre-scaffolded zip for the low-bandwidth fallback.
- Deploy fallback chain: Netlify drag-and-drop → GitHub Pages → local `npm run preview` if the network is dead.
- Backup hand video file for laptops without webcams.
- 12 printed snippet cards for the use/don't-use sorting activity.
- One bug per pair prepared for Step 6.
- Antigravity (or Claude Code / Copilot) installed and signed in, with quota checked, on at least the instructor machine.

---

## Sources

- [Antigravity — Subagents](https://antigravity.google/docs/subagents)
- [Antigravity — Rules and Workflows](https://antigravity.google/docs/rules-workflows)
- [Antigravity — Getting Started](https://antigravity.google/docs/getting-started)
- [Astro docs — Islands architecture and `client:` directives](https://docs.astro.build/en/concepts/islands/)
- [MediaPipe — Hand landmark detection](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)

Model context-window figures and tool file paths change fast. Re-verify both at the pre-delivery freeze check ([10-sources-and-freeze-checks.md](10-sources-and-freeze-checks.md)).
