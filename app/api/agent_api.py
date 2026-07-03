
from fastapi import APIRouter
from app.schemas.agent_schema import AgentRunRequest, AgentRunResponse
from app.services.business.agent_service import AgentService

router = APIRouter()

agent_service = AgentService()


@router.post("/run", response_model=AgentRunResponse)
def run_agent(request: AgentRunRequest):
    """
    Runs the complete multi-agent workflow.
    """

    return agent_service.run_agent(request)


@router.post("/plan")
def create_agent_plan(request: AgentRunRequest):
    """
    Creates an execution plan before running agents.
    """

    return agent_service.create_plan(request)


@router.get("/trace/{run_id}")
def get_agent_trace(run_id: str):
    """
    Returns agent execution trace.
    """

    return agent_service.get_trace(run_id)