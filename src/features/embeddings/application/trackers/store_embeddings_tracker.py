from uuid import UUID
from src.broker import BaseEvent, AsyncProducer
from src.tracking import ProgressStage, ProgressTracker

class StoreEmbeddingsTracker(ProgressTracker):
    def __init__(
        self,
        producer: AsyncProducer,
        total_steps: int = 1, 
        publish_every: int = 1
    ):
        super().__init__(
            stage = ProgressStage(
                name="Guardando",
                start=80,
                end=100
            ), 
            total_steps=total_steps, 
            publish_every=publish_every
        )

        self.__producer = producer

    def calculate_progress(self, current: int, total:int):
        span = self._stage.end - self._stage.start
        return int(self._stage.start + (current / total) * span)


    
    async def publish(
        self,
        event: BaseEvent,
        knowledge_id: UUID,
        progress: int
    ):
        status = "Guardando embeddings..."

        if progress == 100:
            status = "Guardado"
        payload = {
            "knowledge_id": knowledge_id,
            "update": {
                "stage": self._stage.name,
                "status": status,
                "progress": progress
            }
            
        }

        event_copy = event.model_copy()
        event_copy.payload = payload

        await self.__producer.publish(
            routing_key="documents.sessions.embeddings_update",
            event=event_copy
        )
