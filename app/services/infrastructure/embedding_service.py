from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Creates embeddings for document chunks and user queries.

    The same model must be used for:
    - document embeddings
    - query embeddings

    Otherwise FAISS similarity search would compare incompatible vectors.
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
    ) -> list[dict]:
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

        return [
            {
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "document_id": chunk.get("document_id"),
                "filename": chunk.get("filename"),
                "embedding": vector,
            }
            for chunk, vector in zip(chunks, vectors)
        ]

    def embed_query(self, query: str):
        """
        Converts a user query into a vector for FAISS search.

        The query uses the same SentenceTransformer model as the documents.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        vector = self.model.encode(
            query,
            convert_to_numpy=True,
        )

        return vector