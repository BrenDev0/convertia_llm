from src.di.container import Container
from src.broker.infrastructure.pikaaio.async_consumer import RabbitMqAsyncConsumer
from src.features.communication.application.handlers import broadcast

def __register_hanlders():
    Container.register_factory(
        key="broadcasting_handler",
        factory=lambda: broadcast.BroadcastHandler()
    )


def __register_consumers():
    Container.register_factory(
        key="broadcasting_consumer",
        factory=lambda: RabbitMqAsyncConsumer(
            queue_name="communication.websocket_broadcast.q",
            handler=Container.resolve("broadcasting_handler")
        )
    )


def register_broker_dependencies():
    __register_hanlders()
    __register_consumers()