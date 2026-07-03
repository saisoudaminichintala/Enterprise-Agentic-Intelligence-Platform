from app.graph.state import AgentState


def cache_checker_node(state: AgentState):
    """
    Checks whether a similar answer already exists in semantic cache.

    Test behavior:
    - If question contains 'cached', simulate cache hit.
    - Otherwise, simulate cache miss.
    """

    question = state["question"].lower()
    cache_hit = "cached" in question

    return {
        "cache_hit": cache_hit,
        "agents_used": state["agents_used"] + ["cache_checker_agent"]
    }