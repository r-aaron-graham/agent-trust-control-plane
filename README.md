# Agent Trust Control Plane

A detailed reference implementation showing why **RAG is not enough** on its own and what it looks like to put a real **control plane** around an AI agent.

This repository is intentionally designed to support the architectural argument from the article:

> **RAG Is Not Enough: Building the Control Plane Around an AI Agent**

The code demonstrates a request lifecycle where retrieval is only one part of the system. Every request also passes through:

- identity and role resolution
- policy evaluation
- scoped retrieval
- answer generation
- runtime evaluation
- audit logging
- human review escalation when confidence is weak

---

## Why this repository exists

Many AI agent examples stop at:

- retrieve context
- prompt the model
- return the answer

That is useful for experimentation, but it does not create a governable system.

This repository demonstrates a more operational approach where the agent is treated as infrastructure rather than just an interface.

### What this repository proves

This scaffold is built to show:

- architecture thinking beyond prompting
- role-aware and policy-aware control flow
- retrieval that is scoped by authorization context
- runtime evaluation rather than offline-only scoring
- traceability and audit logging
- a simple but credible human review path
- a prototype-to-production mindset

---

## Core request lifecycle

```text
User Request
  -> Identity Resolution
  -> Policy Evaluation
  -> Role-Scoped Retrieval
  -> Answer Generation
  -> Runtime Evaluation
  -> Audit Logging
  -> Return / Fallback / Human Review
```

---

## Repository structure

```text
agent-trust-control-plane/
├── app/
│   ├── data/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── config.py
│   ├── dependencies.py
│   ├── logging_config.py
│   └── main.py
├── docs/
├── frontend/
├── scripts/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Main features

### 1. Identity-aware request handling
The API accepts request metadata through headers and uses role context to constrain what the caller may access.

### 2. Policy engine
A policy layer decides:

- whether the request is allowed
- which tools are permitted
- what document scope is allowed
- whether a destructive or high-risk request should be blocked or escalated

### 3. Scoped retrieval
Retrieval is not global. Search results are filtered by document classification and role permissions.

### 4. Runtime evaluation
Generated responses are scored for:

- groundedness
- citation coverage
- confidence
- escalation conditions

### 5. Audit log and traces
Each request writes a traceable event containing:

- user and role context
- retrieved source ids
- policy outcome
- generated answer metadata
- evaluation scores
- final disposition

### 6. Human review path
Low-confidence or high-risk responses are routed into a lightweight review queue rather than returned blindly.

---

## Quickstart

### Local setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Start the API
5. Open the frontend

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- API docs: `http://localhost:8000/docs`
- Demo UI: `frontend/index.html`

---

## Example API usage

### Health check

```bash
curl http://localhost:8000/api/v1/health
```

### Query the agent

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -H "X-User-Id: aaron" \
  -H "X-User-Role: architect" \
  -d '{
    "query": "How should we design a traceable AI agent for internal runbooks?",
    "requested_tools": ["search_docs"]
  }'
```

### Read a trace

```bash
curl http://localhost:8000/api/v1/traces/<trace_id>
```

---

## Demo behavior

This repo uses a deterministic answer generator instead of a paid LLM so the control plane behavior is easy to test locally.

The answer generator:

- summarizes retrieved documents
- includes citations
- respects allowed tool lists
- produces structured metadata for evaluation

In a real deployment, the same orchestration pattern can sit in front of OpenAI, Anthropic, Azure OpenAI, local models, or another model gateway.

---

## Production notes

This is a **reference implementation**, not a full enterprise platform.

For a production path, the next obvious upgrades are:

- PostgreSQL and persistent storage
- OpenTelemetry traces
- external vector search backend
- proper IAM integration
- richer evaluation datasets
- async review workflows
- provider failover and retry strategies
- policy rules managed outside code
- redaction and prompt injection defenses

---

## Screens and assets to add next

- trace viewer UI
- retrieval diagnostics table
- review queue panel
- policy decision inspector
- architecture diagram screenshot
- latency and escalation metrics dashboard

---

## Tests included

The repository includes tests for:

- policy blocking logic
- evaluation thresholds
- end-to-end query flow
- review queue behavior

Run tests with:

```bash
pytest -q
```

---

## Why this matters

RAG improves context. It does not by itself establish identity, authorization, policy, evaluation, observability, or safe operational boundaries.

That is the purpose of this repository: to show what a more governable AI agent looks like in code.
