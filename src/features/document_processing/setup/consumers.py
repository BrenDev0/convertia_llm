import logging
import threading
from src.features.document_processing.dependencies.broker import (
    get_chunk_text_consumer, 
    get_extract_text_consumer,
    get_download_document_consumer
)

logger = logging.getLogger(__name__)

def setup_document_processing_consumers():
    try:
        chunk_text_consumer = get_download_document_consumer()
        thread = threading.Thread(target=chunk_text_consumer.start, daemon=True)
        thread.start()

        extract_text_consumer = get_extract_text_consumer()
        thread = threading.Thread(target=extract_text_consumer.start, daemon=True)
        thread.start()

        chunk_text_consumer = get_chunk_text_consumer()
        thread = threading.Thread(target=chunk_text_consumer.start, daemon=True)
        thread.start()

        logger.info("document processing consumers setup")

    except Exception as e:
        logger.error("Error setting up document processing consumers")
        raise