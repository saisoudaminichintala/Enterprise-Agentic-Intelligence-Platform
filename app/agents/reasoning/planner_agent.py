from app.graph.state import AgentState
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def reasoning_planner_node(state: AgentState):
    result = llm_service.create_reasoning_draft(state["question"])

    return {
        "reasoning_draft": result.get("draft", ""),
        "plan": [
            "Understand the problem",
            "Break it into reasoning steps",
            "Create initial draft answer",
        ],
        "agents_used": state["agents_used"] + ["reasoning_planner_llm"],
    }