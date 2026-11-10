"""Exercise the reference API with local fixtures and no model provider."""

from fastapi.testclient import TestClient

from app.main import app


def main() -> None:
    headers = {"X-User-Id": "demo-user", "X-User-Role": "architect"}
    cases = (
        ("Cited answer", "How should we design a traceable AI agent for internal runbooks?"),
        ("Policy decision", "Delete all records from the system"),
        ("Review escalation", "zxqv blorf"),
    )

    with TestClient(app) as client:
        for label, query in cases:
            response = client.post(
                "/api/v1/query",
                headers=headers,
                json={"query": query, "requested_tools": ["search_docs"]},
            )
            response.raise_for_status()
            result = response.json()
            trace = client.get(f"/api/v1/traces/{result['trace_id']}")
            trace.raise_for_status()
            print(
                f"{label}: status={result['status']}, "
                f"citations={len(result['citations'])}, "
                f"trace={trace.json()['final_status']}, "
                f"review={'queued' if result['review_id'] else 'none'}"
            )


if __name__ == "__main__":
    main()
