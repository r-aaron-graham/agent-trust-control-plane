from app.models.domain import PolicyDecision, UserContext


ROLE_SCOPES = {
    "analyst": ["internal_docs"],
    "architect": ["internal_docs"],
    "admin": ["internal_docs", "security_docs"],
}

ROLE_TOOLS = {
    "analyst": ["search_docs"],
    "architect": ["search_docs", "get_metadata"],
    "admin": ["search_docs", "get_metadata", "run_workflow"],
}

BLOCKED_TERMS = ["delete", "drop database", "exfiltrate", "wipe"]


class PolicyService:
    """
    Applies a deliberately simple but explicit policy model.

    The purpose is to show architectural placement of policy, not to claim
    production-complete governance logic.
    """

    def evaluate(
        self,
        user: UserContext,
        query: str,
        requested_tools: list[str] | None = None,
    ) -> PolicyDecision:
        requested_tools = requested_tools or []
        q = query.lower()

        for term in BLOCKED_TERMS:
            if term in q:
                return PolicyDecision(
                    allowed=False,
                    reason=f"Blocked high-risk request containing '{term}'",
                    allowed_tools=[],
                    data_scope=[],
                    risk_level="high",
                )

        scopes = ROLE_SCOPES.get(user.role)
        allowed_tools = ROLE_TOOLS.get(user.role)

        if scopes is None or allowed_tools is None:
            return PolicyDecision(
                allowed=False,
                reason=f"Unknown or unauthorized role '{user.role}'",
                allowed_tools=[],
                data_scope=[],
                risk_level="high",
            )

        disallowed_requested_tools = [t for t in requested_tools if t not in allowed_tools]
        if disallowed_requested_tools:
            return PolicyDecision(
                allowed=False,
                reason=f"Requested disallowed tools: {', '.join(disallowed_requested_tools)}",
                allowed_tools=allowed_tools,
                data_scope=scopes,
                risk_level="medium",
            )

        risk_level = "medium" if "security" in q or "admin" in q else "low"

        return PolicyDecision(
            allowed=True,
            reason="approved",
            allowed_tools=allowed_tools,
            data_scope=scopes,
            risk_level=risk_level,
        )
