from app.graph.state import AgentState


def knowledge_planner_node(state: AgentState):
    return {
        "plan": [
            "Understand knowledge request",
            "Rewrite query if needed",
            "Retrieve relevant documents",
            "Grade retrieved chunks",
            "Prepare grounded answer"
        ],
        "agents_used": state["agents_used"] + ["knowledge_planner"]
    }