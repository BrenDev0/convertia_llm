from src.broker import PikaAioAsyncConsumer
from ...domain import CreateMessageQueueConfig, ChatHistoryQueueConfig
from ...application import CreateMessageHandler, ChatHistoryHandler

class PikaaioCreateMessageConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: CreateMessageQueueConfig, 
        handler: CreateMessageHandler
    ):
        super().__init__(config, handler)

class PikaaioChatHistoryConsumer(PikaAioAsyncConsumer):
    def __init__(
        self, 
        config: ChatHistoryQueueConfig, 
        handler: ChatHistoryHandler
    ):
        super().__init__(config, handler)