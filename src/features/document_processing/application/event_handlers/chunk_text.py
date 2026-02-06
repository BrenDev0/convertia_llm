from src.broker.domain import handlers, base_event, producer
from src.features.document_processing.domain import text_chunker, schemas
from src.features.document_processing.application.trackers.chunk_text_tracker import ChunkTextTracker

class ChunkTextHandler(handlers.Handler):
    def __init__(
        self,
        text_chunker: text_chunker.TextChunker,
        producer: producer.Producer
    ):
        self.__text_chunker = text_chunker
        self.__producer = producer

    def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        payload = schemas.ChunkTextPayload(**parsed_event.payload)
        progress_tracker = ChunkTextTracker(
            producer=self.__producer,
            total_steps=1,
            publish_every=1
        )

        metadata = {
            "user_id": parsed_event.user_id,
            "agent_id": parsed_event.agent_id,
            "knowledge_id": payload.knowledge_id
        }

        chunks = self.__text_chunker.chunk(
            text=payload.text,
            metadata=metadata,
            max_tokens=1000,
            token_overlap=200
        )

        progress = progress_tracker.step()
        if progress_tracker.should_publish():
            progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=payload.knowledge_id,
                progress=progress
            )

        embed_chunks_payload = {
            "knowledge_id": payload.knowledge_id,
            "chunks": chunks
        }

        parsed_event.payload = embed_chunks_payload



        self.__producer.publish(
            routing_key="document.text.chunked",
            event=parsed_event
        )