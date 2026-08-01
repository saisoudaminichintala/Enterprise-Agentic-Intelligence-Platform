from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService


llm_service = LLMService()


def response_composer_node(state: AgentState) -> dict:
    """
    Produces the final response from the normalized output of the
    supervisor branch selected for the request.

    The execution branch consumes execution_answer produced by the
    execution_response_composer node instead of interpreting raw
    tool output directly.
    """

    route = state.get("route", "general")
    agents_used = state.get("agents_used", [])

    if route == "knowledge":
        result = llm_service.compose_knowledge_answer(
            question=state.get("question", ""),
            retrieved_docs=state.get("retrieved_docs", []),
            citations=state.get("citations", []),
        )

        answer = result.get(
            "answer",
            "The knowledge workflow did not generate an answer.",
        )

        composer_agent = "response_composer_llm"

    elif route == "execution":
        answer = state.get(
            "execution_answer",
            "The execution workflow did not generate an answer.",
        )

        composer_agent = "response_composer"

    elif route == "reasoning":
        reasoning_draft = state.get(
            "reasoning_draft",
            "The reasoning workflow did not generate an answer.",
        )

        verification_result = state.get(
            "verification_result",
            "not_verified",
        )

        answer = (
            f"{reasoning_draft}\n\n"
            f"Verification: {verification_result}"
        )

        composer_agent = "response_composer"

    else:
        answer = (
            state.get("final_answer")
            or state.get("general_response")
            or f"General response for: {state.get('question', '')}"
        )

        composer_agent = "response_composer"

    return {
        "final_answer": answer,
        "agents_used": agents_used + [composer_agent],
    }