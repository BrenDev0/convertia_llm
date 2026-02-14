from uuid import UUID
from src.broker.domain import base_event, producer
from src.tracking.domain.entites import ProgressStage
from src.tracking.application.progress_tracker import ProgressTracker

class EmbeddingsProgressTracker(ProgressTracker):
    def __init__(
        self, 
        producer: producer.AsyncProducer, 
        total_steps: int = 1, 
        publish_every: int = 1,
    ):
        
        super().__init__(
            stage=ProgressStage(
                name="Embedding",
                start=60,
                end=80
            ), 
            total_steps=total_steps, 
            publish_every=publish_every
        )

        self.__producer = producer

    async def publish(
        self,
        event: base_event.BaseEvent,
        knowledge_id: UUID,
        progress: int,
        error: bool = False
    ):
        payload = {
            "knowledge_id": knowledge_id,
            "update": {
                "stage": self._stage.name,
                "status": "Creando los embeddings...",
                "progress": progress
            }  
        }

        if error:
            payload = {
            "knowledge_id": knowledge_id,
            "update": {
                "stage": self._stage.name,
                "status": "Error creando embeddings",
                "progress": 0
            }  
        }

        event_copy = event.model_copy()

        event_copy.payload = payload

        await self.__producer.publish(
            routing_key="documents.sessions.embeddings_update",
            event=event_copy
        )