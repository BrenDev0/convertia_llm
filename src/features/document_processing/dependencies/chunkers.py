import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.document_processing.domain.text_chunker import TextChunker
from src.features.document_processing.infrastructure.tiktoken.text_chunker import TiktokenTextChunker

logger = logging.getLogger(__name__)

def get_text_chunker() -> TextChunker:
    try:
        instance_key = "text_chunker"
        processor = Container.resolve(instance_key)

    except DependencyNotRegistered:
        processor = TiktokenTextChunker()
        Container.register(instance_key, processor)
        logger.debug(f"{instance_key} registered")

    return processor 