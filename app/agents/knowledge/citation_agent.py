from app.graph.state import AgentState


def citation_node(state: AgentState):
    """
    Prepares citation/source metadata for final response.

    Later:
    - Include document name
    - Page number
    - Chunk id
    - Confidence score
    """

    citations = [
        f"source-{index + 1}"
        for index, _ in enumerate(state["retrieved_docs"])
    ]

    return {
        "citations": citations,
        "agents_used": state["agents_used"] + ["citation_agent"]
    }