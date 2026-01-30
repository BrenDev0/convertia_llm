import os 
import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.persistence.domain import (
    vector_repository
)
from src.persistence.infrastructure.qdrant.vector_repository import QdrantVectorRepository

logger = logging.getLogger(__name__)

def get_vector_repository() -> vector_repository.VectorRepository:
    try:
        instance_key = "vector_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        connection_url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")

        if not connection_url or not api_key:
            raise ValueError("Qdrant variables not set")

        repository = QdrantVectorRepository(
            connection_url=connection_url,
            api_key=api_key
        )

        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository
