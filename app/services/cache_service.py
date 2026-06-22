from app.schemas import GenerateResponse
from app.services.vector_store import vectorstore

def build_cache_response(
    response: str,
    cache_status: bool,
    cached: bool,
    simailarity_score: float,
    latency: float,
    embedding_generated: bool,
) -> GenerateResponse:
    return GenerateResponse(
        response=response,
        cache_status=cache_status,
        cached=cached,
        simailarity_score=simailarity_score,
        latency=latency,
        embedding_generated=embedding_generated,
    )

def store_cache_entry(
        prompt: str,
        response: str,
        embedding_generated: list[float],
        model: str,
        temperature: float,
        cache_status: str = "MISS"
) -> None:
    vectorstore.store_cache_item(
        prompt=prompt,
        response=response,
        embedding=embedding_generated,
        model=model,
        temperature=temperature,
        cache_status=cache_status
    )

def update_cache_hit(cache_result) -> None:
    payload = cache_result.payload or {}

    current_cache_hits = payload.get("cache_hits" , 0)

    vectorstore.update_cache_hit(
        point_id=cache_result.id,
        current_cache_hits=current_cache_hits
    )

def get_total_cache_items() -> int:
    return vectorstore.get_total_cache_items()

def get_collection_info():
    return vectorstore.get_collection_info()




