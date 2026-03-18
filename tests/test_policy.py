from app.models.domain import UserContext
from app.services.policy import PolicyService


def test_blocks_destructive_terms():
    service = PolicyService()
    user = UserContext(user_id="u1", role="architect")
    decision = service.evaluate(user=user, query="delete all records", requested_tools=["search_docs"])
    assert decision.allowed is False
    assert "Blocked high-risk request" in decision.reason


def test_unknown_role_denied():
    service = PolicyService()
    user = UserContext(user_id="u2", role="guest")
    decision = service.evaluate(user=user, query="show me runbooks", requested_tools=["search_docs"])
    assert decision.allowed is False
    assert "Unknown or unauthorized role" in decision.reason


def test_disallowed_tools_denied():
    service = PolicyService()
    user = UserContext(user_id="u3", role="analyst")
    decision = service.evaluate(user=user, query="show me runbooks", requested_tools=["run_workflow"])
    assert decision.allowed is False
    assert "Requested disallowed tools" in decision.reason
