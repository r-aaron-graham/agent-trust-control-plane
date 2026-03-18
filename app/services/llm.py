from app.models.domain import GenerationResult, RetrievedDocument


class LLMService:
    """
    Deterministic answer generator used so the control plane can be exercised
    without external model dependencies.

    A production deployment would replace this with a provider gateway.
    """

    def generate(
        self,
        query: str,
        context: list[RetrievedDocument],
        allowed_tools: list[str],
    ) -> GenerationResult:
        if not context:
            return GenerationResult(
                answer=(
                    "I do not have enough authorized supporting context to answer confidently. "
                    "Please broaden the permitted document scope or submit this request for review."
                ),
                citations=[],
                tool_calls=[],
            )

        selected = context[:3]
        bullet_points = [
            f"- {doc.title}: {doc.content}"
            for doc in selected
        ]
        answer = (
            f"Request: {query}\n\n"
            "Grounded summary based on authorized sources:\n"
            + "\n".join(bullet_points)
            + "\n\n"
            f"Allowed tools in this session: {', '.join(allowed_tools) if allowed_tools else 'none'}."
        )
        citations = [doc.doc_id for doc in selected]

        return GenerationResult(
            answer=answer,
            citations=citations,
            tool_calls=[],
        )
