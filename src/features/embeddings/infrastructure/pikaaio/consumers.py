from src.broker import PikaAioAsyncConsumer
from ...domain import EbedChunksQueueConfig, StoreEmbeddingsQueueConfig, UpdateEmbeddingsStatusQueueConfig
from ...application import EmbedChunksHandler, StoreEmbeddingsHandler,UpdateEmeddingStatusHandler

class PikaAioEmbedChunksConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: EbedChunksQueueConfig, 
        handler: EmbedChunksHandler
    ):
        super().__init__(config, handler)

class PikaAioStoreEmbeddingsConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: StoreEmbeddingsQueueConfig, 
        handler: StoreEmbeddingsHandler
    ):
        super().__init__(config, handler)

class PikaAioUpdateEmbeddingsStatusConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: UpdateEmbeddingsStatusQueueConfig, 
        handler: UpdateEmeddingStatusHandler
    ):
        super().__init__(config, handler)