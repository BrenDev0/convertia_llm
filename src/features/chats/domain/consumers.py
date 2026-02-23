from src.broker.domain import AsyncConsumer, QueueConfig

class CreateChatQueConfig(QueueConfig):
    exchange: str = "chats"
    queue_name: str = "chats.create_chat.q"
    routing_key: str = "chats.chat.create"


class CreateChatConsumer(AsyncConsumer):
    pass
