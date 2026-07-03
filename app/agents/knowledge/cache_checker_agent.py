from app.graph.state import AgentState


def cache_checker_node(state: AgentState):
    """
    Checks whether a similar answer already exists in semantic cache.

    Right now:
    - Always returns cache miss.

    Later:
    - Compare query embedding against cached queries.
    - If cache hit, skip retrieval and LLM generation.
    """

    return {
        "cache_hit": False,
        "agents_used": state["agents_used"] + ["cache_checker_agent"]
    }