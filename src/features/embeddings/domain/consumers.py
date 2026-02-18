from src.broker import QueueConfig, AsyncConsumer

class EbedChunksQueueConfig(QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.embed_chunks.q"
    routing_key: str = "document.text.chunked"


class StoreEmbeddingsQueueConfig(QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.store_embeddings.q"
    routing_key: str = "documents.text.embedded"


class UpdateEmbeddingsStatusQueueConfig(QueueConfig):
    exchange: str ="documents"
    queue_name: str ="documents.update_embedding_status.q"
    routing_key: str ="documents.status.update"


class EmbedChunksConsumer(AsyncConsumer):
    pass

class StoreEmbeddingsConsumer(AsyncConsumer):
    pass

class UpdateEmbeddingsStatusConsumer(AsyncConsumer):
    pass

