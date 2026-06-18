from fastapi import FastAPI

from app.routes import health , generate



app = FastAPI(
  title = "LLM API",
  description = "A semantic caching proxy for LLM APIs using embedding and vector search",
  version = "1.0.0"
)

app.include_router(health.router)
app.include_router(generate.router)

@app.on_event("startup")
async def startup_event():

    vector_store.create_collection_if_not_exists()








