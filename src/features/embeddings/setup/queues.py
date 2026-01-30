import logging
from src.broker.dependencies.connection import get_broker_connection
logger = logging.getLogger(__name__)

def setup_embedding_queues():
    try:
        connection = get_broker_connection()
        channel = connection.get_channel()

        channel.queue_declare("documents.embed_chunks.q")

        channel.queue_bind(
                exchange="documents",
                queue="documents.embed_chunks.q",
                routing_key="document.text.chunked"
            )
        
        logger.info("embedding queues setup")
    
    except Exception as e:
        logger.error("Error setting up embedding queues")
        raise

    finally:
        channel.close()

