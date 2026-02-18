from src.broker import PikaAioAsyncConsumer
from ...domain import BroadcastingQueueConfig
from ...application import BroadcastHandler


class PikaAioBroadcastingConsumer(PikaAioAsyncConsumer):
    def __init__(
        self,
        config: BroadcastingQueueConfig,
        handler: BroadcastHandler
    ):
        super().__init__(
            config=config,
            handler=handler
        )