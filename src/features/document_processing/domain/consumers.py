from src.broker.domain import queue_config, consumer

class ExtractTextQueueConfig(queue_config.QueueConfig):
    exchange:str = "documents"
    queue_name: str = "documents.extract_text.q"
    routing_key: str ="documents.incomming"


class ChunkTextQueueConfig(queue_config.QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.chunk_text.q"
    routing_key: str = "documents.text.extracted"


class ExtractTextConsumer(consumer.AsyncConsumer):
    pass


class ChunkTextConsumer(consumer.AsyncConsumer):
    pass