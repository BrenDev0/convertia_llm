from src.di.container import Container
from src.features.knowledge_base.application.handlers import store_embeddings, update_embedding_status
from src.broker.infrastructure.rabbitmq.consumer import RabbitMqConsumer

def __register_handlers():
    Container.register_factory(
        key="store_embeddings_handler",
        factory=lambda: store_embeddings.StoreEmbeddingsHandler(
            vector_repository=Container.resolve("vector_repository"),
            producer=Container.resolve("documents_producer")
        )
    )

    Container.register_factory(
        key="update_embeddings_status",
        factory=lambda: update_embedding_status.UpdateEmeddingStatus(
            async_http_client=Container.resolve("async_http_client")
        )
    )


def __register_consumers():
    Container.register_factory(
        key="store_embeddings_consumer",
        factory=lambda: RabbitMqConsumer(
            queue_name="documents.store_embeddings.q",
            handler=Container.resolve("store_embeddings_handler")
        )
    )

    Container.register_factory(
        key="update_embeddings_status_consumer",
        factory=lambda: RabbitMqConsumer(
            queue_name="documents.update_embedding_status.q",
            handler=Container.resolve("update_embeddings_status")
        )
    )


def register_broker_dependencies():
    __register_handlers
    __register_consumers