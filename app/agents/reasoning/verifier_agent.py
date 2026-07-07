from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def verifier_node(state: AgentState):
    result = llm_service.verify_reasoning_answer(
        question=state["question"],
        answer=state["reasoning_draft"],
    )

    return {
        "verification_result": result.get("verification_result", "needs_revision"),
        "agents_used": state["agents_used"] + ["verifier_agent_llm"],
    }