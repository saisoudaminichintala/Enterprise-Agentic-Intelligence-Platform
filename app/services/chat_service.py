# app/services/chat_service.py

from app.schemas.chat_schema import ChatRequest, ChatResponse


class ChatService:
    """
    ChatService contains the business logic for chat-related operations.

    API layer responsibility:
        - Accept HTTP request
        - Validate request using Pydantic
        - Call this service
        - Return response

    Service layer responsibility:
        - Decide how to process the chat request
        - Later call LangGraph agent
        - Later store conversation history
        - Later handle memory, cache, and tracing
    """

    def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        Processes a normal chat request.

        Right now:
            - Returns a dummy response.

        Later:
            - Call master supervisor LangGraph
            - Retrieve conversation memory
            - Save response to DB
            - Return answer with citations
        """

        return ChatResponse(
            answer=f"Dummy service response for: {request.question}",
            conversation_id=request.conversation_id,
            sources=[]
        )

    def get_chat_history(self, conversation_id: str):
        """
        Returns conversation history for a given conversation_id.

        Right now:
            - Returns empty history.

        Later:
            - Fetch messages from PostgreSQL or SQLite.
        """

        return {
            "conversation_id": conversation_id,
            "messages": []
        }

    def stream_chat(self, request: ChatRequest):
        """
        Placeholder for streaming chat response.

        Later:
            - Stream LLM tokens using Server-Sent Events.
            - Useful for ChatGPT-like UI.
        """

        return {
            "message": "Streaming will be implemented later",
            "question": request.question
        }