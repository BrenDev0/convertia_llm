from src.features.document_processing.dependencies import (
    broker,
    chunkers,
    processors
)

def setup_document_proccessing_dependencies():
    chunkers.register_chunker_dependencies()
    processors.register_processors()
    broker.register_broker_depenencies()
