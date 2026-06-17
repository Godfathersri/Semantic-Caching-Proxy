from pydantic import BaseModel
from typing import Optional


class GenerateRequest(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7


class GenerateResponse(BaseModel):
    success: bool
    response: str

    cache_status: str
    similarity_score: Optional[float] = None

    latency_ms: float