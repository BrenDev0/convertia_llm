import logging
from src.di.container import Container
from src.broker.infrastructure.pika.connection import create_connection
logger = logging.getLogger(__name__)

def setup_embedding_queues():
    try:
        connection = create_connection()
        channel = connection.channel()

        channel.queue_declare("documents.embed_chunks.q")
        channel.queue_declare("documents.store_embeddings.q")
        channel.queue_declare("documents.update_embedding_status.q")
        channel.queue_declare("documents.delete_embeddings.q")

        channel.queue_bind(
            exchange="documents",
            queue="documents.store_embeddings.q",
            routing_key="documents.text.embedded"
        )

        channel.queue_bind(
            exchange="documents",
            queue="documents.update_embedding_status.q",
            routing_key="documents.status.update"
        )

        channel.queue_bind(
            exchange="documents",
            queue="documents.delete_embeddings.q",
            routing_key="documents.embeddings.delete"
        )
        logger.info("Knowledge base queues setup")

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
        connection.close()

