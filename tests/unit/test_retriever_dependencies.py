import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.core.dependencies import get_retriever_service
from app.services.infrastructure.retriever_service import RetrieverService


def test_get_retriever_service_returns_retriever_service():
    with patch(
        "app.core.dependencies.get_embedding_service",
        return_value=object(),
    ), patch(
        "app.core.dependencies.get_vectorstore_service",
        return_value=object(),
    ):
        service = get_retriever_service()

    assert isinstance(service, RetrieverService)
