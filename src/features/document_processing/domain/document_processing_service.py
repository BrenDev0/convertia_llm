from abc import ABC, abstractmethod
from typing import List
from src.persistence.domain.entities import DocumentChunk

class DocumentProcessingService(ABC):
    @abstractmethod
    def process_txt(self, file_bytes: bytes, filename: str) -> List[DocumentChunk]:
        raise NotImplementedError
    
    @abstractmethod
    def process_pdf(self, file_bytes: bytes) -> List[DocumentChunk]:
       raise NotImplementedError