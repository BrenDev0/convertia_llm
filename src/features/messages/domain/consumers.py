from src.broker import QueueConfig, AsyncConsumer

class CreateMessageQueueConfig(QueueConfig):
    exchange: str = "chats"
    queue_name: str = "chats.create_message.q"
    routing_key: str = "chats.message.create"


class ChatHistoryQueueConfig(QueueConfig):
    exchange: str = "chats"
    queue_name: str = "chats.update_history.q"
    routing_key: str = "chats.history.update"


class CreateMessageConsumer(AsyncConsumer):
    pass

class ChatHistoryConsumer(AsyncConsumer):
    pass