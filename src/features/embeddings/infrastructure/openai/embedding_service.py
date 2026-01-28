import tiktoken
from typing import List
from openai import AsyncOpenAI
from src.features.embeddings.domain import entities, embedding_service
from src.features.embeddings.infrastructure.openai.schemas import OpenAiEmbeddingResposne
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
        embeddings = []
        
        for text in texts:
            response = await self._client.embeddings.create(
                model=self._model,
                input=text
            )
            
            parsed_response = OpenAiEmbeddingResposne.model_validate(response.model_dump()) 

            batch_embeddings = [item.embedding for item in parsed_response.data]
            embeddings.extend(batch_embeddings)
        
        return entities.EmbeddingResult(
            chunks=document_chunks,
            embeddings=embeddings
        )
    
    async def embed_query(self, query: str) -> List[float]:
        response = await self._client.embeddings.create(
            model=self._model,
            input=query
        )

        parsed_response = OpenAiEmbeddingResposne.model_validate(response.model_dump()) 

        return parsed_response.data[0].embedding
    
