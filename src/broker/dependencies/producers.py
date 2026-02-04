import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.broker.domain.producer import Producer
from src.broker.infrastructure.rabbitmq.producer import RabbitMqProducer

logger = logging.getLogger(__name__)

def register_producers():
    Container.register_factory(
        key="documents_producer",
        factory=lambda: RabbitMqProducer(
            exchange="documents"
        )
    )
