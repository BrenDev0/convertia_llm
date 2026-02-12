import logging
import json
import time
import pika

from src.broker.domain.consumer import Consumer
from src.broker.infrastructure.pika.connection import create_connection

logger = logging.getLogger(__name__)


class RabbitMqConsumer(Consumer):
    def __init__(self, queue_name, handler, worker_count: int = 1):
        self._queue_name = queue_name
        self._handler = handler
        self.__worker_count = worker_count
        self.__connection = None
        self.__channel = None
        self.__should_reconnect = True

    def start(self):
        while self.__should_reconnect:
            try:
                self.__connect()
                self.__consume()

            except pika.exceptions.AMQPConnectionError as e:
                logger.warning(
                    f"RabbitMQ connection lost for queue "
                    f"{self._queue_name}. Reconnecting in 5s..."
                )
                self.__cleanup()
                time.sleep(5)

            except Exception:
                logger.exception(
                    f"Unexpected error in consumer "
                    f"{self._queue_name}. Reconnecting in 5s..."
                )
                self.__cleanup()
                time.sleep(5)


    def __connect(self):
        logger.info(f"Connecting consumer to queue: {self._queue_name}")
        self.__connection = create_connection()
        self.__channel = self.__connection.channel()

        self.__channel.basic_qos(prefetch_count=self.__worker_count)
        self.__channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=self.handle,
        )

    def __consume(self):
        logger.info(f"Listening on queue: {self._queue_name}")
        self.__channel.start_consuming()

    def __cleanup(self):
        try:
            if self.__channel and self.__channel.is_open:
                self.__channel.close()
        except Exception:
            pass

        try:
            if self.__connection and self.__connection.is_open:
                self.__connection.close()
        except Exception:
            pass

        self.__channel = None
        self.__connection = None

    def handle(self, ch, method, properties, body):
        try:
            payload = json.loads(body)

            self._handler.handle(payload)

            ch.basic_ack(method.delivery_tag)

        except Exception:
            logger.exception(
                f"Error handling payload in queue "
                f"{self._queue_name}"
            )
            ch.basic_nack(method.delivery_tag, requeue=False)