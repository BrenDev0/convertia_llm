from src.broker.domain import consumer, queue_config


class BroadcastingQueueConfig(queue_config.QueueConfig):
    exchange: str = "communication"
    queue_name: str = "communication.websocket_broadcast.q"
    routing_key: str = "communication.websocket.broadcast"


class BroadcastingConsumer(consumer.AsyncConsumer):
    pass