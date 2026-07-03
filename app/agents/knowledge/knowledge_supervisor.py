from app.graph.state import AgentState


def knowledge_supervisor_node(state: AgentState):
    question = state["question"].lower()

    if any(word in question for word in ["pdf", "document", "uploaded"]):
        strategy = "document_rag"
    elif "search" in question:
        strategy = "semantic_search"
    else:
        strategy = "general_knowledge_retrieval"

    return {
        "knowledge_strategy": strategy,
        "agents_used": state["agents_used"] + ["knowledge_supervisor"]
    }