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
            "plan": [],
            "retrieved_docs": [],
            "final_answer": None,
            "agents_used": []
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