from pydantic import BaseModel
from typing import Dict, Any

class WebsocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]