from src.broker import QueueConfig, AsyncConsumer


class BroadcastingQueueConfig(QueueConfig):
    exchange: str = "communication"
    queue_name: str = "communication.websocket_broadcast.q"
    routing_key: str = "communication.websocket.broadcast"


class BroadcastingConsumer(AsyncConsumer):
    pass