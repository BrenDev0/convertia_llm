from pydantic import BaseModel

class QueueConfig(BaseModel):
    exchange: str
    queue_name: str 
    routing_key: str 