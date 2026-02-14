from src.broker.infrastructure.pikaaio.async_consumer import PikaAioAsyncConsumer
from src.features.sessions.domain.consumers import UpdateEmbeddingsSessionQueueConfig
from src.features.sessions.application.handlers import update_embeddings_session

class PikaAioUpdateEmbeddingsStatusConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: UpdateEmbeddingsSessionQueueConfig, 
        handler: update_embeddings_session.UpdateEmbeddingSession
    ):
        super().__init__(config, handler)