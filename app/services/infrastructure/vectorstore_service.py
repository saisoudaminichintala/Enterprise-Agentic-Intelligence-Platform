from app.infrastructure.vector_store.qdrant_vector_store import (
    QdrantVectorStore,
)
from app.infrastructure.vector_store.vector_models import (
    VectorChunk,
    VectorSearchResult,
)


class VectorStoreService:
    """
    Application-facing vector storage service.

    This class hides the concrete vector database implementation
    from the rest of the application.

    Current implementation:
        QdrantVectorStore -> Qdrant Cloud

    DocumentService and RetrieverService depend on this class,
    not directly on the Qdrant SDK.
    """

    def __init__(
        self,
        qdrant_vector_store: QdrantVectorStore,
    ) -> None:
        self._vector_store = qdrant_vector_store

    def initialize(self) -> None:
        """
        Initialize the underlying vector collection.
        """
        self._vector_store.initialize()

    @property
    def collection_name(self) -> str:
        """
        Expose the underlying collection name for diagnostics and agents.
        """
        return self._vector_store.collection_name

    def add_documents(
        self,
        chunks: list[VectorChunk],
    ) -> dict:
        """
        Store document chunks in Qdrant.

        This method keeps the older application-facing method name
        so DocumentService does not need a major rewrite.
        """

        chunks_indexed = self._vector_store.upsert_chunks(
            chunks
        )

        return {
            "status": "INDEXED",
            "chunks_indexed": chunks_indexed,
        }

    def search(
        self,
        query_embedding: list[float],
        *,
        limit: int = 5,
        document_id: str | None = None,
        score_threshold: float | None = None,
    ) -> list[VectorSearchResult]:
        """
        Search Qdrant using a query embedding.
        """

        return self._vector_store.search(
            query_embedding=query_embedding,
            limit=limit,
            document_id=document_id,
            score_threshold=score_threshold,
        )

    def similarity_search_by_vector(
        self,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Backward-compatible search method.

        Existing code that still calls the old vector-search method
        can continue working during the migration.
        """

        results = self.search(
            query_embedding=query_vector,
            limit=top_k,
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
            for result in results
        ]

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete all chunks belonging to a document.
        """

        self._vector_store.delete_document(
            document_id
        )

    def count_documents(self) -> int:
        """
        Return the number of stored vector points.

        This counts chunks, not unique uploaded documents.
        """

        return self._vector_store.count_points()

    def health_check(self) -> bool:
        """
        Check whether Qdrant is reachable and healthy.
        """

        return self._vector_store.health_check()