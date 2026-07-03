
from app.schemas.rag_schema import RagRetrieveRequest, RagRetrieveResponse, RagDocument


class RagService:
    """
    RagService handles retrieval-related logic.

    RAG means:
        Retrieval Augmented Generation

    The user question is used to search documents.
    The retrieved document chunks are passed to the LLM.
    The LLM answers based on those chunks.
    """

    def retrieve_documents(self, request: RagRetrieveRequest) -> RagRetrieveResponse:
        """
        Retrieves relevant document chunks.

        Right now:
            - Returns dummy document chunk.

        Later:
            - Convert query into embedding
            - Search FAISS/Chroma
            - Return top-k matching chunks
        """

        return RagRetrieveResponse(
            query=request.query,
            documents=[
                RagDocument(
                    content="Dummy retrieved document chunk from service layer",
                    score=0.91,
                    source="sample.pdf"
                )
            ]
        )

    def grade_documents(self, request: RagRetrieveRequest):
        """
        Grades retrieved documents for relevance.

        Later:
            - LLM grader will decide if chunks are useful.
        """

        return {
            "query": request.query,
            "grade": "RELEVANT"
        }