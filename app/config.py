from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    GEMINI_API_KEY: str


    LLM_PROVIDER: str
    LLM_Model: str

    EMBEDDING_PROVIDER: str
    Embedding_Model: str
    EMBEDDING_DIMENSION: int

    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    QDRANT_DISTANCE: str
    QDRANT_SIMILARITY_THRESHOLD: float

    ENABLE_CACHE_JUDGE: bool
    QDRANT_HIGH_CONFIDENCE_THRESHOLD: float
    QDRANT_JUDGE_THRESHOLD: float
    CACHE_JUDGE_MODEL: str

    class Config:
        env_file = ".env"


settings = Settings()