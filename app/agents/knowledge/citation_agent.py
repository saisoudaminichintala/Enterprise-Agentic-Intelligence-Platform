from app.graph.state import AgentState


def citation_node(state: AgentState):
    """
    Prepares citation/source metadata for the final response.

    If cache hit:
        citations come from cached response metadata.

    If cache miss:
        citations come from retrieved documents.
    """

    if state["cache_hit"]:
        citations = ["cached-answer-source"]
    else:
        documents = state.get("retrieved_docs") or state.get("retrieved_documents") or []
        citations = [
            f"source-{index + 1}"
            for index, _ in enumerate(documents)
        ]

    return {
        "citations": citations,
        "agents_used": state["agents_used"] + ["citation_agent"]
    }