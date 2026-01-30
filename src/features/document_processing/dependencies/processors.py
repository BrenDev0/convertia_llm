import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.document_processing.domain.pdf_processor import PdfProcessor
from src.features.document_processing.infrastructure.pypdf.pdf_processor import PypdfProcessor

logger = logging.getLogger(__name__)

def get_pdf_processor() -> PdfProcessor:
    try:
        instance_key = "pdf_processor"
        processor = Container.resolve(instance_key)

    except DependencyNotRegistered:
        processor = PypdfProcessor()
        Container.register(instance_key, processor)
        logger.debug(f"{instance_key} registered")

    return processor