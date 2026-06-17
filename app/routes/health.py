from fastapi import APIRouter


router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Welcome to the LLM API",
        "docs": "/docs"
    }


@router.get("/health")
def health_check():
  return {
      "status": "ok",
      "message": "LLM API is healthy"
    }