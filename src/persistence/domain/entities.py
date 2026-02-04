from pydantic import BaseModel
from typing import Any, Dict
from uuid import UUID

class DocumentChunk(BaseModel):
    content: str
    metadata: Dict[str, Any]
    chunk_id: UUID