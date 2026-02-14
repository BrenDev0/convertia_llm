import asyncio
import inspect
import json
import logging
import aio_pika
from typing import Union
from src.broker.infrastructure.pikaaio.connection import get_async_connection
from src.broker.domain import consumer, handlers, queue_config

logger = logging.getLogger(__name__)


class PikaAioAsyncConsumer(consumer.AsyncConsumer):
    def __init__(
        self, 
        config: queue_config.QueueConfig,
        handler: handlers.AsyncHandler
    ):
        self.exchange = config.exchange
        self.queue_name = config.queue_name
        self.routing_key = config.routing_key
        self._handler = handler
        self._stop_event = asyncio.Event()

    async def handle(self, message: aio_pika.IncomingMessage):
        async with message.process():
            payload = json.loads(message.body)
            
            await self._handler.handle(payload)
            

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

        await self._stop_event.wait()