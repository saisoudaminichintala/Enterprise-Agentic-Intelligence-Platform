class EmbeddingService:
    """
    Converts text chunks into vectors.

    Right now:
    - returns dummy vectors.

    Later:
    - OpenAI embeddings
    - HuggingFace embeddings
    """

    def create_embeddings(self, chunks: list[str]):
        return [
            {
                "chunk": chunk,
                "embedding": [0.1, 0.2, 0.3]
            }
            for chunk in chunks
        ]