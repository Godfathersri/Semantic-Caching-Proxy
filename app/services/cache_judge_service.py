from app.config import settings
from app.exceptions import (
    GeminiAPIError,
    GeminiUnavailableError,
)
from app.logger import logger
from app.services.gemini_client import client


async def judge_cache_reuse(
    user_prompt: str,
    cached_prompt: str,
    cached_response: str,
) -> bool:
    """
    Determines whether a cached response can safely answer
    the current user prompt.

    Returns:
        True  -> Reuse cached response
        False -> Generate a new response
    """

    logger.info("Invoking cache judge")

    judge_prompt = f"""
You are an AI cache validator.

Your task is to determine whether the cached response fully
and correctly answers the new user prompt.

Consider the following:

- Does the cached response answer the user's request?
- Is any important information missing?
- Would generating a new response significantly improve the answer?

Respond with ONLY one word:

true

or

false

User Prompt:
{user_prompt}

Cached Prompt:
{cached_prompt}

Cached Response:
{cached_response}
"""

    try:

        response = client.models.generate_content(
            model=settings.LLM_Model,
            contents=judge_prompt,
        )

        if not response.text:
            raise GeminiAPIError(
                "Judge returned an empty response."
            )

        decision = response.text.strip().lower()

        if decision.startswith("true"):
            logger.info(
                "Cache judge approved reuse"
            )
            return True

        if decision.startswith("false"):
            logger.info(
                "Cache judge rejected reuse"
            )
            return False

        raise GeminiAPIError(
            f"Unexpected judge response: {decision}"
        )

    except (
        GeminiAPIError,
        GeminiUnavailableError,
    ):
        raise

    except Exception as e:

        logger.error(
            f"Cache judge failed: {str(e)}"
        )

        error_message = str(e)

        if (
            "503" in error_message
            or "UNAVAILABLE" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):
            raise GeminiUnavailableError(
                "Gemini service is under heavy load."
            )

        raise GeminiAPIError(
            error_message
        )