import json
import logging
from typing import Any, Dict, Union

import aio_pika
from pydantic import BaseModel

from src.broker.infrastructure.pikaaio.connection import get_async_connection

logger = logging.getLogger(__name__)

class RabbitMqAsyncProducer:
    def __init__(self, exchange: str):
        self._exchange_name = exchange

    async def publish(
        self,
        routing_key: str,
        event: Union[BaseModel, Dict[str, Any], str],
    ) -> None:
        connection = await get_async_connection()
        channel: aio_pika.abc.AbstractChannel = await connection.channel()

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

            exchange = await channel.declare_exchange(
                self._exchange_name,
                aio_pika.ExchangeType.TOPIC,
                durable=True,
            )

            message = aio_pika.Message(
                body=body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type=content_type,
            )

            await exchange.publish(message, routing_key=routing_key)

        except Exception:
            logger.exception(f"Error publishing to {routing_key}")
            raise

        finally:
            try:
                await channel.close()
            except Exception:
                pass
