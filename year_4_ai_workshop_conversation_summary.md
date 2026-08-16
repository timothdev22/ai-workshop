# Fourth-Year Generative AI Workshop — Conversation Summary

## 1. Context

The existing proposal is a 4-year Generative AI / AI Productivity Skill Development Program for B.Tech Artificial Intelligence & Data Science students at AKT Memorial College of Engineering and Technology.

The proposal progresses broadly as:

- **Year I:** Generative AI & AI Productivity Tools
- **Year II:** AI Agents & Intelligent Application Development
- **Year III:** MLOps & AI Deployment
- **Year IV:** Enterprise AI, Advanced Applications & Career Readiness

The proposal states that the program is intended to be hands-on, industry-oriented, and practical, with technical sessions, demonstrations, guided laboratory activities, mini-projects, assessments, and career readiness.

The current Year IV plan is:

### Day 1 — Enterprise AI & Responsible AI
- Enterprise AI applications
- Responsible AI
- Ethics
- Governance
- Data privacy
- Enterprise AI case studies and practical exercises

### Day 2 — AI-Assisted Software Development
- AI-assisted coding
- Debugging
- Documentation
- Testing
- Productivity
- AI coding assistants and software development tools

### Day 3 — Capstone Project & Career Readiness
- AI solution development
- Technical assessment
- Resume enhancement
- Interview preparation
- AI-based capstone project
- Technical presentation
- Resume optimization
- Mock interview

The proposal also states that the overall training duration is **3 days / 8 hours per day / 24 hours total**.

---

## 2. Initial concern about Year IV

The main concern was that Year IV felt too vague and not technically advanced enough for final-year AI & Data Science students.

The existing Year IV material focuses heavily on:
- Enterprise AI awareness
- Responsible AI
- AI-assisted software development
- Career preparation

It does not explicitly provide enough practical depth on modern AI engineering topics such as:
- Building RAG systems from scratch
- Fine-tuning models
- Creating AI agents from primitives
- Using agent frameworks
- Building and deploying an end-to-end AI application

The proposed improvement was therefore to make Year IV much more implementation-oriented.

---

## 3. Initial proposed technical direction

The initial idea was to teach students a practical progression:

1. High-level understanding of how AI / LLMs work
2. RAG overview
3. Build a RAG system
4. Explain fine-tuning
5. Create a small dataset
6. Fine-tune a model
7. Explain AI agents
8. Build a simple agent from scratch
9. Build an agent using a built-in/framework library
10. Build an AI application using these concepts

A preferred teaching format was:

> Roughly 30 minutes of explanation followed by around 2 hours of hands-on implementation.

The goal was to avoid excessive theory and make students actually build things.

---

## 4. Important prerequisite questions

Before finalizing the curriculum, it was identified that the college should provide more information about the students.

The proposal says the students are **B.Tech Artificial Intelligence & Data Science students**, and says they have a strong theoretical foundation in AI, Machine Learning, Deep Learning, and Data Analytics.

However, the proposal does NOT establish their actual hands-on proficiency.

Important questions to ask the college:

### Student background
- What year/semester are the students currently in?
- What subjects have they already completed?
- Have they studied:
  - Python
  - Data Structures
  - Machine Learning
  - Deep Learning
  - NLP
  - Neural Networks
  - Databases / SQL
  - Web development
  - Cloud
  - MLOps?

### Existing GenAI experience
- Have they used LLM APIs?
- Have they built an LLM application?
- Have they previously built RAG systems?
- Have they used vector databases?
- Have they used AI agents?
- Have they used Hugging Face?
- Have they used PyTorch / TensorFlow?

### Software engineering
- Are they comfortable with Python?
- Have they used REST APIs / JSON?
- Have they used Git/GitHub?
- Can they create and manage Python environments?
- Can they debug a basic application?

### Infrastructure
- How many students will attend?
- How many laptops will actually be available?
- Will students have individual laptops or share?
- What are the laptop specifications?
- Is GPU access available?
- How reliable is the internet?
- Can students create GitHub and AI API accounts before the workshop?

### Program history
A particularly important question:

> Have these students actually completed the Year I–III modules described in the proposal?

