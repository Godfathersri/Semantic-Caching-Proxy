from fastapi import HTTPException
from google import genai

from app.config import settings


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
        response = client.models.embed_content(
            model=settings.Embedding_Model,
            contents=text,
            config={
                "output_dimension": settings.EMBEDDING_DIMENSION
            }
        )
        embedding = response.embeddings[0].values

        if not embedding:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate embedding"
            )
        
        return embedding
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(
          status_code=500,
          detail=f"Embedding generation failed: {str(e)}"   
        ) 
