from src.broker.dependencies import producers

def setup_broker_dependecies():
    producers.register_producers()