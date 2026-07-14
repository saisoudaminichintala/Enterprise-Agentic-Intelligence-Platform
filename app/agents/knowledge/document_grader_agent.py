from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService


llm_service = LLMService()


def document_grader_node(
    state: AgentState,
) -> dict:
    original_documents = state["retrieved_docs"]

    print(
        "Documents before grading:",
        original_documents,
    )

    result = llm_service.grade_documents(
        question=state["question"],
        documents=original_documents,
    )

    print(
        "Document grader result:",
        result,
    )

    relevant_documents = result.get(
        "relevant_documents"
    )

    if not relevant_documents:
        relevant_documents = original_documents

    return {
        "retrieved_docs": relevant_documents,
        "document_grade_reason": result.get(
            "reason",
            "No grading reason provided.",
        ),
        "agents_used": (
            state["agents_used"]
            + ["document_grader_llm"]
        ),
    }