from abc import ABC, abstractmethod
from typing import List
from src.persistence.domain.entities import DocumentChunk
from src.features.embeddings.domain.entities import EmbeddingResult

class EmbeddingService(ABC):
    @abstractmethod
    async def embed_document(
        self,
        document_chunks: List[DocumentChunk]
    ) -> EmbeddingResult:
        raise NotImplementedError
    
    @abstractmethod
    async def embed_query(self, query: str) -> List[float]:
        raise NotImplementedError
    