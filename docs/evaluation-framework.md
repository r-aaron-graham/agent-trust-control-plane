# Evaluation Framework

This repository includes a simple runtime evaluator with three goals:

1. detect missing or weak support
2. surface confidence and review conditions
3. keep evaluation logic inside the request lifecycle

## Current metrics

- groundedness score
- citation coverage
- review required flag
- confidence label

## Why runtime evaluation matters

Offline evaluation alone is not enough for agent workflows. Some decisions need to happen at runtime:

- whether evidence is sufficient
- whether the result should be released
- whether the output should fall back or escalate
- whether the request context itself is high risk
