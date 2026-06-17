from fastapi import HTTPException
from google import genai

from app.config import settings


if not settings.GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured"
    )


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


async def generate_llm_response(
    prompt: str,
    model: str = "gemini-2.5-flash"
) -> str:
    """
    Send prompt to Gemini and return generated text.
    """

    if not prompt or not prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )

    try:

        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="LLM returned an empty response"
            )

        return response.text

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM request failed: {str(e)}"
        )