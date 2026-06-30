from app.graph.state import AgentState


def execution_supervisor_node(state: AgentState):
    return {
        "agents_used": state["agents_used"] + ["execution_supervisor"]
    }