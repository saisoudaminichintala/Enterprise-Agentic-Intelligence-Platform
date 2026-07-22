import logging
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client import models

from app.infrastructure.vector_store.vector_models import (
    VectorChunk,
    VectorSearchResult,
)


logger = logging.getLogger(__name__)


class QdrantVectorStore:
    """
    Infrastructure adapter responsible for all communication
    with Qdrant Cloud.

    Other layers should not instantiate QdrantClient directly.
    """

    def __init__(
        self,
        *,
        url: str,
        api_key: str,
        collection_name: str,
        vector_dimension: int,
    ) -> None:
        if not url.strip():
            raise ValueError("Qdrant URL cannot be empty.")

        if not api_key.strip():
            raise ValueError("Qdrant API key cannot be empty.")

        if not collection_name.strip():
            raise ValueError(
                "Qdrant collection name cannot be empty."
            )

        if vector_dimension <= 0:
            raise ValueError(
                "Vector dimension must be greater than zero."
            )

        self._collection_name = collection_name
        self._vector_dimension = vector_dimension

        self._client = QdrantClient(
            url=url,
            api_key=api_key,
            timeout=30,
        )

    @property
    def collection_name(self) -> str:
        return self._collection_name

    def initialize(self) -> None:
        """
        Create the collection when it does not exist.

        If it already exists, verify that its vector dimension
        matches the configured embedding model.
        """

        if self._client.collection_exists(
            collection_name=self._collection_name
        ):
            self._validate_existing_collection()

            logger.info(
                "Using existing Qdrant collection '%s'.",
                self._collection_name,
            )
            return

        self._client.create_collection(
            collection_name=self._collection_name,
            vectors_config=models.VectorParams(
                size=self._vector_dimension,
                distance=models.Distance.COSINE,
            ),
        )

        logger.info(
            "Created Qdrant collection '%s' with dimension %s.",
            self._collection_name,
            self._vector_dimension,
        )

    def upsert_chunks(
        self,
        chunks: list[VectorChunk],
    ) -> int:
        """
        Insert new chunks or replace chunks with matching point IDs.

        Returns the number of points submitted to Qdrant.
        """

        if not chunks:
            return 0

        points: list[models.PointStruct] = []

        for chunk in chunks:
            self._validate_embedding(chunk.embedding)

            payload: dict[str, Any] = {
                "document_id": chunk.document_id,
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                **chunk.metadata,
            }

            point = models.PointStruct(
                id=chunk.point_id,
                vector=chunk.embedding,
                payload=payload,
            )

            points.append(point)

        self._client.upsert(
            collection_name=self._collection_name,
            points=points,
            wait=True,
        )

        logger.info(
            "Upserted %s chunks into collection '%s'.",
            len(points),
            self._collection_name,
        )

        return len(points)

    def search(
        self,
        query_embedding: list[float],
        *,
        limit: int = 5,
        document_id: str | None = None,
        score_threshold: float | None = None,
    ) -> list[VectorSearchResult]:
        """
        Search for chunks similar to the supplied query embedding.

        Optionally restrict search to one document.
        """

        self._validate_embedding(query_embedding)

        if limit <= 0:
            raise ValueError(
                "Search limit must be greater than zero."
            )

        query_filter = self._build_document_filter(document_id)

        response = self._client.query_points(
            collection_name=self._collection_name,
            query=query_embedding,
            query_filter=query_filter,
            limit=limit,
            score_threshold=score_threshold,
            with_payload=True,
            with_vectors=False,
        )

        return [
            self._map_search_result(point)
            for point in response.points
        ]

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Delete every vector chunk belonging to a document.
        """

        if not document_id.strip():
            raise ValueError("Document ID cannot be empty.")

        document_filter = self._build_document_filter(
            document_id
        )

        self._client.delete(
            collection_name=self._collection_name,
            points_selector=models.FilterSelector(
                filter=document_filter
            ),
            wait=True,
        )

        logger.info(
            "Deleted Qdrant points for document '%s'.",
            document_id,
        )

    def delete_points(
        self,
        point_ids: list[int | str],
    ) -> None:
        """
        Delete specific test or production points by ID.
        """

        if not point_ids:
            return

        self._client.delete(
            collection_name=self._collection_name,
            points_selector=models.PointIdsList(
                points=point_ids
            ),
            wait=True,
        )

    def count_points(self) -> int:
        """
        Return the current number of points in the collection.
        """

        result = self._client.count(
            collection_name=self._collection_name,
            exact=True,
        )

        return int(result.count)

    def health_check(self) -> bool:
        """
        Verify that Qdrant is reachable and the collection exists.
        """

        try:
            collection = self._client.get_collection(
                collection_name=self._collection_name
            )

            return (
                collection.status
                == models.CollectionStatus.GREEN
            )

        except Exception:
            logger.exception(
                "Qdrant health check failed for collection '%s'.",
                self._collection_name,
            )
            return False

    def _validate_existing_collection(self) -> None:
        collection = self._client.get_collection(
            collection_name=self._collection_name
        )

        vector_configuration = (
            collection.config.params.vectors
        )

        existing_dimension = getattr(
            vector_configuration,
            "size",
            None,
        )

        if existing_dimension is None:
            raise RuntimeError(
                "Unable to determine the existing Qdrant "
                "collection's vector dimension."
            )

        if existing_dimension != self._vector_dimension:
            raise RuntimeError(
                "Qdrant collection dimension mismatch. "
                f"Collection '{self._collection_name}' expects "
                f"{existing_dimension} values, but the configured "
                f"embedding model produces "
                f"{self._vector_dimension} values."
            )

    def _validate_embedding(
        self,
        embedding: list[float],
    ) -> None:
        if len(embedding) != self._vector_dimension:
            raise ValueError(
                "Invalid embedding dimension. "
                f"Expected {self._vector_dimension}, "
                f"received {len(embedding)}."
            )

    @staticmethod
    def _build_document_filter(
        document_id: str | None,
    ) -> models.Filter | None:
        if document_id is None:
            return None

        return models.Filter(
            must=[
                models.FieldCondition(
                    key="document_id",
                    match=models.MatchValue(
                        value=document_id
                    ),
                )
            ]
        )

    @staticmethod
    def _map_search_result(
        point: models.ScoredPoint,
    ) -> VectorSearchResult:
        payload = dict(point.payload or {})

        document_id = str(
            payload.pop("document_id", "")
        )
        chunk_id = str(
            payload.pop("chunk_id", "")
        )
        text = str(
            payload.pop("text", "")
        )

        return VectorSearchResult(
            point_id=str(point.id),
            document_id=document_id,
            chunk_id=chunk_id,
            text=text,
            score=float(point.score),
            metadata=payload,
        )