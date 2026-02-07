from pydantic import BaseModel
from typing import List
from uuid import UUID
from src.persistence.domain.entities import DocumentChunk

class EmbedChunksData(BaseModel):
    knowledge_id: UUID
    chunks: List[DocumentChunk]

