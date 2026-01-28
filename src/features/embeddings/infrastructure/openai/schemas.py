from pydantic import BaseModel
from typing import List

class OpenAiEmbeddingObject(BaseModel):
   object: str
   index: int
   embedding: List[float]

class OpenAiUsage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class OpenAiEmbeddingResposne(BaseModel):
  object: str
  data: List[OpenAiEmbeddingObject] 
  model: str
  usage: OpenAiUsage


