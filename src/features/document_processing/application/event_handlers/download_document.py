from src.broker.domain import handlers, base_event, producer
from src.features.document_processing.domain import schemas
from src.features.http.domain.async_http_client import AsyncHttpClient

class DownloadDocument(handlers.AsyncHandler):
    def __init__(
        self,
        producer: producer.Producer,
        async_http_client: AsyncHttpClient
    ):
        self.__producer = producer
        self.__async_http_client = async_http_client

    async def handle(
        self,
        event
    ):
        parsed_event= base_event.BaseEvent(**event)
        payload = schemas.DownloadDocumentPayload(**parsed_event.payload)

        response = await self.__async_http_client.get_request(
            endpoint=payload.file_url
        )

        file_bytes = response.content

        extract_text_payload = schemas.ExtractTextPayload(
            user_id=payload.user_id,
            agent_id=payload.agent_id,
            knowledge_id=payload.knowledge_id,
            file_type=payload.file_type,
            file_bytes=file_bytes
        )

        parsed_event.payload = extract_text_payload.model_dump()

        self.__producer.publish(
            routing_key="documents.raw",
            event= parsed_event
        )


