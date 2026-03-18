from fastapi import APIRouter, Header

from app.dependencies import identity_service, orchestrator_service, retrieval_service
from app.models.schemas import IngestRequest, QueryRequest, QueryResponse

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
def ingest_document(payload: IngestRequest) -> dict:
    retrieval_service.ingest(
        doc_id=payload.doc_id,
        title=payload.title,
        classification=payload.classification,
        content=payload.content,
    )
    return {"status": "ingested", "doc_id": payload.doc_id}
