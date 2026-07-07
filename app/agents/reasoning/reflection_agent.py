from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def reflection_node(state: AgentState):
    result = llm_service.reflect_and_improve(
        question=state["question"],
        draft=state["reasoning_draft"],
        feedback=state["critic_feedback"],
    )

    return {
        "reasoning_draft": result.get("improved_answer", state["reasoning_draft"]),
        "reflection_notes": result.get("reflection_notes", ""),
        "agents_used": state["agents_used"] + ["reflection_agent_llm"],
    }