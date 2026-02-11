from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID

class ExtractTextPayload(BaseModel):
    knowledge_id: UUID
    file_type: str
    file_url: str

class ChunkTextData(BaseModel):
    knowledge_id: UUID
    text: str

class DownloadDocumentPayloadWebsocket(BaseModel):
    user_id: UUID
    agent_id: UUID
    knowledge_id: UUID
    file_type: str
    file_url: str

    model_config=ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        str_min_length=1,
        alias_generator=to_camel
    )

class DownloadDocumentPayloadRest(DownloadDocumentPayloadWebsocket):
    connection_id: UUID