from pydantic import BaseModel

class InvokeAgentPayload(BaseModel):
    input: str
    prompt: str
    max_tokens: int
    temperature: float
    transcripts: bool