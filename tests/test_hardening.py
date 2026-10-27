"""Access control, validation and review-state tests for the control plane API."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.dependencies import retrieval_service, review_service
from app.main import app

client = TestClient(app)
ADMIN = {"X-User-Id": "ada", "X-User-Role": "admin"}
DOC = {"title": "Runbook addendum", "classification": "internal_docs", "content": "Rotate keys quarterly."}


def ingest(doc_id: str, headers: dict | None = None, **overrides):
    return client.post("/api/v1/ingest", headers=headers or {}, json={"doc_id": doc_id, **DOC, **overrides})


def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_tests_use_a_temporary_corpus():
    tracked = Path(__file__).resolve().parents[1] / "app" / "data" / "sample_documents.json"
    assert retrieval_service.data_path.resolve() != tracked.resolve()


@pytest.mark.parametrize(
    "headers",
    [{}, {"X-User-Role": "analyst"}, {"X-User-Role": "architect"}, {"X-User-Role": "ADMINISTRATOR"}],
)
def test_ingest_requires_admin(headers):
    assert ingest("doc-denied", headers).status_code == 403


def test_admin_can_ingest_and_document_becomes_searchable():
    assert ingest("doc-rotation", ADMIN, content="Quarterly credential rotation procedure.").status_code == 200
    on_disk = json.loads(retrieval_service.data_path.read_text())
    assert any(d["doc_id"] == "doc-rotation" for d in on_disk)
    hits = retrieval_service.search("quarterly credential rotation", scope=["internal_docs"])
    assert hits[0].doc_id == "doc-rotation"


def test_duplicate_doc_id_is_rejected():
    assert ingest("doc-dup", ADMIN).status_code == 200
    assert ingest("doc-dup", ADMIN).status_code == 409


@pytest.mark.parametrize(
    "overrides",
    [
        {"classification": "top_secret"},
        {"content": ""},
        {"doc_id": "../../etc/passwd"},
        {"title": ""},
    ],
)
def test_ingest_validates_payload(overrides):
    payload = {"doc_id": "doc-valid", **DOC, **overrides}
    assert client.post("/api/v1/ingest", headers=ADMIN, json=payload).status_code == 422


def test_security_docs_are_scoped_to_admins():
    ingest("doc-sec", ADMIN, classification="security_docs", content="Zebra protocol escalation matrix.")
    assert retrieval_service.search("zebra protocol escalation", scope=["internal_docs"]) == []
    assert retrieval_service.search("zebra protocol escalation", scope=["internal_docs", "security_docs"])


@pytest.mark.parametrize("role", ["intern", "root", ""])
def test_unknown_roles_are_denied(role):
    res = client.post(
        "/api/v1/query",
        headers={"X-User-Role": role} if role else {},
        json={"query": "How should we design a traceable AI agent?", "requested_tools": []},
    )
    body = res.json()
    if role:
        assert body["status"] == "denied"
    else:
        # No role header falls back to the least-privileged analyst role.
        assert body["status"] != "denied"


def test_disallowed_tool_is_denied():
    res = client.post(
        "/api/v1/query",
        headers={"X-User-Role": "analyst"},
        json={"query": "Run the deployment workflow for runbooks", "requested_tools": ["run_workflow"]},
    )
    assert res.json()["status"] == "denied"
    assert "run_workflow" in res.json()["policy_reason"]


def test_review_cannot_be_resolved_twice():
    case = review_service.create(trace_id="trace-x", reason="low groundedness", answer_preview="...")
    assert client.post(f"/api/v1/reviews/{case.review_id}/reject").status_code == 200
    flip = client.post(f"/api/v1/reviews/{case.review_id}/approve")
    assert flip.status_code == 409
    assert review_service.get(case.review_id).status == "rejected"


def test_unknown_review_and_trace_are_404():
    assert client.post("/api/v1/reviews/review-nope/approve").status_code == 404
    assert client.get("/api/v1/traces/trace-nope").status_code == 404


def test_cors_does_not_allow_credentials():
    res = client.options(
        "/api/v1/query",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert res.headers.get("access-control-allow-credentials") != "true"
