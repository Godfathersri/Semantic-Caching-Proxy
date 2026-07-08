from app.config import settings
from app.logger import logger
from app.services.vector_store import vectorstore
from app.services.cache_service import update_cache_hit
from app.services.cache_judge_service import judge_cache_reuse


async def lookup_cache(
    prompt: str,
    embedding: list[float],
) -> dict:
    """
    Searches the semantic cache and determines whether
    a cached response can be reused.

    Returns:
        {
            "hit": bool,
            "response": str | None,
            "similarity_score": float | None,
            "matched_prompt": str | None,
            "judge_used": bool,
            "judge_decision": str | None,
            "cache_decision_reason": str | None,
        }
    """

    cache_result = vectorstore.search_similar(
        embedding=embedding
    )

    logger.info(
        f"Cache search completed. Result: {cache_result}"
    )

    if not cache_result:
        logger.info(
            "No cache match found | calling Gemini"
        )

        return {
            "hit": False,
            "judge_used": False,
            "judge_decision": None,
            "cache_decision_reason": "No cache match found",
        }

    similarity_score = cache_result.score

    logger.info(
        f"Potential cache match found | score={similarity_score:.2f}"
    )

    payload = cache_result.payload or {}

    if not payload:
        logger.warning(
            "Cache HIT candidate found, but payload is missing"
        )

        return {
            "hit": False,
            "judge_used": False,
            "judge_decision": None,
            "cache_decision_reason": "Missing payload",
        }

    cached_response = payload.get("response")

    if not cached_response:
        logger.warning(
            "Cache HIT candidate found, but cached response is missing"
        )

        return {
            "hit": False,
            "judge_used": False,
            "judge_decision": None,
            "cache_decision_reason": "Missing cached response",
        }

    #
    # High confidence
    #
    if similarity_score >= settings.QDRANT_HIGH_CONFIDENCE_THRESHOLD:

        logger.info(
            f"High confidence cache HIT | score={similarity_score:.2f}"
        )

        update_cache_hit(cache_result)

        return {
            "hit": True,
            "response": cached_response,
            "similarity_score": similarity_score,
            "matched_prompt": payload.get("prompt"),
            "judge_used": False,
            "judge_decision": None,
            "cache_decision_reason": "High confidence semantic match",
        }

    #
    # Medium confidence -> Judge
    #
    if similarity_score >= settings.QDRANT_JUDGE_THRESHOLD:

        logger.info(
            f"Medium confidence match | score={similarity_score:.2f}"
        )

        if not settings.ENABLE_CACHE_JUDGE:

            logger.info(
                "Cache judge disabled | treating as MISS"
            )

            return {
                "hit": False,
                "judge_used": False,
                "judge_decision": None,
                "cache_decision_reason": "Judge disabled",
            }

        logger.info(
            "Invoking cache judge"
        )

        approved = await judge_cache_reuse(
            user_prompt=prompt,
            cached_prompt=payload.get("prompt", ""),
            cached_response=cached_response,
        )

        if approved:

            logger.info(
                "Cache judge approved cache reuse"
            )

            update_cache_hit(cache_result)

            return {
                "hit": True,
                "response": cached_response,
                "similarity_score": similarity_score,
                "matched_prompt": payload.get("prompt"),
                "judge_used": True,
                "judge_decision": "APPROVED",
                "cache_decision_reason": "Approved by LLM judge",
            }

        logger.info(
            "Cache judge rejected cache reuse"
        )

        return {
            "hit": False,
            "judge_used": True,
            "judge_decision": "REJECTED",
            "cache_decision_reason": "Rejected by LLM judge",
        }

    #
    # Low confidence
    #
    logger.info(
        f"Low confidence match | score={similarity_score:.2f} | calling Gemini"
    )

    return {
        "hit": False,
        "judge_used": False,
        "judge_decision": None,
        "cache_decision_reason": "Similarity below judge threshold",
    }