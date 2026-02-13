import asyncio
import inspect
import json
import logging
import aio_pika
from typing import Union
from src.broker.infrastructure.pikaaio.connection import get_async_connection
from src.broker.domain import consumer, handlers

logger = logging.getLogger(__name__)


class RabbitMqAsyncConsumer(consumer.AsyncConsumer):
    def __init__(
        self, 
        exchange: str, 
        queue_name: str, 
        routing_key: str, 
        handler: Union[handlers.AsyncHandler, handlers.Handler]
    ):
        self.exchange = exchange
        self.queue_name = queue_name
        self.routing_key = routing_key
        self._handler = handler

    async def handle(self, message: aio_pika.IncomingMessage):
        async with message.process():
            payload = json.loads(message.body)

            if inspect.iscoroutinefunction(self._handler.handle):
                await self._handler.handle(payload)
            else:
                await asyncio.to_thread(self._handler.handle, payload)

    async def start(self):
        connection = await get_async_connection()
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=1)

        exchange = await channel.declare_exchange(
            self.exchange,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        queue = await channel.declare_queue(
            self.queue_name,
            durable=True,
        )

        await queue.bind(exchange, routing_key=self.routing_key)
        await queue.consume(self.handle)

        logger.info(f"Listening on queue: {self.queue_name}")

        await asyncio.Future()
