from app.graph.state import AgentState


def workflow_planner_node(state: AgentState):
    return {
        "plan": [
            "Understand requested action",
            "Identify required tool",
            "Check if approval is needed",
            "Prepare execution payload"
        ],
        "agents_used": state["agents_used"] + ["workflow_planner"]
    }