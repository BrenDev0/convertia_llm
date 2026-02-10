from src.features.websocket.dependencies import broker

def setup_websocket_dependencies():
    broker.register_broker_dependencies()