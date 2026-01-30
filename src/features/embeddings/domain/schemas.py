from pydantic import BaseModel
from typing import List
from src.persistence.domain.entities import DocumentChunk

class EmbedChunksPayload(BaseModel):
    chunks: List[DocumentChunk]