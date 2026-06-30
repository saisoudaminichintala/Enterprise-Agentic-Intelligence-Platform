from app.graph.state import AgentState


def master_supervisor_node(state: AgentState):
    """
    Central supervisor for the entire system.

    Right now it only records that it ran.
    Later it will:
    - Validate the route selected by request_router
    - Decide whether the task needs knowledge, reasoning, or execution
    - Enforce safety and approval policies
    """

    return {
        "agents_used": state["agents_used"] + ["master_supervisor"]
    }