from src.broker import PikaAioAsyncConsumer
from ...domain import UpdateEmbeddingsSessionQueueConfig
from ...application import UpdateEmbeddingSession

class PikaAioUpdateEmbeddingsSessionConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: UpdateEmbeddingsSessionQueueConfig, 
        handler: UpdateEmbeddingSession
    ):
        super().__init__(config, handler)