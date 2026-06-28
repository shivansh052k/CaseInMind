# CaseInMind — Project Progress

## Problem Statement

### Context

Civil litigation in the United States is a multi-stage, document-intensive process spanning from case intake through investigation, pleadings, discovery, motions, and settlement — a lifecycle that can stretch across months to years. For a solo litigation attorney, this process demands an enormous amount of paralegal-level groundwork: ingesting and organizing case documents, researching precedents, drafting complaints and motions, managing discovery, and preparing settlement strategies. This work is repetitive, time-consuming, and cognitively expensive — yet it must be done with precision before the lawyer can apply their actual expertise: legal judgment and strategy.

Today, this paralegal work is either done manually by the attorney themselves — stealing time from higher-value work — or outsourced to paralegals and associates, which is financially inaccessible for solo practitioners. Existing AI tools like Eve Legal automate discrete tasks within this workflow, but they are fundamentally **static workflow automation systems** — they do not learn from outcomes, do not reason about strategy, and do not improve over time. They are sophisticated autocomplete, not intelligent agents.

---

### The Problem

**There is no AI system today that acts as a true learning paralegal partner for a solo civil litigation attorney** — one that not only executes paralegal work autonomously across the full pre-trial lifecycle, but continuously learns from lawyer feedback, historical case outcomes, and live case dynamics to improve its decisions, strategies, and outputs over time.

The gap is not in automation. The gap is in **adaptive intelligence** — a system that gets demonstrably better the more it works, that understands the strategic context of a case, and that can be trusted to operate with increasing autonomy as it earns that trust through verifiable, measurable performance.

---

### What We Are Building

**CaseInMind** — A Civil Litigation AI Paralegal Agent powered by LLMs, multi-agent orchestration, and a hybrid RL framework, designed to serve as an autonomous, continuously learning paralegal partner for solo civil litigation attorneys across Stages 1–7 of the litigation lifecycle, delivered as a full-stack web application.

The system operates across the full pre-trial lifecycle:

- **Stage 1 — Case Intake & Evaluation:** Ingest client documents, extract facts, identify claims, assess case viability, and generate a structured case overview
- **Stage 2 — Pre-Filing Investigation:** Autonomously research similar cases and precedents, identify legal theories, map evidence to claims, and surface weaknesses
- **Stage 3 — Complaint Drafting:** Generate jurisdiction-aware, grounded complaints with verified citations
- **Stage 4 — Pleadings Analysis:** Analyze defendant responses, identify vulnerabilities, and suggest counter-strategies
- **Stage 5 — Discovery:** Generate interrogatories, document requests, and deposition questions; analyze incoming discovery for gaps and inconsistencies
- **Stage 6 — Motion Drafting & Strategy:** Draft motions with grounded legal reasoning; recommend motion strategy based on case posture
- **Stage 7 — Settlement Intelligence:** Analyze comparable case settlements, model likely outcomes, and prepare negotiation strategy briefs

---

### The Technical Differentiation — Hybrid RL at the Core

Unlike existing legal AI tools, CaseMind is not a static system. It is built around a **three-layer hybrid RL framework** that makes it the only legal AI agent that learns:

**Layer 1 — Offline RL (Foundation)**
Before touching any live case, the agent is pre-trained on historical civil litigation data — case outcomes, settlement amounts, motion success rates, discovery patterns — from public sources including CourtListener (9M+ opinions) and the Caselaw Access Project. This gives the agent a strong prior over what good paralegal work looks like and what strategies tend to succeed in which case types.

**Layer 2 — RLHF (Active Learning from the Lawyer)**
During live case work, the lawyer provides structured feedback on every agent output — accepting, rejecting, or editing drafts and research. This feedback trains a reward model that learns the lawyer's preferences, style, risk tolerance, and strategic priorities. Over time, the agent adapts to the specific attorney it works with, producing outputs that require less and less correction.

**Layer 3 — Online RL / RLVR (Outcome-Driven Strategy Optimization)**
As cases progress and resolve — motions succeed or fail, settlements are reached or not, discovery produces useful material or not — these verifiable outcomes serve as reward signals. The agent learns which research strategies, motion approaches, and discovery patterns lead to better case outcomes, continuously refining its decision-making within and across cases.

---

### Evaluation, Monitoring & Observability as First-Class Citizens

CaseMind treats agent quality, performance, and explainability as core system properties — not afterthoughts:

**Evaluation**
- LLM-as-Judge pipelines for output quality assessment at every stage
- Citation verification against real legal databases to prevent hallucination
- Stage-level performance benchmarks — motion success prediction accuracy, settlement estimate error, discovery coverage rate
- Reward model quality tracking to detect signal degradation and drift

**Monitoring**
- Real-time tracking of agent performance metrics across all active cases
- RLHF reward signal health monitoring
- Output quality trends over time — is the agent actually improving?
- Anomaly detection for unexpected agent behavior or output degradation

**Observability**
- Full distributed tracing across the entire multi-agent pipeline
- Every agent decision, tool call, reasoning chain, and intermediate state is captured and traceable
- End-to-end visibility into *why* the agent made a decision — not just *what* it did
- Lawyer-facing audit trail: every action taken by the agent is reviewable before execution
- Developer-facing trace explorer: deep inspection of agent internals for debugging, improvement, and research

---

### Delivery

A full-stack web application providing a lawyer-facing interface for case management, agent interaction, feedback collection, and audit review — with full distributed observability built into the system from day one.

---

### Why This Matters

- **For the lawyer:** A solo attorney gains the equivalent of a continuously improving paralegal that works 24/7, learns their preferences, and gets measurably better with every case
- **For the field:** The first open, research-grade civil litigation AI agent with hybrid RL at its core — filling a gap that commercial products like Eve Legal have explicitly left open
- **For the portfolio:** A full-stack demonstration of LLMs + multi-agent orchestration + hybrid RL + evaluation + monitoring + full distributed observability in a high-stakes, real-world domain

---

### Constraints

- **Compute budget:** $0 — built entirely on free tier APIs, open source models, and free legal data sources (CourtListener, Caselaw Access Project, and equivalents). Zero budget forces the best engineering decisions — build lean, learn what actually matters.
- **Scope:** Civil litigation as anchor domain, architecture designed for extensibility to other legal domains
- **Primary user:** Solo civil litigation attorney
---

## System Architecture

### Overall Architectural Pattern

**Hierarchical Orchestrator-Worker** with an Event-Driven, Asynchronous communication backbone.

- One **Master Orchestrator Agent** owns the case state, decomposes tasks, routes to specialist workers, manages human-in-the-loop checkpoints, and holds the RL decision layer
- **Seven Specialist Worker Agents** — one per lifecycle stage — each focused, specialized, and independently improvable
- A **Free Conversational Agent** sits alongside the pipeline as a privileged agent with full case context access
- All agents share the same memory system, data layer, and observability infrastructure
- Orchestrator receives only summaries and routing signals from workers — never full outputs — to explicitly mitigate context overflow at 7 workers

---

### UX & Application Flow

```
┌─────────────────────────────────────┐
│             DASHBOARD               │
│  [Case Block]  [Case Block]  [+New] │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         CASE CREATION FLOW          │
│  Structured Form + Agentic Flow     │
│  ├── Hard facts (form)              │
│  ├── Document upload + type tagging │
│  └── Agent extracts, clarifies,     │
│      fills gaps autonomously        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         CASE WORKSPACE              │
│  ├── Overview & Case Summary        │
│  ├── Investigation                  │
│  ├── Drafting                       │
│  ├── Pleadings                      │
│  ├── Discovery                      │
│  ├── Motions                        │
│  ├── Settlement                     │
│  ├── Document Hub                   │
│  └── Chat (Free Conversational      │
│           Agent — resizable panel,  │
│           collapsed by default,     │
│           activated via button)     │
└─────────────────────────────────────┘
```

---

### Document Hub

Single unified document repository per case. Every document uploaded with a **type tag** that tells agents how to use it:

- **Case Documents** — core case files, contracts, evidence, medical records, complaints
- **Supporting Documents** — prior citations, precedents, similar verdicts, legal references
- **Discovery Documents** — received discovery materials, depositions, interrogatory responses
- **Court Filings** — filed complaints, motions, orders from the court
- **Correspondence** — emails, demand letters, opposing counsel communications

Documents can be added at **any point** during the case lifecycle. Type metadata flows through the entire memory and retrieval system so agents always know what kind of document they are working with and use it accordingly.

---

### Agent Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        WEB APPLICATION                        │
│                                                              │
│   CASE WORKSPACE                    CHAT INTERFACE           │
│   (Sectional Pages)                 (Free Agent)             │
└────────────────────────────┬─────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                  MASTER ORCHESTRATOR AGENT                    │
│                                                              │
│   Case State Management │ Task Decomposition                 │
│   Stage Routing │ HITL Checkpoints │ RL Decision Layer       │
│   Receives summaries only from workers (context safety)      │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬────────────────┘
   │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│ S1  ││ S2  ││ S3  ││ S4  ││ S5  ││ S6  ││ S7  │
