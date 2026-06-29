from pydantic import BaseModel
from typing import Optional

class DocumentResponse(BaseModel):
     document_id: str
     filename: str
     status: str

class DocumentIndexRequest(BaseModel):
     document_id:Optional[str]=None
