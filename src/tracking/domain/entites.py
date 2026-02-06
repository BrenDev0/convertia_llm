from pydantic import BaseModel

class ProgressStage(BaseModel):
    name: str
    start: int
    end: int

