from pydantic import BaseModel


class ExecutionPlan(BaseModel):
    workflow_strategy: str
    tool_needed: str
    requires_approval: bool
    risk_level: str
    execution_steps: list[str]
    confidence: float
    reason: str