│Intak││Inves││Draft││Plea ││Disco││Motio││Settl│
│Agent││Agent││Agent││Agent││Agent││Agent││Agent│
└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘
   └──────┴──────┴──────┴──────┴──────┴──────┘
                          │
         ┌────────────────▼─────────────────┐
         │      FREE CONVERSATIONAL AGENT    │
         │                                  │
         │  Full case context access        │
         │  Can call any worker on demand   │
         │  Queries legal data layer        │
         │  Interactions feed RLHF signal   │
         │  Feeds back into episodic memory │
         └────────────────┬─────────────────┘
                          │
         ┌────────────────▼─────────────────┐
         │           MEMORY SYSTEM           │
         │                                  │
         │  Working Memory                  │
         │  (current context window)        │
         │                                  │
         │  Episodic Memory                 │
         │  (case actions, decisions,       │
         │   tool calls, HITL interactions) │
         │                                  │
         │  Semantic Memory                 │
         │  (lawyer preferences, style,     │
         │   risk tolerance, jurisdiction   │
         │   patterns across cases)         │
         │  [consolidated from episodic     │
         │   via explicit triggers]         │
         │                                  │
         │  Procedural Memory               │
         │  (learned strategies, motion     │
         │   patterns, winning approaches)  │
         └────────────────┬─────────────────┘
                          │
         ┌────────────────▼─────────────────┐
         │         HYBRID RL ENGINE         │
         │                                  │
         │  Layer 1 — Offline RL            │
         │  (pre-trained on historical      │
         │   case data before live cases)   │
         │                                  │
         │  Layer 2 — RLHF                  │
         │  (lawyer feedback trains         │
         │   reward model continuously)     │
         │                                  │
         │  Layer 3 — Online RL / RLVR      │
         │  (verifiable case outcomes as    │
         │   reward signals)                │
         │                                  │
         │  All three layers train          │
         │  periodically on free compute    │
         │  (Colab / Kaggle free GPU tiers) │
         │  using efficient algorithms      │
         │  (GRPO / DPO over PPO)           │
         └────────────────┬─────────────────┘
                          │
         ┌────────────────▼─────────────────┐
         │    EVALUATION + MONITORING +      │
         │         OBSERVABILITY             │
         │                                  │
         │  Evaluation                      │
         │  LLM-as-Judge pipelines          │
         │  Citation verification           │
         │  Stage-level benchmarks          │
         │  Reward model drift tracking     │
         │                                  │
         │  Monitoring                      │
         │  Real-time performance metrics   │
         │  RLHF signal health              │
         │  Output quality trends           │
         │  Anomaly detection               │
         │                                  │
         │  Observability                   │
         │  Full distributed tracing        │
         │  across entire multi-agent       │
         │  pipeline                        │
         │  Every decision, tool call,      │
         │  reasoning chain captured        │
         │  Lawyer-facing audit trail       │
         │  Developer-facing trace explorer │
         └────────────────┬─────────────────┘
                          │
         ┌────────────────▼─────────────────┐
         │         STATE MANAGEMENT          │
         │                                  │
         │  Checkpoint at every stage       │
         │  boundary                        │
         │  Full case persistence across    │
         │  sessions                        │
         │  Resume from any checkpoint      │
         │  Audit trail built in            │
         └────────────────┬─────────────────┘
                          │
         ┌────────────────▼─────────────────┐
         │          RANKING LAYER            │
         │                                  │
         │  Stage 1 — BM25 + Vector Search  │
         │  (hybrid retrieval, top-N        │
         │   candidates from ChromaDB       │
         │   + legal data sources)          │
         │                                  │
         │  Stage 2 — Cross-Encoder         │
         │  Re-ranking                      │
         │  (deep semantic re-scoring of    │
         │   top-N → top-K, runs locally    │
         │   on MacBook CPU)                │
         │                                  │
         │  Stage 3 — Learning-to-Rank      │
         │  (LTR with stage-aware features, │
         │   trained on lawyer feedback     │
         │   signals via XGBoost LambdaRank │
         │   → final top-5 to agent)        │
         │                                  │
         │  Stage-aware weights per agent   │
         │  (Motion ≠ Settlement ≠          │
         │   Discovery ranking priorities)  │
         └────────────────┬─────────────────┘
                          │
         ┌────────────────▼─────────────────┐
         │          LEGAL DATA LAYER         │
         │                                  │
         │  CourtListener API               │
         │  (9M+ opinions, free)            │
         │                                  │
         │  Caselaw Access Project          │
         │  (6.9M decisions, free bulk)     │
         │                                  │
         │  Document Hub                    │
         │  (case-specific documents with   │
         │   type-tagged metadata)          │
         └──────────────────────────────────┘
```

---

### Guardrail Layer — Tiered, Applied Selectively

Guardrails are first-class execution logic in CaseInMind — not an afterthought. In legal AI, hallucinated citations have resulted in $10,000+ court sanctions, attorney-client privilege can be waived by sending raw case data to public AI APIs (United States v. Heppner, 2026), and unauthorized practice of law is an active litigation risk. Every layer below is non-negotiable.

```
LAWYER INPUT
     │
     ▼
┌─────────────────────────────────────┐
│  TIER 1 — INPUT GUARDRAILS          │
│  (Every request, local, fast)       │
│  LLM Guard:                         │
│  ├── PII detection + scrubbing      │
│  │   (protects attorney-client      │
│  │    privilege before API call)    │
│  └── Prompt injection detection     │
└──────────────┬──────────────────────┘
               │ (clean, scrubbed input)
               ▼
     ORCHESTRATOR + AGENTS
               │
               ▼
┌─────────────────────────────────────┐
│  TIER 2 — AGENT SCOPE GUARDRAILS   │
│  (Between orchestrator + workers)   │
│  NeMo Guardrails (structured pipe)  │
│  ├── Each agent confined to its     │
│  │   designated stage only          │
│  └── Hard topic + authority limits  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  TIER 3 — AGENTIC SECURITY         │
│  (High-stakes operations only)      │
│  LlamaFirewall:                     │
│  ├── PromptGuard 2 (BERT-sized,    │
│  │   runs locally on MacBook CPU)   │
│  │   — jailbreak + injection in     │
│  │   retrieved legal documents      │
│  └── AlignmentCheck (selective      │
│      API call for motion drafting,  │
│      settlement, complaint filing)  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  TIER 4 — OUTPUT GUARDRAILS        │
│  (Every output before lawyer sees)  │
│  Guardrails AI:                     │
│  ├── Structured output validation   │
│  └── Custom legal validators        │
│  CourtListener Citation API:        │
│  └── Every citation verified        │
│      before output — hallucination  │
│      guard, zero fabricated cases   │
│  LLM-as-Judge (Groq free):          │
│  └── Factual grounding check        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  TIER 5 — LEGAL-SPECIFIC GUARDRAILS│
│  (Always-on, every output)          │
│  ├── UPL disclaimer enforced on     │
│  │   every output — agent never     │
│  │   concludes legal matters,       │
│  │   always defers to lawyer        │
│  ├── PII output check — no client   │
│  │   data leaks in responses        │
│  └── Confidence flagging — low      │
│      confidence outputs flagged     │
│      for mandatory lawyer review    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  TIER 6 — HUMAN-IN-THE-LOOP        │
│  (Final safety net, architecture)   │
│  ├── Every agent output reviewable  │
│  │   and editable before use        │
│  ├── No irreversible action without │
│  │   explicit lawyer approval       │
│  └── Full audit trail of every      │
│      guardrail trigger              │
└──────────────┬──────────────────────┘
               │
               ▼
         LAWYER SEES OUTPUT
