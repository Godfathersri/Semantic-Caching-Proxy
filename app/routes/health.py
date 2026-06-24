from fastapi import APIRouter
from app.config import settings
from app.services.vector_store import vectorstore


router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Welcome to the LLM API",
        "docs": "/docs"
    }


@router.get("/health")
def health_check():
    qdrant_status = "Unknown"

    try: 
        vectorstore.check_qdrant_connection()
        qdrant_status = "Connected"
    except Exception:
        qdrant_status = "disconnected"
    
    llm_status = "configured" if settings.GEMINI_API_KEY else "missing_api_key"
  

    return {
        "status": "ok",
        "qdrant_status" : qdrant_status,
        "llm_provider": settings.LLM_PROVIDER,
        "llm_status": llm_status,
        "embedding_model": settings.Embedding_Model,
        "collection_name" : settings.QDRANT_COLLECTION,
        "message": "LLM API is healthy"
    }