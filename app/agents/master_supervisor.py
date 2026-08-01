from app.graph.state import AgentState


from app.graph.state import AgentState


ROUTE_TO_SUPERVISOR = {
    "knowledge": "knowledge_supervisor",
    "reasoning": "reasoning_supervisor",
    "execution": "execution_supervisor",
    "general": "general_responder",
}


def master_supervisor_node(state: AgentState) -> dict:
    route = state.get("route", "general")

    selected_supervisor = ROUTE_TO_SUPERVISOR.get(
        route,
        "general_responder",
    )

    print("MASTER RECEIVED ROUTE:", repr(route))
    print("MASTER SELECTED:", selected_supervisor)

    return {
        "selected_supervisor": selected_supervisor,
        "agents_used": state.get("agents_used", [])
        + ["master_supervisor"],
    }