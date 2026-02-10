from pydantic import BaseModel
from uuid import UUID
from src.persistence.domain.entities import DocumentChunk
from typing import List

class UpdateEmbeddingStatusPayload(BaseModel):
    knowledge_id: UUID
    is_embedded: bool

class StoreChunksData(BaseModel):
    total_batches: int
    batch_index: int
    chunks: List[DocumentChunk]
    embeddings: List[List[float]]
    knowledge_id: UUID

class DeleteEmbeddingsPayload(BaseModel):
    user_id: UUID
    knowledge_id: UUID