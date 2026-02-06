from src.broker.domain import handlers, base_event, producer
from src.features.document_processing.domain import pdf_processor, schemas
from src.http.domain.async_http_client import AsyncHttpClient
from src.features.document_processing.application.trackers.extract_text_tracker import ExtractTextTracker

class ExtractTextHandler(handlers.AsyncHandler):
    def __init__(
        self,
        pdf_processor: pdf_processor.PdfProcessor,
        producer: producer.Producer,
        async_http_client: AsyncHttpClient
    ):
        self.__pdf_processor = pdf_processor
        self.__producer = producer
        self.__async_http_client = async_http_client

    async def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        payload = schemas.ExtractTextPayload(**parsed_event.payload)
        progress_tracker = ExtractTextTracker(
            producer=self.__producer,
            total_steps=2,
            publish_every=1
        )

        response = await self.__async_http_client.request(
            endpoint=payload.file_url,
            method="GET"
        )

        progress = progress_tracker.step()
        if progress_tracker.should_publish():
            progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=payload.knowledge_id,
                progress=progress
            )

        file_bytes = response.content

        if payload.file_type == "application/pdf":
            text = self.__pdf_processor.process(file_bytes)
        
        elif payload.file_type == "text/plain" or payload.file_type == "text/markdown":
            text = file_bytes.decode('utf-8')

        progress = progress_tracker.step()
        if progress_tracker.should_publish():
            progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=payload.knowledge_id,
                progress=progress
            )

        chunk_payload = schemas.ChunkTextPayload(
            knowledge_id=payload.knowledge_id,
            text=text
        )

        parsed_event.payload = chunk_payload.model_dump()

        self.__producer.publish(
            routing_key="documents.text.extracted",
            event=parsed_event
        )



        
