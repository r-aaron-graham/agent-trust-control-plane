from fastapi import APIRouter, HTTPException

from app.dependencies import audit_service
from app.models.schemas import TraceRecord

router = APIRouter(tags=["traces"])


@router.get("/traces", response_model=list[TraceRecord])
def list_traces() -> list[TraceRecord]:
    return [
        TraceRecord(
            trace_id=event.trace_id,
            timestamp=event.timestamp,
            user_id=event.user_id,
            role=event.role,
            query=event.query,
            policy_reason=event.policy_reason,
            allowed_tools=event.allowed_tools,
            retrieved_sources=event.retrieved_sources,
            model_name=event.model_name,
            groundedness_score=event.groundedness_score,
            citation_coverage=event.citation_coverage,
            final_status=event.final_status,
            metadata=event.metadata,
        )
        for event in audit_service.list()
    ]


@router.get("/traces/{trace_id}", response_model=TraceRecord)
def get_trace(trace_id: str) -> TraceRecord:
    event = audit_service.get(trace_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Trace not found")

    return TraceRecord(
        trace_id=event.trace_id,
        timestamp=event.timestamp,
        user_id=event.user_id,
        role=event.role,
        query=event.query,
        policy_reason=event.policy_reason,
        allowed_tools=event.allowed_tools,
        retrieved_sources=event.retrieved_sources,
        model_name=event.model_name,
        groundedness_score=event.groundedness_score,
        citation_coverage=event.citation_coverage,
        final_status=event.final_status,
        metadata=event.metadata,
    )
