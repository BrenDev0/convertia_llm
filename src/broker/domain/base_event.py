from pydantic import BaseModel
from  typing import Dict, Any, Optional
from uuid import UUID

class BaseEvent(BaseModel):
    user_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None
    connection_id: UUID
    payload: Dict[str, Any]