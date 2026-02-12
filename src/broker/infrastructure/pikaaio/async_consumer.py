import asyncio
import json
import logging
import aio_pika
from aio_pika import IncomingMessage

from src.broker.infrastructure.pikaaio.connection import create_async_connection
from src.broker.domain import consumer, handlers

logger = logging.getLogger(__name__)


class RabbitMqAsyncConsumer(consumer.AsyncConsumer):
    def __init__(
        self,
        queue_name: str,
        handler: handlers.AsyncHandler,
        worker_count: int = 1,
    ):
        self.queue_name = queue_name
        self._handler = handler
        self.__worker_count = worker_count
        self._connection: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.RobustChannel | None = None

    async def handle(self, message: IncomingMessage):
        async with message.process():
            try:
                payload = json.loads(message.body)
                await self._handler.handle(payload)

            except Exception:
                logger.exception(
                    f"Error handling payload in queue {self.queue_name}"
                )

    async def start(self):
        while True:
            try:
                logger.info(f"Connecting async consumer: {self.queue_name}")

                self._connection = await create_async_connection()
                self._channel = await self._connection.channel()

                await self._channel.set_qos(
                    prefetch_count=self.__worker_count
                )

                # Robust queue declaration
                queue = await self._channel.declare_queue(
                    self.queue_name,
                    durable=True,
                )

                await queue.consume(self.handle)

                logger.info(
                    f"Listening on queue: {self.queue_name}"
                )

                await self._connection.closed()

            except aio_pika.exceptions.AMQPException:
                logger.warning(
                    f"Connection lost for {self.queue_name}. "
                    f"Reconnecting in 5s..."
                )
                await asyncio.sleep(5)

            except Exception:
                logger.exception(
                    f"Unexpected error in async consumer "
                    f"{self.queue_name}. Reconnecting in 5s..."
                )
                await asyncio.sleep(5)
