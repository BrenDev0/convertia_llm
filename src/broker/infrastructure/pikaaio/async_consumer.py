import asyncio
import json
import logging
from typing import Dict, Any
from src.broker.infrastructure.pikaaio.connection import create_async_connection
from src.broker.domain.consumer import AsyncConsumer

logger = logging.getLogger(__name__)

class RabbitMqAsyncConsumer(AsyncConsumer):
    def __init__(self, queue_name: str, handler: AsyncConsumer):
        self.queue_name = queue_name
        self._handler = handler
        self._connection = None
        self._channel = None

    async def _on_message(self, message):
        async with message.process():
            try:
                payload: Dict[str, Any] = json.loads(message.body)
                await self._handler.handle(payload)
                logger.info(f"Processed payload from {self.queue_name}: {payload}")
            except Exception as e:
                logger.error(
                    f"Error handling payload in queue {self.queue_name}: {e}"
                )
                await message.nack(requeue=False)

    async def handle(self, payload: Dict[str, Any]):
        await self._handler.handle(payload)

    async def start(self):
        self._connection = await create_async_connection()
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=1)

        queue = await self._channel.get_queue(self.queue_name, ensure=False)
        await queue.consume(self._on_message)

        logger.info(f"Listening on queue: {self.queue_name}")
        await asyncio.Future() 
