from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.schemas.agent_schema import AgentRunRequest
from app.services.business.agent_service import AgentService


class ChatService:
    """
    ChatService handles user-facing chat requests.

    Instead of directly returning a dummy response, it now delegates
    the request to AgentService.

    This means /chat and /agents/run can both use the same LangGraph workflow.
    """

    def __init__(self):
        self.agent_service = AgentService()

    def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        Converts a chat request into an agent run request.

        Flow:
            ChatRequest
                ↓
            AgentRunRequest
                ↓
            AgentService.run_agent()
                ↓
            LangGraph workflow
                ↓
            ChatResponse
        """

        agent_request = AgentRunRequest(
            question=request.question,
            agent_type="master_supervisor"
        )

        agent_response = self.agent_service.run_agent(agent_request)

        return ChatResponse(
            answer=agent_response.final_answer,
            conversation_id=request.conversation_id,
            sources=[]
        )

    def get_chat_history(self, conversation_id: str):
        return {
            "conversation_id": conversation_id,
            "messages": []
        }

    def stream_chat(self, request: ChatRequest):
        return {
            "message": "Streaming will be implemented later",
            "question": request.question
        }