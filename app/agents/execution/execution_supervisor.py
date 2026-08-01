from app.graph.state import AgentState
from app.schemas.execution_schema import ExecutionPlan
from app.services.infrastructure.llm_service import LLMService


llm_service = LLMService()


def execution_supervisor_node(state: AgentState) -> dict:
    """
    Creates a high-level execution plan.

    This node decides the execution strategy but does not select
    or execute individual tools.
    """

    question = state.get("question", "").strip()
    agents_used = state.get("agents_used", [])

    if not question:
        return {
            "workflow_strategy": "no_execution",
            "execution_plan": {},
            "approval_required": False,
            "agents_used": agents_used + ["execution_supervisor_llm"],
        }

    raw_plan = llm_service.create_execution_plan(question)
    plan = ExecutionPlan.model_validate(raw_plan)

    return {
        "workflow_strategy": plan.workflow_strategy,
        "execution_plan": plan.model_dump(),
        "approval_required": plan.requires_approval,
        "agents_used": agents_used + ["execution_supervisor_llm"],
    }