from src.features.embeddings.dependencies import services, broker

def setup_embeddings_dependencies():
    services.register_services_dependencies()
    broker.register_broker_dependencies()