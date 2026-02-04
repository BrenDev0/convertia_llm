from src.broker.domain import handlers, base_event, producer
from src.features.embeddings.domain import embedding_service, schemas


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

        result = await self.__embedding_service.embed_document(
            document_chunks=payload.chunks
        )

        store_chunks_payload = {
            "embeddings": result.embeddings,
            "chunks": result.chunks,
            "knowledge_id": payload.knowledge_id
        }
        parsed_event.payload = store_chunks_payload

        self.__producer.publish(
            routing_key="documents.text.embedded",
            event=parsed_event
        )


        