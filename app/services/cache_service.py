from app.schemas import GenerateResponse
from app.services.vector_store import vectorstore
from app.logger import logger


def build_cache_response(
    response: str,
    cache_status: str,
    cached: bool,
    similarity_score: float | None,
    matched_prompt: str | None,
    latency_ms: float,
    embedding_generated: bool,
    pii_detected: bool = False,
    pii_types: list[str] | None = None
) -> GenerateResponse:

    return GenerateResponse(
        success=True,
        response=response,

        cache_status=cache_status,
        cached=cached,

        similarity_score=similarity_score,
        matched_prompt=matched_prompt,

        latency_ms=latency_ms,
        embedding_generated=embedding_generated,
        pii_detected=pii_detected,
        pii_types=pii_types or []
    )


def store_cache_entry(
    prompt: str,
    response: str,
    embedding: list[float],
    model: str,
    temperature: float,
    cache_status: str = "MISS"
) -> None:

    logger.info(f"Storing cache entry | model={model}")

    vectorstore.store_cache_item(
        prompt=prompt,
        response=response,
        embedding=embedding,
        model=model,
        temperature=temperature,
        cache_status=cache_status
    )


def update_cache_hit(
    cache_result
) -> None:

     logger.info(f"Updating cache hit | id={cache_result.id}")

    payload = cache_result.payload or {}

    vectorstore.update_cache_hit(
        point_id=str(cache_result.id),
        payload=payload
    )


def get_total_cache_items() -> int:
    return vectorstore.get_total_cache_items()


def get_collection_info():
    return vectorstore.get_collection_info()