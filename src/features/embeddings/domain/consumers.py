from src.broker.domain import consumer, queue_config

class EbedChunksQueueConfig(queue_config.QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.embed_chunks.q"
    routing_key: str = "document.text.chunked"


class StoreEmbeddingsQueueConfig(queue_config.QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.store_embeddings.q"
    routing_key: str = "documents.text.embedded"


class UpdateEmbeddingsStatusQueueConfig(queue_config.QueueConfig):
    exchange: str ="documents"
    queue_name: str ="documents.update_embedding_status.q"
    routing_key: str ="documents.status.update"


class EmbedChunksConsumer(consumer.AsyncConsumer):
    pass

class StoreEmbeddingsConsumer(consumer.AsyncConsumer):
    pass

class UpdateEmbeddingsStatusConsumer(consumer.AsyncConsumer):
    pass

