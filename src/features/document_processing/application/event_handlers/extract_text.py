import json
from src.broker import AsyncHandler, BaseEvent, DocumentsProducer
from src.http import AsyncHttpClient
from src.persistence import SessionRepository
from ...domain import PdfProcessor, ExtractTextPayload, ChunkTextData
from ..trackers.extract_text_tracker import ExtractTextTracker


class ExtractTextHandler(AsyncHandler):
    def __init__(
        self,
        pdf_processor: PdfProcessor,
        producer: DocumentsProducer,
        async_http_client: AsyncHttpClient,
        session_repository: SessionRepository
    ):
        self.__pdf_processor = pdf_processor
        self.__producer = producer
        self.__async_http_client = async_http_client
        self.__session_repository = session_repository

    async def handle(self, event):
        parsed_event = BaseEvent(**event)
        payload = ExtractTextPayload(**parsed_event.payload)
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
                await progress_tracker.publish(
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
            await progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=payload.knowledge_id,
                progress=0,
                error=True
            )
            
            update_status_payload = {
                "knowledge_id": payload.knowledge_id,
                "status": "ERROR"
            }

            parsed_event.payload = update_status_payload
            
            await self.__producer.publish(
                routing_key="documents.status.update",
                event=parsed_event
            )

            raise


        progress = progress_tracker.step()
        if progress_tracker.should_publish():
            await progress_tracker.publish(
                event=parsed_event.model_copy(),
                knowledge_id=payload.knowledge_id,
                progress=progress
            )


        session_data = ChunkTextData(
            knowledge_id=payload.knowledge_id,
            text=text
        )
        
        self.__session_repository.set_session(
            key=str(parsed_event.event_id),
            value=json.dumps(session_data.model_dump(mode="json"))
        )


        if hasattr(parsed_event, "payload"):
            delattr(parsed_event, "payload")

        await self.__producer.publish(
            routing_key="documents.text.extracted",
            event=parsed_event
        )



        
