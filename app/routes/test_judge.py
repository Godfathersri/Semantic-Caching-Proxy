from fastapi import APIRouter
from pydantic import BaseModel

from app.services.cache_judge_service import judge_cache_reuse

router = APIRouter(
    prefix="/test",
    tags=["Testing"],
)


class JudgeRequest(BaseModel):
    user_prompt: str
    cached_prompt: str
    cached_response: str


@router.post("/judge")
async def test_cache_judge(request: JudgeRequest):

    result = await judge_cache_reuse(
        user_prompt=request.user_prompt,
        cached_prompt=request.cached_prompt,
        cached_response=request.cached_response,
    )

    return {
        "success": True,
        "judge_result": result,
    }