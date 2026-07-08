from app.schemas import GenerateResponse
from app.services.cache_service import build_cache_response


def test_generate_response_exposes_judge_fields_with_defaults():
    response = GenerateResponse(
        success=True,
        response="ok",
        cache_status="HIT",
        cached=True,
        similarity_score=0.9,
        matched_prompt="previous prompt",
        latency_ms=10.5,
        embedding_generated=True,
    )

    assert response.judge_used is False
    assert response.judge_decision is None
    assert response.cache_decision_reason is None


def test_build_cache_response_includes_judge_fields_with_defaults():
    result = build_cache_response(
        response="cached-response",
        cache_status="MISS",
        cached=False,
        similarity_score=None,
        matched_prompt=None,
        latency_ms=12.3,
        embedding_generated=True,
    )

    assert result.judge_used is False
    assert result.judge_decision is None
    assert result.cache_decision_reason is None
