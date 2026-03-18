# Threat Model (Lightweight)

This is a simplified threat model for the demo implementation.

## Risks addressed

- unauthorized retrieval across document classifications
- disallowed tool requests
- unreviewed low-confidence outputs
- missing traceability for decisions

## Risks only partially addressed

- prompt injection
- data poisoning
- model-level jailbreaks
- multi-tenant isolation
- transport-level security hardening
- secret management
- full IAM integration

## Design responses in this repo

- role-to-scope mapping in the policy service
- explicit tool allow lists by role
- runtime review path for weak outputs
- audit logging for every query lifecycle
