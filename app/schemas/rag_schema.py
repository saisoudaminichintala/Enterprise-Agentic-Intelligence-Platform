from pydantic import BaseModel, Field
from typing import List

class RagRetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = 5


class RagDocument(BaseModel):
    content: str
    score: float
    source: str


class RagRetrieveResponse(BaseModel):
    query: str
    documents: List[RagDocument]
