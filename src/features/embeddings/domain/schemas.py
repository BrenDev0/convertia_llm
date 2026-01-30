from pydantic import BaseModel
from typing import List
from src.persistence.domain.entities import DocumentChunk

class EmbedChunksEvent(BaseModel):
    chunks: List[DocumentChunk]