```

**Conversational Agent — Additional Layer:**
NeMo Guardrails wraps the Free Conversational Agent specifically with conversational flow control — hard UPL prevention, topic boundary enforcement, and scope limits. Applied only to the chat interface, not the structured pipeline.

**Attorney-Client Privilege Protection:**
PII scrubbing via LLM Guard runs BEFORE any prompt leaves MacBook. Only legally necessary context is sent to external APIs — never raw case facts. This is the architectural response to United States v. Heppner (2026).

---

### Two Interaction Modes

**Mode 1 — Structured Pipeline**
Orchestrator drives agents stage by stage. Each stage completes, checkpoints, awaits lawyer review and approval before proceeding. All six guardrail tiers active. Predictable, auditable, RL-optimized.

**Mode 2 — Free Conversational Agent**
Lawyer talks naturally at any time. Agent reasons over full case context, calls workers and tools on demand. Every interaction feeds back into episodic memory and becomes RLHF signal. Panel is collapsed by default, activated via single button, resizable to any width on screen. NeMo Guardrails wraps this mode for conversational flow control.

Both modes share the same memory, data layer, RL engine, observability infrastructure, and guardrail stack. Two interfaces to the same brain.

---

### Case Creation Flow

1. **Structured Form** — case name, type, jurisdiction, parties, key dates, statutes of limitations
2. **Document Upload** — lawyer uploads any documents with type tags at any time
3. **Agentic Flow** — agent reads uploaded documents, extracts automatically, asks clarifying questions, fills gaps autonomously
4. **Case Block Created** — appears on dashboard once intake is complete
5. **Case Workspace Unlocked** — all sectional pages accessible for that case

---

### Key Architectural Decisions

| Decision | Choice | Reason |
|---|---|---|
| Orchestration Pattern | Hierarchical Orchestrator-Worker | Best cost-accuracy tradeoff, 70% of production deployments, full control and auditability |
| Communication | Event-driven, asynchronous | Cases span days/weeks — synchronous breaks under LLM latency and HITL pauses |
| State Management | Checkpoint-based at every stage boundary | Resilience, audit trail, HITL resume, zero wasted compute on failure |
| Memory | Four-layer — Working, Episodic, Semantic, Procedural | Gap between has-memory and no-memory larger than gap between model choices |
| RL Training | Periodic on free compute (Colab/Kaggle) using GRPO/DPO | $0 budget — collect continuously, train periodically, still architecturally correct |
| Interaction | Dual-mode — Structured Pipeline + Free Conversational Agent | Structured for predictability, conversational for lawyer-natural interaction |
| Documents | Single hub with type-tagged metadata | Agent uses document type to reason differently across the same corpus |
| Budget | $0 — free APIs, open source models, free legal data | Zero budget forces best engineering decisions |

---

### Architecture Compatibility Verdict

| Component | Feasible | At $0 | Risk Level |
|---|---|---|---|
| Hierarchical Orchestrator-Worker | ✅ | ✅ | Low — orchestrator receives summaries only |
| Event-Driven Communication | ✅ | ✅ | None |
| Checkpoint State Management | ✅ | ✅ | None |
| Four-Layer Memory | ✅ | ✅ | Medium — episodic → semantic consolidation needs explicit design |
| Hybrid RL Pipeline | ✅ | ✅ | Low — periodic training on free compute |
| Eval + Monitor + Observe | ✅ | ✅ | None |
| Free Conversational Agent | ✅ | ✅ | None |
| Document Hub | ✅ | ✅ | None |
| Legal Data Layer | ✅ | ✅ | None |
| Six-Tier Guardrail System | ✅ | ✅ | Low — tiered application prevents latency stacking |
| Three-Stage Ranking Layer | ✅ | ✅ | None — all tools free, run locally |

---

## Data Sources

### Two Categories

**Runtime Data** — what agents query live during case work
**Training Data** — what we use to train the Offline RL layer

---

### Runtime Data Sources

**1. CourtListener API** *(Primary — Case Law + Citations + Dockets)*
- 9M+ opinions from 2,000+ courts
- RECAP Archive — federal dockets and filings
- Citation Lookup API — parse and verify every citation in a block of text, direct hallucination guard
- Semantic Search API — domain-adapted embedding model (Inception/ModernBERT), free
- Free with EDU membership (generous rate limits at no cost for students)
- Token authentication via Authorization HTTP Header
- Weekly maintenance window: 21:00–23:59PT Thursdays
- ⚠️ Action required before Phase 0: Sign up for free CourtListener EDU membership

**2. eCFR API** *(Federal Regulations)*
- Full text of all 50 CFR titles
- No API key required
- Updated daily — live authoritative federal regulations
- Used during Investigation and Motion stages for regulatory context

**3. Federal Register API** *(Regulatory Changes)*
- Rules, proposed rules, notices from all federal agencies
- No API key required
- Used during Investigation stage for recent regulatory changes affecting a case

**4. GovInfo Bulk Data** *(Statutes + Court Records)*
- Free bulk access to ECFR, federal court records, statutes
- No key required
- Direct from US Government — authoritative

---

### Training Data Sources

**5. Caselaw Access Project — Harvard** *(Primary Offline RL Corpus)*
- 6.7M cases, 360 years of US legal history (1658–2020)
- 40M+ pages, machine-readable, fully open, no limitations
- Available directly on HuggingFace (free-law/Caselaw_Access_Project)
- Primary corpus for Offline RL pre-training

**6. Pile of Law** *(Broad Legal Pre-training Corpus)*
- 256GB open corpus of English legal and administrative text
- Opinions, regulations, contracts — broad legal language coverage
- Used for broad legal language pre-training before civil litigation fine-tuning

**7. CUAD Dataset** *(Contract Analysis Training)*
- Expert-annotated contract review dataset from EDGAR filings
- 25 contract types, expert annotations on clause types and risks
- Direct training utility for Drafting and Settlement agents

**8. EDGAR via SEC** *(Contract Precedents)*
- Free, open API — no restrictions
- Real contracts filed with the SEC
- Used for contract analysis and settlement intelligence agent training

**9. ICPSR Federal Court Cases Integrated Database** *(Structured Civil Outcome Signals)*
- Official public record of federal court business from 100 court offices
- Data collected at two points per case: filing and termination
- Provides structured outcome data: case type, court, termination method (jury verdict, bench trial, settlement, default, dismissed), award information
- Civil case as unit of analysis — directly usable as RL reward signals
- Free and public — Federal Judicial Center via ICPSR
- Going back to the 1970s, updated bi-annually
- ⚠️ Note: Does not include actual settlement dollar amounts (confidential by definition)

**10. Grounded Synthetic Data** *(Settlement Amounts + Preference Pairs)*
- Real civil settlement amounts are private by law — no free database exists
- Commercial sources (LexisNexis Verdict & Settlement Analyzer, VerdictSearch) are paid only
- Our approach: grounded synthetic generation anchored in real sources:
  - Real case facts from CourtListener and Caselaw Access Project
  - Real statistical distributions from Federal Judicial Caseload Statistics (aggregate award ranges by case type, published free by US Courts)
  - Expert-defined rules for reasonable settlement ranges per case type and jurisdiction
  - Synthetic preference pairs for RLHF generated from real case documents
- Validated approach: used in LawGPT (50K synthetic legal examples), SynLexLM, and other legal AI research
- Generated at $0 using open source models on free compute

---

### Data Source to CaseInMind Stage Mapping

| Data Source | Stages Used | Purpose |
|---|---|---|
| CourtListener API | All stages (runtime) | Case law, citations, dockets, hallucination guard |
| eCFR API | S2 Investigation, S6 Motion | Federal regulatory context |
| Federal Register API | S2 Investigation | Recent regulatory changes |
| GovInfo Bulk | S2, S6 (runtime + training) | Statutes, court records |
| Caselaw Access Project | Offline RL training | Primary legal pre-training corpus |
| Pile of Law | Offline RL training | Broad legal language pre-training |
| CUAD | Offline RL training | Contract clause analysis |
| EDGAR | S3 Drafting, S7 Settlement (training + runtime) | Contract precedents |
| ICPSR Federal Court IDB | RL reward signals | Structured civil case outcome signals |
| Grounded Synthetic Data | All RL layers | Settlement scenarios, preference pairs |

---

### Key Data Action Items

1. Sign up for CourtListener EDU membership (free) before Phase 0
2. Download Caselaw Access Project from HuggingFace before Phase 6 (Offline RL)
3. Download ICPSR Federal Court Cases IDB before Phase 6 (RL reward signals)
4. Build grounded synthetic data pipeline in Phase 6 before RLHF training

---

## Permanent Project Constraints — Read This First

**These constraints apply to every single decision in this project. Claude Code must read this before writing a single line.**

### Who is building this
A student (ML Engineer) building this as a personal portfolio project on a **MacBook (512GB storage)**. Zero monthly budget. No cloud GPUs. No paid APIs.

### The core philosophy
**Best possible architecture that runs today on student constraints, designed so every component can be swapped for SOTA the moment constraints loosen — without touching the architecture.**

This means:
- The architecture is the asset, not the models
- Every model choice is a placeholder behind an interface, not a hard dependency
- Every dataset choice is the best free option, replaceable with richer data later
- Every inference provider is swappable via a single config change
- Performance today is a baseline — the architecture must be able to carry SOTA later

### What this means in practice
- **Models** → smallest capable free model that proves the architecture works. Replace with larger/better model later via config.
- **Data** → smallest representative subset that validates the pipeline. Scale data volume later.
- **Inference** → free API tiers only. No local GPU inference (MacBook only). No paid tiers.
- **Training** → no training on MacBook. Free Colab/Kaggle GPU tiers only, periodically.
- **Storage** → everything must fit comfortably on a 512GB MacBook alongside the OS and other files. No multi-GB dataset downloads during development.
- **Complexity** → build the simplest thing that proves the architecture, then add complexity only when needed.

### The swap principle
Every component must be behind an abstraction layer:
- LLM provider → swap Groq free → paid Claude/GPT-4 via one config change
- Embedding model → swap MiniLM → Inception legal model → larger model via one config change
- Data → swap small subset → full corpus via one config change
- Vector store → swap local ChromaDB → Pinecone/Weaviate via one config change
- RL training → swap lightweight reward model → full PPO pipeline via one config change

### What we are NOT building right now
- A production system
- A system that handles real lawyer data at scale
- A system with SLA guarantees
- A system that requires GPU locally
- A system that costs money to run

### What we ARE building
- A fully working end-to-end architecture that demonstrates every component
- A system where every component is real, not mocked
- A portfolio piece that shows depth of understanding across LLMs + agents + RL + eval + observability
- A foundation that a future team or funded version could scale without redesigning

**If any decision requires money, local GPU, or more than ~50GB of local storage — it is the wrong decision for this phase.**

---

## LLM & Inference Stack

### Two Completely Separate Things

**Inference** — calling agents during case work → free API calls to provider servers. MacBook sends HTTP request, provider runs the model, response comes back. Zero local compute. Zero MacBook storage impact.

**Reward Model Training** — RLHF training → happens on Google Colab free T4 GPU, not MacBook. Train → push LoRA adapter to HuggingFace Hub → call via HuggingFace Inference API.

---

### Inference — Via Free APIs

All three providers expose OpenAI-compatible endpoints. One interface across all providers. Swap to better model via single config change when constraints loosen.

| Role | Model | Provider | Limits | Why |
|---|---|---|---|---|
| Orchestrator + Complex Agents | Gemini 2.5 Flash | Google AI Studio free | 1,500 req/day, 1M token context | Long context handles full case state, strong reasoning |
| Fast Worker Agents + Conversational Chat | Llama 3.3 70B | Groq free | 1,000 RPD, 100K tokens/day | 700+ tokens/sec, fast enough for real-time agent loops |
| High-Stakes Reasoning (Motion, Settlement) | DeepSeek R1 | OpenRouter :free | 20 RPM, 50 req/day base | Best open reasoning model, free fallback |

**Provider priority order:**
1. Groq — primary for speed-critical agent calls
2. Google AI Studio — primary for complex reasoning and long-context
3. OpenRouter :free — fallback + high-stakes reasoning

**Multi-provider failover:** When Groq rate limits hit → fall back to Gemini Flash. When Gemini hits limits → fall to OpenRouter free models. Single gateway layer, automatic routing.

**Swap principle:** Replace Groq Llama → paid Claude/GPT-4 via one config line when constraints loosen.

---

### Reward Model — Train on Colab, Host on HuggingFace

| What | Choice | Detail |
|---|---|---|
| Base model | Llama 3.1 8B or Qwen 2.5 7B | Both trainable on Colab free T4 with QLoRA + Unsloth |
| Training method | QLoRA + Unsloth | 2x faster training, 70% less VRAM, fits in 15GB T4 VRAM |
| Training data | 1,000–5,000 lawyer preference pairs | Starts small from app usage, grows incrementally |
| Hosting | HuggingFace Hub (free) | Push LoRA adapter after training |
| Inference | HuggingFace Inference API (free tier) | Call trained reward model from app |

**Swap principle:** Replace 8B reward model → larger model, full PPO pipeline when GPU resources available.

---

### Embedding Model — Run Locally on MacBook CPU

Embedding runs locally but is NOT compute-heavy. Documents embedded once on upload, stored in vector DB, not re-embedded on every request. MacBook CPU handles this fine.

| Role | Model | Size | Why |
|---|---|---|---|
| Legal text (primary) | Free Law Project Inception (Free-Law-Project/modernbert-embed-base_finetune_512) | ~400MB | Legal-domain-adapted, fine-tuned on CourtListener opinions, understands legal terminology and case relationships |
| General text (fallback) | all-MiniLM-L6-v2 | ~90MB | Lightweight, fast on CPU, well-supported across all vector DBs |

**Swap principle:** Replace Inception → larger legal embedding model when compute allows.

---

### Dataset Reality — Nothing Massive on MacBook

| Dataset | Where It Lives | When Accessed |
|---|---|---|
| Caselaw Access Project (6.7M cases) | HuggingFace streaming or small 10K subset on Colab | Phase 6 — Offline RL training on Colab only |
| ICPSR Federal Court Cases IDB | Downloaded to Colab when needed | Phase 6 — RL reward signals on Colab only |
| Lawyer preference pairs (RLHF) | Generated incrementally in local app DB | Grows during app usage, tiny size |
| CUAD + EDGAR | HuggingFace streaming on Colab | Phase 6 training only |
| Runtime case documents | Lawyer uploads via app | Lives in local vector DB, small per-case |

MacBook storage impact from LLM stack: ~490MB total (Inception 400MB + MiniLM 90MB).

---

### Training Workflow (Phase 6)

1. Collect lawyer feedback preference pairs during Phase 1–5 app usage
2. Open Google Colab free T4 runtime
3. Load Llama 3.1 8B or Qwen 2.5 7B in 4-bit QLoRA via Unsloth
4. Train reward model on preference pairs (1,000–5,000 examples)
5. Save LoRA adapter → push to HuggingFace Hub (free)
6. Call trained reward model via HuggingFace Inference API from app
7. Repeat periodically as more feedback accumulates

---

## Guardrail System

### Why Guardrails Are Non-Negotiable in Legal AI

- Hallucinated citations have resulted in $10,000+ court sanctions (Noland v. Land of the Free, 2025)
- Sending raw case data to public AI APIs can waive attorney-client privilege (United States v. Heppner, S.D.N.Y. 2026)
- Unauthorized practice of law by AI is now active litigation (Nippon Life Insurance v. OpenAI, N.D. Ill. 2026)
- Courts treat hallucinated citations as sanctionable conduct under Rule 11

Guardrails in CaseInMind are not a feature — they are structural components of every agent interaction.

---

### Six-Tier Architecture

**Tier 1 — Input Guardrails (Every request, local, fast)**
- Tool: LLM Guard (runs locally on MacBook, zero API cost, milliseconds)
- PII detection and scrubbing from ALL prompts BEFORE anything leaves MacBook
- Prompt injection detection — legal documents may contain malicious instructions
- Protects attorney-client privilege by ensuring raw case facts are never sent to external APIs
- Applied to: every input from lawyer and every document retrieved from Document Hub

**Tier 2 — Agent Scope Guardrails (Between orchestrator and workers)**
- Tool: NeMo Guardrails (runs locally, Colang configuration)
- Each specialist agent is hard-constrained to its designated stage only
- Intake agent cannot draft motions. Motion agent cannot make settlement decisions.
- Prevents agents from exceeding their designated authority
- Applied to: all orchestrator → worker routing decisions

**Tier 3 — Agentic Security Guardrails (High-stakes operations only)**
- Tool: LlamaFirewall (Meta, open source, free)
- PromptGuard 2 — BERT-sized model (~110-340M params), runs on MacBook CPU
  - Detects jailbreak attempts and indirect prompt injection in retrieved legal documents
  - Applied to all operations
- AlignmentCheck — chain-of-thought audit via selective LLM API call
  - Inspects whether agent reasoning has been hijacked by malicious content
  - Applied selectively to: motion drafting, settlement analysis, complaint filing ONLY
  - Not applied to routine calls — preserves free API quota

**Tier 4 — Output Guardrails (Every output before lawyer sees it)**
- Tool: Guardrails AI (Python, runs locally) + CourtListener Citation API + LLM-as-Judge
- Guardrails AI: structured output validation, custom legal validators via Pydantic
- CourtListener Citation Lookup API: every single citation verified against real database
  - Fabricated cases blocked before reaching lawyer
  - Zero hallucinated citations reach the lawyer
- LLM-as-Judge (Groq free tier): factual grounding check on all claims
- Applied to: every agent output before delivery to lawyer

**Tier 5 — Legal-Specific Guardrails (Always-on, every output)**
- UPL (Unauthorized Practice of Law) disclaimer enforced on every single output
  - Agent never concludes legal matters, never gives direct legal advice
  - Always defers to lawyer for final judgment
- PII output check — no client data leaks in agent responses
- Confidence flagging — low confidence outputs flagged for mandatory lawyer review
- Applied to: every output, no exceptions

**Tier 6 — Human-in-the-Loop (Final safety net, architectural)**
- Every agent output is reviewable and editable by the lawyer before use
- No agent action is irreversible without explicit lawyer approval
- Full audit trail of every guardrail trigger logged for observability
- Applied to: all staged outputs via HITL checkpoints

**Conversational Agent — Additional Layer:**
NeMo Guardrails wraps the Free Conversational Agent with conversational flow control:
- Hard UPL prevention
- Topic boundary enforcement
- Scope limits (cannot make binding legal decisions)

---

### Tool Summary

| Tool | Tier | Runs Where | Cost | Purpose |
|---|---|---|---|---|
| LLM Guard | 1 | Locally on MacBook | Free | PII scrubbing, prompt injection detection |
| NeMo Guardrails | 2, Chat | Locally on MacBook | Free | Agent scope enforcement, conversational flow |
| LlamaFirewall PromptGuard 2 | 3 | Locally on MacBook CPU (BERT-sized) | Free | Jailbreak + indirect injection detection |
| LlamaFirewall AlignmentCheck | 3 | Selective API call (high-stakes only) | Free tier | Agent reasoning alignment audit |
| Guardrails AI | 4 | Locally on MacBook | Free | Structured output validation, custom legal validators |
| CourtListener Citation API | 4 | API call | Free | Citation verification, hallucination prevention |
| LLM-as-Judge | 4 | Groq free API | Free | Factual grounding verification |
| UPL + PII + Confidence checks | 5 | Locally on MacBook | Free | Legal-specific always-on safety |
| HITL Checkpoints | 6 | Architecture-level | Free | Human oversight, final safety net |

All tools: free, open source, MacBook compatible.

---

### Attorney-Client Privilege Protection

Critical architectural decision driven by United States v. Heppner (2026):
- LLM Guard PII scrubbing runs BEFORE any prompt leaves MacBook
- Only legally necessary context sent to external APIs — never raw case facts
- Case documents stored locally in vector DB — never uploaded raw to Groq or Google
- This is non-negotiable and enforced at Tier 1 on every single request

---

### Swap Principle

Replace any guardrail tool with enterprise equivalent via config change:
- LLM Guard → Lakera Guard or AWS Bedrock Guardrails
- NeMo Guardrails → custom policy engine
- Guardrails AI → proprietary validator suite
- LLM-as-Judge → dedicated hallucination detection model (Patronus AI Lynx)

---

## Agent Orchestration Framework

### Decision: LangGraph

**Why LangGraph over all alternatives:**
- Hierarchical orchestrator-worker pattern is native — root StateGraph routes to subgraphs
- Stateful, long-running workflows are its core design purpose — cases span days/weeks
- First-class HITL via `interrupt_before=["node_name"]` — pauses for lawyer review at any stage
- SQLite checkpointer — local MacBook, zero infrastructure, single .db file per case
- Each case is a `thread_id` — fully isolated state per matter
- Works with any OpenAI-compatible provider — Groq, Google AI Studio, OpenRouter all supported via LangChain integrations (ChatGroq, ChatGoogleGenerativeAI, ChatOpenAI with base_url)
- OpenTelemetry integration — feeds our observability layer without LangSmith
- MIT license — free
- Pure Python — no GPU, MacBook native
- Already on Shivansh's resume (LangGraph PII triage engine at HeinOnline, LangGraph memory orchestration at A2IL) — zero learning curve

**LangGraph maps to CaseInMind:**

| CaseInMind Need | LangGraph Feature |
|---|---|
| Master Orchestrator Agent | Root StateGraph node routing to subgraphs |
| 7 Specialist Worker Agents | 7 subgraphs, each a focused StateGraph |
| Checkpoint at every stage boundary | SqliteSaver — writes state after every node |
| HITL pause at each stage | interrupt_before=["node_name"] |
| Case persists across sessions | thread_id per case — isolated per matter |
| Resume from any checkpoint | Built-in — reload from SQLite by thread_id |
| Event-driven async | LangGraph async-first with asyncio |
| Free Conversational Agent | Separate subgraph with full state access |
| Observability hooks | OpenTelemetry callbacks — no LangSmith needed |

**LangSmith:** NOT used. We build our own observability with Arize Phoenix + Prometheus + Grafana (all free, all open source).

**Memory interaction with four-layer system:**
LangGraph checkpointing handles Working Memory (current execution state). Our external stores handle Episodic, Semantic, and Procedural memory. They are complementary — LangGraph state transitions flow into our episodic memory as logs.

**Swap principle:** SQLite checkpointer → PostgreSQL checkpointer via one config change when scaling.

---

## Agent Orchestration Framework

### Decision: LangGraph

**Why LangGraph over alternatives:**
- CrewAI: strong for prototyping but trails on production observability and error recovery. Teams migrate to LangGraph when they need production-grade state management. We start where we'll end up.
- AutoGen: conversation-first pattern, better for agent debate workflows, not long-running stage-gated legal pipelines
- OpenAI/Google SDKs: vendor-locked. We are multi-provider by design.

**How LangGraph maps to CaseInMind:**

| CaseInMind Need | LangGraph Feature |
|---|---|
| Master Orchestrator Agent | Root `StateGraph` node routing to subgraphs |
| 7 Specialist Worker Agents | 7 subgraphs, each a focused `StateGraph` |
| Checkpoint at every stage boundary | `SqliteSaver` — writes state after every node |
| Human-in-the-loop at each stage | `interrupt_before=["node_name"]` — pauses for lawyer review |
| Case persists across sessions | `thread_id` per case — each case is isolated thread |
| Resume from any checkpoint | Reload state from SQLite by thread_id |
| Event-driven async communication | LangGraph async-first with asyncio |
| Conditional routing between stages | Conditional edges based on case state |
| Free Conversational Agent | Separate subgraph with full state access |
| Observability hooks | OpenTelemetry callback integration |

**State persistence:** `langgraph-checkpoint-sqlite` — single `.db` file, ~15ms write latency, runs locally on MacBook. Swap to PostgreSQL via one config change when scaling.

**License:** MIT. Free. No LangSmith required — we use open source observability stack.

**Swap principle:** Replace SQLite checkpointer → PostgreSQL checkpointer via one config change.

---

## Complete Tech Stack

### Guiding Principle
Every tool chosen is: free at student scale, open source, MacBook-compatible, and replaceable with an enterprise equivalent via config — never touching architecture.

---

### Storage Layer

**ChromaDB — Vector Store**
- Purpose: Episodic memory embeddings, semantic memory, document hub retrieval, legal case embeddings
- Runs locally, single Python package, persists to local folder
- Native LangChain integration, supports custom embedding functions (Inception model via SentenceTransformer interface)
- Swap principle: Replace → Qdrant (production performance) or Pinecone (managed cloud) via config

**SQLite — Structured Storage**
- Two separate database files:
  - `langgraph_state.db` — LangGraph checkpoint state (managed by LangGraph)
  - `caseinmind.db` — Case metadata, RLHF preference pairs, guardrail trigger logs, lawyer profiles
- Zero infrastructure, perfectly sufficient for solo lawyer use case
- Swap principle: Replace `caseinmind.db` → PostgreSQL when multi-user scaling needed

**HuggingFace Hub — Model Registry**
- Purpose: Version control for reward model LoRA adapters, dataset hosting, model cards
- Free, standard in research community
- Push after every Colab training run

---

### ML & Training Layer

**W&B (Weights & Biases) — Experiment Tracking**
- Purpose: Track RL training runs on Colab — reward model metrics, RLHF preference pair quality, QLoRA hyperparameters, training loss curves
- Free tier: individual researchers, unlimited experiments, 5GB storage (LoRA adapters are 50-100MB each — well within limits)
- Integration: `report_to="wandb"` in Unsloth TrainingArguments, works natively on Colab
- Already on resume — zero learning curve
- Swap principle: Replace → MLflow self-hosted when data residency or enterprise requirements arrive

**Why NOT Airflow:** LangGraph handles agent orchestration. GitHub Actions cron handles scheduled training job triggers. Airflow solves a scaling problem we don't have yet — adding it now is over-engineering.

**Why NOT MLflow now:** HuggingFace Hub covers model registry. W&B covers experiment tracking. MLflow requires self-hosted infrastructure (PostgreSQL + storage server) adding unnecessary overhead at this stage.

**Unsloth + QLoRA + TRL + PEFT** — Training tools (decided in LLM stack section)

---

### Document Processing Layer

**PyMuPDF (fitz) — PDF Parsing**
- Purpose: Parse legal documents uploaded to Document Hub (PDFs are the dominant legal document format)
- Fastest, most accurate Python PDF parser, free, open source
- Feeds into LLM Guard PII scanner before any content is processed
- Used in: Document Hub ingestion pipeline on every lawyer upload

**python-docx — Word Document Parsing**
- Purpose: Parse Word documents uploaded to Document Hub
- Some legal documents arrive as .docx files
- Free, open source

---

### Backend Layer

**FastAPI — API Server**
- Purpose: Serve the agent pipeline, memory reads/writes, guardrail checks, WebSocket connections for streaming agent outputs to frontend
- Already on resume — zero learning curve
- Async-first, compatible with LangGraph async execution
- Native WebSocket + Server-Sent Events (SSE) for real-time streaming of agent outputs to lawyer — lawyer sees agent progress in real-time, not waiting for full response

**Pydantic — Data Validation**
- Purpose: Input/output validation across FastAPI endpoints and Guardrails AI structured output validation
- FastAPI uses Pydantic natively; Guardrails AI is built on Pydantic — same library, zero overhead

---

### Frontend Layer

**Next.js — Web Application**
- Purpose: Full case workspace, dashboard, resizable chat panel, document hub UI, observability views
- Already on resume — zero learning curve
- TypeScript throughout

---

### Development & DevOps Layer

**uv — Python Package Management**
- Purpose: Python dependency management and virtual environments
- 2025/2026 standard — 10-100x faster than pip/poetry, lockfile-based
- Use from Phase 0, not pip, not Poetry

**pytest — Testing**
- Purpose: Unit tests for agent logic, integration tests for guardrail pipeline, end-to-end stage workflow tests
- Standard Python testing, free

**GitHub Actions — CI/CD**
- Purpose: Run tests on every commit, scheduled training job notifications, deployment automation
- Free for public repositories
- For Colab training: Actions triggers a Kaggle API automated training run (free GPU alternative to manual Colab) OR notifies developer to run Colab manually

**Docker + Docker Compose — Local Services**
- Purpose: Run observability stack locally (Prometheus, Grafana, Arize Phoenix)
- ~650MB RAM total — acceptable on any MacBook with 16GB+ RAM
- Single `docker-compose.yml` starts the full observability stack

---

### Observability Layer

Applied across ALL phases from Phase 0 onward — instrument early, not as an afterthought.

**OpenTelemetry SDK — Instrumentation Standard**
- Added to Python codebase — instruments every LLM call, agent step, tool call, guardrail trigger as a traceable span
- Vendor-neutral — emit once, ship to any backend via config
- GenAI semantic conventions stable as of early 2026
- Never changes regardless of what observability backend we use

**Arize Phoenix — LLM Trace Backend + Evals**
- Purpose: Store and visualize agent reasoning chains, LLM calls, tool use, hallucination evals
- Local-first, runs in Docker, OpenTelemetry-native, LangGraph integration built-in
- Free, open source (Elastic 2.0)

**Prometheus — Metrics Storage**
- Purpose: Time-series metrics — request counts per agent, latency histograms, token usage per stage, API rate limit hits, error rates
- Runs in Docker, ~100MB RAM, free

**Grafana — Visualization**
- Purpose: Dashboards for both lawyer-facing performance views and developer-facing system health
- Connects to Prometheus (metrics) and Arize Phoenix (traces)
- Runs in Docker, ~200MB RAM, free open source version

---

### Full Tech Stack Compatibility Matrix

All integration points verified:

| Integration | Compatible | Note |
|---|---|---|
| LangGraph + ChromaDB | ✅ | Native via LangChain |
| LangGraph + SQLite (dual DB) | ✅ | Separate file paths, no conflict |
| ChromaDB + Inception embeddings | ✅ | SentenceTransformer interface |
| FastAPI + LangGraph async | ✅ | Both asyncio-based |
| FastAPI + WebSocket/SSE streaming | ✅ | FastAPI native, zero extra infra |
| NeMo Guardrails + LangGraph | ✅ | Wraps at LLM level, not graph level |
| Guardrails AI + Pydantic + FastAPI | ✅ | Same library, native |
| W&B + Unsloth + Colab | ✅ | report_to="wandb" native support |
| OTel + LangGraph + Arize Phoenix | ✅ | Native LangGraph integration |
| Docker Compose + MacBook | ✅ | ~650MB RAM total |
| uv + all packages | ✅ | All tools on PyPI |
| LLM Guard + FastAPI | ✅ | Python middleware |
| PyMuPDF + python-docx + pipeline | ✅ | Standard parsing |
| pytest + LangGraph | ✅ | Standard Python testing |
| GitHub Actions + CI/CD | ✅ | Free for public repos |
| rank_bm25 + ChromaDB hybrid retrieval | ✅ | Native Python, no conflicts |
| MiniLM cross-encoder + sentence-transformers | ✅ | Already in stack, same library |
| XGBoost LTR + Colab training | ✅ | Standard Python, free GPU on Colab |

---


---

### Ranking Layer

The ranking layer is a first-class component sitting between retrieval and every agent context window. Every agent that does research — Investigation, Discovery, Motion, Settlement, Conversational — passes all retrieved results through this pipeline before they reach the LLM. Without it, agents receive raw vector similarity results. With it, agents receive the most legally relevant, stage-appropriate content available.

```
Query
  │
  ▼
