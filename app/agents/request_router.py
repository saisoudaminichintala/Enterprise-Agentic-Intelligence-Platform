from app.graph.state import AgentState


def request_router_node(state: AgentState):
    question = state["question"].lower()

    if any(word in question for word in ["document", "pdf", "upload", "rag", "search"]):
        route = "knowledge"
    elif any(word in question for word in ["create", "send", "execute", "approve", "workflow"]):
        route = "execution"
    elif any(word in question for word in ["analyze", "compare", "decide", "plan", "reason"]):
        route = "reasoning"
    else:
        route = "general"

    return {
        "route": route,
        "agents_used": state["agents_used"] + ["request_router"]
    }