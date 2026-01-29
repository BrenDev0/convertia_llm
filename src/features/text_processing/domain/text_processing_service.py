from abc import ABC, abstractmethod
from typing import List
from src.persistence.domain.entities import DocumentChunk

class TextProcessingService(ABC):
    @abstractmethod
    def process_text(self, file_bytes: bytes, filename: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def process_pdf_text(self, file_bytes: bytes) -> str:
       raise NotImplementedError
    
    @abstractmethod
    def chunk_text(self, text: str, max_tokens: int, token_overlap: int) -> List[DocumentChunk]:
        raise NotImplementedError