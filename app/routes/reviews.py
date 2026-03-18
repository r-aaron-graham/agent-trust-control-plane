from fastapi import APIRouter, HTTPException

from app.dependencies import review_service
from app.models.schemas import ReviewActionResponse, ReviewRecord

router = APIRouter(tags=["reviews"])


@router.get("/reviews", response_model=list[ReviewRecord])
def list_reviews() -> list[ReviewRecord]:
    return [
        ReviewRecord(
            review_id=case.review_id,
            trace_id=case.trace_id,
            created_at=case.created_at,
            status=case.status,
            reason=case.reason,
            answer_preview=case.answer_preview,
        )
        for case in review_service.list()
    ]


@router.post("/reviews/{review_id}/approve", response_model=ReviewActionResponse)
def approve_review(review_id: str) -> ReviewActionResponse:
    case = review_service.approve(review_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Review case not found")
    return ReviewActionResponse(
        review_id=review_id,
        status=case.status,
        message="Review approved",
    )


@router.post("/reviews/{review_id}/reject", response_model=ReviewActionResponse)
def reject_review(review_id: str) -> ReviewActionResponse:
    case = review_service.reject(review_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Review case not found")
    return ReviewActionResponse(
        review_id=review_id,
        status=case.status,
        message="Review rejected",
    )
