from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=3, description="User request or question")
    requested_tools: list[str] = Field(default_factory=list)


class QueryResponse(BaseModel):
    trace_id: str
    status: str
    answer: str | None = None
    citations: list[str] = Field(default_factory=list)
    policy_reason: str
    groundedness_score: float | None = None
    citation_coverage: float | None = None
    review_id: str | None = None


class IngestRequest(BaseModel):
    doc_id: str
    title: str
    classification: str
    content: str


class TraceRecord(BaseModel):
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
    metadata: dict[str, Any]


class ReviewRecord(BaseModel):
    review_id: str
    trace_id: str
    created_at: datetime
    status: str
    reason: str
    answer_preview: str


class ReviewActionResponse(BaseModel):
    review_id: str
    status: str
    message: str


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
