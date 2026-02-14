from src.broker.infrastructure.pikaaio.async_consumer import PikaAioAsyncConsumer
from src.features.document_processing.domain.consumers import ExtractTextQueueConfig, ChunkTextQueueConfig
from src.features.document_processing.application.event_handlers import extract_text, chunk_text

class PikaAioExtractTextConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: ExtractTextQueueConfig, 
        handler: extract_text.ExtractTextHandler
    ):
        super().__init__(config, handler)


class PikaAioChunkTextConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: ChunkTextQueueConfig, 
        handler: chunk_text.ChunkTextHandler
    ):
        super().__init__(config, handler)
