from src.broker.dependencies import connection, producers

def setup_broker_dependecies():
    connection.register_connection()
    producers.register_producers()