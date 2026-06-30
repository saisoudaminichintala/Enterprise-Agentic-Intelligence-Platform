from app.graph.state import AgentState


def retriever_node(state: AgentState):
    return {
        "retrieved_docs": [
            "Dummy document chunk 1",
            "Dummy document chunk 2"
        ],
        "agents_used": state["agents_used"] + ["retriever_agent"]
    }