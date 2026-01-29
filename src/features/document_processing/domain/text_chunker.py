from abc import ABC, abstractmethod
from typing import List
from src.persistence.domain.entities import DocumentChunk

class TextChunker(ABC):
    @abstractmethod
    def chunk(
    self, 
    text: str, 
    max_tokens: int, 
    token_overlap: int
) -> List[DocumentChunk]:
        raise NotImplementedError