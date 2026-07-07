from app.graph.state import AgentState


def workflow_planner_node(state: AgentState):
    execution_plan = state["execution_plan"]

    return {
        "plan": execution_plan.get("execution_steps", []),
        "agents_used": state["agents_used"] + ["workflow_planner_agent"],
    }