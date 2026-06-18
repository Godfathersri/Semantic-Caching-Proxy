from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    GEMINI_API_KEY: str

    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "semantic_cache"
    QDRANT_SIMILARITY_THRESHOLD: float = 0.90


    class Config:
        env_file = ".env"


settings = Settings()