from pydantic import BaseModel
from typing import Optional


class GenerateResponse(BaseModel):
    success: bool
    response: str

    cache_status: str
    similarity_score: Optional[float] = None

    latency_ms: float


class GenerateResponse(BaseModel):
    success: bool
    response: str
    cached: bool = False