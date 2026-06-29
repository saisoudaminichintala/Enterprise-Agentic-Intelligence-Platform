from fastapi import APIRouter
from app.schemas.workflow_schema import WorkflowRequest, WorkflowApprovalRequest
from app.services.workflow_service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()


@router.post("/execute")
def execute_workflow(request: WorkflowRequest):
    return workflow_service.execute_workflow(request)


@router.post("/approve")
def approve_workflow(request: WorkflowApprovalRequest):
    return workflow_service.approve_workflow(request)