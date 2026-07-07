from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def critic_node(state: AgentState):
    result = llm_service.critique_reasoning(
        question=state["question"],
        draft=state["reasoning_draft"],
    )

    return {
        "critic_feedback": result.get("feedback", ""),
        "agents_used": state["agents_used"] + ["critic_agent_llm"],
    }