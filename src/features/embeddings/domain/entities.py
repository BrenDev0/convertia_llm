from pydantic import BaseModel
from typing import List
from src.persistence import DocumentChunk

class EmbeddingResult(BaseModel):
    chunks: List[DocumentChunk]
    embeddings: List[List[float]]
