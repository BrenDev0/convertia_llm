from src.di import Injector
from .domain import (
    TextChunker,
    PdfProcessor,
    ChunkTextConsumer,
    ChunkTextQueueConfig,
    ExtractTextConsumer,
    ExtractTextQueueConfig
)
from .infrastructure import (
    PikaAioChunkTextConsumer, 
    PikaAioExtractTextConsumer,
    PypdfProcessor,
    TiktokenTextChunker
)

from .application import (
    ExtractTextHandler,
    ChunkTextHandler
)


def register_broker_dependencies(injector: Injector):
    injector.register(TextChunker, TiktokenTextChunker)
    injector.register(PdfProcessor, PypdfProcessor)
    
    injector.register(ExtractTextHandler)
    injector.register(ChunkTextHandler)

    injector.register(ChunkTextQueueConfig)
    injector.register(ChunkTextConsumer, PikaAioChunkTextConsumer)
    
    injector.register(ExtractTextQueueConfig)
    injector.register(ExtractTextConsumer, PikaAioExtractTextConsumer)


def register_api_dependencies(injector: Injector):
    pass


def register_shared_dependencies(injector: Injector):
    pass