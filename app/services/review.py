from __future__ import annotations

from datetime import UTC, datetime
from threading import Lock
from uuid import uuid4

from app.models.domain import ReviewCase


class ReviewService:
    """
    Simple in-memory human review queue.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._cases: dict[str, ReviewCase] = {}

    def create(self, trace_id: str, reason: str, answer_preview: str) -> ReviewCase:
        case = ReviewCase(
            review_id=f"review-{uuid4().hex[:8]}",
            trace_id=trace_id,
            created_at=datetime.now(UTC),
            status="pending",
            reason=reason,
            answer_preview=answer_preview[:400],
        )
        with self._lock:
            self._cases[case.review_id] = case
        return case

    def list(self) -> list[ReviewCase]:
        return sorted(self._cases.values(), key=lambda c: c.created_at, reverse=True)

    def get(self, review_id: str) -> ReviewCase | None:
        return self._cases.get(review_id)

    def approve(self, review_id: str) -> ReviewCase | None:
        case = self._cases.get(review_id)
        if case:
            case.status = "approved"
        return case

    def reject(self, review_id: str) -> ReviewCase | None:
        case = self._cases.get(review_id)
        if case:
            case.status = "rejected"
        return case
