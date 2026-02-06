import logging
import json
import asyncio
import threading
from src.broker.domain.consumer import Consumer
from src.broker.domain.handlers import AsyncHandler
from src.broker.infrastructure.rabbitmq.connection import create_connection

logger = logging.getLogger(__name__)

class RabbitMqConsumer(Consumer):
    def __init__(self, queue_name, handler):
        self._queue_name = queue_name
        self._event_handler = handler

        self._connection = None
        self._channel = None

        self._loop = None
        self._loop_thread = None
        self._loop_ready = threading.Event()

    def _start_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop_ready.set()
        self._loop.run_forever()

    def start(self):
        self._loop_thread = threading.Thread(
            target=self._start_loop,
            daemon=True
        )
        self._loop_thread.start()

        self._loop_ready.wait()

        self._connection = create_connection()
        self._channel = self._connection.channel()

        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=self.handle
        )

        logger.info(f"Listening on queue: {self._queue_name}")
        self._channel.start_consuming()

    def handle(self, ch, method, properties, body):
        try:
            payload = json.loads(body)

            if isinstance(self._event_handler, AsyncHandler):
                future = asyncio.run_coroutine_threadsafe(
                    self._event_handler.handle(payload),
                    self._loop
                )
                future.result()
            else:
                self._event_handler.handle(payload)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception:
            logger.error(
                f"Error handling task in queue ::: {self._queue_name}, ::: delivery_tag={method.delivery_tag} :::"
            )
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
