# app/services/agent_service.py

import uuid
from app.schemas.agent_schema import AgentRunRequest, AgentRunResponse


class AgentService:
    """
    AgentService controls agent execution.

    Right now:
        - Returns dummy supervisor results.

    Later:
        - Calls LangGraph graph.invoke()
        - Tracks each agent step
        - Stores run trace
        - Handles failures and retries
    """

    def run_agent(self, request: AgentRunRequest) -> AgentRunResponse:
        """
        Runs the master supervisor agent.

        Later this will be the main entry point to LangGraph.
        """

        return AgentRunResponse(
            run_id=str(uuid.uuid4()),
            final_answer=f"Master supervisor processed: {request.question}",
            agents_used=[
                "request_router",
                "master_supervisor",
                "knowledge_supervisor",
                "response_composer"
            ]
        )

    def create_plan(self, request: AgentRunRequest):
        """
        Creates a dummy execution plan.

        Later:
            - Planner agent will break the question into subtasks.
        """

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
        """
        Returns execution trace for an agent run.

        Later:
            - Pull trace from LangSmith, DB, or in-memory trace store.
        """

        return {
            "run_id": run_id,
            "trace": []
        }