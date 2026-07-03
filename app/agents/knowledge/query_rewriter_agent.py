from app.graph.state import AgentState


def query_rewriter_node(state: AgentState):
    """
    Rewrites the user's question into a cleaner retrieval query.

    Later:
    - Use an LLM to rewrite vague/long questions.
    - Expand acronyms.
    - Add domain-specific search terms.
    """

    rewritten_query = state["question"].strip()

    return {
        "rewritten_query": rewritten_query,
        "agents_used": state["agents_used"] + ["query_rewriter_agent"]
    }