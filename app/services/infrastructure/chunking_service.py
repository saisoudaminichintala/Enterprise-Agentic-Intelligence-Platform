class ChunkingService:
    """
    Splits document text into smaller chunks.

    Why?
    - LLMs and vector DBs work better with chunks than full documents.
    """

    def chunk_text(self, text: str, chunk_size: int = 500):
        return [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]