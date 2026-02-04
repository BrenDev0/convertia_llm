from pydantic import BaseModel
from uuid import UUID

class ExtractTextPayload(BaseModel):
    knowledge_id: UUID
    file_type: str
    file_url: str

class ChunkTextPayload(BaseModel):
    knowledge_id: UUID
    text: str
    

class DownloadDocumentPayload(BaseModel):
    user_id: UUID
    agent_id: UUID
    connection_id: UUID
    knowledge_id: UUID
    file_type: str
    file_url: str