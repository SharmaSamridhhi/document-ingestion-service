from pydantic import BaseModel
from typing import List
import uuid

class DocumentResponse(BaseModel):
    document_id: uuid.UUID
    chunks: List[str]

    class Config:
        from_attributes = True