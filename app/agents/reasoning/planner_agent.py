from app.graph.state import AgentState


def reasoning_planner_node(state: AgentState):
    return {
        "plan": [
            "Break the complex problem into subtasks",
            "Analyze each subtask",
            "Check assumptions",
            "Prepare final reasoning response"
        ],
        "agents_used": state["agents_used"] + ["reasoning_planner"]
    }