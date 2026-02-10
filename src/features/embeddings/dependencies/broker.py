import logging
import os
from src.broker.infrastructure.pika import producer
from src.di.container import Container
from src.broker.infrastructure.pikaaio import async_consumer
from src.features.embeddings.application.event_handlers.embed_chunks import EmbedChunksHandler

logger = logging.getLogger(__name__)

def __register_hanlders():
    Container.register_factory(
        key="embed_chunks_handler",
        factory=lambda: EmbedChunksHandler(
            embedding_serivce=Container.resolve("embedding_service"),
            producer=producer.RabbitMqProducer(exchange="documents"),
            session_repository=Container.resolve("session_repository")
        )
    )

def __register_consumers():
    Container.register_factory(
        key="embed_chunks_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            queue_name="documents.embed_chunks.q",
            handler=Container.resolve("embed_chunks_handler")
        )
    )

def register_broker_dependencies():
    __register_hanlders()
    __register_consumers()