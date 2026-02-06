import logging
import asyncio
from src.broker.domain import handlers, base_event, producer
from src.features.embeddings.domain import embedding_service, schemas
from src.features.embeddings.application.trackers.embeddings_progress_tracker import EmbeddingsProgressTracker

logger = logging.getLogger(__name__)
class EmbedChunksHandler(handlers.AsyncHandler):
    def __init__(
        self,
        embedding_serivce: embedding_service.EmbeddingService,
        producer: producer.Producer
    ):
        self.__embedding_service=embedding_serivce
        self.__producer = producer
    
    async def handle(self, event: base_event.BaseEvent):
        parsed_event = base_event.BaseEvent(**event)
        payload = schemas.EmbedChunksPayload(**parsed_event.payload)

        workers = asyncio.Semaphore(10) # do not overload api

        tasks = [
            self.__task_handler(chunk.content, workers)
            for chunk in payload.chunks
        ]

        embeddings = []
        progress_tracker = EmbeddingsProgressTracker(
            producer=self.__producer,
            total_steps=len(tasks),
            publish_every=10
        )

        for promise in asyncio.as_completed(tasks):
            result = await promise

            embeddings.append(result)
            progress = progress_tracker.step()

            if progress_tracker.should_publish():
                progress_tracker.publish(
                    event=parsed_event.model_copy(),
                    knowledge_id=payload.knowledge_id,
                    progress=progress
                )

        # Do not overload rabbitmq
        batch_size = 64
        batches = [
            {
                "chunks": payload.chunks[i:i + batch_size],
                "embeddings": embeddings[i:i + batch_size]
            }
            
            for i in range(0, len(payload.chunks), batch_size)
        ]

        total_batches = len(batches)

        for index, batch in enumerate(batches, start=1):
            store_chunks_payload = {
                "total_batches": total_batches,
                "batch_index": index,
                "embeddings": batch["embeddings"],
                "chunks": batch["chunks"],
                "knowledge_id": str(payload.knowledge_id)
            }

            parsed_event.payload = store_chunks_payload
            
            self.__producer.publish(
                routing_key="documents.text.embedded",
                event=parsed_event
            )
        
    async def __task_handler(
        self,
        chunk: str,
        workers: asyncio.Semaphore
    ):
        async with workers:
            return await self.__embedding_service.embed_query(chunk)


        