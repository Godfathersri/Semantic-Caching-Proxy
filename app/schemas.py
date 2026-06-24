from pydantic import BaseModel, Field, field_validator
from typing import Optional



ALLOWED_MODELS = [
    "gemini-2.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-2.0-flash",
    "gemini-2.5-flash"
]

class GenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description = "User promt sent to LLM"
    )
    model: str = Field(
        default="gemini-2.5-flash",
        description="LLM model to use"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Sampling temperature for response generation"
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        cleaned_prompt = value.strip()

        if not cleaned_prompt:
            raise ValueError("Prompt cannot be empty")
        
        if len(cleaned_prompt) > 5000:
            raise ValueError("Prompt is too long.")
        
        return cleaned_prompt

    @field_validator("model")
    @classmethod
    def validate_model(cls, value:str) -> str:
        if value not in ALLOWED_MODELS:
            raise ValueError(
                f"Invalid model. Allowed models are: {','.join(ALLOWED_MODELS)}"
            )
        return value 

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