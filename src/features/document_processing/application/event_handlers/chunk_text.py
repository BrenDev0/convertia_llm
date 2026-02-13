import json
from src.broker.domain import handlers, base_event, producer
from src.features.document_processing.domain import text_chunker, schemas
from src.features.document_processing.application.trackers.chunk_text_tracker import ChunkTextTracker
from src.persistence.domain.session_repository import SessionRepository

class ChunkTextHandler(handlers.Handler):
    def __init__(
        self,
        text_chunker: text_chunker.TextChunker,
        producer: producer.AsyncProducer,
        session_repository: SessionRepository
    ):
        self.__text_chunker = text_chunker
        self.__producer = producer
        self.__session_repository = session_repository

    async def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        progress_tracker = ChunkTextTracker(
            producer=self.__producer,
            total_steps=1,
            publish_every=1
        )

        session = self.__session_repository.get_session(
            key=str(parsed_event.event_id)
        )

        if not session:
            raise ValueError("No session found")
        
        data = schemas.ChunkTextData(**session)

        metadata = {
            "user_id": parsed_event.user_id,
            "agent_id": parsed_event.agent_id,
            "knowledge_id": data.knowledge_id
        }

        try:
            chunks = self.__text_chunker.chunk(
                text=data.text,
                metadata=metadata,
                max_tokens=1000,
                token_overlap=200
            )

        except Exception:
            await progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=data.knowledge_id,
                progress=0,
                error=True
            )
            update_status_payload = {
                "knowledge_id": data.knowledge_id,
                "status": "ERROR"
            }

            parsed_event.payload = update_status_payload
            
            await self.__producer.publish(
                routing_key="documents.status.update",
                event=parsed_event
            )

            raise

        progress = progress_tracker.step()
        if progress_tracker.should_publish():
            await progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=data.knowledge_id,
                progress=progress
            )

        session_data = {
            "knowledge_id": str(data.knowledge_id),
            "chunks": [
                chunk.model_dump(mode="json") 
                for chunk in chunks
            ]
        }

        self.__session_repository.set_session(
            key=str(parsed_event.event_id),
            value=json.dumps(session_data)
        )

        await self.__producer.publish(
            routing_key="document.text.chunked",
            event=parsed_event
        )