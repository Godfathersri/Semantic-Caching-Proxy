from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    GEMINI_API_KEY: str


    LLM_PROVIDER: str = "gemini"
    LLM_Model: str = "gemini-2.0-flash"

    EMBEDDING_PROVIDER: str = "gemini"
    Embedding_Model: str = "gemini-embedding-001"
    EMBEDDING_DIMENSION: int = 768

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "semantic_cache"
    QDRANT_DISTANCE: str = "COSINE"
    QDRANT_SIMILARITY_THRESHOLD: float = 0.90


    class Config:
        env_file = ".env"


settings = Settings()