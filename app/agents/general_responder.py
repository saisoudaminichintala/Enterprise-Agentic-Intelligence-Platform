from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService


llm_service = LLMService()


def general_responder_node(state: AgentState) -> dict:
    """
    Handles simple requests that do not require retrieval,
    complex reasoning, or external tools.
    """

    question = state.get("question", "").strip()
    agents_used = state.get("agents_used", [])

    if not question:
        return {
            "general_response": "Please provide a request.",
            "agents_used": agents_used + ["general_responder"],
        }

    try:
        answer = llm_service.generate_general_response(question)
    except Exception:
        answer = (
            "I can help with simple text transformations, direct questions, "
            "summaries, or rewrites."
        )

    return {
        "general_response": answer,
        "agents_used": agents_used + ["general_responder_llm"],
    }