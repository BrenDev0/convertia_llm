from src.features.document_processing.dependencies.setup import setup_document_proccessing_dependencies
from src.features.embeddings.dependencies.setup import setup_embeddings_dependencies
from src.features.http.dependencies.setup import setup_http_dependencies

def setup_dependencies():
    setup_document_proccessing_dependencies()
    setup_embeddings_dependencies()
    setup_http_dependencies()