from src.broker import AsyncConsumer, QueueConfig

class ExtractTextQueueConfig(QueueConfig):
    exchange:str = "documents"
    queue_name: str = "documents.extract_text.q"
    routing_key: str ="documents.incomming"


class ChunkTextQueueConfig(QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.chunk_text.q"
    routing_key: str = "documents.text.extracted"


class ExtractTextConsumer(AsyncConsumer):
    pass


class ChunkTextConsumer(AsyncConsumer):
    pass