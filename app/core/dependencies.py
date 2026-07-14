# app/core/dependencies.py

from app.services.infrastructure.embedding_service import EmbeddingService
from app.services.infrastructure.vectorstore_service import VectorStoreService
from app.services.infrastructure.retriever_service import RetrieverService


_embedding_service = EmbeddingService()
_vectorstore_service = VectorStoreService()

_retriever_service = RetrieverService(
    embedding_service=_embedding_service,
    vectorstore_service=_vectorstore_service,
)


def get_embedding_service() -> EmbeddingService:
    return _embedding_service


def get_vectorstore_service() -> VectorStoreService:
    return _vectorstore_service


def get_retriever_service() -> RetrieverService:
    return _retriever_service