The proposal says Year II covers AI Agents, LLM APIs and RAG, while Year III covers Git/GitHub, FastAPI, Streamlit, Docker and AI deployment. However, that describes the proposed curriculum, not necessarily the students' real proficiency.

---

## 5. New information from a previous workshop instructor

A person who conducted a similar workshop provided useful practical feedback:

- Students primarily want to **learn what modern AI is about and explore it**.
- A major takeaway they want is **something they can put on their resume**.
- The previous workshop had serious infrastructure problems:
  - Internet connectivity problems
  - Not all students had laptops
  - Students sometimes had to share laptops
- Students may be familiar with concepts such as Git and APIs but have **limited hands-on experience**.
- It is better NOT to ask students to invent their own project during a short workshop.
- Instead, the instructor should:
  - Give students a predefined project
  - Have a completed/reference implementation ready
  - Guide students through building it
  - Ensure they finish something working
  - Help them put the project on GitHub / resume

This information significantly changes the recommended teaching approach.

---

# 6. Revised core philosophy

The workshop should NOT be:

> Day 1 = RAG  
> Day 2 = Fine-tuning  
> Day 3 = Agents

as three disconnected technical topics.

Instead, the recommended approach is:

> **Understand → Build → Ship**

The entire three-day program should revolve around **one guided, resume-worthy AI application**.

The desired final outcome:

> Every student or pair leaves with a working AI application, a GitHub repository, and ideally a deployed URL that can be included on their resume.

This is more valuable than students merely hearing about several AI concepts.

---

# 7. Recommended revised Year IV structure

## Day 1 — Understanding Modern AI Applications

Because internet/laptop availability may be unreliable, Day 1 should tolerate more theory and demonstrations.

Topics:

- How LLMs work at a high level
- Tokens
- Embeddings
- Context windows
- LLM APIs
- Prompting
- Why hallucinations happen
- RAG
- Chunking
- Embeddings and vector search
- Vector databases
- Tool calling
- AI agents
- RAG vs fine-tuning vs agents
- Enterprise AI use cases
- Responsible AI
- Security and privacy

The instructor should then demonstrate the **complete finished project** students will build.

This gives students a clear destination.

---

# 8. Day 2 — Build the AI Application

Day 2 should be the main hands-on day.

Students should all build the same predefined application rather than inventing their own project.

Recommended approach:

- Provide starter repository
- Provide data/documents
- Provide architecture
- Provide starter code
- Provide expected output
- Have a completed reference implementation ready
- Guide students through the implementation

Potential application architecture:

```text
User
  ↓
Web UI
  ↓
LLM / Agent
  ├── RAG tool
  ├── Search / external tool
  └── Calculator / API
  ↓
Response
```

The application could be an **AI College Assistant** or **AI Research Assistant**, depending on the chosen project.

For example, an AI College Assistant could:

- Answer questions about college documents
- Use RAG to retrieve relevant information
- Use tools such as calculator/search/database
- Use an agent to decide which tool is appropriate

---

# 9. RAG teaching approach

RAG should remain a core practical topic.

Students should understand the basic pipeline:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Top-K Context
    ↓
LLM
    ↓
Answer
```

However, because of time and infrastructure constraints, it may not be wise to make students implement every component completely from scratch.

Recommended teaching sequence:

1. Explain RAG architecture
2. Show a small implementation from primitives
3. Explain what each component does
4. Then use a practical library/vector database for the actual application
5. Integrate the RAG into the final project

The goal is for students to understand what happens inside RAG instead of simply copying a high-level framework call.

---

# 10. Fine-tuning approach

Fine-tuning is valuable, but it should probably NOT be a mandatory core deliverable given the infrastructure.

Potential problems:
- Limited laptops
- No guaranteed GPU
- Internet issues
- Limited time
- Fine-tuning can consume a lot of debugging time

Recommended approach:

### Teach conceptually:
- Prompting vs RAG vs fine-tuning
- Pre-training vs fine-tuning
- Supervised fine-tuning
- Dataset creation
- Training/validation split
- LoRA
- PEFT
- Quantization
- Evaluation

A useful comparison:

| Problem | Typical approach |
|---|---|
| Model needs private/current information | RAG |
| Model needs specific behavior/style/format | Fine-tuning |
| Model needs to use external tools/actions | Agents/tool calling |
| Need to improve instructions/behavior | Prompting / model selection / fine-tuning depending on case |

### Optional hands-on:
Use a prepared Google Colab notebook.

Students can:
1. Inspect a small dataset
2. Modify/create a small dataset
3. Run a small LoRA fine-tuning
4. Compare base vs fine-tuned model

Fine-tuning should be an optional/secondary practical exercise rather than a requirement that every student must successfully complete.

---

# 11. AI Agents approach

Agents should probably be the "wow" part of the workshop.

First explain that an agent is not magic.

A simple conceptual agent loop:

```text
User
  ↓
