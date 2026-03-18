from app.models.domain import UserContext


class IdentityService:
    """
    Demo identity resolver.

    In a real system this would integrate with SSO, IAM, or a session/JWT layer.
    """

    def resolve(self, user_id: str | None, role: str | None) -> UserContext:
        return UserContext(
            user_id=user_id or "anonymous",
            role=(role or "analyst").lower(),
            display_name=user_id or "anonymous",
        )
