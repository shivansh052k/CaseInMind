# CaseInMind

**A Civil Litigation AI Paralegal Agent** — powered by LLMs, hierarchical multi-agent orchestration, and a three-layer hybrid RL framework, built to act as an autonomous, continuously learning paralegal partner for solo civil litigation attorneys across the full pre-trial lifecycle.

Built entirely on free-tier APIs, open-source models, and free legal data sources — $0 compute budget, MacBook-native, no cloud GPUs, no paid APIs.

---

## The Problem

Civil litigation is document-intensive and repetitive — intake, investigation, drafting, pleadings, discovery, motions, settlement — spanning months to years. Solo attorneys either eat this cost themselves or can't afford paralegal help. Existing legal AI tools automate discrete tasks but don't learn from outcomes or improve over time — they're static workflow automation, not adaptive intelligence.

CaseInMind closes that gap: an agent system that gets measurably better the more it's used, understands case strategy in context, and earns increasing autonomy through verifiable performance.

## What It Does

CaseInMind operates across all 7 stages of the pre-trial civil litigation lifecycle:

| Stage | Function |
|---|---|
| 1. Intake & Evaluation | Ingest documents, extract facts, assess case viability |
| 2. Pre-Filing Investigation | Research precedents, map evidence to claims, surface weaknesses |
| 3. Complaint Drafting | Generate jurisdiction-aware complaints with verified citations |
| 4. Pleadings Analysis | Analyze defendant responses, identify vulnerabilities |
| 5. Discovery | Generate interrogatories/requests, analyze incoming discovery |
| 6. Motion Drafting & Strategy | Draft motions, recommend strategy based on case posture |
| 7. Settlement Intelligence | Model outcomes, prepare negotiation briefs |

Delivered as a full-stack web app: a lawyer-facing dashboard, per-case workspace, document hub, and a resizable free-form chat agent alongside the structured pipeline.

## What Makes It Different — Hybrid RL

CaseInMind is the only part of its category that *learns*, via three RL layers:

1. **Offline RL** — pre-trained on historical case outcomes (CourtListener, Caselaw Access Project) for a strong prior on what good paralegal work looks like.
2. **RLHF** — every lawyer accept/reject/edit action trains a reward model on that specific attorney's preferences, style, and risk tolerance.
3. **Online RL / RLVR** — real case outcomes (motions won/lost, settlements reached) become reward signals that refine strategy over time.

All training happens periodically on free Colab/Kaggle GPU tiers — never on the MacBook.

## Architecture

**Pattern:** Hierarchical Orchestrator-Worker, event-driven and asynchronous.

- A **Master Orchestrator** owns case state, decomposes tasks, routes to workers, manages human-in-the-loop checkpoints, and holds the RL decision layer. It receives summaries only from workers — never full outputs — to avoid context overflow.
- **7 specialist worker agents**, one per lifecycle stage, each independently improvable.
- A **Free Conversational Agent** sits alongside the pipeline with full case-context access and can call any worker on demand.
- A shared **four-layer memory system** — working, episodic, semantic, procedural.
- A **three-stage ranking layer** (BM25 + vector hybrid retrieval → cross-encoder re-ranking → learning-to-rank) sits between retrieval and every agent's context window.
- A **six-tier guardrail stack** — input PII scrubbing, agent scope limits, jailbreak/injection detection, output citation verification, always-on legal-specific checks (UPL, confidence flagging), and human-in-the-loop as the final safety net.
- **Checkpointing at every stage boundary** so a case can be resumed from any point across sessions.

Full architectural detail, data flow diagrams, and the guardrail tier breakdown live in `Project description.md`.

## Tech Stack

| Layer | Choice |
|---|---|
| Orchestration | LangGraph (StateGraph, SqliteSaver checkpointing, `interrupt_before` for HITL) |
| LLM inference | Groq (Llama 3.3 70B) · Google AI Studio (Gemini 2.5 Flash) · OpenRouter (DeepSeek R1) — multi-provider failover |
| Reward model | Llama 3.1 8B / Qwen 2.5 7B, QLoRA + Unsloth on Colab, hosted on HuggingFace Hub |
| Embeddings | Free Law Project Inception (legal-domain) + MiniLM fallback, run locally on CPU |
| Vector store | ChromaDB |
| Structured storage | SQLite (`langgraph_state.db` + `caseinmind.db`, kept separate) |
| Backend | FastAPI + Pydantic, async, WebSocket/SSE streaming |
| Frontend | Next.js + TypeScript |
| Document parsing | PyMuPDF (PDF) + python-docx |
| Guardrails | LLM Guard · NeMo Guardrails · LlamaFirewall · Guardrails AI · CourtListener Citation API |
| Ranking | rank_bm25 + ChromaDB hybrid retrieval, MiniLM cross-encoder, XGBoost LambdaRank |
| Observability | OpenTelemetry → Arize Phoenix, Prometheus, Grafana (all via Docker Compose) |
| Experiment tracking | Weights & Biases |
| Package management | uv |
| CI/CD | GitHub Actions |

Every component sits behind a swap-friendly interface — see `Project description.md` for the full enterprise upgrade path per component.

## Data Sources

**Runtime:** CourtListener API (9M+ opinions, citation verification), eCFR API, Federal Register API, GovInfo bulk data.
**Training:** Caselaw Access Project (6.7M cases), Pile of Law, CUAD, EDGAR, ICPSR Federal Court Cases IDB, and grounded synthetic settlement data (since real settlement amounts are private by law).

## Repo Layout

```
caseinmind/
├── backend/
│   ├── agents/
│   │   ├── orchestrator/
│   │   ├── workers/            # intake, investigation, drafting, pleadings,
│   │   │                       # discovery, motions, settlement
│   │   └── conversational/
│   ├── memory/                 # working, episodic, semantic, procedural
│   ├── guardrails/              # input, scope, security, output, legal
│   ├── rl/                     # offline, rlhf, online
│   ├── data/                   # sources (API clients), processing
│   ├── api/                    # FastAPI app
│   ├── database/                # SQLite schema + init
│   └── observability/           # OpenTelemetry tracer
├── frontend/                    # Next.js app (Phase 1+)
├── training/notebooks/          # Colab notebooks (RL, Phase 6)
├── tests/
│   ├── unit/
│   └── integration/
├── docker/                      # docker-compose.yml (observability stack)
├── .github/workflows/           # CI
├── pyproject.toml
├── .env.example
└── Project description.md       # full architecture & phase spec (source of truth)
```

The full phase-by-phase task list (Phases 0–9) and ownership split lives in `Project description.md`.

## Getting Started

```bash
git clone https://github.com/shivansh052k/CaseInMind.git
cd CaseInMind

curl -LsSf https://astral.sh/uv/install.sh | sh   # install uv, if not already installed
uv python pin 3.11
uv sync                                            # installs all dependencies

cp .env.example .env                               # fill in your API keys (never commit this file)
```

Once Phase 0 is complete, the observability stack runs via:

```bash
docker compose -f docker/docker-compose.yml up -d
```

## Contributors

| | Focus areas |
|---|---|
| **Sada** | CI/CD, Data sources, Ranking layer, Agent orchestration, FastAPI/WebSocket, Observability, Next.js frontend |
| **Shivansh** | Database & state, LLM providers, Document processing, Guardrails, Memory system, Conversational agent, RL pipeline, Evaluation |

## License

MIT — see [LICENSE](LICENSE).
