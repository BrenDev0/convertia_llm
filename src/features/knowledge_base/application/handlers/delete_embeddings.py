import logging
from src.broker.domain import base_event, handlers, producer
from src.persistence.domain.vector_repository import VectorRepository
from src.features.knowledge_base.domain import schemas

logger = logging.getLogger(__name__)

class DeleteEmbeddingsHandler(handlers.Handler):
    def __init__(
        self,
        vector_repository: VectorRepository,
        documents_producer: producer.Producer,
        communication_producer: producer.Producer
    ):
        self.__vector_repository = vector_repository
        self.__documents_producer = documents_producer
        self.__communication_producer = communication_producer

    def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        payload = schemas.DeleteEmbeddingsPayload(**parsed_event.payload)

        try:
            logger.debug("in delete embeddings::::::::::::::::")
            self.__vector_repository.delete_embeddings(
                key="knowledge_id",
                value=payload.knowledge_id,
                namespace="convertia"
            )
        
        except Exception:
            error_payload = {
                "type": "ERROR",
                "data": {
                    "detail": "Error borrando documento"
                }
            }

            parsed_event.payload = error_payload
            self.__communication_producer.publish(
                routing_key="communication.websocket.broadcast",
                event=parsed_event
            )

            logger.exception("Error deleting embeddings")
            return 

        embedding_status_payload = schemas.UpdateEmbeddingStatusPayload(
            knowledge_id=payload.knowledge_id,
            status="NO PROCESADO"
        )

        parsed_event.payload = embedding_status_payload.model_dump()

        self.__documents_producer.publish(
            routing_key="documents.status.update",
            event=parsed_event
        )        