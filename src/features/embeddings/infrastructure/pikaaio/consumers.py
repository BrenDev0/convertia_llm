from src.broker.infrastructure.pikaaio.async_consumer import PikaAioAsyncConsumer
from src.features.embeddings.domain.consumers import EbedChunksQueueConfig, StoreEmbeddingsQueueConfig, UpdateEmbeddingsStatusQueueConfig
from src.features.embeddings.application.event_handlers import embed_chunks, store_embeddings, update_embedding_status

class PikaAioEmbedChunksConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: EbedChunksQueueConfig, 
        handler: embed_chunks.EmbedChunksHandler
    ):
        super().__init__(config, handler)

class PikaAioStoreEmbeddingsConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: StoreEmbeddingsQueueConfig, 
        handler: store_embeddings.StoreEmbeddingsHandler
    ):
        super().__init__(config, handler)

class PikaAioUpdateEmbeddingsStatusConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: UpdateEmbeddingsStatusQueueConfig, 
        handler: update_embedding_status.UpdateEmeddingStatusHandler
    ):
        super().__init__(config, handler)
