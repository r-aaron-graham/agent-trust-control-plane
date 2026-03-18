from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging_config import configure_logging
from app.routes.health import router as health_router
from app.routes.query import router as query_router
from app.routes.reviews import router as reviews_router
from app.routes.traces import router as traces_router

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Reference implementation for an AI agent control plane with "
        "identity-aware retrieval, policy checks, evaluation, audit logging, "
        "and human review."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(query_router, prefix="/api/v1")
app.include_router(traces_router, prefix="/api/v1")
app.include_router(reviews_router, prefix="/api/v1")


@app.get("/")
def root() -> dict:
    return {
        "service": settings.app_name,
        "message": "Agent Trust Control Plane is running",
        "docs": "/docs",
    }
