from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def request_router_node(state: AgentState):
    """
    LLM-powered request router.

    Router responsibility:
    - Classify the request
    - Store route, confidence, and reason in AgentState
    """

    result = llm_service.classify_route(state["question"])

    route = result.get("route", "general")

    if route not in ["knowledge", "reasoning", "execution", "general"]:
        route = "general"

    return {
        "route": route,
        "router_confidence": float(result.get("confidence", 0.0)),
        "router_reason": result.get("reason", ""),
        "agents_used": state["agents_used"] + ["request_router_llm"]
    }