from src.features.document_processing.dependencies.setup import setup_document_proccessing_dependencies
from src.features.embeddings.dependencies.setup import setup_embeddings_dependencies
from src.features.http.dependencies.setup import setup_http_dependencies
from src.broker.dependencies.setup import setup_broker_dependecies

def setup_dependencies():
    setup_document_proccessing_dependencies()
    setup_embeddings_dependencies()
    setup_http_dependencies()
    setup_broker_dependecies()