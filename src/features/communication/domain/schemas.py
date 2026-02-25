from pydantic import BaseModel
from uuid import UUID

class IncommingMessageData(BaseModel):
    agent_id: UUID
    input: str