Stage 1 — Hybrid Retrieval
  BM25 (rank_bm25) + ChromaDB vector search → top-50 candidates
  │
  ▼
Stage 2 — Cross-Encoder Re-ranking
  Deep semantic re-scoring → top-10
  Runs locally on MacBook CPU (MiniLM cross-encoder, ~90MB)
  │
  ▼
Stage 3 — Learning-to-Rank (LTR)
  Stage-aware feature scoring → final top-5 to agent context window
  XGBoost LambdaRank trained on lawyer feedback signals
  │
  ▼
Agent Context Window
```

**Stage 1 — Hybrid Retrieval**
- Tool: `rank_bm25` (pure Python BM25, zero dependencies) + ChromaDB vector search
- BM25 captures exact legal term matches (case names, statutes, specific legal phrases)
- Vector search captures semantic similarity (conceptually related cases)
- Combined via Reciprocal Rank Fusion (RRF) — standard hybrid retrieval fusion method
- Returns top-50 candidates per query

**Stage 2 — Cross-Encoder Re-ranking**
- Tool: `cross-encoder/ms-marco-MiniLM-L-6-v2` via `sentence-transformers` (already in stack)
- ~90MB model, runs on MacBook CPU in milliseconds per batch
- Performs deep pairwise scoring between query and each candidate — far more accurate than bi-encoder retrieval alone
- Reduces top-50 → top-10
- Swap principle: replace MiniLM cross-encoder → legal-domain fine-tuned cross-encoder when GPU available

**Stage 3 — Learning-to-Rank (LTR)**
- Tool: XGBoost with `rank:ndcg` objective (already well-known from resume — XGBoost at Koders)
- Features per candidate: BM25 score, cross-encoder score, document type match, stage relevance score, recency, citation count in corpus, prior lawyer interaction with this document
- Trained periodically on Colab free GPU using accumulated lawyer feedback signals
- Stage-aware: different feature weights per agent — Motion agent prioritizes precedents with similar fact patterns; Settlement agent prioritizes cases with similar award outcomes; Discovery agent prioritizes documents with contradictions
- Reduces top-10 → final top-5 delivered to agent context window
- Lawyer feedback on agent outputs (accept/reject/edit) is the primary LTR training signal — connects directly to RLHF pipeline

**Why This Matters for RL:**
LTR feedback signals from lawyer interactions flow directly into the RL pipeline. The ranking layer is not isolated — it is a learning component that gets better as the lawyer uses the system, creating a compounding improvement loop:
```
Lawyer feedback → LTR training → better ranking → better agent context → better outputs → more useful feedback
```

**Ranking Layer Tools:**

| Tool | Purpose | Runs Where | Cost |
|---|---|---|---|
| `rank_bm25` | BM25 lexical retrieval | Locally on MacBook | Free |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | Cross-encoder re-ranking | Locally on MacBook CPU | Free (HuggingFace) |
| XGBoost (rank:ndcg) | Learning-to-rank | MacBook (inference) + Colab (training) | Free |
| Reciprocal Rank Fusion | Hybrid retrieval fusion | In-code, no library needed | Free |

Add to `pyproject.toml`: `rank-bm25`, `xgboost` (sentence-transformers already included)

**Swap principle:** Replace MiniLM cross-encoder → larger legal cross-encoder; replace XGBoost LTR → neural LTR model when GPU available.

### What We Explicitly Did Not Include

| Tool | Reason |
|---|---|
| Airflow | LangGraph + GitHub Actions covers all orchestration and scheduling |
| MLflow | HuggingFace Hub + W&B covers model registry and experiment tracking at $0 |
| Redis | SQLite caching sufficient at this scale; add later if needed |
| DVC | HuggingFace datasets + git covers data versioning at this scale |
| Kubernetes | Docker Compose sufficient; swap when scaling |
| LangSmith | Paid; Arize Phoenix covers LLM observability at $0 |

### Swap Principle — Enterprise Upgrade Paths

| Current (Student) | Enterprise Replacement | Effort |
|---|---|---|
| ChromaDB | Qdrant / Pinecone | Config change |
| SQLite | PostgreSQL | Config change |
| W&B free | W&B Pro / MLflow enterprise | Config change |
| Arize Phoenix | Datadog LLM / Langfuse Pro | Config change |
| Groq/Google free | Paid Claude / GPT-4 APIs | Config change |
| Colab training | Dedicated GPU cluster | Training script unchanged |
| Docker Compose | Kubernetes | Infrastructure layer only |

---

## Development Phases

### Important — Read Before Every Phase

**Phases are a plan, not a law.**

Every phase below is a starting point. Steps will be added, removed, reordered, or modified on the fly as development reveals new requirements, better approaches, or constraints we didn't anticipate. This is expected and correct engineering behavior.

**Claude Code must:**
- Follow the phase plan as the default
- Deviate from it when reality demands — and note why
- Never block progress waiting for a plan that doesn't fit the situation
- Flag any step that seems wrong or incomplete before executing it

**The architecture decisions are fixed. The implementation steps are flexible.**

---

## Phase 0 — Project Foundation

### Goal
Create the project skeleton with all tooling configured, all dependencies installable, all external APIs verified reachable, and the observability stack running locally. No agent logic yet. When Phase 0 is done, you can open the project on any MacBook and have a working development environment in under 10 minutes.

---

### Major Step 1 — Repository & Project Setup

**Minor Steps:**
- Initialize GitHub repository: `caseinmind` — public repo
- Install `uv` globally: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Initialize uv project: `uv init caseinmind`
- Set Python version: `uv python pin 3.11`
- Create `pyproject.toml` with all dependencies declared upfront:
  - Core: `langgraph`, `langgraph-checkpoint-sqlite`, `langchain-core`, `langchain-groq`, `langchain-google-genai`, `langchain-openai`, `chromadb`, `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`
  - Guardrails: `llm-guard`, `guardrails-ai`, `nemoguardrails`, `llamafirewall`
  - Embeddings: `sentence-transformers`
  - Document parsing: `pymupdf`, `python-docx`
  - Observability: `opentelemetry-sdk`, `opentelemetry-exporter-otlp-proto-grpc`, `opentelemetry-instrumentation-fastapi`, `prometheus-client`
  - ML/Training: `wandb`, `datasets`
  - Ranking: `rank-bm25`, `xgboost`
  - Testing: `pytest`, `pytest-asyncio`, `httpx`
- Install all: `uv sync`
- Verify: `uv run python -c "import langgraph; print('OK')"` — must print OK
- Note: `llamafirewall` automatically downloads small guard models from HuggingFace on first use — this is expected behavior, not an error

---

### Major Step 2 — Folder Structure

**Minor Steps:**
Create the following directory structure exactly — do not deviate:

```
caseinmind/
├── backend/
│   ├── agents/
│   │   ├── orchestrator/
│   │   │   └── __init__.py
│   │   ├── workers/
│   │   │   ├── intake/
│   │   │   ├── investigation/
│   │   │   ├── drafting/
│   │   │   ├── pleadings/
│   │   │   ├── discovery/
│   │   │   ├── motions/
│   │   │   └── settlement/
│   │   └── conversational/
│   │       └── __init__.py
│   ├── memory/
│   │   ├── working/
│   │   ├── episodic/
│   │   ├── semantic/
│   │   └── procedural/
│   ├── guardrails/
│   │   ├── input/
│   │   ├── scope/
│   │   ├── security/
│   │   ├── output/
│   │   └── legal/
│   ├── rl/
│   │   ├── offline/
│   │   ├── rlhf/
│   │   └── online/
│   ├── data/
│   │   ├── sources/
│   │   └── processing/
│   ├── api/
│   │   └── __init__.py
│   ├── database/
│   │   └── __init__.py
│   └── observability/
│       └── __init__.py
├── frontend/
├── training/
│   └── notebooks/
├── tests/
│   ├── unit/
│   └── integration/
├── docker/
│   └── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── .env.example
├── .env              (gitignored)
└── README.md
```

Every `__init__.py` listed above must be created as an empty file. The folder structure is the contract for the entire project.

---

### Major Step 3 — Environment Configuration

**Minor Steps:**
- Create `.env.example` with all required keys documented:
```
# LLM Inference
GROQ_API_KEY=
GOOGLE_API_KEY=
OPENROUTER_API_KEY=

