from pydantic import BaseModel
from  typing import Dict, Any, Optional
from uuid import UUID

class BaseEvent(BaseModel):
    event_id: UUID
    connection_id: UUID
    user_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None
    payload: Optional[Dict[str, Any]]