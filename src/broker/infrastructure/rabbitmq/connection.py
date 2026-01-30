import pika
import threading
import os

class RabbitMqConnection:
    _connection = None
    _lock = threading.Lock()

    @classmethod
    def get_connection(cls):
        host = os.getenv("BROKER_HOST")
        port = os.getenv("BROKER_PORT")
        user = os.getenv("BROKER_USER")
        password = os.getenv("BROKER_PASSWORD")

        if not host or not port or not user or not password:
            raise ValueError("Broker variables  not set")

        try:
            port = int(port)
        except ValueError:
            raise ValueError("'RABBITMQ_PORT' must be an integer.")

        credentials = pika.PlainCredentials(user, password)

        with cls._lock:
            params = pika.ConnectionParameters(
                host=host,
                port=port,
                virtual_host="/",
                heartbeat=60,
                credentials=credentials,
                blocked_connection_timeout=300,
            )

            cls._connection = pika.BlockingConnection(params)
            return cls._connection

    @classmethod
    def get_channel(cls):
        conn = cls.get_connection()
        return conn.channel()