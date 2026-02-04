from src.broker.domain import handlers, base_event, producer
from src.features.embeddings.domain import embedding_service, schemas, entities


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

        parsed_event.payload = result.model_dump()

        self.__producer.publish(
            routing_key="documents.text.embedded",
            event=parsed_event
        )


        