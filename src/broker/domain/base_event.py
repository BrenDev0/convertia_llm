from pydantic import BaseModel
from  typing import Dict, Any 
from uuid import UUID

class BaseEvent(BaseModel):
    connection_id: UUID
    payload: Dict[str, Any]