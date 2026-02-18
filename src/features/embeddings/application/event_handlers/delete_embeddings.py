import logging
from src.broker import BaseEvent, CommunicationProducer, DocumentsProducer, AsyncHandler
from src.persistence import VectorRepository
from ...domain import DeleteEmbeddingsPayload, UpdateEmbeddingStatusPayload

logger = logging.getLogger(__name__)

class DeleteEmbeddingsHandler(AsyncHandler):
    def __init__(
        self,
        vector_repository: VectorRepository,
        documents_producer: DocumentsProducer,
        communication_producer: CommunicationProducer
    ):
        self.__vector_repository = vector_repository
        self.__documents_producer = documents_producer
        self.__communication_producer = communication_producer

    async def handle(self, event):
        parsed_event = BaseEvent(**event)
        payload = DeleteEmbeddingsPayload(**parsed_event.payload)

        try:
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
            await self.__communication_producer.publish(
                routing_key="communication.websocket.broadcast",
                event=parsed_event
            )

            logger.exception("Error deleting embeddings")
            return 

        embedding_status_payload = UpdateEmbeddingStatusPayload(
            knowledge_id=payload.knowledge_id,
            status="NO PROCESADO"
        )

        parsed_event.payload = embedding_status_payload.model_dump()

        await self.__documents_producer.publish(
            routing_key="documents.status.update",
            event=parsed_event
        )        