LLM
  ↓
Does it need a tool?
  ├── No → Final answer
  └── Yes
        ↓
      Call tool
        ↓
      Tool result
        ↓
      LLM
        ↓
      Continue / final answer
```

Then build a tiny agent from primitives.

Possible tools:
- Calculator
- Search
- Database lookup
- Weather/API
- Python function

After students understand the basic loop, introduce an agent framework/library.

The progression should be:

> Agent from scratch → Agent framework → Real application

This helps students understand WHY agent frameworks exist rather than simply copying framework code.

---

# 12. Teach students how to actually ship the application

A key realization from the discussion is that **shipping skills may be more valuable than teaching another theoretical AI topic**.

Students should learn practical steps such as:

### Project structure
- `requirements.txt`
- `.env`
- `.env.example`
- `.gitignore`
- README
- basic error handling
- logging

### Git/GitHub
- Create repository
- Clone repository
- Commit changes
- Push changes
- Publish project
- Avoid exposing API keys

### Deployment
Show them how to take the application and make it accessible through a URL.

Vercel can be used if it fits the chosen architecture, but the learning objective is not "learn Vercel."

The objective is:

> **Take an AI application and make it accessible through a working URL.**

If another deployment platform is simpler for the chosen stack, use that instead.

---

# 13. Day 3 — Finish, Deploy & Portfolio

The current proposal's Capstone & Career Readiness concept can be retained, but the meaning of "capstone" should change.

Students should NOT be asked to independently invent an AI solution.

Instead:

> Finish, customize, deploy and present the application they built during Day 2.

Activities:

### Finish the application
- Debug
- Improve prompts
- Test RAG
- Improve UI
- Add/modify a tool
- Handle errors

### GitHub
Create a clean repository:

```text
my-ai-agent/
│
├── app/
├── data/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── ...
```

### README
Students should document:
- Problem
- Solution
- Architecture
- Technologies
- How RAG works
- How the agent works
- Screenshots
- Demo URL
- Future improvements

### Resume
Instead of:

> "Attended Generative AI workshop"

students can have a project entry describing what they actually built, e.g.:

> **AI Research Assistant — Generative AI Project**  
> Developed and deployed an AI-powered research assistant using LLMs, Retrieval-Augmented Generation (RAG), vector search and tool-calling agents. Implemented document retrieval and AI-powered question answering and deployed the application as a web service.

---

# 14. Suggested three-day structure

| | Day 1 | Day 2 | Day 3 |
|---|---|---|---|
| Theme | **Understand** | **Build** | **Ship** |
| Theory | High | Low | Low |
| RAG | Explain | Implement | Integrate |
| Agents | Explain + demo | Implement | Improve |
| Fine-tuning | Explain/demo | Optional Colab | — |
| Coding | Demo | Heavy | Heavy |
| Git | Intro | Use | Publish |
| Deployment | Demo | Prepare | Deploy |
| Resume | — | — | Major focus |
| Project | See finished product | Build it | Finish + present |

This also preserves the original proposal's intended themes:

- Enterprise AI → contextualize why the application matters
- Responsible AI → cover safety/privacy/governance
- AI-assisted development → use AI coding assistants while building
- Capstone → complete the guided application
- Career readiness → GitHub + deployment + README + resume + presentation

---

# 15. Teaching format

The preferred teaching philosophy is:

### 20–30% explanation
### 60–70% implementation
### 10–20% challenge/evaluation

An 8-hour day could roughly contain:

- 45 min conceptual session
- 30 min live coding/demo
- 2 hours guided hands-on
- Break
- 2 hours hands-on challenge
- Debugging/Q&A
- Mini-project/assessment
- Review

The exact timing can be adjusted based on infrastructure and student proficiency.

---

# 16. Laptop/infrastructure strategy

The workshop should be designed assuming **2 students may need to share one laptop**.

Rather than treating this purely as a limitation, use pair programming:

- **Driver:** operates the laptop
- **Navigator:** reads instructions, thinks through code, catches errors
- Swap roles every 20–30 minutes

The workshop should also be prepared for three infrastructure levels:

### Level 1 — Internet works
Normal APIs and cloud services.

### Level 2 — Internet is slow
Use:
- Prepared datasets
- Cached files
- Prebuilt vector database
- Fewer API calls
- Colab

### Level 3 — Internet completely fails
Still be able to teach:
- Architecture
- Code walkthrough
- RAG mechanics
- Agent loop
- Fine-tuning concepts
- Git concepts
- Deployment walkthrough

The instructor should have the complete project working beforehand and be able to demonstrate it without relying on students' environments.

---

# 17. Pre-work / prerequisite material

The idea of sending **1–2 hours of prerequisite videos before the workshop** is strongly supported by the new constraints.

Possible pre-work:

### 30 min — Python/API basics
- Python functions
- JSON
- REST APIs
- Environment variables
- Calling APIs

### 20 min — ML/LLM fundamentals
- Neural networks
- Tokens
- Embeddings
- LLMs
- Transformer intuition

### 20 min — Git/GitHub
- Clone
- Commit
- Push
- Pull

### 20 min — GenAI basics
- Prompting
- LLM API
- Basic Python + LLM application

Then provide a setup guide and ideally a small setup-checking script.

The goal is to avoid spending workshop time teaching basic syntax or fixing everyone's environment.

---

# 18. Most important unresolved questions for the college

Before finalizing the Year IV curriculum, ask:

1. How many fourth-year students will participate?
2. How many laptops will actually be available?
3. Will students have individual laptops or share?
4. What are the laptop specifications?
5. What internet bandwidth/reliability will be available?
6. Can students create GitHub accounts beforehand?
7. Can students create required AI API accounts beforehand?
8. Can prerequisite videos/materials be sent before the workshop?
9. Have the students previously completed the Year I–III modules in the proposal?
10. What is their actual proficiency in Python?
11. What is their actual ML/DL proficiency?
12. Have they previously used LLM APIs?
13. Have they previously built RAG systems?
14. Have they previously used AI agents?
15. Have they used Git/GitHub in real projects?
16. Do they have access to GPU/Colab?
17. What does the college expect students to achieve at the end of the program?

---

# 19. Final recommended philosophy

The strongest version of this workshop is NOT:

> "Teach students RAG, fine-tuning and agents."

It is:

> **"Teach students how modern AI applications are built, then guide them through building and shipping one themselves."**

The technologies become the means:

```text
LLM
 │
 ├── Prompting
 │
 ├── RAG
 │    ├── Embeddings
 │    ├── Chunking
 │    ├── Retrieval
 │    └── Vector DB
 │
 ├── Fine-tuning
 │    ├── Dataset
 │    ├── SFT
 │    ├── LoRA/PEFT
 │    └── Evaluation
 │
 └── Agents
      ├── Tools
      ├── Function calling
      ├── State
      ├── Agent loop
      └── Framework
           ↓
      AI Application
           ↓
      GitHub
           ↓
      Deployment
           ↓
      Resume / Portfolio
```

The key outcome should be:

> **Students leave with something that actually works and that they can show someone.**

This is likely to be more memorable and useful to the students than trying to maximize the number of GenAI concepts covered in three days.

---

## Source note

The uploaded proposal confirms that the target audience is B.Tech AI & Data Science students, that the program is intended to be hands-on and industry-oriented, that Year II already proposes AI Agents/RAG, Year III proposes deployment/MLOps, and that Year IV currently focuses on Enterprise AI, AI-assisted software development, capstone work and career readiness. fileciteturn0file0L96-L102 fileciteturn0file0L197-L228 fileciteturn0file0L229-L258 fileciteturn0file0L259-L296

The infrastructure constraints, student behavior, and workshop observations in this summary come from the discussion with the user and the feedback they received from another workshop instructor.
