import uuid
from fastapi import UploadFile
from app.schemas.document_schema import DocumentResponse, DocumentIndexRequest


class DocumentService:
    """
    Handles document-related business logic.

    Later this service will:
    - Save uploaded files to local storage/S3
    - Extract text from PDF/DOCX/TXT
    - Split text into chunks
    - Generate embeddings
    - Store chunks in vector DB
    """

    async def upload_document(self, file: UploadFile) -> DocumentResponse:
        return DocumentResponse(
            document_id=str(uuid.uuid4()),
            filename=file.filename,
            status="UPLOADED"
        )

    def list_documents(self):
        return {
            "documents": []
        }

    def index_documents(self, request: DocumentIndexRequest):
        return {
            "status": "INDEXING_STARTED",
            "document_id": request.document_id
        }

    def delete_document(self, document_id: str):
        return {
            "document_id": document_id,
            "status": "DELETED"
        }