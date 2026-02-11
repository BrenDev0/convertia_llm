import asyncio
import json
import logging
import traceback
from aio_pika import IncomingMessage
from src.broker.infrastructure.pikaaio.connection import create_async_connection
from src.broker.domain import consumer, handlers

logger = logging.getLogger(__name__)

class RabbitMqAsyncConsumer(consumer.AsyncConsumer):
    def __init__(self, queue_name: str, handler: handlers.AsyncHandler ,worker_count: int = 1):
        self.queue_name = queue_name
        self._handler = handler
        self.__worker_count = worker_count
        self._connection = None
        self._channel = None

    async def handle(self, message: IncomingMessage):
        async with message.process():
            try: 
                payload = json.loads(message.body)
                await self._handler.handle(payload)
            except Exception as e:
                logger.exception(
                    f"Error handling payload in queue {self.queue_name}"
                )
        
    async def start(self):
        self._connection = await create_async_connection()
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=self.__worker_count)

        queue = await self._channel.get_queue(self.queue_name, ensure=False)
        await queue.consume(self.handle)

        logger.info(f"Listening on queue: {self.queue_name}")
        await asyncio.Future() 
