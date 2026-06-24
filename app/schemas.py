from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    prompt: str
    model: str = "gemini-2.5-flash"
    temperature: float = 0.7

class GenerateResponse(BaseModel):
    success: bool
    response: str

    cache_status: str
    cached: bool

    similarity_score: Optional[float] = None
    matched_prompt: Optional[str] = None

    latency_ms: float
    embedding_generated: bool = False

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail