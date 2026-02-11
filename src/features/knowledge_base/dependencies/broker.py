from src.broker.infrastructure.pika import consumer, producer
from src.di.container import Container
from src.features.knowledge_base.application.handlers import store_embeddings, update_embedding_status, delete_embeddings
from src.broker.infrastructure.pikaaio import async_consumer

def __register_handlers():
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
    __register_handlers()
    __register_consumers()