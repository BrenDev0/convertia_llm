import logging
import asyncio
import json
from uuid import uuid4
from src.broker.domain import handlers, base_event, producer
from src.features.embeddings.domain import embedding_service, schemas
from src.features.embeddings.application.trackers.embeddings_progress_tracker import EmbeddingsProgressTracker
from src.persistence.domain.session_repository import SessionRepository

logger = logging.getLogger(__name__)
class EmbedChunksHandler(handlers.AsyncHandler):
    def __init__(
        self,
        embedding_serivce: embedding_service.EmbeddingService,
        producer: producer.Producer,
        session_repository: SessionRepository
    ):
        self.__embedding_service = embedding_serivce
        self.__producer = producer
        self.__session_repository = session_repository
    
    async def handle(self, event: base_event.BaseEvent):
        parsed_event = base_event.BaseEvent(**event)
        session = self.__session_repository.get_session(
            key=str(parsed_event.event_id)
        )

        if not session:
            raise ValueError("No session found")
        
        data = schemas.EmbedChunksData(**session)

        workers = asyncio.Semaphore(10) # do not overload api

        tasks = [
            self.__task_handler(chunk.content, workers)
            for chunk in data.chunks
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
                    knowledge_id=data.knowledge_id,
                    progress=progress
                )
        
        self.__session_repository.delete_session(
            key=str(parsed_event.event_id)
        )

        # allow next consumer to store while storing in redis
        batch_size = 64
        batches = [
            {
                "chunks": data.chunks[i:i + batch_size],
                "embeddings": embeddings[i:i + batch_size]
            }
            
            for i in range(0, len(data.chunks), batch_size)
        ]

        total_batches = len(batches)

        for index, batch in enumerate(batches, start=1):
            store_chunks_data = {
                "total_batches": total_batches,
                "batch_index": index,
                "embeddings": batch["embeddings"],
                "chunks": [
                    chunk.model_dump(mode="json")
                    for chunk in batch["chunks"]
                ],
                "knowledge_id": str(data.knowledge_id)
            }

            batch_event = base_event.BaseEvent(
               event_id=uuid4(),
               user_id=parsed_event.user_id,
               agent_id=parsed_event.agent_id,
               connection_id=parsed_event.connection_id
            )

            self.__session_repository.set_session(
                key=str(batch_event.event_id),
                value=json.dumps(store_chunks_data)
            )
            
            self.__producer.publish(
                routing_key="documents.text.embedded",
                event=batch_event
            )
        
    async def __task_handler(
        self,
        chunk: str,
        workers: asyncio.Semaphore
    ):
        async with workers:
            return await self.__embedding_service.embed_query(chunk)


        