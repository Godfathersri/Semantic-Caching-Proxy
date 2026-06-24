from fastapi import HTTPException
from google import genai
from app.logger import logger
from app.config import settings
from app.exceptions import EmbeddingError


if not settings.GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")


client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_embedding(text:str) -> list[float]:
    """
    Generating embedding for the given text
    """

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )
    
    if settings.EMBEDDING_PROVIDER != "gemini":
        raise HTTPException(
            status_code=400,
            detail=f"unsupported embedding provider: {settings.EMBEDDING_PROVIDER}"
        )
    
    try:
        logger.info("Generating embedding")
        response = client.models.embed_content(
            model=settings.Embedding_Model,
            contents=text,
            config={
                "output_dimensionality": settings.EMBEDDING_DIMENSION
            }
        )
        embedding = response.embeddings[0].values

        if not embedding:
            logger.error(
                "Embedding service returned empty embedding"
            )
            raise HTTPException(
                status_code=500,
                detail="Failed to generate embedding"
            )
        
        logger.info(
            "Embedding generated successfully"
        )
        return embedding
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Embedding generation failed: {str(e)}")
        raise EmbeddingError(
            f"Embedding generation failed: {str(e)}"
        )
