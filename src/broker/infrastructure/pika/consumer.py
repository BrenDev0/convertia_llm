import logging
import json
from src.broker.domain.consumer import Consumer
from src.broker.infrastructure.pika.connection import create_connection

logger = logging.getLogger(__name__)

class RabbitMqConsumer(Consumer):
    def __init__(self, queue_name, handler):
        self._queue_name = queue_name
        self._handler = handler

    def start(self):
        connection = create_connection()
        channel = connection.channel()

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=self.handle
        )

        logger.info(f"Listening on queue: {self._queue_name}")
        channel.start_consuming()

    def handle(self, ch, method, properties, body):
        try:
            payload = json.loads(body)
            self._handler.handle(payload)
            ch.basic_ack(method.delivery_tag)

        except Exception:
            logger.exception(
                    f"Error handling payload in queue {self._queue_name}"
                )
            ch.basic_nack(method.delivery_tag, requeue=False)

