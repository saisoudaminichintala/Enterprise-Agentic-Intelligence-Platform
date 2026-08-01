from app.core.dependencies import (
    get_qdrant_vector_store,
)
from app.infrastructure.vector_store.vector_models import (
    VectorChunk,
)


def create_test_vector(
    first_value: float,
    second_value: float,
) -> list[float]:
    return [
        first_value,
        second_value,
        *([0.0] * 382),
    ]


vector_store = get_qdrant_vector_store()

vector_store.initialize()

print(
    "Qdrant healthy:",
    vector_store.health_check(),
)

print(
    "Points before cleanup:",
    vector_store.count_points(),
)


# Remove the earlier manually inserted points.
vector_store.delete_points([1, 2, 3])

print(
    "Points after cleanup:",
    vector_store.count_points(),
)


test_chunk = VectorChunk(
    point_id="11111111-1111-4111-8111-111111111111",
    document_id="architecture-test-document",
    chunk_id="architecture-test-document-chunk-0",
    text=(
        "The Knowledge Supervisor retrieves relevant "
        "enterprise documents."
    ),
    embedding=create_test_vector(1.0, 0.0),
    metadata={
        "filename": "architecture_test.txt",
        "chunk_index": 0,
        "page_number": 1,
    },
)

inserted_count = vector_store.upsert_chunks(
    [test_chunk]
)

print("Inserted:", inserted_count)
print("Current points:", vector_store.count_points())


results = vector_store.search(
    create_test_vector(1.0, 0.0),
    limit=3,
)

for result in results:
    print()
    print("Point ID:", result.point_id)
    print("Document ID:", result.document_id)
    print("Chunk ID:", result.chunk_id)
    print("Text:", result.text)
    print("Score:", result.score)
    print("Metadata:", result.metadata)