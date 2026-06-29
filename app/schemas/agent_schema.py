from pydantic import BaseModel, Field
from typing import Optional, List

class AgentRunRequest(BaseModel):
    question: str = Field(..., min_length=1)
    agent_type: Optional[str] = "master_supervisor"

class AgentRunResponse(BaseModel):
    run_id: str
    final_answer: str
    agents_used: List[str]
