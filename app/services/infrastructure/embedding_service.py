class EmbeddingService:
    def create_embeddings(self, chunks: list[dict]):
        return [
            {
                "chunk_id": chunk["chunk_id"],
                "content": chunk["content"],
                "embedding": [0.1, 0.2, 0.3]
            }
            for chunk in chunks
        ]