from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def query_rewriter_node(state: AgentState):
    """
    LLM-powered query rewriting agent.

    Purpose:
    - Convert the user question into a better retrieval query.
    - Improve vector search quality.
    - Keep retrieval separate from answer generation.
    """

    result = llm_service.rewrite_query(state["question"])

    rewritten_query = result.get("rewritten_query") or state["question"]

    return {
        "rewritten_query": rewritten_query,
        "query_rewrite_reason": result.get("reason", ""),
        "agents_used": state["agents_used"] + ["query_rewriter_llm"]
    }