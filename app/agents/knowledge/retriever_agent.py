from app.core.dependencies import (
    get_retriever_service,
    get_vectorstore_service,
)
from app.graph.state import AgentState


retriever_service = get_retriever_service()


def retriever_node(
    state: AgentState,
) -> dict:
    query = state.get("rewritten_query") or state["question"]

    shared_vectorstore = get_vectorstore_service()

    print(
        "Retriever vector store ID:",
        id(shared_vectorstore),
    )

    print(
        "FAISS vectors before retrieval:",
        shared_vectorstore.index.ntotal,
    )

    results = retriever_service.retrieve(
        query=query,
        top_k=5,
    )

    print("Retriever query:", query)
    print("Raw FAISS results:", results)

    retrieved_docs = [
        (
            f"Source: {result.get('filename', 'unknown')}\n"
            f"Chunk ID: {result.get('chunk_id', 'unknown')}\n"
            f"Distance: {result.get('score')}\n"
            f"Content: {result.get('content', '')}"
        )
        for result in results
    ]

    return {
        "retrieved_docs": retrieved_docs,
        "agents_used": (
            state["agents_used"]
            + ["retriever_agent_faiss"]
        ),
    }