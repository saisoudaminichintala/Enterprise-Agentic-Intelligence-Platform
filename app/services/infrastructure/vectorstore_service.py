import faiss
import numpy as np


class VectorStoreService:
    """
    Stores embeddings in FAISS and performs similarity search.
    """

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_documents(self, embedded_chunks):
        if not embedded_chunks:
            return {
                "status": "NO_DOCUMENTS",
                "chunks_indexed": 0
            }

        vectors = np.array(
            [item["embedding"] for item in embedded_chunks],
            dtype="float32"
        )

        self.index.add(vectors)

        for item in embedded_chunks:
            self.documents.append({
                "chunk_id": item["chunk_id"],
                "content": item["content"]
            })

        return {
            "status": "INDEXED",
            "chunks_indexed": len(embedded_chunks)
        }

    def similarity_search_by_vector(self, query_vector, top_k: int = 5):
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_vector], dtype="float32")

        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for distance, index in zip(distances[0], indices[0]):
            if index == -1:
                continue

            document = self.documents[index]

            results.append({
                "chunk_id": document["chunk_id"],
                "content": document["content"],
                "score": float(distance)
            })

        return results