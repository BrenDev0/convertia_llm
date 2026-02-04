import os 
import logging
from src.di.container import Container
from src.persistence.infrastructure.qdrant.vector_repository import QdrantVectorRepository

logger = logging.getLogger(__name__)

def register_repositories():
    connection_url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not connection_url or not api_key:
        raise ValueError("Qdrant variables not set")
    
    Container.register_factory(
        key="vector_repository",
        factory=lambda: QdrantVectorRepository(
            connection_url=connection_url,
            api_key=api_key
        )
    )
