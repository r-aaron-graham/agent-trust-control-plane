from app.models.domain import EvaluationResult, GenerationResult, RetrievedDocument


class EvaluationService:
    """
    Lightweight runtime evaluator.

    This intentionally uses transparent heuristic thresholds so the control logic
    is easy to understand and test.
    """

    def score(
        self,
        result: GenerationResult,
        context: list[RetrievedDocument],
        risk_level: str = "low",
    ) -> EvaluationResult:
        if not context:
            return EvaluationResult(
                status="review_required",
                groundedness_score=0.2,
                citation_coverage=0.0,
                requires_review=True,
                confidence_label="low",
                reasons=["No authorized context retrieved"],
            )

        citation_coverage = round(len(result.citations) / max(len(context[:3]), 1), 2)
        groundedness_score = 0.9 if result.citations else 0.35

        reasons: list[str] = []
        requires_review = False
        status = "approved"
        confidence_label = "high"

        if risk_level == "high":
            groundedness_score = min(groundedness_score, 0.65)
            reasons.append("High-risk request context")
            requires_review = True
            status = "review_required"
            confidence_label = "medium"

        if citation_coverage < 0.6:
            reasons.append("Insufficient citation coverage")
            requires_review = True
            status = "fallback"
            confidence_label = "medium"

        if groundedness_score < 0.7:
            reasons.append("Groundedness score below release threshold")
            requires_review = True
            status = "review_required"
            confidence_label = "low"

        return EvaluationResult(
            status=status,
            groundedness_score=round(groundedness_score, 2),
            citation_coverage=citation_coverage,
            requires_review=requires_review,
            confidence_label=confidence_label,
            reasons=reasons,
        )
