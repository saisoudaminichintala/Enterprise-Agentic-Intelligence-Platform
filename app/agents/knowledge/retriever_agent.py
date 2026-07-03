from app.graph.state import AgentState


def retriever_node(state: AgentState):
    query = state["rewritten_query"] or state["question"]

    return {
        "retrieved_docs": [
            f"Dummy retrieved chunk 1 for query: {query}",
            f"Dummy retrieved chunk 2 for query: {query}"
        ],
        "agents_used": state["agents_used"] + ["retriever_agent"]
    }