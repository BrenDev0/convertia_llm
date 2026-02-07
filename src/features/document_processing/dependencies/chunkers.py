import logging
from src.di.container import Container
from src.features.document_processing.infrastructure.tiktoken.text_chunker import TiktokenTextChunker

logger = logging.getLogger(__name__)

def register_chunker_dependencies():
    Container.register_factory(
        key="text_chunker",
        factory=lambda: TiktokenTextChunker()
    )
