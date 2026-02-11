import logging
from src.broker.infrastructure.pika.connection import create_connection
logger = logging.getLogger(__name__)

def setup_knowledge_base_queues():
    try:
        connection = create_connection()
        channel = connection.channel()

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

    except Exception:
        logger.error("Error setting up knowledge base queues")
        raise

    finally:
        channel.close()
        connection.close()