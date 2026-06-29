import uuid
from app.schemas.workflow_schema import WorkflowRequest, WorkflowApprovalRequest


class WorkflowService:
    """
    Handles workflow execution logic.

    Later this will:
    - Select tools
    - Create action plans
    - Require approval for risky actions
    - Execute external APIs
    - Store workflow status
    """

    def execute_workflow(self, request: WorkflowRequest):
        return {
            "run_id": str(uuid.uuid4()),
            "task": request.task,
            "status": "WAITING_FOR_APPROVAL" if request.requires_approval else "EXECUTED"
        }

    def approve_workflow(self, request: WorkflowApprovalRequest):
        return {
            "run_id": request.run_id,
            "approved": request.approved,
            "status": "APPROVED" if request.approved else "REJECTED",
            "comments": request.comments
        }