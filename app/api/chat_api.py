
from fastapi import APIRouter
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Chat endpoint.

    This endpoint receives the user question and delegates the real logic
    to ChatService.

    """

    return chat_service.process_chat(request)


@router.post("/stream")
def stream_chat(request: ChatRequest):
    """
    Streaming chat endpoint.

    Later this will return token-by-token responses.
    """

    return chat_service.stream_chat(request)


@router.get("/history/{conversation_id}")
def get_chat_history(conversation_id: str):
    """
    Returns previous messages for a conversation.
    """

    return chat_service.get_chat_history(conversation_id)