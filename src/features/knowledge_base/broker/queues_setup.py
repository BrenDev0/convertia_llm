import logging
from src.broker.infrastructure.rabbitmq.connection import create_connection
logger = logging.getLogger(__name__)

def setup_knowledge_base_queues():
    try:
        connection = create_connection()
        channel = connection.channel()

        channel.queue_declare("documents.store_embeddings.q")

        channel.queue_bind(
            exchange="documents",
            queue="documents.store_embeddings.q",
            routing_key="documents.text.embedded"
        )

        logger.info("Knowledge base queues setup")

    except Exception as e:
        logger.error("Error setting up knowledge base queues")
        raise

    finally:
        channel.close()
        connection.close()