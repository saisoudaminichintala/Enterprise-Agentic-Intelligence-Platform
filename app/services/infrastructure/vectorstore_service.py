class VectorStoreService:
    def __init__(self):
        self.index = []

    def add_documents(self, embedded_chunks):
        self.index.extend(embedded_chunks)

        return {
            "status": "INDEXED",
            "chunks_indexed": len(embedded_chunks)
        }

    def similarity_search(self, query: str, top_k: int = 5):
        return self.index[:top_k]