from pydantic import BaseModel
from src.broker import AsyncConsumer, QueueConfig


class InvokeClientAgentQueueConfig(QueueConfig):
    exchange: str = "chats"
    queue_name: str = "chats.invoke_client_llm.q"
    routing_key: str = "chats.llm.client.invoke"


class InvokeClientAgentconsumer(AsyncConsumer):
    pass