import logging
from src.di.container import Container
from src.broker.infrastructure.rabbitmq.consumer import RabbitMqConsumer
from src.features.document_processing.application.event_handlers import chunk_text, extract_text



logger = logging.getLogger(__name__)

def __register_handlers():
    Container.register_factory(
        key="extract_text_handler",
        factory=lambda: extract_text.ExtractTextHandler(
            pdf_processor=Container.resolve("pdf_processor"),
            producer=Container.resolve("documents_producer"),
            async_http_client=Container.resolve("async_http_client"),
        )
    )

    Container.register_factory(
        key="chunk_text_handler",
        factory=lambda: chunk_text.ChunkTextHandler(
            text_chunker=Container.resolve("text_chunker"),
            producer=Container.resolve("documents_producer")
        )
    )

  

def __register_consumers():
    Container.register_factory(
        key="extract_text_consumer",
        factory=lambda: RabbitMqConsumer(
            queue_name="documents.extract_text.q",
            handler=Container.resolve("extract_text_handler")
        )
    )

    Container.register_factory(
        key="chunk_text_consumer",
        factory=lambda: RabbitMqConsumer(
            queue_name="documents.chunk_text.q",
            handler=Container.resolve("chunk_text_handler")
        )
    )

def register_broker_depenencies():
    __register_handlers()
    __register_consumers()




