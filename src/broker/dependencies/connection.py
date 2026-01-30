import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.broker.infrastructure.rabbitmq.connection import RabbitMqConnection

logger = logging.getLogger(__name__)

def get_broker_connection():
    try:
        instance_key = "broker_connection"
        connection = Container.resolve(instance_key)

    except DependencyNotRegistered:
        connection = RabbitMqConnection()

        Container.register(instance_key, connection)

        logger.debug(f"{instance_key} registered")

    return connection