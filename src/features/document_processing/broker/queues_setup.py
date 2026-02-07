import logging
from src.broker.infrastructure.pika.connection import create_connection
logger = logging.getLogger(__name__)


def setup_document_processing_queues():
    try:

        connection = create_connection()
        channel = connection.channel()

        channel.queue_declare("documents.extract_text.q")
        channel.queue_declare("documents.chunk_text.q")

    
        channel.queue_bind(
            exchange="documents",
            queue="documents.extract_text.q",
            routing_key="documents.incomming"
        )

        channel.queue_bind(
            exchange="documents",
            queue="documents.chunk_text.q",
            routing_key="documents.text.extracted"
        )

        logger.info("document processing queues setup")

    except Exception:
        logger.error("Error setting up document processing queues")
        raise
    
    finally:
        channel.close()
        connection.close()