from pydantic import BaseModel, Field
from typing import Optional, List

class ChatRequest(BaseModel):
    question:str
    conversation_id:Optional[str]=None



class ChatResponse(BaseModel):
    answer:str
    conversation_id:Optional[str]=None
    sources:List[str]=[]