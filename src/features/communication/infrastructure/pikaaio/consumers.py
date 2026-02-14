from src.broker.infrastructure.pikaaio.async_consumer import PikaAioAsyncConsumer
from src.features.communication.domain.consumers import BroadcastingQueueConfig
from src.features.communication.application.handlers import broadcast


class PikaAioBroadcastingConsumer(PikaAioAsyncConsumer):
    def __init__(
        self,
        config: BroadcastingQueueConfig,
        handler: broadcast.BroadcastHandler
    ):
        super().__init__(
            config=config,
            handler=handler
        )