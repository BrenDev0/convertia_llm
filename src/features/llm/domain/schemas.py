from pydantic import BaseModel

class InvokeAgentPayload(BaseModel):
    input: str
    prompt: str
    temperature: float
    transcripts: bool