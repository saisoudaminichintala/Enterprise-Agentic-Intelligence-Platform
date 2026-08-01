from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService


llm_service = LLMService()


EXECUTION_KEYWORDS = {
    "calculate",
    "compute",
    "multiply",
    "divide",
    "subtract",
    "add",
    "sum",
    "percentage",
    "percent",
    "search the web",
    "web search",
    "latest",
    "current",
    "run",
    "execute",
    "query",
    "sql",
    "github",
    "use a tool",
}


def requires_execution(question: str) -> bool:
    normalized_question = question.lower().strip()

    return any(
        keyword in normalized_question
        for keyword in EXECUTION_KEYWORDS
    )


def request_router_node(state: AgentState) -> dict:
    question = state.get("question", "")

    result = llm_service.classify_route(question)
    route = str(result.get("route", "general")).strip().lower()

    print("ROUTER QUESTION:", question)
    print("ROUTER RAW RESULT:", result)
    print("ROUTER RAW ROUTE:", repr(route))

    allowed_routes = {
        "knowledge",
        "reasoning",
        "execution",
        "general",
    }

    if route not in allowed_routes:
        print("INVALID ROUTE—FALLING BACK TO GENERAL:", repr(route))
        route = "general"

    print("ROUTER FINAL ROUTE:", route)

    return {
        "route": route,
        "router_confidence": float(
            result.get("confidence", 0.0)
        ),
        "router_reason": result.get("reason", ""),
        "agents_used": state.get("agents_used", [])
        + ["request_router_llm"],
    }