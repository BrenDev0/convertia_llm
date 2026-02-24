from uuid import UUID
from src.persistence import VectorRepository
from ...domain import EmbeddingService


class GetRAGContext:
    def __init__(
        self,
        vector_repository: VectorRepository,
        embedding_service: EmbeddingService
    ):
        self.__vector_repository = vector_repository
        self.__embedding_service = embedding_service

    async def execute(
        self,
        agent_id: UUID,
        input: str,
        prompt: str
    ):
        embedded_input = await self.__embedding_service.embed_query(input)

        result = self.__vector_repository.query_context(
            query_vector=embedded_input,
            agent_id=agent_id
        )

        if len(result) != 0:
            context = "\n".join(result)
            prompt = prompt + context 

        return prompt
        

        

