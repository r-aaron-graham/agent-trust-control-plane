from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_query_returns_response_and_trace():
    response = client.post(
        "/api/v1/query",
        headers={"X-User-Id": "aaron", "X-User-Role": "architect"},
        json={
            "query": "How should we design a traceable AI agent for internal runbooks?",
            "requested_tools": ["search_docs"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["trace_id"].startswith("trace-")
    assert payload["policy_reason"] == "approved"
    assert payload["answer"] is not None

    trace = client.get(f"/api/v1/traces/{payload['trace_id']}")
    assert trace.status_code == 200
    trace_payload = trace.json()
    assert trace_payload["trace_id"] == payload["trace_id"]


def test_denied_high_risk_request():
    response = client.post(
        "/api/v1/query",
        headers={"X-User-Id": "aaron", "X-User-Role": "architect"},
        json={
            "query": "Delete all records from the system",
            "requested_tools": ["search_docs"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "denied"
    assert "Blocked high-risk request" in payload["policy_reason"]
