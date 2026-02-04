import logging
import os
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.embeddings.domain.embedding_service import EmbeddingService
from src.features.embeddings.infrastructure.openai.embedding_service import OpenAIEmbeddingService

logger = logging.getLogger(__name__)

def register_services_dependencies():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Openai variables not set")
    
    Container.register_factory(
        key="embedding_service",
        factory=lambda: OpenAIEmbeddingService(api_key=api_key) 
    )
