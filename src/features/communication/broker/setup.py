import logging
from src.broker.infrastructure.pika.connection import create_connection
logger = logging.getLogger(__name__)


def setup_communication_queues():
    try:
        connection = create_connection()
        channel = connection.channel()

        channel.queue_declare("communication.websocket_broadcast.q")

        channel.queue_bind(
            exchange="communication",
            queue="communication.websocket_broadcast.q",
            routing_key="communication.websocket.broadcast"
        )

    except Exception as e:
        logger.error("Error setting up websocket queues")
        raise

    finally:
        channel.close()
        connection.close()