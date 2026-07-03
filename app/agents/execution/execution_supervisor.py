from app.graph.state import AgentState


def execution_supervisor_node(state: AgentState):
    question = state["question"].lower()

    if any(word in question for word in ["approve", "approval"]):
        strategy = "human_approval_required"
    elif any(word in question for word in ["create", "send", "execute"]):
        strategy = "tool_execution_with_validation"
    else:
        strategy = "workflow_planning_only"

    return {
        "workflow_strategy": strategy,
        "agents_used": state["agents_used"] + ["execution_supervisor"]
    }