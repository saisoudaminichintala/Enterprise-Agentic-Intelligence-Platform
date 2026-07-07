from app.graph.state import AgentState
from app.schemas.execution_schema import ExecutionPlan
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def execution_supervisor_node(state: AgentState):
    raw_plan = llm_service.create_execution_plan(state["question"])
    plan = ExecutionPlan(**raw_plan)

    return {
        "workflow_strategy": plan.workflow_strategy,
        "execution_plan": plan.model_dump(),
        "approval_required": plan.requires_approval,
        "agents_used": state["agents_used"] + ["execution_supervisor_llm"],
    }