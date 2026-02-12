import json
import logging
from typing import Dict, Any, Union
import pika
from pydantic import BaseModel

from src.broker.infrastructure.pika.connection import create_connection

logger = logging.getLogger(__name__)


class RabbitMqProducer:
    def __init__(self, exchange: str):
        self.__exchange = exchange
        self.__connection: pika.BlockingConnection | None = None

    def __connect(self) -> None:
        logger.info("Creating new RabbitMQ connection...")
        self.__connection = create_connection()

    def __ensure_connection(self) -> None:
        if self.__connection is None or self.__connection.is_closed:
            logger.warning("RabbitMQ connection missing or closed. Reconnecting...")
            self.__connect()

    def __reset_connection(self) -> None:
        if self.__connection:
            try:
                self.__connection.close()
            except Exception:
                pass
        self.__connection = None

    def publish(
        self,
        routing_key: str,
        event: Union[BaseModel, Dict[str, Any], str],
    ) -> None:
        channel = None

        try:
            self.__ensure_connection()

            if isinstance(event, BaseModel):
                body = event.model_dump_json()
            elif isinstance(event, dict):
                body = json.dumps(event)
            else:
                body = str(event)

            channel = self.__connection.channel()

            channel.basic_publish(
                exchange=self.__exchange,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2, 
                    content_type="application/json",
                ),
                mandatory=True,
            )

        except pika.exceptions.AMQPError as e:
            logger.error(
                f"AMQP error publishing to '{routing_key}': {e}"
            )

            self.__reset_connection()
            raise

        except Exception as e:
            logger.exception(
                f"Unexpected error publishing to '{routing_key}'"
            )

            self.__reset_connection()
            raise

        finally:
            if channel and channel.is_open:
                try:
                    channel.close()
                except Exception:
                    logger.debug("Channel already closed or failed to close.")
