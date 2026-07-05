from app.graph.state import AgentState
from app.schemas.knowledge_schema import KnowledgeExecutionPlan
from app.services.infrastructure.llm_service import LLMService

llm_service = LLMService()


def knowledge_supervisor_node(state: AgentState):
    """
    LLM-powered Knowledge Supervisor.

    It does not retrieve documents itself.
    It creates a structured execution plan that downstream nodes follow.
    """

    raw_plan = llm_service.create_knowledge_execution_plan(state["question"])

    plan = KnowledgeExecutionPlan(**raw_plan)

    return {
        "knowledge_strategy": plan.knowledge_strategy,
        "knowledge_execution_plan": plan.model_dump(),
        "agents_used": state["agents_used"] + ["knowledge_supervisor_llm"]
    }