import logging
from src.broker.infrastructure.pika.connection import create_connection
logger = logging.getLogger(__name__)

def setup_sessions_queues():
    try:
        connection = create_connection()
        channel = connection.channel()

        channel.queue_declare("documents.embeddings_session_update.q")

        channel.queue_bind(
            exchange="documents",
            queue="documents.embeddings_session_update.q",
            routing_key="documents.sessions.embeddings_update"
        )

    except Exception:
        logger.error("Error setting up sessions queues")
        raise

    finally:
        channel.close()
        connection.close()