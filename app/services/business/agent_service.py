import uuid
from app.schemas.agent_schema import AgentRunRequest, AgentRunResponse
from app.graph.graph_builder import build_agent_graph


class AgentService:
    def __init__(self):
        self.graph = build_agent_graph()

    def run_agent(self, request: AgentRunRequest) -> AgentRunResponse:
        initial_state = {
            "question": request.question,
            "route": None,
            "router_confidence": 0.0,
            "router_reason": "",
            "selected_supervisor": None,
            "execution_strategy": None,
            "knowledge_strategy": None,
            "reasoning_strategy": None,
            "workflow_strategy": None,
            "rewritten_query": None,
            "query_rewrite_reason": "",
            "cache_hit": False,
            "citations": [],
            "plan": [],
            "retrieved_docs": [],
            "document_grade_reason": "",
            "final_answer": None,
            "agents_used": [],
            "knowledge_execution_plan": {},
            "reasoning_execution_plan": {},
            "reasoning_draft": "",
            "critic_feedback": "",
            "reflection_notes": "",
            "verification_result": "",
            "execution_plan": {},
            "approval_required": False,
            "approval_status": "NOT_REQUIRED",
            "tool_result": "",
            "selected_tool": "",
            "tool_input": {},
        }   
        

        result = self.graph.invoke(initial_state)

        return AgentRunResponse(
            run_id=str(uuid.uuid4()),
            final_answer=result["final_answer"],
            agents_used=result["agents_used"]
        )

    def create_plan(self, request: AgentRunRequest):
        return {
            "question": request.question,
            "plan": [
                "Classify request",
                "Choose supervisor",
                "Retrieve knowledge",
                "Reason over results",
                "Generate final response"
            ]
        }

    def get_trace(self, run_id: str):
        return {
            "run_id": run_id,
            "trace": []
        }