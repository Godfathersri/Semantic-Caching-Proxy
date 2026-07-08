from fastapi import HTTPException
from google import genai

from app.exceptions import GeminiAPIError, GeminiUnavailableError
from app.services.gemini_client import client

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

        error_message = str(e)
        if (
            "503" in error_message
            or "UNAVAILABLE" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):
            raise GeminiUnavailableError(
                "Gemini service is under heavy load"
            )

        raise GeminiAPIError(error_message)