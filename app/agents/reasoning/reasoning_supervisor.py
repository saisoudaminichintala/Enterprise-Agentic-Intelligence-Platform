from app.graph.state import AgentState


def reasoning_supervisor_node(state: AgentState):
    return {
        "agents_used": state["agents_used"] + ["reasoning_supervisor"]
    }