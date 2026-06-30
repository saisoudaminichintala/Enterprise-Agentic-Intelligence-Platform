from app.graph.state import AgentState


def critic_node(state: AgentState):
    """
    Dummy critic agent.

    Later:
    - Reviews answer quality
    - Checks gaps
    - Flags missing assumptions
    """

    return {
        "agents_used": state["agents_used"] + ["critic_agent"]
    }