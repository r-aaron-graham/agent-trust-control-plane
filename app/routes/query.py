from fastapi import APIRouter, Header, HTTPException

from app.dependencies import identity_service, orchestrator_service, retrieval_service
from app.models.schemas import IngestRequest, QueryRequest, QueryResponse
from app.services.retrieval import DuplicateDocumentError

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query_agent(
    request: QueryRequest,
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
) -> QueryResponse:
    user = identity_service.resolve(user_id=x_user_id, role=x_user_role)
    return orchestrator_service.handle_query(user=user, request=request)


@router.post("/ingest")
def ingest_document(
    payload: IngestRequest,
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
) -> dict:
    # Writing to the retrieval corpus changes what every user's agent can see,
    # so it is restricted to admins (same demo identity headers as /query).
    user = identity_service.resolve(user_id=x_user_id, role=x_user_role)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can ingest documents")
    try:
        retrieval_service.ingest(
            doc_id=payload.doc_id,
            title=payload.title,
            classification=payload.classification,
            content=payload.content,
        )
    except DuplicateDocumentError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"status": "ingested", "doc_id": payload.doc_id}
