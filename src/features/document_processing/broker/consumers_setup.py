import logging
import threading
from src.di.container import Container


logger = logging.getLogger(__name__)

def setup_document_processing_consumers():
    try:
        chunk_text_consumer = Container.resolve("download_document_consumer")
        thread = threading.Thread(target=chunk_text_consumer.start, daemon=True)
        thread.start()

        extract_text_consumer = Container.resolve("extract_text_consumer")
        thread = threading.Thread(target=extract_text_consumer.start, daemon=True)
        thread.start()

        chunk_text_consumer = Container.resolve("chunk_text_consumer")
        thread = threading.Thread(target=chunk_text_consumer.start, daemon=True)
        thread.start()

        logger.info("document processing consumers setup")

    except Exception as e:
        logger.error("Error setting up document processing consumers")
        raise