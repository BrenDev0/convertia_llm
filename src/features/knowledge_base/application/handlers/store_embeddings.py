import logging
from src.broker.domain import base_event, handlers, producer
from src.persistence.domain.vector_repository import VectorRepository
from src.features.knowledge_base.domain import schemas
from src.features.knowledge_base.application.trackers.store_embeddings_tracker import StoreEmbeddingsTracker
from src.persistence.domain.session_repository import SessionRepository

logger = logging.getLogger(__name__)

class StoreEmbeddingsHandler(handlers.Handler):
    def __init__(
        self,
        vector_repository: VectorRepository,
        producer: producer.Producer,
        session_repository: SessionRepository
    ):
        self.__vector_repository = vector_repository
        self.__producer = producer
        self.__session_repsoitory = session_repository

    def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        session = self.__session_repsoitory.get_session(
            key=str(parsed_event.event_id)
        )

        if not session:
            raise ValueError("No session found")
        
        data = schemas.StoreChunksData(**session)

        progress_tracker = StoreEmbeddingsTracker(
            producer=self.__producer,
            total_steps=data.total_batches,
            publish_every=1
        )

        self.__vector_repository.store_embeddings(
            embeddings=data.embeddings,
            chunks=data.chunks,
            namespace="convertia"
        )

        progress = progress_tracker.calculate_progress(
            current=data.batch_index,
            total=data.total_batches
        )

        progress_tracker.publish(
            event=parsed_event.model_copy(),
            knowledge_id=data.knowledge_id,
            progress=progress
        )

        self.__session_repsoitory.delete_session(
            key=str(parsed_event.event_id)
        )
        
        if int(data.batch_index) == int(data.total_batches):
            embedding_status_payload = schemas.UpdateEmbeddingStatusPayload(
                knowledge_id=data.knowledge_id,
                is_embedded=True
            )

            parsed_event.payload = embedding_status_payload.model_dump()

            self.__producer.publish(
                routing_key="documents.status.update",
                event=parsed_event

            )

