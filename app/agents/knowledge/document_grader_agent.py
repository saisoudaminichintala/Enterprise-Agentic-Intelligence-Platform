from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def document_grader_node(state: AgentState):
    result = llm_service.grade_documents(
        question=state["question"],
        documents=state["retrieved_docs"]
    )

    return {
        "retrieved_docs": result.get("relevant_documents", state["retrieved_docs"]),
        "document_grade_reason": result.get("reason", ""),
        "agents_used": state["agents_used"] + ["document_grader_llm"]
    }