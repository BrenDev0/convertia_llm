import logging
import os
from src.di.container import Container
from src.broker.infrastructure.pikaaio import async_consumer, async_producer
from src.features.embeddings.application.event_handlers import embed_chunks, store_embeddings, delete_embeddings, update_embedding_status

logger = logging.getLogger(__name__)

def __register_hanlders():
    Container.register_factory(
        key="embed_chunks_handler",
        factory=lambda: embed_chunks.EmbedChunksHandler(
            embedding_serivce=Container.resolve("embedding_service"),
            producer=async_producer.RabbitMqAsyncProducer(exchange="documents"),
            session_repository=Container.resolve("session_repository")
        )
    )

    Container.register_factory(
        key="store_embeddings_handler",
        factory=lambda: store_embeddings.StoreEmbeddingsHandler(
            vector_repository=Container.resolve("vector_repository"),
            producer=async_producer.RabbitMqAsyncProducer(exchange="documents"),
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
            documents_producer=async_producer.RabbitMqAsyncProducer("documents"),
            communication_producer=async_producer.RabbitMqAsyncProducer(exchange="communication")
        )
    )

def __register_consumers():
    Container.register_factory(
        key="embed_chunks_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            exchange="documents",
            queue_name="documents.embed_chunks.q",
            routing_key="document.text.chunked",
            handler=Container.resolve("embed_chunks_handler")
        )
    )

    Container.register_factory(
        key="store_embeddings_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            exchange="documents",
            queue_name="documents.store_embeddings.q",
            routing_key="documents.text.embedded",
            handler=Container.resolve("store_embeddings_handler")
        )
    )

    Container.register_factory(
        key="update_embeddings_status_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            exchange="documents",
            queue_name="documents.update_embedding_status.q",
            routing_key="documents.status.update",
            handler=Container.resolve("update_embeddings_status_handler")
        )
    )

    Container.register_factory(
        key="delete_embeddings_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            exchange="documents",
            queue_name="documents.delete_embeddings.q",
            routing_key="documents.embeddings.delete",
            handler=Container.resolve("delete_embeddings_handler")
        )
    )

def register_broker_dependencies():
    __register_hanlders()
    __register_consumers()