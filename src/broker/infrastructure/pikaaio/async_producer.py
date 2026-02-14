import json
import logging
from typing import Any, Dict, Union

import aio_pika
from pydantic import BaseModel

from src.broker.infrastructure.pikaaio.connection import get_async_connection

logger = logging.getLogger(__name__)


class PikaAioAsyncProducer:
    def __init__(self, exchange: str):
        self._exchange_name = exchange
        self._channel: aio_pika.RobustChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None

    async def _ensure_channel(self):
        if self._channel is None or self._channel.is_closed:
            connection = await get_async_connection()

            self._channel = await connection.channel()

            self._exchange = await self._channel.declare_exchange(
                self._exchange_name,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )

    async def publish(
        self,
        routing_key: str,
        event: Union[BaseModel, Dict[str, Any], str],
    ) -> None:
        await self._ensure_channel()

        try:
            if isinstance(event, BaseModel):
                body = event.model_dump_json().encode()
                content_type = "application/json"
            elif isinstance(event, dict):
                body = json.dumps(event).encode()
                content_type = "application/json"
            else:
                body = str(event).encode()
                content_type = "text/plain"

            message = aio_pika.Message(
                body=body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type=content_type,
            )

            await self._exchange.publish(message, routing_key=routing_key)

        except Exception:
            logger.exception(f"Error publishing to {routing_key}")
            raise


class PikaAioDocumentsProducer(PikaAioAsyncProducer):
    def __init__(self):
        super().__init__(exchange="documents")

class PikaAioCommunicationsProducer(PikaAioAsyncProducer):
    def __init__(self):
        super().__init__(exchange="communication")
