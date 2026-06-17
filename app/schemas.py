from pydantic import BaseModel
from typing import Optional


class GenerateRequest(BaseModel):
    prompt: str
    model: str
    temperature: float = 0


class GenerateResponse(BaseModel):
    success: bool
    response: str
    cached: bool = False