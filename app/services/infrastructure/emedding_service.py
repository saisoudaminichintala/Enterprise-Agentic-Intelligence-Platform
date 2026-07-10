from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Creates real embeddings using sentence-transformers.

    Model:
    - all-MiniLM-L6-v2
    - lightweight
    - good for local semantic search
    """

    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def create_embeddings(self, chunks: list[dict]):
        texts = [chunk["content"] for chunk in chunks]
        vectors = self.model.encode(texts, convert_to_numpy=True)

        embedded_chunks = []

        for chunk, vector in zip(chunks, vectors):
            embedded_chunks.append({
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "embedding": vector
            })

        return embedded_chunks

    def embed_query(self, query: str):
        return self.model.encode([query], convert_to_numpy=True)[0]