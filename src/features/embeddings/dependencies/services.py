import logging
import os
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.embeddings.domain.embedding_service import EmbeddingService
from src.features.embeddings.infrastructure.openai.embedding_service import OpenAIEmbeddingService

logger = logging.getLogger(__name__)

def get_embedding_service() -> EmbeddingService:
    try:
        instance_key = "embedding_service",
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Openai variables not set")
        
        service = OpenAIEmbeddingService(api_key=api_key) 
        
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service