# Agent Trust Control Plane

[![CI](https://github.com/r-aaron-graham/agent-trust-control-plane/actions/workflows/ci.yml/badge.svg)](https://github.com/r-aaron-graham/agent-trust-control-plane/actions/workflows/ci.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

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

### Docker

```bash
docker compose up --build
```

The image runs as a non-root user and has a healthcheck on `/api/v1/health`. No API keys are needed; answers come from a deterministic generator.

### Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | `Agent Trust Control Plane` | Service name in `/health` |
| `APP_ENV` | `development` | Environment label |
| `LOG_LEVEL` | `INFO` | Python logging level |
| `CORS_ORIGINS` | `*` | Comma-separated allowed origins. Set real origins when deployed. |
| `RETRIEVAL_DATA_PATH` | `app/data/sample_documents.json` | Corpus file read by retrieval and written by `/api/v1/ingest` |

### Identity model

Identity comes from the `X-User-Id` and `X-User-Role` headers so the policy layer is easy to explore. That is a demo stand-in for SSO or JWT validation: in a real deployment, put this behind an authenticating gateway that sets those headers. Writing to the corpus (`POST /api/v1/ingest`) requires the `admin` role, because it changes what every user's agent can retrieve.

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
- access control and validation: only admins can ingest, unknown classifications and malformed IDs are rejected, duplicate document IDs return 409, security documents stay out of non-admin scopes, unknown roles and disallowed tools are denied
- review state: a resolved review cannot be flipped (409)
- tests run against a temporary copy of the corpus, so they never modify tracked data

Run tests with:

```bash
pip install -r requirements-dev.txt
make lint   # ruff
make test   # pytest with coverage
```

CI also builds the Docker image, waits for its healthcheck, checks an approved and a denied query end to end, and confirms anonymous ingest is refused.

---

## Why this matters

RAG improves context. It does not by itself establish identity, authorization, policy, evaluation, observability, or safe operational boundaries.

That is the purpose of this repository: to show what a more governable AI agent looks like in code.
