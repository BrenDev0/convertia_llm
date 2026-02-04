import logging
from src.di.container import Container
from src.broker.infrastructure.rabbitmq.connection import RabbitMqConnection

logger = logging.getLogger(__name__)

def register_connection():
    Container.register_factory(
        key="broker_connection",
        factory=lambda: RabbitMqConnection()
    )

