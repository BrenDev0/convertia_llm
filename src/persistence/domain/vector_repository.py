from abc import ABC, abstractmethod
from typing import List, Optional, Callable
from uuid import UUID
from pydantic import BaseModel
from src.persistence.domain.entities import DocumentChunk

class DeleteFilter(BaseModel):
    filename: Optional[str] = None
    user_id: Optional[str] = None  
    company_id: Optional[str] = None
    document_id: Optional[str] = None

class VectorRepository(ABC):
    @abstractmethod
    def store_embeddings(
        self,
        embeddings: List[List[float]],
        chunks: List[DocumentChunk],
        namespace: str,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ):
        raise NotImplementedError
    
    @abstractmethod
    def delete_embeddings(
        self,
        namespace: str,
        **filters
    ):
        raise NotImplementedError
    
    @abstractmethod
    def create_namespace(
        self,
        name: str,
        size: int
    ):
        raise NotImplementedError
    
    @abstractmethod
    def delete_namespace(self, namespace: str) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def delete_embeddings(self, key: str, value: UUID, namespace: str,):
        raise NotImplementedError