from pydantic import BaseModel


class ReasoningExecutionPlan(BaseModel):
    reasoning_strategy: str
    decompose_problem: bool
    critique_answer: bool
    reflect_and_improve: bool
    verify_final_answer: bool
    confidence: float
    reason: str