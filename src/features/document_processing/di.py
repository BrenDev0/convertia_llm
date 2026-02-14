from src.di.injector import Injector
from src.features.document_processing.domain import consumers, text_chunker, pdf_processor
from src.features.document_processing.infrastructure.pikaaio.consumers import PikaAioChunkTextConsumer, PikaAioExtractTextConsumer
from src.features.document_processing.infrastructure.pypdf.pdf_processor import PypdfProcessor
from src.features.document_processing.infrastructure.tiktoken.text_chunker import TiktokenTextChunker
from src.features.document_processing.application.event_handlers import extract_text, chunk_text


def register_broker_dependencies(injector: Injector):
    injector.register(text_chunker.TextChunker, TiktokenTextChunker)
    injector.register(pdf_processor.PdfProcessor, PypdfProcessor)
    
    injector.register(extract_text.ExtractTextHandler)
    injector.register(chunk_text.ChunkTextHandler)

    injector.register(consumers.ChunkTextQueueConfig)
    injector.register(consumers.ChunkTextConsumer, PikaAioChunkTextConsumer)
    
    injector.register(consumers.ExtractTextQueueConfig)
    injector.register(consumers.ExtractTextConsumer, PikaAioExtractTextConsumer)


def register_api_dependencies(injector: Injector):
    pass


def register_shared_dependencies(injector: Injector):
    pass