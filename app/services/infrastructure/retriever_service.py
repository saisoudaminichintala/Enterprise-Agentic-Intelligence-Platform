# app/services/infrastructure/retriever_service.py

from app.services.infrastructure.embedding_service import (
    EmbeddingService,
)
from app.services.infrastructure.vectorstore_service import (
    VectorStoreService,
)


class RetrieverService:
    """
    Performs semantic retrieval using an embedding model
    and the configured Qdrant vector store.

    Dependencies are supplied through constructor injection.

    Flow:
        query
          ↓
        EmbeddingService
          ↓
        query embedding
          ↓
        QdrantVectorStore
          ↓
        matching document chunks
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vectorstore_service: VectorStoreService,
    ) -> None:
        self.embedding_service = embedding_service
        self.vectorstore_service = vectorstore_service

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
        score_threshold: float | None = None,
    ) -> list[dict]:
        """
        Convert the query into an embedding and retrieve the
        most semantically relevant document chunks from Qdrant.
        """

        normalized_query = query.strip()

        if not normalized_query:
            return []

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        query_embedding = (
            self.embedding_service.embed_query(
                normalized_query
            )
        )

        search_results = self.vectorstore_service.search(
            query_embedding=query_embedding,
            limit=top_k,
            document_id=document_id,
            score_threshold=score_threshold,
        )

        return [
            {
                "point_id": result.point_id,
                "document_id": result.document_id,
                "chunk_id": result.chunk_id,
                "text": result.text,
                "score": result.score,
                "metadata": result.metadata,
            }
            for result in search_results
        ]