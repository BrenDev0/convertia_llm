from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Any

class ChatEvent(BaseModel):
    event_id: UUID
    connection_id: UUID
    agent_id: UUID
    chat_id: UUID
    payload: Dict[str, Any]