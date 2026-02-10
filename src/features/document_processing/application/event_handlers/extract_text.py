import json
from src.broker.domain import handlers, base_event, producer
from src.features.document_processing.domain import pdf_processor, schemas
from src.http.domain.async_http_client import AsyncHttpClient
from src.features.document_processing.application.trackers.extract_text_tracker import ExtractTextTracker
from src.persistence.domain.session_repository import SessionRepository

class ExtractTextHandler(handlers.AsyncHandler):
    def __init__(
        self,
        pdf_processor: pdf_processor.PdfProcessor,
        producer: producer.Producer,
        async_http_client: AsyncHttpClient,
        session_repository: SessionRepository
    ):
        self.__pdf_processor = pdf_processor
        self.__producer = producer
        self.__async_http_client = async_http_client
        self.__session_repository = session_repository

    async def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        payload = schemas.ExtractTextPayload(**parsed_event.payload)
        progress_tracker = ExtractTextTracker(
            producer=self.__producer,
            total_steps=2,
            publish_every=1
        )

        try:

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

        except Exception:
            progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=payload.knowledge_id,
                progress=0,
                error=True
            )
            raise


        progress = progress_tracker.step()
        if progress_tracker.should_publish():
            progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=payload.knowledge_id,
                progress=progress
            )


        session_data = schemas.ChunkTextData(
            knowledge_id=payload.knowledge_id,
            text=text
        )
        
        self.__session_repository.set_session(
            key=str(parsed_event.event_id),
            value=json.dumps(session_data.model_dump(mode="json"))
        )


        if hasattr(parsed_event, "payload"):
            delattr(parsed_event, "payload")

        self.__producer.publish(
            routing_key="documents.text.extracted",
            event=parsed_event
        )



        
