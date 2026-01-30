from src.broker.domain import handlers, base_event, producer
from src.features.document_processing.domain import pdf_processor, schemas

class ExtractTextHandler(handlers.Handler):
    def __init__(
        self,
        pdf_processor: pdf_processor.PdfProcessor,
        producer: producer.Producer
    ):
        self.__pdf_processor = pdf_processor
        self.__producer = producer

    def handle(self, event):
        parsed_event = base_event.BaseEvent(**event)
        payload = schemas.ExtractTextPayload(**parsed_event.payload)

        if payload.file_type == "application/pdf":
            text = self.__pdf_processor.process(payload.file_bytes)
        
        elif payload.file_type == "text/plain" or payload.file_type == "text/markdown":
            text = payload.file_bytes.decode('utf-8')

        chunk_payload = schemas.ChunkTextPayload(
            user_id=payload.user_id,
            agent_id=payload.agent_id,
            knowledge_id=payload.knowledge_id,
            text=text
        )

        parsed_event.payload = chunk_payload

        self.__producer.publish(
            routing_key="documents.text.extracted",
            event=parsed_event
        )



        
