from app.services.infrastructure.embedding_service import EmbeddingService
from app.services.infrastructure.vectorstore_service import VectorStoreService


class RetrieverService:
    """
    Retrieves relevant document chunks using embeddings + FAISS.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vectorstore_service: VectorStoreService
    ):
        self.embedding_service = embedding_service
        self.vectorstore_service = vectorstore_service

    def retrieve(self, query: str, top_k: int = 5):
        query_vector = self.embedding_service.embed_query(query)

        return self.vectorstore_service.similarity_search_by_vector(
            query_vector=query_vector,
            top_k=top_k
        )