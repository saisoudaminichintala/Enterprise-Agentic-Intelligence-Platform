import faiss
import numpy as np


class VectorStoreService:
    """
    Shared in-memory FAISS vector store.

    FAISS stores vectors. The documents list stores metadata at the
    corresponding vector position.
    """

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: list[dict] = []

    def add_documents(
        self,
        embedded_chunks: list[dict],
    ) -> dict:
        if not embedded_chunks:
            return {
                "status": "NO_DOCUMENTS",
                "chunks_indexed": 0,
            }

        vectors = np.asarray(
            [item["embedding"] for item in embedded_chunks],
            dtype=np.float32,
        )

        if vectors.ndim != 2:
            raise ValueError(
                f"Expected a 2D embedding matrix, received {vectors.shape}"
            )

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                "Embedding dimension mismatch: "
                f"index expects {self.dimension}, "
                f"received {vectors.shape[1]}"
            )

        self.index.add(vectors)

        for item in embedded_chunks:
            self.documents.append(
                {
                    "chunk_id": item["chunk_id"],
                    "content": item["content"],
                    "document_id": item.get("document_id"),
                    "filename": item.get("filename"),
                }
            )

        return {
            "status": "INDEXED",
            "chunks_indexed": len(embedded_chunks),
            "total_chunks": self.index.ntotal,
        }

    def similarity_search_by_vector(
        self,
        query_vector,
        top_k: int = 5,
    ) -> list[dict]:
        if self.index.ntotal == 0:
            return []

        query_matrix = np.asarray(
            [query_vector],
            dtype=np.float32,
        )

        actual_top_k = min(top_k, self.index.ntotal)

        distances, indices = self.index.search(
            query_matrix,
            actual_top_k,
        )

        results = []

        for distance, document_index in zip(
            distances[0],
            indices[0],
        ):
            if document_index == -1:
                continue

            document = self.documents[document_index]

            results.append(
                {
                    "chunk_id": document["chunk_id"],
                    "content": document["content"],
                    "document_id": document.get("document_id"),
                    "filename": document.get("filename"),
                    "score": float(distance),
                }
            )

        return results