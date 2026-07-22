from functools import lru_cache

from app.config.settings import settings
from app.infrastructure.vector_store.qdrant_vector_store import (
    QdrantVectorStore,
)
from app.services.infrastructure.embedding_service import (
    EmbeddingService,
)
from app.services.infrastructure.retriever_service import (
    RetrieverService,
)
from app.services.infrastructure.vectorstore_service import (
    VectorStoreService,
)


@lru_cache
def get_qdrant_vector_store() -> QdrantVectorStore:
    vector_store = QdrantVectorStore(
        url=settings.qdrant_url,
        api_key=(
            settings.qdrant_api_key.get_secret_value()
        ),
        collection_name=(
            settings.qdrant_collection_name
        ),
        vector_dimension=(
            settings.embedding_dimension
        ),
    )

    vector_store.initialize()

    return vector_store


@lru_cache
def get_vectorstore_service() -> VectorStoreService:
    return VectorStoreService(
        qdrant_vector_store=get_qdrant_vector_store()
    )


@lru_cache
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


@lru_cache
def get_retriever_service() -> RetrieverService:
    return RetrieverService(
        embedding_service=get_embedding_service(),
        vectorstore_service=get_vectorstore_service(),
    )