from fastapi import HTTPException
from google import genai
from app.logger import logger
from app.config import settings
from app.exceptions import GeminiAPIError, GeminiUnavailableError

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
        logger.info(
            f"Calling Gemini | model={model}"
        )
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        if not response.text:
            logger.error(
                "Gemini returned empty response"
            )
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
            logger.error(
                f"Gemini unavailable: {error_message}"
            )
            raise GeminiUnavailableError(
                "Gemini service is under heavy load"
            )

        logger.error(
            f"Gemini generation failed: {error_message}"
        )
        raise GeminiAPIError(error_message)