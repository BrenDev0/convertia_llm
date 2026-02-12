from src.features.communication.dependencies import broker

def setup_communication_dependencies():
    broker.register_broker_dependencies()