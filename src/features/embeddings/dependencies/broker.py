import logging
import os
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.broker.domain import consumer
from src.broker.dependencies.producers import get_documents_producer
from src.broker.infrastructure.rabbitmq.consumer import RabbitMqConsumer
from src.features.embeddings.application.event_handlers.embed_chunks import EmbedChunksHandler
from src.features.embeddings.dependencies.services import get_embedding_service

logger = logging.getLogger(__name__)

def get_embed_chunks_handler() -> EmbedChunksHandler:
    try:
        instance_key = "embed_chunks_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = EmbedChunksHandler(
            embedding_serivce=get_embedding_service(),
            producer=get_documents_producer()
        )

        Container.register(instance_key, handler)
        logger.debug(f"{instance_key} registered")

    return handler

def get_embed_chunks_consumer() -> consumer.Consumer:
    try: 
        instance_key = "embed_chunks_consumer"
        consumer = Container.resolve(instance_key)

    except DependencyNotRegistered:
        consumer = RabbitMqConsumer(
            queue_name="documents.embed_chunks.q",
            handler=get_embed_chunks_handler()
        )

        Container.register(instance_key, consumer)
        logger.debug(f"{instance_key} register")

    return consumer