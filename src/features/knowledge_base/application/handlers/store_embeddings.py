from src.broker.domain import base_event, handlers, producer
from src.persistence.domain.vector_repository import VectorRepository
from src.features.embeddings.domain import entities 
from src.features.knowledge_base.domain.schemas import KnowledgeEmbeddingEStatus

class StoreEmbeddingsHandler(handlers.Handler):
    def __init__(
        self,
        vector_repository: VectorRepository,
        producer: producer.Producer
    ):
        self.__vector_repository = vector_repository
        self.__producer = producer

    def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        payload = entities.EmbeddingsPayload(**parsed_event.payload)

        self.__vector_repository.store_embeddings(
            embeddings=payload.embeddings,
            chunks=payload.chunks,
            namespace="convertia"
        )

        embedding_status_payload = KnowledgeEmbeddingEStatus(
            user_id=parsed_event.user_id,
            knowledge_id=payload.knowledge_id
        )


        self.__producer.publish(
            routing_key="documents.embeddings.stored"
        )

