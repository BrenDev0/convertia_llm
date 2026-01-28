import tiktoken
import uuid
from typing import List
from openai import AsyncOpenAI
from src.features.embeddings.domain import entities, embedding_service
from src.persistence.domain.entities import DocumentChunk

class OpenAIEmbeddingService(embedding_service.EmbeddingService):
    def __init__(self, api_key: str, model: str = "text-embedding-3-large"):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._encoding = tiktoken.get_encoding("cl100k_base")
    
    async def embed_document(
        self,
        document_chunks: List[DocumentChunk]
    ) -> entities.EmbeddingResult:
        texts = [chunk.content for chunk in document_chunks]
        batch_size = 64
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = await self._client.embeddings.create(
                model=self._model,
                input=batch
            )
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
        
        return entities.EmbeddingResult(
            chunks=document_chunks,
            embeddings=embeddings
        )
    
    async def embed_query(self, query: str) -> List[float]:
        result = await self._client.embeddings.create(
            model=self._model,
            input=query
        )
        return result.data[0].embedding
    