# Legal Data
COURTLISTENER_API_TOKEN=

# Experiment Tracking
WANDB_API_KEY=

# Database
SQLITE_STATE_DB_PATH=./data/langgraph_state.db
SQLITE_APP_DB_PATH=./data/caseinmind.db

# ChromaDB
CHROMA_PERSIST_PATH=./data/chroma

# Observability
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=caseinmind
```
- Create `.env` from `.env.example` and fill in all keys (gitignored)
- Create `.gitignore` — must include: `.env`, `__pycache__`, `.venv`, `*.db`, `chroma/`, `data/`, `*.pyc`
- Create `/data/` directory for local storage (gitignored)

---

### Major Step 4 — Database Initialization

**Minor Steps:**
- Create `backend/database/models.py` — SQLite schema:
  - `cases` table: id, name, type, jurisdiction, status, created_at, updated_at
  - `documents` table: id, case_id, filename, doc_type, content_path, created_at
  - `preference_pairs` table: id, case_id, stage, chosen, rejected, created_at
  - `guardrail_logs` table: id, case_id, tier, trigger_type, input_hash, action_taken, created_at
- Create `backend/database/init_db.py` — creates all tables on first run using sqlite3 standard library
- Verify: `uv run python backend/database/init_db.py` — must complete without errors
- Confirm two separate SQLite files exist:
  - `data/langgraph_state.db` — owned by LangGraph (created automatically when first graph runs)
  - `data/caseinmind.db` — owned by our schema (created by init_db.py now)

---

### Major Step 5 — External API Connections Verified

**⚠️ Sign up for CourtListener EDU membership before this step**

**Minor Steps:**
- Create `backend/data/sources/courtlistener.py` — CourtListener API client:
  - `search_opinions(query, jurisdiction, limit)` method
  - `verify_citation(citation_text)` method
  - Token auth via `COURTLISTENER_API_TOKEN` from env
  - Base URL: `https://www.courtlistener.com/api/rest/v4/`
