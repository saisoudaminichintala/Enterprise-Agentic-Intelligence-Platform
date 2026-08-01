# Enterprise Agentic Intelligence Platform

> A production-inspired multi-agent AI platform built with FastAPI, LangGraph, Groq, and Qdrant to demonstrate routing, retrieval, tool execution, and agent orchestration in a modular backend.

---

## Overview

The Enterprise Agentic Intelligence Platform is a working example of an enterprise-style AI system that goes beyond a single prompt-response loop. It combines:

- request routing across knowledge, reasoning, execution, and general branches
- a hierarchical supervisor architecture with LangGraph
- retrieval-augmented generation for document-based questions
- tool selection and execution for calculator and web-search-style tasks
- structured response composition with deterministic fallbacks

The implementation is organized around clear layers: API, business services, agents, graph state, tools, and infrastructure.

---

## What is implemented now

### Multi-agent orchestration

- request router and master supervisor
- specialized knowledge, reasoning, and execution supervisors
- graph-based execution flow with explicit state transitions
- agent usage tracking throughout the workflow

### Knowledge workflow

- document upload and indexing flow
- vector search integration with Qdrant
- retrieval, document grading, citation generation, and answer composition
- state-safe handling when retrieval data is missing

### Execution workflow

- tool registry with registered tools for:
  - calculator
  - web search
  - generic fallback execution
- tool selection and execution via dedicated agent nodes
- response composition for successful and failed tool execution

### General workflow

- general responder for simple direct questions and text transformations
- LLM-backed general responses with fallback behavior if the model call fails

---

## Current architecture

```text
Client
  │
  ▼
FastAPI endpoints
  │
  ▼
AgentService / graph runner
  │
  ▼
Request Router → Master Supervisor
  │
  ├── Knowledge Supervisor
  │     └── Retriever / Grader / Citation / Composer
  │
  ├── Reasoning Supervisor
  │     └── Planner / Critic / Reflection / Verifier
  │
  └── Execution Supervisor
        └── Workflow Planner / Tool Selector / Tool Executor / Response Composer
```

---

## Technology stack

| Layer | Technologies |
| --- | --- |
| Backend | Python, FastAPI |
| Orchestration | LangGraph |
| LLM provider | Groq |
| Embeddings | Sentence Transformers |
| Vector database | Qdrant |
| Validation | Pydantic |
| Configuration | pydantic-settings |

---

## Quick start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Set the required environment values for Groq and Qdrant access, depending on your local setup.

### 3. Run the API

```bash
uvicorn main:app --reload
```

The app will be available at:

- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/agents/run

---

## API surface

### Agent execution

POST /agents/run

Example payload:

```json
{
  "question": "What is LangGraph?",
  "agent_type": "master_supervisor"
}
```

Response:

```json
{
  "run_id": "...",
  "final_answer": "...",
  "agents_used": ["request_router_llm", "master_supervisor", "..."]
}
```

### Document workflow

- POST /documents/upload
- GET /documents
- POST /documents/index
- DELETE /documents/{document_id}

### RAG and workflow endpoints

- /rag/...
- /workflow/...
- /health/...
- /metrics/...
- /chat/...

---

## Repository structure

```text
Enterprise-Agentic-Intelligence-Platform/
├── app/
│   ├── agents/
│   │   ├── execution/
│   │   ├── knowledge/
│   │   └── reasoning/
│   ├── api/
│   ├── config/
│   ├── core/
│   ├── graph/
│   ├── schemas/
│   ├── services/
│   │   ├── business/
│   │   └── infrastructure/
│   └── tools/
├── docs/
├── tests/
├── main.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Testing

Run the unit tests with:

```bash
pytest
```

The test suite covers tool execution, execution response composition, and Qdrant-related behaviors.

---

## Recent updates

The project has recently been expanded to include:

- LLM-backed general responses for simple requests
- calculator execution support in the tool workflow
- generic fallback tool behavior for simple transformations
- robust response composition fallbacks when LLM formatting fails
- improved state handling for knowledge workflow steps that do not always receive retrieved documents

---

## Notes

This repository is intended as an educational and portfolio-style implementation of an enterprise-inspired agent platform. It demonstrates how modular agents, workflow orchestration, retrieval pipelines, and tools can be combined into a coherent backend architecture.
