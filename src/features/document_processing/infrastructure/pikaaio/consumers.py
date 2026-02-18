from src.broker import PikaAioAsyncConsumer
from ...domain import ExtractTextQueueConfig, ChunkTextQueueConfig
from ...application import ExtractTextHandler, ChunkTextHandler

class PikaAioExtractTextConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: ExtractTextQueueConfig, 
        handler: ExtractTextHandler
    ):
        super().__init__(config, handler)


class PikaAioChunkTextConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: ChunkTextQueueConfig, 
        handler: ChunkTextHandler
    ):
        super().__init__(config, handler)
