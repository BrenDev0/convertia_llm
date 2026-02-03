from pydantic import BaseModel
from uuid import UUID

class ExtractTextPayload(BaseModel):
    user_id: UUID
    agent_id: UUID
    knowledge_id: UUID
    file_type: str
    file_bytes: bytes

class ChunkTextPayload(BaseModel):
    user_id: UUID
    agent_id: UUID
    knowledge_id: UUID
    text: str
    

class KnowledgeBaseRequest(BaseModel):
    user_id: UUID
    connection_id: UUID
    knowledge_id: UUID
    file_type: str
    file_bytes: bytes