from app.graph.state import AgentState


def human_approval_node(state: AgentState):
    if state["approval_required"]:
        approval_status = "WAITING_FOR_HUMAN_APPROVAL"
    else:
        approval_status = "NOT_REQUIRED"

    return {
        "approval_status": approval_status,
        "agents_used": state["agents_used"] + ["human_approval_agent"],
    }