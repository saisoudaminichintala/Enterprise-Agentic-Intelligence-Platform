from app.graph.state import AgentState


def human_approval_node(state: AgentState):
    return {
        "agents_used": state["agents_used"] + ["human_approval_agent"]
    }