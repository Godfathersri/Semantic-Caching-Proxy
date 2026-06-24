from fastapi import FastAPI

from app.config import settings

from app.routes import health, generate, cache

from app.services.vector_store import vectorstore

app = FastAPI(
    title="LLM API",
    description="A semantic caching proxy for LLM APIs using embedding and vector search",
    version="1.0.0"
)

app.include_router(health.router)

app.include_router(generate.router)

app.include_router(cache.router)

@app.on_event("startup")
async def startup_event():
    print("Starting up the application...")


    if settings.LLM_PROVIDER == "gemini" and not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing. Please add it to the environment variables.")
    
    print("API Key validation passed.") 

    vectorstore.check_qdrant_connection()
    print("Qdrant collection successfully checked/created.")

    vectorstore.create_collection_if_not_exists()
    print("Qdrant collection ready")

    print("Routes loaded: /health, /generate, /cache/stats, /cache/items")
    print("Application startup compelete successfully.")