- Create `backend/data/sources/ecfr.py` — eCFR API client:
  - `search_regulations(query)` method
  - No API key required
  - Base URL: `https://www.ecfr.gov/api/search/v1/results`
- Create `tests/integration/test_data_sources.py`:
  - Test CourtListener search returns results for `"civil litigation breach of contract"`
  - Test citation lookup returns valid response for a known case
  - Test eCFR returns results for `"civil procedure"`
- Run: `uv run pytest tests/integration/test_data_sources.py -v` — all must pass

---

### Major Step 6 — LLM Provider Connections Verified

**Minor Steps:**
- Create `backend/api/llm_router.py` — unified LLM client with multi-provider failover:
  - Primary: Groq (Llama 3.3 70B) via `langchain-groq`
  - Secondary: Google AI Studio (Gemini 2.5 Flash) via `langchain-google-genai`
  - Fallback: OpenRouter (DeepSeek R1) via `langchain-openai` with `base_url="https://openrouter.ai/api/v1"`
  - `get_llm(tier="fast"|"reasoning"|"fallback")` function — single entry point for all LLM calls
  - All keys loaded from env, never hardcoded
- Create `tests/integration/test_llm_providers.py`:
  - Test each provider returns a response to `"Say hello in one word"`
  - Test failover logic switches providers when primary unavailable
