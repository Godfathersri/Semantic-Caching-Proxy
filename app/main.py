from fastapi import FastAPI

from app.routes import health , generate
from app.services.vector_store import vectorstore



app = FastAPI(
  title = "LLM API",
  description = "A semantic caching proxy for LLM APIs using embedding and vector search",
  version = "1.0.0"
)

app.include_router(health.router)
app.include_router(generate.router)

@app.on_event("startup")
async def startup_event():
  # Call create on the imported vectorstore instance
  vectorstore.create_collection_if_not_exists()








