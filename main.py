from fastapi import FastAPI
from app.api import (
    health_api,
    chat_api,
    agent_api,
    document_api,
    rag_api,
    workflow_api,
    metrics_api
)

app = FastAPI(
    title="Enterprise Agentic Intelligence Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "application": "Enterprise Agentic Intelligence Platform",
        "version": "1.0.0",
        "status": "Running"
    }

app.include_router(health_api.router, prefix="/health", tags=["Health"])
app.include_router(chat_api.router, prefix="/chat", tags=["Chat"])
app.include_router(agent_api.router, prefix="/agents", tags=["Agents"])
app.include_router(document_api.router, prefix="/documents", tags=["Documents"])

app.include_router(rag_api.router, prefix="/rag", tags=["RAG"])
app.include_router(workflow_api.router, prefix="/workflow", tags=["Workflow"])
app.include_router(metrics_api.router, prefix="/metrics", tags=["Metrics"])