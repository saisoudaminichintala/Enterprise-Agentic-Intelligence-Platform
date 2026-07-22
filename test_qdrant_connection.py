import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv(
    "QDRANT_COLLECTION_NAME",
    "enterprise_agentic_platform",
)

if not qdrant_url:
    raise ValueError("QDRANT_URL is missing")

if not qdrant_api_key:
    raise ValueError("QDRANT_API_KEY is missing")


client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
)


def create_test_vector(
    first_value: float,
    second_value: float,
) -> list[float]:
    """
    Create a simple 384-dimensional vector.

    The first two values distinguish the test records.
    The remaining 382 values are zero.
    """
    return [
        first_value,
        second_value,
        *([0.0] * 382),
    ]


points = [
    PointStruct(
        id=1,
        vector=create_test_vector(1.0, 0.0),
        payload={
            "document_id": "employee-handbook",
            "chunk_id": "employee-handbook-chunk-1",
            "filename": "employee_handbook.pdf",
            "page_number": 3,
            "text": (
                "Employees must receive manager approval "
                "before submitting travel expenses."
            ),
        },
    ),
    PointStruct(
        id=2,
        vector=create_test_vector(0.9, 0.1),
        payload={
            "document_id": "travel-policy",
            "chunk_id": "travel-policy-chunk-1",
            "filename": "travel_policy.pdf",
            "page_number": 5,
            "text": (
                "Travel reimbursement requests require "
                "approval from the employee's manager."
            ),
        },
    ),
    PointStruct(
        id=3,
        vector=create_test_vector(0.0, 1.0),
        payload={
            "document_id": "security-policy",
            "chunk_id": "security-policy-chunk-1",
            "filename": "security_policy.pdf",
            "page_number": 8,
            "text": (
                "Passwords must contain at least twelve "
                "characters and use multifactor authentication."
            ),
        },
    ),
]


result = client.upsert(
    collection_name=collection_name,
    points=points,
    wait=True,
)

print("Upsert result:")
print(result)

collection_info = client.get_collection(collection_name)

print()
print("Current point count:")
print(collection_info.points_count)