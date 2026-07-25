# Qdrant Vector Database

> How the platform stores and retrieves semantic document embeddings using Qdrant Cloud.

---

# Overview

The Enterprise Agentic Intelligence Platform uses **Qdrant Cloud** as its vector database.

Qdrant stores vector embeddings generated from uploaded documents and enables fast semantic search during Retrieval-Augmented Generation (RAG).

---

# Why Qdrant?

Initially, the project used FAISS for local vector search.

As the platform evolved, it was migrated to Qdrant Cloud because it provides features that are better suited for scalable applications.

Key benefits include:

* Persistent storage
* Cloud-hosted service
* Fast similarity search
* Metadata filtering
* Scalable collections

---

# How It Works

The retrieval process follows these steps:

```text
Document
    │
    ▼
Chunking
    │
    ▼
Embedding Generation
    │
    ▼
Qdrant Collection
    │
    ▼
Similarity Search
    │
    ▼
Relevant Chunks
```

---

# Collection Structure

Each document is divided into smaller chunks before indexing.

For every chunk, the platform stores:

* Vector embedding
* Document ID
* Chunk ID
* Filename
* Source text

This metadata helps identify where retrieved information originated.

---

# Similarity Search

When a user asks a question:

1. The question is converted into an embedding.
2. Qdrant searches for similar vectors.
3. The most relevant document chunks are returned.
4. Those chunks are used to generate the final response.

This allows the platform to retrieve information based on meaning rather than exact keyword matches.

---

# Integration

Qdrant is accessed through the platform's infrastructure layer.

The main responsibilities include:

* Creating embeddings
* Upserting vectors
* Searching collections
* Returning relevant document chunks

Keeping database interactions inside dedicated services makes it easier to replace or extend the vector store in the future.

---

# Future Enhancements

Planned improvements include:

* Metadata-based filtering
* Multiple collections
* Hybrid search
* Collection management APIs
* Automatic document re-indexing

---

# Conclusion

Qdrant provides the semantic search foundation for the platform's RAG pipeline. By storing document embeddings in a scalable vector database, the platform can efficiently retrieve relevant knowledge and generate grounded responses from enterprise documents.
