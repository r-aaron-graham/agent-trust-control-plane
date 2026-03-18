from app.services.audit import AuditService
from app.services.evaluation import EvaluationService
from app.services.identity import IdentityService
from app.services.llm import LLMService
from app.services.orchestrator import OrchestratorService
from app.services.policy import PolicyService
from app.services.retrieval import RetrievalService
from app.services.review import ReviewService


identity_service = IdentityService()
policy_service = PolicyService()
retrieval_service = RetrievalService()
llm_service = LLMService()
evaluation_service = EvaluationService()
audit_service = AuditService()
review_service = ReviewService()

orchestrator_service = OrchestratorService(
    policy_service=policy_service,
    retrieval_service=retrieval_service,
    llm_service=llm_service,
    evaluation_service=evaluation_service,
    audit_service=audit_service,
    review_service=review_service,
)
