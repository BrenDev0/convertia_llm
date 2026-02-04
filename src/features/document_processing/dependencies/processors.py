import logging
from src.di.container import Container
from src.features.document_processing.infrastructure.pypdf.pdf_processor import PypdfProcessor

logger = logging.getLogger(__name__)

def register_processors():
    Container.register_factory(
        key="pdf_processor",
        factory=lambda: PypdfProcessor()
    )
