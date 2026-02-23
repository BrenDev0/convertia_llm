from src.broker import PikaAioAsyncConsumer
from ...domain import CreateChatQueConfig
from ...application import CreateChatHandler

class PikaaioCreateChatConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: CreateChatQueConfig, 
        handler: CreateChatHandler
    ):
        super().__init__(config, handler)