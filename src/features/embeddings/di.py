from src.di import Injector
from .domain import (
    EmbeddingService,
    EmbedChunksConsumer,
    StoreEmbeddingsQueueConfig,
    StoreEmbeddingsConsumer,
    UpdateEmbeddingsStatusConsumer,
    UpdateEmbeddingsStatusQueueConfig,
    EbedChunksQueueConfig
)
from .application import (
    EmbedChunksHandler,
    StoreEmbeddingsHandler,
    UpdateEmeddingStatusHandler
)

from .infrastructure import (
    PikaAioEmbedChunksConsumer,
    PikaAioStoreEmbeddingsConsumer,
    PikaAioUpdateEmbeddingsStatusConsumer,
    OpenAIEmbeddingService
)



def register_broker_dependencies(injector: Injector):
    injector.register(EmbeddingService, OpenAIEmbeddingService)
    
    injector.register(EmbedChunksHandler)
    injector.register(StoreEmbeddingsHandler)
    injector.register(UpdateEmeddingStatusHandler)
    
    injector.register(EbedChunksQueueConfig)
    injector.register(EmbedChunksConsumer, PikaAioEmbedChunksConsumer)
    
    injector.register(StoreEmbeddingsQueueConfig)
    injector.register(StoreEmbeddingsConsumer, PikaAioStoreEmbeddingsConsumer)
    
    injector.register(UpdateEmbeddingsStatusQueueConfig)
    injector.register(UpdateEmbeddingsStatusConsumer, PikaAioUpdateEmbeddingsStatusConsumer)


def register_api_dependencies(injector: Injector):
    pass


def register_shared_dependencies(injector: Injector):
    pass