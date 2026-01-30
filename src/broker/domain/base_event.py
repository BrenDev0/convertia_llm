from pydantic import BaseModel
from  typing import Dict, Any 

class BaseEvent(BaseModel):
    connection_id: str
    event_data: Dict[str, Any]