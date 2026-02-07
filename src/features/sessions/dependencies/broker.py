from src.di.container import Container
from src.features.sessions.application.handlers import update_embeddings_session
from src.broker.infrastructure.pika.consumer import RabbitMqConsumer

def __register_hanlders():
    Container.register_factory(
        key="update_embeddings_session_hanlder",
        factory=lambda: update_embeddings_session.UpdateEmbeddingSession(
            session_repository=Container.resolve("session_repository")
        )
    )


def __register_consumers():
    Container.register_factory(
        key="update_embeddings_sessions_consumer",
        factory=lambda: RabbitMqConsumer(
            queue_name="documents.embeddings_session_update.q",
            handler=Container.resolve("update_embeddings_session_hanlder")
        )
    )


def register_broker_dependencies():
    __register_hanlders()
    __register_consumers()