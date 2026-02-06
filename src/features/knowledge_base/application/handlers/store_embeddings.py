import logging
from src.broker.domain import base_event, handlers, producer
from src.persistence.domain.vector_repository import VectorRepository
from src.features.knowledge_base.domain.schemas import UpdateEmbeddingStatusPayload, StoreChunksPayload
from src.features.knowledge_base.application.trackers.store_embeddings_tracker import StoreEmbeddingsTracker

logger = logging.getLogger(__name__)

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
        progress_tracker = StoreEmbeddingsTracker(
            producer=self.__producer,
            total_steps=payload.total_batches,
            publish_every=1
        )

        self.__vector_repository.store_embeddings(
            embeddings=payload.embeddings,
            chunks=payload.chunks,
            namespace="convertia"
        )

        progress = progress_tracker.calculate_progress(
            current=payload.batch_index,
            total=payload.total_batches
        )

        progress_tracker.publish(
            event=parsed_event.model_copy(),
            knowledge_id=payload.knowledge_id,
            progress=progress
        )
        
        if int(payload.batch_index) == int(payload.total_batches):
            embedding_status_payload = UpdateEmbeddingStatusPayload(
                knowledge_id=payload.knowledge_id,
                is_embedded=True
            )

            parsed_event.payload = embedding_status_payload.model_dump()

            self.__producer.publish(
                routing_key="documents.embeddings.stored",
                event=parsed_event

            )

