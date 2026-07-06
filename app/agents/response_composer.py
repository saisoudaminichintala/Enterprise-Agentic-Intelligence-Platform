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
            f"Execution response for: {state['question']}. "
            f"Master strategy: {state['execution_strategy']}. "
            f"Workflow strategy: {state['workflow_strategy']}. "
            f"Workflow plan: {state['plan']}."
        )

    elif route == "reasoning":
        answer = (
            f"Reasoning response for: {state['question']}. "
            f"Master strategy: {state['execution_strategy']}. "
            f"Reasoning strategy: {state['reasoning_strategy']}. "
            f"Reasoning plan: {state['plan']}."
        )

    else:
        answer = state["final_answer"] or f"General response for: {state['question']}"

    return {
        "final_answer": answer,
        "agents_used": state["agents_used"] + ["response_composer_llm" if route == "knowledge" else "response_composer"],
    }