from src.di.injector import Injector
from src.features.sessions.domain import consumers
from src.features.sessions.infrastructure.pikaaio.consumers import PikaAioUpdateEmbeddingsStatusConsumer
from src.features.sessions.application.handlers import update_embeddings_session


def register_broker_dependencies(injector: Injector):
    injector.register(update_embeddings_session.UpdateEmbeddingSession)
    
    injector.register(consumers.UpdateEmbeddingsSessionQueueConfig)
    injector.register(consumers.UpdateEmbeddingsSessionConsumer, PikaAioUpdateEmbeddingsStatusConsumer)


def register_api_dependencies(injector: Injector):
    pass


def register_shared_dependencies(injector: Injector):
    pass