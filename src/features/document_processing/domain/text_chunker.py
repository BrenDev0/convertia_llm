from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.persistence.domain.entities import DocumentChunk

class TextChunker(ABC):
    @abstractmethod
    def chunk(
    self, 
    text: str, 
    metadata: Dict[str, Any],
    max_tokens: int, 
    token_overlap: int
) -> List[DocumentChunk]:
        raise NotImplementedError