from app.graph.state import AgentState


def document_grader_node(state: AgentState):
    """
    Grades retrieved documents for relevance.

    Later:
    - Use an LLM or reranker to remove irrelevant chunks.
    """

    graded_docs = [
        doc for doc in state["retrieved_docs"]
        if doc is not None and len(doc.strip()) > 0
    ]

    return {
        "retrieved_docs": graded_docs,
        "agents_used": state["agents_used"] + ["document_grader_agent"]
    }