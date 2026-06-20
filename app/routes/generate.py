import time
from fastapi import APIRouter, HTTPException

from app.schemas import GenerateRequest, GenerateResponse
from app.services.llm_service import generate_llm_response
from app.services.embedding_service import generate_embedding
from app.services.vector_store import vectorstore
from app.config import settings


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
        # 1. Generate embedding first
        embedding = await generate_embedding(request.prompt)

        print("Embedding generated successfully")
        print("Embedding dimension:", len(embedding))

        # 2. Search Qdrant cache
        cache_result = vectorstore.search_similar(
            embedding=embedding
        )

        print("Cache search completed. Result:", cache_result)

        # 3. Check if cache result exists
        if cache_result:
            print("Potential cache match found")
            print("Similarity score:", cache_result.score)

            # 4. Check if score is above threshold
            if (
                cache_result.score is not None
                and cache_result.score >= settings.QDRANT_SIMILARITY_THRESHOLD
            ):
                payload = cache_result.payload or {}

                if not payload:
                    print("Cache HIT candidate found, but payload is missing")
                else:
                    cached_response = payload.get("response")

                    if not cached_response:
                        print("Cache HIT candidate found, but response is missing from payload")
                    else:
                        print("Cache HIT")
                        print("Returning cached response")

                        latency_ms = round((time.time() - start_time) * 1000, 2)

                        return GenerateResponse(
                            success=True,
                            response=cached_response,
                            cache_status="HIT",
                            cached=True,
                            similarity_score=cache_result.score,
                            latency_ms=latency_ms,
                            embedding_generated=True
                        )
            else:
                print("Cache match below similarity threshold")
        else:
            print("No cache match found")

        # 5. If code reaches here, it means cache HIT did not happen
        print("Cache MISS")
        print("Calling Gemini")

        llm_response = await generate_llm_response(
            prompt=request.prompt,
            model=request.model
        )

        # 6. Store new response in Qdrant
        vectorstore.store_cache_item(
            prompt=request.prompt,
            response=llm_response,
            embedding=embedding,
            model=request.model,
            cache_status="MISS"
        )

        print("Stored item successfully")

        latency_ms = round((time.time() - start_time) * 1000, 2)

        return GenerateResponse(
            success=True,
            response=llm_response,
            cache_status="MISS",
            cached=False,
            similarity_score=None,
            latency_ms=latency_ms,
            embedding_generated=True
        )

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"LLM API Failed: {str(error)}"
        )
