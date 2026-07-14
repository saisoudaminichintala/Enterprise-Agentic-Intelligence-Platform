# app/services/infrastructure/retriever_service.py

from app.services.infrastructure.embedding_service import EmbeddingService
from app.services.infrastructure.vectorstore_service import VectorStoreService


class RetrieverService:
    """
    Performs semantic retrieval using an embedding model and FAISS.

    This class does not create or import global dependencies.
    Its required services are passed through constructor injection.

    Flow:
        query
          ↓
        EmbeddingService
          ↓
        query vector
          ↓
        VectorStoreService
          ↓
        matching document chunks
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vectorstore_service: VectorStoreService,
    ):
        self.embedding_service = embedding_service
        self.vectorstore_service = vectorstore_service

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Converts the query into an embedding and searches the shared
        FAISS vector index.
        """

        if not query or not query.strip():
            return []

        query_vector = self.embedding_service.embed_query(query)

        return self.vectorstore_service.similarity_search_by_vector(
            query_vector=query_vector,
            top_k=top_k,
        )