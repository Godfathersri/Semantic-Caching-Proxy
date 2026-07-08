from google import genai
from app.config import settings


if not settings.GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured"
    )
    
client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)