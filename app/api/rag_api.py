
from fastapi import APIRouter
from app.schemas.rag_schema import RagRetrieveRequest, RagRetrieveResponse
from app.services.business.rag_service import RagService

router = APIRouter()

rag_service = RagService()


@router.post("/retrieve", response_model=RagRetrieveResponse)
def retrieve_documents(request: RagRetrieveRequest):
    """
    Tests RAG retrieval separately.
    """

    return rag_service.retrieve_documents(request)


@router.post("/grade")
def grade_documents(request: RagRetrieveRequest):
    """
    Tests document grading separately.
    """

    return rag_service.grade_documents(request)