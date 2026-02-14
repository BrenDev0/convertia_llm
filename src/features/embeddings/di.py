from src.di.injector import Injector
from src.features.embeddings.domain import embedding_service, consumers
from src.features.embeddings.application.event_handlers import (
    embed_chunks,
    store_embeddings,
    update_embedding_status
)
from src.features.embeddings.infrastructure.openai.embedding_service import OpenAIEmbeddingService
from src.features.embeddings.infrastructure.pikaaio.consumers import (
    PikaAioEmbedChunksConsumer,
    PikaAioStoreEmbeddingsConsumer,
    PikaAioUpdateEmbeddingsStatusConsumer
)



def register_broker_dependencies(injector: Injector):
    injector.register(embedding_service.EmbeddingService, OpenAIEmbeddingService)
    
    injector.register(embed_chunks.EmbedChunksHandler)
    injector.register(store_embeddings.StoreEmbeddingsHandler)
    injector.register(update_embedding_status.UpdateEmeddingStatusHandler)
    
    injector.register(consumers.EbedChunksQueueConfig)
    injector.register(consumers.EmbedChunksConsumer, PikaAioEmbedChunksConsumer)
    
    injector.register(consumers.StoreEmbeddingsQueueConfig)
    injector.register(consumers.StoreEmbeddingsConsumer, PikaAioStoreEmbeddingsConsumer)
    
    injector.register(consumers.UpdateEmbeddingsStatusQueueConfig)
    injector.register(consumers.UpdateEmbeddingsStatusConsumer, PikaAioUpdateEmbeddingsStatusConsumer)


def register_api_dependencies(injector: Injector):
    pass


def register_shared_dependencies(injector: Injector):
    pass