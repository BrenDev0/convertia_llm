from pydantic import BaseModel
from uuid import UUID

class KnowledgeEmbeddingEStatus(BaseModel):
    user_id: UUID
    knowledge_id: UUID
    is_embedded: bool