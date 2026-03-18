# Architecture Notes

## Purpose

This repository demonstrates an **AI agent control plane** rather than only an answer-generation pipeline.

## Key architectural principle

RAG belongs to the **capability layer**. The following belong to the **control layer**:

- identity
- authorization
- policy evaluation
- runtime evaluation
- auditability
- review routing
- traceability

## Request lifecycle

```mermaid
flowchart LR
    A[User Request] --> B[Identity Resolution]
    B --> C[Policy Evaluation]
    C --> D[Scoped Retrieval]
    D --> E[Answer Generation]
    E --> F[Runtime Evaluation]
    F --> G{Needs Review?}
    G -- No --> H[Return Answer]
    G -- Yes --> I[Human Review Queue]
    H --> J[Audit Log]
    I --> J[Audit Log]
```

## Why this architecture is useful

A request should not move directly from prompt to response in systems where:

- authorization matters
- tool usage has consequences
- auditability is required
- confidence may be weak
- human review may be appropriate
