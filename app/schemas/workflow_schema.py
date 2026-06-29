from pydantic import BaseModel, Field
from typing import Optional


class WorkflowRequest(BaseModel):
    task: str = Field(..., min_length=1)
    requires_approval: bool = True


class WorkflowApprovalRequest(BaseModel):
    run_id: str
    approved: bool
    comments: Optional[str] = None