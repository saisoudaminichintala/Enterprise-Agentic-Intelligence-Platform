from app.graph.state import AgentState


def knowledge_supervisor_node(state: AgentState):
    return {
        "agents_used": state["agents_used"] + ["knowledge_supervisor"]
    }