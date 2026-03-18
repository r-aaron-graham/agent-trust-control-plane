from app.models.domain import GenerationResult, RetrievedDocument
from app.services.evaluation import EvaluationService


def test_review_required_when_no_context():
    service = EvaluationService()
    result = GenerationResult(answer="No data", citations=[])
    evaluation = service.score(result=result, context=[], risk_level="low")
    assert evaluation.requires_review is True
    assert evaluation.status == "review_required"


def test_approved_when_citations_present():
    service = EvaluationService()
    context = [
        RetrievedDocument(doc_id="doc-001", title="t", classification="internal_docs", content="c", score=0.9)
    ]
    result = GenerationResult(answer="Answer", citations=["doc-001"])
    evaluation = service.score(result=result, context=context, risk_level="low")
    assert evaluation.requires_review is False
    assert evaluation.status == "approved"