- Run: `uv run pytest tests/integration/test_llm_providers.py -v` — all must pass

---

### Major Step 7 — Observability Stack Running

**Minor Steps:**
- Create `docker/docker-compose.yml` with:
  - OTel Collector on ports 4317 (gRPC) and 4318 (HTTP)
  - Arize Phoenix on port 6006
  - Prometheus on port 9090
  - Grafana on port 3000 (default login: admin/admin)
- Create `backend/observability/tracer.py`:
  - Initialize OpenTelemetry SDK
  - Configure OTLP exporter pointing to `OTEL_EXPORTER_OTLP_ENDPOINT`
  - Export `get_tracer(name: str)` function for use across all agents
  - Export `meter` for Prometheus metrics
  - Service name from `OTEL_SERVICE_NAME` env var
- Run: `docker compose -f docker/docker-compose.yml up -d`
- Verify Phoenix: `curl http://localhost:6006` returns HTML
- Verify Prometheus: `curl http://localhost:9090/-/healthy` returns OK
- Verify Grafana: `curl http://localhost:3000/api/health` returns OK
- Send a test span: small test script that creates a span via `get_tracer` — verify it appears in Phoenix UI at `http://localhost:6006`

---

### Major Step 8 — CI Pipeline Running

**Minor Steps:**
- Create `.github/workflows/ci.yml`:
  - Trigger: every push to `main` and every pull request
  - Steps: install uv → `uv sync` → `uv run pytest tests/unit/ -v`
  - Unit tests only in CI (integration tests require API keys, run locally only)
- Create `tests/unit/test_placeholder.py` — one simple passing test confirming the test suite runs
- Push to GitHub — Actions tab must show green on first run

---

### Done Criteria — Phase 0

Phase 0 is complete when ALL of the following are true. Do NOT proceed to Phase 1 until every box is checked:

- [ ] `uv sync` runs without errors on fresh clone
- [ ] All folders and `__init__.py` files exist as specified
- [ ] `.env` configured with all API keys filled in
- [ ] `uv run python backend/database/init_db.py` creates `data/caseinmind.db` without errors
- [ ] `uv run pytest tests/integration/test_data_sources.py -v` — all pass
- [ ] `uv run pytest tests/integration/test_llm_providers.py -v` — all pass
- [ ] `docker compose up -d` starts all four services without errors
- [ ] Test span visible in Arize Phoenix UI at `http://localhost:6006`
- [ ] Prometheus accessible at `http://localhost:9090`
- [ ] Grafana accessible at `http://localhost:3000`
- [ ] GitHub Actions CI green on first push

---

### Notes for Claude Code — Phase 0

1. **uv only** — never use pip directly. All package operations via `uv add` or `uv sync`
2. **Python 3.11** — pinned. Do not use 3.12 or 3.13 — maximum package compatibility
3. **Never commit `.env`** — contains API keys. `.gitignore` must cover it from day one
4. **Two SQLite files, not one** — `langgraph_state.db` belongs to LangGraph exclusively, `caseinmind.db` belongs to our schema exclusively. Never mix them
5. **All API keys from environment only** — zero hardcoded keys anywhere in codebase, ever
6. **Docker Compose for observability only** — the main app does NOT run in Docker during development
7. **llamafirewall downloads models automatically** — on first import it downloads small BERT-sized guard models from HuggingFace. This is expected, not an error. Ensure internet connection on first run
8. **CourtListener EDU membership required** — sign up at courtlistener.com before Step 5. Free for students
9. **Phases are flexible** — if any step above needs to change during execution, change it and note why

