import time
from fastapi import APIRouter, HTTPException

from app.schemas import GenerateRequest, GenerateResponse
from app.services.llm_service import generate_llm_response
from app.services.embedding_service import generate_embedding
from app.services.vector_store import vectorstore
from app.services.cache_service import build_cache_response, store_cache_entry, update_cache_hit
from app.services.pii_service import detect_pii
from app.logger import logger

from app.config import settings
from app.exceptions import (
    EmbeddingError,
    QdrantSearchError,
    QdrantStorageError,
    GeminiUnavailableError,
    GeminiAPIError
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

        pii_detected , pii_types = detect_pii(request.prompt)

        if pii_detected:
            llm_response = await generate_llm_response(
                prompt = request.prompt,
                model = request.model,
            )
            latency_ms = round((time.time() - start_time) * 1000, 2)

            return GenerateResponse(
                success=True,
                response=llm_response,
                cache_status="SKIPPED_PII",
                cached=False,
                similarity_score=None,
                latency_ms=latency_ms,
                matched_prompt=None,
                embedding_generated=True,
                PII_detected = True,
                pii_types=pii_types
            )
        
        embedding = await generate_embedding(request.prompt)

        logger.info("Embedding generated successfully")
        logger.info(f"Embedding dimension: {len(embedding)}")

        cache_result = vectorstore.search_similar(
            embedding=embedding
        )

        logger.info(f"Cache search completed. Result: {cache_result}")

        if cache_result:
            logger.info(f"Potential cache match found | Similarity score: {cache_result.score}")

            if (
                cache_result.score is not None
                and cache_result.score >= settings.QDRANT_SIMILARITY_THRESHOLD
            ):
                payload = cache_result.payload or {}

                if not payload:
                    logger.info("Cache HIT candidate found, but payload is missing")
                else:
                    cached_response = payload.get("response")

                    if not cached_response:
                        logger.info("Cache HIT candidate found, but response is missing from payload")
                    else:
                        logger.info(f"Cache HIT | score={similarity_score:.2f}")

                        update_cache_hit(cache_result)

                        latency_ms = round((time.time() - start_time) * 1000, 2)

                        return build_cache_response(
                            response=cached_response,
                            cache_status="HIT",
                            cached=True,
                            similarity_score=cache_result.score,
                            latency_ms=latency_ms,
                            matched_prompt=payload.get("prompt"),
                            embedding_generated=True
                        )
            else:
                logger.info("Cache MISS | calling Gemini")
        else:
            logger.info("Cache no found | calling Gemini")

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
            cache_status="MISS"
        )

        print("Stored item successfully")

        latency_ms = round((time.time() - start_time) * 1000, 2)

        return build_cache_response(
            response=llm_response,
            cache_status="MISS",
            cached=False,
            similarity_score=None,
            latency_ms=latency_ms,
            matched_prompt=None,
            embedding_generated=True
        )

    except HTTPException:
        raise

    except EmbeddingError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code":
                        "EMBEDDING_FAILED",
                    "message":
                        str(error)
                }
            }
        )

    except QdrantSearchError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code":
                        "QDRANT_SEARCH_FAILED",
                    "message":
                        str(error)
                }
            }
        )

    except QdrantStorageError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code":
                        "QDRANT_STORE_FAILED",
                    "message":
                        str(error)
                }
            }
        )

    except GeminiUnavailableError:

        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "error": {
                    "code":
                        "GEMINI_UNAVAILABLE",
                    "message":
                        "LLM provider temporarily unavailable"
                }
            }
        )

    except GeminiAPIError as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code":
                        "GEMINI_API_ERROR",
                    "message":
                        str(error)
                }
            }
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code":
                        "INTERNAL_SERVER_ERROR",
                    "message":
                        str(error)
                }
            }
        )