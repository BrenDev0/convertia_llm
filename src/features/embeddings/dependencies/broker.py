import logging
import os
from src.broker.infrastructure.pika import producer
from src.di.container import Container
from src.broker.infrastructure.pikaaio import async_consumer
from src.broker.infrastructure.pika import consumer
from src.features.embeddings.application.event_handlers import embed_chunks, store_embeddings, delete_embeddings, update_embedding_status

logger = logging.getLogger(__name__)

def __register_hanlders():
    Container.register_factory(
        key="embed_chunks_handler",
        factory=lambda: embed_chunks.EmbedChunksHandler(
            embedding_serivce=Container.resolve("embedding_service"),
            producer=producer.RabbitMqProducer(exchange="documents"),
            session_repository=Container.resolve("session_repository")
        )
    )

    Container.register_factory(
        key="store_embeddings_handler",
        factory=lambda: store_embeddings.StoreEmbeddingsHandler(
            vector_repository=Container.resolve("vector_repository"),
            producer=producer.RabbitMqProducer(exchange="documents"),
            session_repository=Container.resolve("session_repository")
        )
    )

    Container.register_factory(
        key="update_embeddings_status_handler",
        factory=lambda: update_embedding_status.UpdateEmeddingStatus(
            async_http_client=Container.resolve("async_http_client")
        )
    )

    Container.register_factory(
        key="delete_embeddings_handler",
        factory=lambda: delete_embeddings.DeleteEmbeddingsHandler(
            vector_repository=Container.resolve("vector_repository"),
            documents_producer=producer.RabbitMqProducer("documents"),
            communication_producer=producer.RabbitMqProducer(exchange="communication")
        )
    )

def __register_consumers():
    Container.register_factory(
        key="embed_chunks_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            queue_name="documents.embed_chunks.q",
            handler=Container.resolve("embed_chunks_handler"),
            worker_count=10
        )
    )

    Container.register_factory(
        key="store_embeddings_consumer",
        factory=lambda: consumer.RabbitMqConsumer(
            queue_name="documents.store_embeddings.q",
            handler=Container.resolve("store_embeddings_handler")
        )
    )

    Container.register_factory(
        key="update_embeddings_status_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            queue_name="documents.update_embedding_status.q",
            handler=Container.resolve("update_embeddings_status_handler")
        )
    )

    Container.register_factory(
        key="delete_embeddings_consumer",
        factory=lambda: consumer.RabbitMqConsumer(
            queue_name="documents.delete_embeddings.q",
            handler=Container.resolve("delete_embeddings_handler")
        )
    )

def register_broker_dependencies():
    __register_hanlders()
    __register_consumers()