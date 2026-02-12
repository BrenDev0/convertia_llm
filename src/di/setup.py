from src.features.document_processing.dependencies.setup import setup_document_proccessing_dependencies
from src.features.embeddings.dependencies.setup import setup_embeddings_dependencies
from src.http.dependencies.setup import setup_http_dependencies
from src.persistence.dependencies.setup import setup_persistence_dependencies
from src.features.sessions.dependencies.setup import setup_sessions_dependencies
from src.features.communication.dependencies.setup import setup_communication_dependencies

def setup_dependencies():
    setup_document_proccessing_dependencies()
    setup_embeddings_dependencies()
    setup_http_dependencies()
    setup_persistence_dependencies()
    setup_sessions_dependencies()
    setup_communication_dependencies()