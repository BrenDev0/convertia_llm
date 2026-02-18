from src.di import Injector
from .domain import UpdateEmbeddingsSessionQueueConfig, UpdateEmbeddingsSessionConsumer
from .infrastructure import PikaAioUpdateEmbeddingsStatusConsumer
from .application import UpdateEmbeddingSession


def register_broker_dependencies(injector: Injector):
    injector.register(UpdateEmbeddingSession)
    
    injector.register(UpdateEmbeddingsSessionQueueConfig)
    injector.register(UpdateEmbeddingsSessionConsumer, PikaAioUpdateEmbeddingsStatusConsumer)


def register_api_dependencies(injector: Injector):
    pass


def register_shared_dependencies(injector: Injector):
    pass