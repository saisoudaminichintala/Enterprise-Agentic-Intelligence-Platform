from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class VectorChunk:
    """
    A document chunk prepared for vector storage.

    This is our platform's internal representation.
    It does not depend on Qdrant SDK classes.
    """

    point_id: str
    document_id: str
    chunk_id: str
    text: str
    embedding: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VectorSearchResult:
    """
    A normalized search result returned to the application.

    The Shared Retriever should receive this object rather than
    a raw Qdrant SDK response.
    """

    point_id: str
    document_id: str
    chunk_id: str
    text: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)