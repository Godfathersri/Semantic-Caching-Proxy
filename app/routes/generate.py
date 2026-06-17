import time 
from fastapi import APIRouter , HTTPException

from app.schemas import GenerateRequest , GenerateResponse
from app.services.llm_service import generate_llm_response


router = APIRouter()

@router.post("/generate" , response_model=GenerateResponse)
async def generate_response(request: GenerateRequest):
  start_time = time.time()

  if not request.prompt or not request.prompt.strip():
    raise HTTPException(
      status_code = 400,
      detail = "Prompt cannot be empty "
    )
  
  try:
    llm_response = await generate_llm_response(
      prompt= request.prompt,
      model = request.model
    )

    latency_ms = round((time.time() - start_time) * 1000 , 2)

    return GenerateResponse(
      success = True,
      response = llm_response,
      cache_status = "MISS",
      cached= False,
      similarity_score = None,
      latency_ms = latency_ms
    )
  except ValueError as error:
    raise HTTPException(
      status_code = 500,
      detail = str(error)
    )
  except Exception as error:
    raise HTTPException(
      status_code = 500,
      detail = f"LLM API Failed: {str(error)}"
    )
   