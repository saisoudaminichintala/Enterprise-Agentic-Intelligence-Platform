from app.graph.state import AgentState


def general_responder_node(state: AgentState):
    return {
        "final_answer": f"General response for: {state['question']}",
        "agents_used": state["agents_used"] + ["general_responder"]
    }