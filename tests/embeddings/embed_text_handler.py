import pytest 
from unittest.mock import Mock
from src.features.embeddings.application.event_handlers.embed_chunks import EmbedChunksHandler

@pytest.fixure
def embedding_service():
    return Mock()

@pytest.fixture
def document_producer():
    return Mock()

@pytest.fixture
def handler(
    embedding_service,
    document_producer
):
    return EmbedChunksHandler(
        embedding_serivce=embedding_service,
        producer=document_producer
    )

def test_success(
    embedding_service,
    document_producer,
    handler
):
    pass
