from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.models.domain import AuditEvent, UserContext
from app.models.schemas import QueryRequest, QueryResponse
from app.services.audit import AuditService
from app.services.evaluation import EvaluationService
from app.services.llm import LLMService
from app.services.policy import PolicyService
from app.services.retrieval import RetrievalService
from app.services.review import ReviewService


class OrchestratorService:
    """
    Coordinates the end-to-end agent lifecycle.
    """

    def __init__(
        self,
        policy_service: PolicyService,
        retrieval_service: RetrievalService,
        llm_service: LLMService,
        evaluation_service: EvaluationService,
        audit_service: AuditService,
        review_service: ReviewService,
    ) -> None:
        self.policy_service = policy_service
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service
        self.evaluation_service = evaluation_service
        self.audit_service = audit_service
        self.review_service = review_service

    def handle_query(self, user: UserContext, request: QueryRequest) -> QueryResponse:
        trace_id = f"trace-{uuid4().hex[:10]}"

        policy = self.policy_service.evaluate(
            user=user,
            query=request.query,
            requested_tools=request.requested_tools,
        )

        if not policy.allowed:
            event = AuditEvent(
                trace_id=trace_id,
                timestamp=datetime.now(UTC),
                user_id=user.user_id,
                role=user.role,
                query=request.query,
                policy_reason=policy.reason,
                allowed_tools=policy.allowed_tools,
                retrieved_sources=[],
                model_name="none",
                groundedness_score=0.0,
                citation_coverage=0.0,
                final_status="denied",
                metadata={"risk_level": policy.risk_level},
            )
            self.audit_service.record(event)
            return QueryResponse(
                trace_id=trace_id,
                status="denied",
                answer=None,
                citations=[],
                policy_reason=policy.reason,
                groundedness_score=0.0,
                citation_coverage=0.0,
                review_id=None,
            )

        context = self.retrieval_service.search(
            query=request.query,
            scope=policy.data_scope,
            top_k=5,
        )

        result = self.llm_service.generate(
            query=request.query,
            context=context,
            allowed_tools=policy.allowed_tools,
        )

        evaluation = self.evaluation_service.score(
            result=result,
            context=context,
            risk_level=policy.risk_level,
        )

        review_id = None
        if evaluation.requires_review:
            review = self.review_service.create(
                trace_id=trace_id,
                reason="; ".join(evaluation.reasons) if evaluation.reasons else "Manual review requested",
                answer_preview=result.answer,
            )
            review_id = review.review_id

        event = AuditEvent(
            trace_id=trace_id,
            timestamp=datetime.now(UTC),
            user_id=user.user_id,
            role=user.role,
            query=request.query,
            policy_reason=policy.reason,
            allowed_tools=policy.allowed_tools,
            retrieved_sources=[doc.doc_id for doc in context],
            model_name=result.model_name,
            groundedness_score=evaluation.groundedness_score,
            citation_coverage=evaluation.citation_coverage,
            final_status=evaluation.status,
            metadata={
                "risk_level": policy.risk_level,
                "review_id": review_id,
                "reasons": evaluation.reasons,
                "citations": result.citations,
            },
        )
        self.audit_service.record(event)

        return QueryResponse(
            trace_id=trace_id,
            status=evaluation.status,
            answer=result.answer,
            citations=result.citations,
            policy_reason=policy.reason,
            groundedness_score=evaluation.groundedness_score,
            citation_coverage=evaluation.citation_coverage,
            review_id=review_id,
        )
