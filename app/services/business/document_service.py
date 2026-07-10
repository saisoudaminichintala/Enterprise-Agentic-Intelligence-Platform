import uuid
from fastapi import UploadFile
from app.schemas.document_schema import DocumentResponse, DocumentIndexRequest
from app.services.infrastructure.storage_service import StorageService
from app.services.infrastructure.parser_service import ParserService
from app.services.infrastructure.chunking_service import ChunkingService
from app.services.infrastructure.embedding_service import EmbeddingService
from app.services.infrastructure.vectorstore_service import VectorStoreService
from app.services.infrastructure.retriever_service import RetrieverService

class DocumentService:
    def __init__(self):
        self.storage_service = StorageService()
        self.parser_service = ParserService()
        self.chunking_service = ChunkingService()
        self.embedding_service = EmbeddingService()
        self.vectorstore_service = VectorStoreService()
        self.retriever_service = RetrieverService(
            embedding_service=self.embedding_service,
            vectorstore_service=self.vectorstore_service
        )
        self.document_store = {}

    async def upload_document(self, file: UploadFile) -> DocumentResponse:
        document_id = str(uuid.uuid4())
        file_path = await self.storage_service.save_file(file)

        self.document_store[document_id] = {
            "document_id": document_id,
            "filename": file.filename,
            "file_path": file_path,
            "status": "UPLOADED"
        }

        return DocumentResponse(
            document_id=document_id,
            filename=file.filename,
            status="UPLOADED"
        )

    def list_documents(self):
        return {
            "documents": list(self.document_store.values())
        }

    def index_documents(self, request: DocumentIndexRequest):
        if request.document_id not in self.document_store:
            return {
                "status": "FAILED",
                "reason": "Document not found",
                "document_id": request.document_id
            }

        document = self.document_store[request.document_id]
        parsed_text = self.parser_service.parse_document(document["file_path"])
        chunks = self.chunking_service.chunk_text(parsed_text)
        embedded_chunks = self.embedding_service.create_embeddings(chunks)

        result = self.vectorstore_service.add_documents(embedded_chunks)

        document["status"] = "INDEXED"

        return {
            "document_id": request.document_id,
            "filename": document["filename"],
            "status": result["status"],
            "chunks_indexed": result["chunks_indexed"]
        }

    def delete_document(self, document_id: str):
        if document_id in self.document_store:
            del self.document_store[document_id]

        return {
            "document_id": document_id,
            "status": "DELETED"
        }