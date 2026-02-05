import logging
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

        embedding_status_copy = parsed_event.model_copy()
        embedding_status_copy.payload = embedding_session_payload

        self.__producer.publish(
            routing_key="documents.sessions.embeddings_update",
            event=embedding_status_copy
        )

        total_chunks = len(payload.chunks)
        embeddings = []

        for index, chunk in enumerate(payload.chunks, start=1):
            result = await self.__embedding_service.embed_query(
                query=chunk.content
            )

            embeddings.append(result)

            chunk_progress = (index / total_chunks) 
            progress = int(60 + (chunk_progress * 20))  # 60 to 80
            
            embedding_session_payload = {
                "knowledge_id": str(payload.knowledge_id),
                "session": {
                    "stage": "Embedding documento...",
                    "status": "Embedding",
                    "progress": progress
                }
            }

            loop_copy = parsed_event.model_copy()

            loop_copy.payload = embedding_session_payload

            self.__producer.publish(
                routing_key="documents.sessions.embeddings_update",
                event=loop_copy
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


        