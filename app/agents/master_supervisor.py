from app.graph.state import AgentState


def master_supervisor_node(state: AgentState):
    """
    Master Supervisor validates router classification and decides
    which domain supervisor should own the request.

    Router answers:
        What type of request is this?

    Master Supervisor answers:
        Which supervisor should handle it?
        What strategy should we follow?
    """

    route = state["route"]

    if route == "knowledge":
        selected_supervisor = "knowledge_supervisor"
        strategy = "retrieve_grade_answer"

    elif route == "reasoning":
        selected_supervisor = "reasoning_supervisor"
        strategy = "plan_critique_reflect"

    elif route == "execution":
        selected_supervisor = "execution_supervisor"
        strategy = "plan_approve_execute"

    else:
        selected_supervisor = "general_responder"
        strategy = "direct_response"

    return {
        "selected_supervisor": selected_supervisor,
        "execution_strategy": strategy,
        "agents_used": state["agents_used"] + ["master_supervisor"]
    }