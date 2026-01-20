from pydantic import BaseModel
from typing import Any, Dict

class DocumentChunk(BaseModel):
    content: str
    metadata: Dict[str, Any]
    chunk_id: str