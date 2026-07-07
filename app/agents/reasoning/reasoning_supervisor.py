from app.graph.state import AgentState
from app.schemas.reasoning_schema import ReasoningExecutionPlan
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def reasoning_supervisor_node(state: AgentState):
    raw_plan = llm_service.create_reasoning_execution_plan(state["question"])
    plan = ReasoningExecutionPlan(**raw_plan)

    return {
        "reasoning_strategy": plan.reasoning_strategy,
        "reasoning_execution_plan": plan.model_dump(),
        "agents_used": state["agents_used"] + ["reasoning_supervisor_llm"],
    }