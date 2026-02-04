from pydantic import BaseModel
from typing import List
from uuid import UUID
from src.persistence.domain.entities import DocumentChunk

class EmbeddingResult(BaseModel):
    chunks: List[DocumentChunk]
    embeddings: List[List[float]]

class EmbeddingsPayload(EmbeddingResult):
    knowledge_id: UUID