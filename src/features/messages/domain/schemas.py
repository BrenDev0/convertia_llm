from pydantic import BaseModel

class CreateMessagePayload(BaseModel):
    type: str
    text: str
    transctipts: bool