from pydantic import BaseModel
from  typing import Dict, Any 

class BaseEvent(BaseModel):
    connection_id: str
    payload: Dict[str, Any]