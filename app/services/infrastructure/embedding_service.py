import uuid

from app.infrastructure.vector_store.vector_models import VectorChunk
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Creates embeddings for document chunks and user queries.

    The same model must be used for:
    - document embeddings
    - query embeddings

    Otherwise Qdrant similarity search would compare incompatible vectors.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def get_dimension(self) -> int:
        """
        Returns the embedding dimension produced by the loaded model.
        """

        dimension = self.model.get_sentence_embedding_dimension()

        if dimension is None:
            raise ValueError(
                "Could not determine the embedding model dimension."
            )

        return dimension

    def create_embeddings(
        self,
        chunks: list[dict],
    ) -> list[VectorChunk]:
        """
        Generates embeddings for document chunks.

        Keeps document metadata so retrieval results can later include:
        - filename
        - document_id
        - chunk_id
        """

        if not chunks:
            return []

        texts = [chunk["content"] for chunk in chunks]

        vectors = self.model.encode(
            texts,
            convert_to_numpy=True,
        )

        embedded_chunks: list[VectorChunk] = []

        for chunk, vector in zip(chunks, vectors):
            metadata = {
                key: value
                for key, value in chunk.items()
                if key not in {"chunk_id", "content", "document_id", "filename", "embedding"}
            }

            point_id = str(uuid.uuid4())

            embedded_chunks.append(
                VectorChunk(
                    point_id=point_id,
                    document_id=str(chunk.get("document_id", "")),
                    chunk_id=str(chunk["chunk_id"]),
                    text=chunk["content"],
                    embedding=vector.tolist(),
                    metadata=metadata,
                )
            )

        return embedded_chunks

    def embed_query(self, query: str):
        """
        Converts a user query into a vector for Qdrant search.

        The query uses the same SentenceTransformer model as the documents.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        vector = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        return vector