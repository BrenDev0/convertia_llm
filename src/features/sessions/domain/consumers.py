from src.broker.domain import queue_config, consumer

class UpdateEmbeddingsSessionQueueConfig(queue_config.QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.embeddings_session_update.q"
    routing_key: str = "documents.sessions.embeddings_update"

class UpdateEmbeddingsSessionConsumer(consumer.AsyncConsumer):
    pass