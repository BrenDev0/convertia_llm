import pika
import os

def create_connection() -> pika.BlockingConnection:
    host = os.getenv("BROKER_HOST")
    port = os.getenv("BROKER_PORT")
    user = os.getenv("BROKER_USER")
    password = os.getenv("BROKER_PASSWORD")

    if not host or not port or not user or not password:
        raise ValueError("Broker variables not set")

    try:
        port = int(port)
    except ValueError:
        raise ValueError("'BROKER_PORT' must be an integer.")

    credentials = pika.PlainCredentials(user, password)

    params = pika.ConnectionParameters(
        host=host,
        port=port,
        virtual_host="/",
        credentials=credentials,
        heartbeat=60,
        blocked_connection_timeout=15,
        connection_attempts=3,
        retry_delay=5,
    )

    return pika.BlockingConnection(params)
