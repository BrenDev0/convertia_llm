import logging
import asyncio
import json
from typing import List
from uuid import uuid4, UUID
from src.persistence import DocumentChunk, SessionRepository
from src.broker import BaseEvent, DocumentsProducer, AsyncHandler
from ...domain import EmbeddingService, EmbedChunksData
from ...application import (
    EmbeddingsProgressTracker,
)


logger = logging.getLogger(__name__)


class EmbedChunksHandler(AsyncHandler):
    def __init__(
        self,
        embedding_serivce: EmbeddingService,
        producer: DocumentsProducer,
        session_repository: SessionRepository,
    ):
        self.__embedding_service = embedding_serivce
        self.__producer = producer
        self.__session_repository = session_repository

    async def handle(self, event: BaseEvent):
        parsed_event = BaseEvent(**event)
        session = self.__session_repository.get_session(
            key=str(parsed_event.event_id)
        )

        if not session:
            raise ValueError("No session found")

        data = EmbedChunksData(**session)

        max_concurrent = asyncio.Semaphore(20)  # do not overload api

        embeddings = []
        
        progress_tracker = EmbeddingsProgressTracker(
            producer=self.__producer,
            total_steps=len(data.chunks),
            publish_every=10,
        )

        try:
            results = await asyncio.gather(
                *[
                    self._task_handler(chunk.content, max_concurrent)
                    for chunk in data.chunks
                ],
                return_exceptions=True,
            )

            for result in results:
                if isinstance(result, Exception):
                    raise result

                embeddings.append(result)
                progress = progress_tracker.step()

                if progress_tracker.should_publish():
                    await progress_tracker.publish(
                        event=parsed_event.model_copy(),
                        knowledge_id=data.knowledge_id,
                        progress=progress,
                    )

        except Exception:
            await progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=data.knowledge_id,
                progress=0,
                error=True,
            )

            update_status_payload = {
                "knowledge_id": data.knowledge_id,
                "status": "ERROR",
            }

            parsed_event.payload = update_status_payload

            await self.__producer.publish(
                routing_key="documents.status.update",
                event=parsed_event,
            )

            raise

        self.__session_repository.delete_session(
            key=str(parsed_event.event_id)
        )

        await self._send_batches(
            user_id=parsed_event.user_id,
            agent_id=parsed_event.agent_id,
            knowledge_id=data.knowledge_id,
            connection_id=parsed_event.connection_id,
            chunks=data.chunks,
            embeddings=embeddings
        )
        

    async def _task_handler(
        self,
        chunk: str,
        max_concurrent: asyncio.Semaphore,
    ):
        async with max_concurrent:
            return await self.__embedding_service.embed_query(chunk)
        

    async def _send_batches(
        self,
        user_id: UUID,
        agent_id: UUID,
        knowledge_id: UUID,
        connection_id: UUID,
        chunks: List[DocumentChunk],
        embeddings,
    ):
        batch_size = 64
        batches = [
            {
                "chunks": chunks[i : i + batch_size],
                "embeddings": embeddings[i : i + batch_size],
            }
            for i in range(0, len(chunks), batch_size)
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
                "knowledge_id": str(knowledge_id),
            }

            batch_event = BaseEvent(
                event_id=uuid4(),
                user_id=user_id,
                agent_id=agent_id,
                connection_id=connection_id,
            )

            self.__session_repository.set_session(
                key=str(batch_event.event_id),
                value=json.dumps(store_chunks_data),
            )

            await self.__producer.publish(
                routing_key="documents.text.embedded",
                event=batch_event,
            )
