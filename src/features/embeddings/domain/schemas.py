from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import List
from uuid import UUID
from src.persistence.domain.entities import DocumentChunk

class EmbedChunksData(BaseModel):
    knowledge_id: UUID
    chunks: List[DocumentChunk]

class UpdateEmbeddingStatusPayload(BaseModel):
    knowledge_id: UUID
    status: str

class StoreChunksData(BaseModel):
    total_batches: int
    batch_index: int
    chunks: List[DocumentChunk]
    embeddings: List[List[float]]
    knowledge_id: UUID

class DeleteEmbeddingsPayload(BaseModel):
    user_id: UUID
    knowledge_id: UUID

    model_config=ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_min_length=1
    )

class DeleteEmbeddingsRequest(BaseModel):
    key: str
    value: UUID

