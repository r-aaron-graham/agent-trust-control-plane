from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class UserContext:
    user_id: str
    role: str
    display_name: str | None = None


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str
    allowed_tools: list[str] = field(default_factory=list)
    data_scope: list[str] = field(default_factory=list)
    risk_level: str = "low"


@dataclass
class RetrievedDocument:
    doc_id: str
    title: str
    classification: str
    content: str
    score: float


@dataclass
class GenerationResult:
    answer: str
    citations: list[str]
    model_name: str = "local-deterministic-generator"
    tool_calls: list[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    status: str
    groundedness_score: float
    citation_coverage: float
    requires_review: bool
    confidence_label: str
    reasons: list[str] = field(default_factory=list)


@dataclass
class AuditEvent:
    trace_id: str
    timestamp: datetime
    user_id: str
    role: str
    query: str
    policy_reason: str
    allowed_tools: list[str]
    retrieved_sources: list[str]
    model_name: str
    groundedness_score: float
    citation_coverage: float
    final_status: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewCase:
    review_id: str
    trace_id: str
    created_at: datetime
    status: str
    reason: str
    answer_preview: str
