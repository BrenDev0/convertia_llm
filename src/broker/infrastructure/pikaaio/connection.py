import os
import aio_pika


_async_connection: aio_pika.RobustConnection = None

async def get_async_connection() -> aio_pika.RobustConnection:
    global _async_connection

    if _async_connection is None or _async_connection.is_closed:
        host = os.getenv("BROKER_HOST")
        port = os.getenv("BROKER_PORT")
        user = os.getenv("BROKER_USER")
        password = os.getenv("BROKER_PASSWORD")

        if not host or not port or not user or not password:
            raise ValueError("Broker environment variables not set")

        try:
            port = int(port)

        except ValueError:
            raise ValueError("'BROKER_PORT' must be an integer.")

        url = f"amqp://{user}:{password}@{host}:{port}/"
        
        _async_connection = await aio_pika.connect_robust(
            url,
            heartbeat=60,
            timeout=15, 
        )
    return _async_connection