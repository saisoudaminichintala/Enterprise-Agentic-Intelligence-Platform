import os
import uuid

from fastapi import UploadFile

from app.schemas.document_schema import (
    DocumentIndexRequest,
    DocumentResponse,
)
from app.services.infrastructure.chunking_service import ChunkingService
from app.services.infrastructure.embedding_service import EmbeddingService
from app.services.infrastructure.parser_service import ParserService
from app.services.infrastructure.storage_service import StorageService
from app.services.infrastructure.vectorstore_service import VectorStoreService


class DocumentService:
    """
    Orchestrates document upload, indexing, listing, and deletion.

    This is a business service. It coordinates infrastructure services,
    but does not implement parsing, embedding, or vector-store operations itself.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vectorstore_service: VectorStoreService,
    ):
        self.storage_service = StorageService()
        self.parser_service = ParserService()
        self.chunking_service = ChunkingService()

        # Shared dependencies are injected.
        self.embedding_service = embedding_service
        self.vectorstore_service = vectorstore_service

        # Temporary in-memory metadata store.
        self.document_store: dict[str, dict] = {}

    async def upload_document(
        self,
        file: UploadFile,
    ) -> DocumentResponse:
        document_id = str(uuid.uuid4())

        file_path = await self.storage_service.save_file(file)

        self.document_store[document_id] = {
            "document_id": document_id,
            "filename": file.filename,
            "file_path": file_path,
            "status": "UPLOADED",
        }

        return DocumentResponse(
            document_id=document_id,
            filename=file.filename or "unknown",
            status="UPLOADED",
        )

    def list_documents(self) -> dict:
        return {
            "documents": list(self.document_store.values()),
        }

    def index_documents(
        self,
        request: DocumentIndexRequest,
    ) -> dict:
        document_id = request.document_id

        if not document_id:
            return {
                "status": "FAILED",
                "reason": "document_id is required",
            }

        if document_id not in self.document_store:
            return {
                "status": "FAILED",
                "reason": "Document not found",
                "document_id": document_id,
            }

        document = self.document_store[document_id]

        parsed_text = self.parser_service.parse_document(
            document["file_path"]
        )

        if not parsed_text.strip():
            return {
                "status": "FAILED",
                "reason": "No text could be extracted from the document",
                "document_id": document_id,
            }

        chunks = self.chunking_service.chunk_text(parsed_text)

        # Add document metadata to every chunk.
        enriched_chunks = [
            {
                **chunk,
                "document_id": document_id,
                "filename": document["filename"],
            }
            for chunk in chunks
        ]

        embedded_chunks = self.embedding_service.create_embeddings(
            enriched_chunks
        )
        
        print(
    "DocumentService vector store ID:",
    id(self.vectorstore_service),
)

        print(
            "Qdrant collection after indexing:",
            self.vectorstore_service._vector_store.collection_name,
        )

        result = self.vectorstore_service.add_documents(
            embedded_chunks
        )

        document["status"] = "INDEXED"
        document["chunks_indexed"] = result["chunks_indexed"]

        return {
            "document_id": document_id,
            "filename": document["filename"],
            "status": result["status"],
            "chunks_indexed": result["chunks_indexed"],
        }

    def delete_document(self, document_id: str) -> dict:
        document = self.document_store.get(document_id)

        if document is None:
            return {
                "document_id": document_id,
                "status": "NOT_FOUND",
            }

        file_path = document.get("file_path")

        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        del self.document_store[document_id]

        # Important limitation:
        # This does not yet delete the document vectors from Qdrant.
        # We will add vector deletion/rebuilding later.

        return {
            "document_id": document_id,
            "status": "DELETED",
        }