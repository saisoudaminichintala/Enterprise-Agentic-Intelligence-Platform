from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def response_composer_node(state: AgentState):
    route = state["route"]

    if route == "knowledge":
        result = llm_service.compose_knowledge_answer(
            question=state["question"],
            retrieved_docs=state["retrieved_docs"],
            citations=state["citations"],
        )

        answer = result.get("answer", "No answer generated.")

    elif route == "execution":
        answer = (
            f"Execution plan: {state['execution_plan']}\n\n"
            f"Approval status: {state['approval_status']}\n\n"
            f"Tool result: {state['tool_result']}"
        )

    elif route == "reasoning":
        answer = (
            f"{state['reasoning_draft']}\n\n"
            f"Verification: {state['verification_result']}"
        )

    else:
        answer = state["final_answer"] or f"General response for: {state['question']}"

    return {
        "final_answer": answer,
        "agents_used": state["agents_used"] + ["response_composer_llm" if route == "knowledge" else "response_composer"],
    }