from uuid import UUID
from src.broker.domain import base_event, producer
from src.tracking.domain.entites import ProgressStage
from src.tracking.application.progress_tracker import ProgressTracker

class StoreEmbeddingsTracker(ProgressTracker):
    def __init__(
        self,
        producer: producer.Producer,
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


    
    def publish(
        self,
        event: base_event.BaseEvent,
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

        self.__producer.publish(
            routing_key="documents.sessions.embeddings_update",
            event=event_copy
        )
