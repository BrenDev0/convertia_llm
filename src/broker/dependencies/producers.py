import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.broker.domain.producer import Producer
from src.broker.infrastructure.rabbitmq.producer import RabbitMqProducer

logger = logging.getLogger(__name__)

def get_documents_producer() -> Producer:
    try:
        instance_key = "documents_producer"
        producer = Container.resolve(instance_key)

    except DependencyNotRegistered:
        producer = RabbitMqProducer(
            exchange="documents"
        )

        Container.register(instance_key, producer)

        logger.debug(f"{instance_key} registered")

    return producer