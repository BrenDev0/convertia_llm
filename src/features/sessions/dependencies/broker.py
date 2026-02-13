from src.di.container import Container
from src.features.sessions.application.handlers import update_embeddings_session
from src.broker.infrastructure.pikaaio import async_consumer, async_producer

def __register_hanlders():
    Container.register_factory(
        key="update_embeddings_session_hanlder",
        factory=lambda: update_embeddings_session.UpdateEmbeddingSession(
            session_repository=Container.resolve("session_repository"),
            producer=async_producer.RabbitMqAsyncProducer(exchange="communication")
        )
    )


def __register_consumers():
    Container.register_factory(
        key="update_embeddings_sessions_consumer",
        factory=lambda: async_consumer.RabbitMqAsyncConsumer(
            exchange="documents",
            queue_name="documents.embeddings_session_update.q",
            routing_key="documents.sessions.embeddings_update",
            handler=Container.resolve("update_embeddings_session_hanlder")
        )
    )


def register_broker_dependencies():
    __register_hanlders()
    __register_consumers()