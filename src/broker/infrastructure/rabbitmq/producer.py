import json 
from pydantic import BaseModel
from typing import Dict, Any, Union
import pika
import logging

from src.broker.infrastructure.rabbitmq.connection import create_connection

logger = logging.getLogger(__name__)

class RabbitMqProducer:
    def __init__(self, exchange: str):
        self.__exchange = exchange
        self.__connection = create_connection()
        self.__channel = self.__connection.channel()

    def publish(
        self,
        routing_key: str,
        event: Union[BaseModel, Dict[str, Any], str],
    ): 
        try:
            if isinstance(event, BaseModel):
                body = event.model_dump_json()
            elif isinstance(event, dict):  
                body = json.dumps(event)
            else:
                body = str(event)
            
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            )
        except Exception as e:
            logger.error(str(e))
            raise