---

## Phase 1 — First Vertical Slice

### Goal
One complete end-to-end working pipeline through Stages 1 and 2 — proves the entire architecture works before expanding to all 7 stages. First demoable artifact.

### Major Steps
1. LangGraph orchestrator skeleton — StateGraph with case state schema defined
2. Intake Worker Agent (Stage 1) — ingests case documents, extracts facts, assesses viability, produces structured case overview
3. Investigation Worker Agent (Stage 2) — researches precedents via CourtListener, maps evidence to legal theories, surfaces weaknesses
4. Basic ranking layer — BM25 (rank_bm25) + ChromaDB hybrid retrieval with Reciprocal Rank Fusion + MiniLM cross-encoder re-ranking; wired into Investigation agent as first implementation
5. SQLite checkpoint integration — case state persists across sessions via SqliteSaver
6. Basic working memory — case state flows through LangGraph graph state
7. Tier 1 input guardrails wired — LLM Guard PII scrubbing before every LLM call
8. Tier 4 output guardrails wired — citation verification via CourtListener on every output
9. FastAPI backend skeleton — basic endpoints to trigger agents and retrieve outputs
10. HITL checkpoint at end of Stage 2 — execution pauses, awaits lawyer approval before continuing
11. OpenTelemetry instrumentation — every agent step, LLM call, tool use, ranking scores traced as spans
12. Basic Next.js frontend — dashboard with case creation form and first case workspace pages showing Stage 1 and 2 outputs

---

## Phase 2 — Expand All Stages

### Goal
All 7 specialist worker agents built and connected through the full pipeline.

### Major Steps
1. Drafting Worker Agent (Stage 3) — complaint drafting with verified citations
2. Pleadings Worker Agent (Stage 4) — defendant response analysis, vulnerability identification
3. Discovery Worker Agent (Stage 5) — interrogatory generation, document requests, discovery gap analysis
4. Motion Worker Agent (Stage 6) — motion drafting with grounded legal reasoning, strategy recommendation
5. Settlement Worker Agent (Stage 7) — comparable case analysis, outcome modeling, negotiation brief
6. Ranking layer extended to all agents — stage-aware ranking weights configured per agent (Motion prioritizes precedent similarity, Settlement prioritizes outcome similarity, Discovery prioritizes contradiction detection)
7. Full orchestrator routing — orchestrator routes correctly across all 7 stages with conditional edges
8. HITL checkpoints at every stage boundary — lawyer reviews and approves before each transition
9. Stage-scoped guardrails — NeMo Guardrails enforces each agent to its designated stage only
10. Full pipeline integration test — a complete case flows from Stage 1 through Stage 7 with ranking active at every stage

---

## Phase 3 — Memory System

### Goal
Upgrade from basic working memory to the full four-layer memory architecture.

### Major Steps
1. Episodic memory layer — every agent decision, tool call, and HITL interaction logged with timestamp, actor, trigger, outcome; vector-embedded and stored in ChromaDB
2. Semantic memory layer — lawyer preferences, style, risk tolerance extracted from episodic logs via consolidation trigger; stored in ChromaDB with structured metadata
3. Procedural memory layer — successful strategies, motion patterns, winning approaches stored as reusable structured records
4. Memory retrieval integration — agents query relevant episodic and semantic memory before executing each task
5. Episodic → semantic consolidation logic — explicit trigger (after N episodes or on case close) that distills episodes into semantic records
6. Memory-aware orchestrator — orchestrator uses procedural memory to inform stage routing decisions
7. LTR training pipeline — collect lawyer feedback signals from Phases 1-2 usage; train XGBoost LambdaRank model on Colab free GPU with accumulated interaction data; integrate trained LTR model into ranking layer Stage 3; ranking now improves based on what the lawyer finds useful

---

## Phase 4 — Free Conversational Agent

### Goal
The chat layer — a privileged agent that reasons over full case context and can call any worker on demand.

### Major Steps
1. Conversational agent subgraph — full access to case state, episodic memory, document hub
2. Worker-on-demand calling — conversational agent can invoke any specialist worker mid-conversation
3. NeMo Guardrails wrapper — UPL prevention, topic boundary enforcement, scope limits for chat
4. RLHF signal capture — every lawyer chat interaction logged as potential preference pair
5. Resizable chat panel in frontend — collapsed by default, single button activation, draggable resize
6. Real-time streaming — agent responses stream token-by-token via FastAPI SSE to frontend

---

## Phase 5 — Document Hub

### Goal
Full document management system with type-tagging and metadata routing.

### Major Steps
1. Document ingestion pipeline — PDF parsing via PyMuPDF, Word parsing via python-docx, text extraction and chunking
2. Document type tagging — lawyer assigns type at upload (Case Documents, Supporting, Discovery, Court Filings, Correspondence)
3. Document embedding and storage — chunks embedded via Inception model, stored in ChromaDB with type metadata
4. Type-aware retrieval — agents query document hub with type filter so each agent uses the right documents
5. Document Hub frontend page — upload interface, type selector, document list with status per case
6. LLM Guard PII scan on every upload — before any document content is stored or sent to LLM

---

## Phase 6 — RL Pipeline

### Goal
All three RL layers implemented — Offline RL, RLHF, and Online RLVR.

### Major Steps
1. Offline RL data preparation — download small representative subset of Caselaw Access Project and ICPSR Federal Court Cases IDB to Colab; preprocess into training format
2. Reward model base training — fine-tune Llama 3.1 8B or Qwen 2.5 7B on legal paralegal preference data via QLoRA + Unsloth on Colab free T4; track with W&B
3. Reward model hosting — push trained LoRA adapter to HuggingFace Hub; wire HuggingFace Inference API call into orchestrator
4. RLHF preference collection — lawyer accept/reject/edit actions on agent outputs automatically logged as preference pairs into `preference_pairs` SQLite table
5. RLHF training loop — periodic re-training of reward model on accumulated preference pairs on Colab; update HuggingFace Hub with new adapter version
6. Grounded synthetic settlement data pipeline — generate settlement scenarios grounded in real case facts from CourtListener and Federal Judicial Caseload Statistics
7. Online RL / RLVR reward signals — case outcomes captured as verifiable reward signals; feed into periodic RL training
8. RL-informed orchestrator decisions — orchestrator uses reward model score to inform routing, strategy selection, and output prioritization

---

## Phase 7 — Evaluation + Monitoring + Full Observability

### Goal
Complete eval, monitoring, and observability systems — every quality metric tracked and visible.

### Major Steps
1. LLM-as-Judge pipeline — Groq free tier judges every agent output for quality, grounding, relevance; scores stored per stage
2. Citation hallucination eval — automated check that every citation in every output exists in CourtListener; hallucination rate tracked as metric
3. Stage-level performance benchmarks — motion quality score, settlement estimate accuracy, discovery coverage rate; all tracked in Prometheus
4. Reward model drift detection — monitor reward model score distribution over time; flag when signal degrades
5. Anomaly detection — alert when agent outputs fall below quality threshold or guardrail trigger rate spikes unexpectedly
6. Grafana dashboards — lawyer-facing performance dashboard and developer-facing system dashboard
7. Arize Phoenix eval integration — hallucination scores, factual grounding scores, agent reasoning traces visible in Phoenix
8. Full distributed tracing audit — every span across entire pipeline verified visible in Phoenix; trace IDs propagated correctly across all agents

---

## Phase 8 — Frontend Polish + Integration Testing

### Goal
The full web application is polished, intuitive, and fully tested end-to-end.

### Major Steps
1. Dashboard — case blocks with status indicators, create new case button, quick stats
2. Case creation flow — structured form + agentic document ingestion + progress indicator
3. Case workspace sectional pages — all 7 stage pages polished with output display, edit capability, approve/reject controls
4. Document Hub page — upload, type tagging, document list, status per document
5. Observability views — quality scores and audit trail visible to lawyer in the UI
6. Chat panel — resizable, streaming, with conversation history per case
7. End-to-end integration tests — a complete synthetic case flows from creation through all 7 stages to settlement with all guardrails, memory, and RL active
8. Cross-browser testing — Chrome, Firefox, Safari on MacBook

---

## Phase 9 — Documentation + Open Source Release

### Goal
The project is portfolio-ready, publicly documented, and reproducible by anyone.

### Major Steps
1. README — project overview, architecture diagram, tech stack, what it does and why it matters
2. Setup guide — step-by-step instructions for any developer to run CaseInMind from scratch
3. Architecture documentation — system design decisions, why each component was chosen, swap paths
4. API documentation — FastAPI auto-generated docs verified and clean
5. Research writeup — the RL approach, evaluation methodology, results on synthetic cases
6. Demo case — a fully worked synthetic civil litigation case included in the repo as a demonstration
7. HuggingFace model card — reward model published with proper documentation
8. GitHub release — tagged v1.0.0 with all assets
