import time
from fastapi import APIRouter, HTTPException

from app.schemas import GenerateRequest, GenerateResponse
from app.services.llm_service import generate_llm_response
from app.services.embedding_service import generate_embedding
from app.services.cache_service import (
    build_cache_response,
    store_cache_entry,
)
from app.services.cache_lookup_service import lookup_cache
from app.services.pii_service import detect_pii

from app.exceptions import (
    EmbeddingError,
    QdrantSearchError,
    QdrantStorageError,
    GeminiUnavailableError,
    GeminiAPIError,
)

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
    start_time = time.time()

    if not request.prompt or not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )

    try:

        pii_detected, pii_types = detect_pii(
            request.prompt
        )

        if pii_detected:

            llm_response = await generate_llm_response(
                prompt=request.prompt,
                model=request.model,
            )

            latency_ms = round(
                (time.time() - start_time) * 1000,
                2
            )

            return GenerateResponse(
                success=True,
                response=llm_response,

                cache_status="SKIPPED_PII",
                cached=False,

                similarity_score=None,
                matched_prompt=None,

                latency_ms=latency_ms,
                embedding_generated=True,

                PII_detected=True,
                pii_types=pii_types,

                judge_used=False,
                judge_decision=None,
                cache_decision_reason=None,
            )

        embedding = await generate_embedding(
            request.prompt
        )

        cache = await lookup_cache(
            prompt=request.prompt,
            embedding=embedding,
        )

        if cache["hit"]:

            latency_ms = round(
                (time.time() - start_time) * 1000,
                2
            )

            return build_cache_response(
                response=cache["response"],

                cache_status="HIT",
                cached=True,

                similarity_score=cache["similarity_score"],
                matched_prompt=cache["matched_prompt"],

                latency_ms=latency_ms,
                embedding_generated=True,

                judge_used=cache["judge_used"],
                judge_decision=cache["judge_decision"],
                cache_decision_reason=cache["cache_decision_reason"],
            )

        llm_response = await generate_llm_response(
            prompt=request.prompt,
            model=request.model,
        )

        store_cache_entry(
            prompt=request.prompt,
            response=llm_response,
            embedding=embedding,
            model=request.model,
            temperature=request.temperature,
            cache_status="MISS",
        )

        latency_ms = round(
            (time.time() - start_time) * 1000,
            2
        )

        return build_cache_response(
            response=llm_response,

            cache_status="MISS",
            cached=False,

            similarity_score=None,
            matched_prompt=None,

            latency_ms=latency_ms,
            embedding_generated=True,

            judge_used=False,
            judge_decision=None,
            cache_decision_reason=None,
        )

    except HTTPException:
        raise

    except EmbeddingError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "EMBEDDING_FAILED",
                    "message": str(error),
                },
            },
        )

    except QdrantSearchError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "QDRANT_SEARCH_FAILED",
                    "message": str(error),
                },
            },
        )

    except QdrantStorageError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "QDRANT_STORE_FAILED",
                    "message": str(error),
                },
            },
        )

    except GeminiUnavailableError:

        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "error": {
                    "code": "GEMINI_UNAVAILABLE",
                    "message": "LLM provider temporarily unavailable",
                },
            },
        )

    except GeminiAPIError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "GEMINI_API_ERROR",
                    "message": str(error),
                },
            },
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": str(error),
                },
            },
        )