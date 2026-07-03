from app.graph.state import AgentState


def reasoning_supervisor_node(state: AgentState):
    question = state["question"].lower()

    if any(word in question for word in ["compare", "versus", "vs"]):
        strategy = "comparative_reasoning"
    elif any(word in question for word in ["plan", "steps", "design"]):
        strategy = "planning_reasoning"
    else:
        strategy = "analytical_reasoning"

    return {
        "reasoning_strategy": strategy,
        "agents_used": state["agents_used"] + ["reasoning_supervisor"]
    }