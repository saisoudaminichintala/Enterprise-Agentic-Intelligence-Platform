from fastapi import APIRouter, UploadFile, File
from app.schemas.document_schema import DocumentResponse, DocumentIndexRequest
from app.services.document_service import DocumentService

router = APIRouter()
document_service = DocumentService()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    return await document_service.upload_document(file)


@router.get("")
def list_documents():
    return document_service.list_documents()


@router.post("/index")
def index_documents(request: DocumentIndexRequest):
    return document_service.index_documents(request)


@router.delete("/{document_id}")
def delete_document(document_id: str):
    return document_service.delete_document(document_id)