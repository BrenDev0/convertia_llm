from src.broker import QueueConfig, AsyncConsumer

class UpdateEmbeddingsSessionQueueConfig(QueueConfig):
    exchange: str = "documents"
    queue_name: str = "documents.embeddings_session_update.q"
    routing_key: str = "documents.sessions.embeddings_update"

class UpdateEmbeddingsSessionConsumer(AsyncConsumer):
    pass