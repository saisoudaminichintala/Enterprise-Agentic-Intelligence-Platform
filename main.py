from fastapi import FastAPI
from app.api import health_api

app = FastAPI(
    title="Enterprise Agentic Intelligence Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Enterprise Agentic Intelligence Platform is running"}

app.include_router(health_api.router, prefix="/health", tags=["Health"])


