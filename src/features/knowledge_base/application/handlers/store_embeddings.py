from src.broker.domain import base_event, handlers, producer
from src.persistence.domain.vector_repository import VectorRepository
from src.features.knowledge_base.domain.schemas import UpdateEmbeddingStatusPayload, StoreChunksPayload

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
        payload = StoreChunksPayload(**parsed_event.payload)

        def progress_callback(current, total):
            progress = int((current / total) * 100)
            progress_payload = {
                "knowledge_id": str(payload.knowledge_id),
                "session": {
                    "stage": "Almacenando embeddings",
                    "status": "Storing",
                    "progress": progress
                }
            }
        
            
            parsed_event.payload = progress_payload
            
            self.__producer.publish(
                routing_key="documents.sessions.embeddings_update",
                event=parsed_event
            )

        self.__vector_repository.store_embeddings(
            embeddings=payload.embeddings,
            chunks=payload.chunks,
            namespace="convertia",
            progress_callback=progress_callback
        )

        embedding_status_payload = UpdateEmbeddingStatusPayload(
            knowledge_id=payload.knowledge_id,
            is_embedded=True
        )

        parsed_event.payload = embedding_status_payload.model_dump()

        self.__producer.publish(
            routing_key="documents.embeddings.stored",
            event=parsed_event

        )

