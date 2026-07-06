class ChunkingService:
    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100):
        chunks = []

        start = 0
        chunk_id = 1

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append({
                "chunk_id": f"chunk-{chunk_id}",
                "content": chunk_text
            })

            chunk_id += 1
            start = end - overlap

        return chunks