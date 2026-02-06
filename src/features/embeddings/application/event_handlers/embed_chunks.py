import logging
import asyncio
from src.broker.domain import handlers, base_event, producer
from src.features.embeddings.domain import embedding_service, schemas

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

        embedding_session_payload = {
            "knowledge_id": str(payload.knowledge_id),
            "session": {
                "stage": "Embedding documento...",
                "status": "Embedding",
                "progress": 60
            }
        }

        parsed_event.payload = embedding_session_payload

        self.__producer.publish(
            routing_key="documents.sessions.embeddings_update",
            event=parsed_event
        )

        workers = asyncio.Semaphore(10)

        tasks = [
            self.__task_handler(chunk.content, workers)
            for chunk in payload.chunks
        ]

        total_chunks = len(tasks)
        embeddings = []
        completed = 0

        for promise in asyncio.as_completed(tasks):
            result = await promise

            embeddings.append(result)

            completed += 1
            progress = int(60 + (completed / total_chunks) * 20)

            parsed_event.payload = {
                "knowledge_id": str(payload.knowledge_id),
                "session": {
                    "stage": "Embedding documento...",
                    "status": "Embedding",
                    "progress": progress
                }
            }

            self.__producer.publish(
                routing_key="documents.sessions.embeddings_update",
                event=parsed_event
            )
                

        store_chunks_payload = {
            "embeddings": embeddings,
            "chunks": payload.chunks,
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


        