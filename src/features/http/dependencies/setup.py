from src.features.http.dependencies import clients

def setup_http_dependencies():
    clients.register_client_dependencies()