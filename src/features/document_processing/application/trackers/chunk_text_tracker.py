from uuid import UUID
from src.broker import BaseEvent, AsyncProducer
from src.tracking import ProgressStage, ProgressTracker


class ChunkTextTracker(ProgressTracker):
    def __init__(
        self,
        producer: AsyncProducer,
        total_steps: int = 1, 
        publish_every: int = 1
    ):
        super().__init__(
            stage = ProgressStage(
                name="Processando",
                start=40,
                end=60
            ), 
            total_steps=total_steps, 
            publish_every=publish_every
        )

        self.__producer = producer

    
    async def publish(
        self,
        event: BaseEvent,
        knowledge_id: UUID,
        progress: int,
        error: bool = False
    ):
        payload = {
            "knowledge_id": knowledge_id,
            "update": {
                "stage": self._stage.name,
                "status": "Processando documento...",
                "progress": progress
            } 
        }

        if error:
            payload = {
            "knowledge_id": knowledge_id,
            "update": {
                "stage": self._stage.name,
                "status": "Error processando documento",
                "progress": 0
            }  
        }

        event_copy = event.model_copy()
        event_copy.payload = payload

        await self.__producer.publish(
            routing_key="documents.sessions.embeddings_update",
            event=event_copy
        )
