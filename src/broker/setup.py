import logging
import asyncio
from src.di.container import Container
from src.broker.infrastructure.pikaaio.connection import get_async_connection
logger = logging.getLogger(__name__)

async def __setup_exchanges():
    try:
        connection = await get_async_connection()
        channel = await connection.channel()

        await channel.declare_exchange(
            name="documents",
            type="topic",
            durable=True
        )
       
        await channel.declare_exchange(
            name="communication",
            type="topic",
            durable=True
        )

        logger.info("Exchanges setup")
    
    except Exception as e:
        logger.error(str(e))
        raise

    finally:
        await channel.close()

async def setup_broker():
    await __setup_exchanges()

    async_consumers = [
        Container.resolve("chunk_text_consumer"),
        Container.resolve("store_embeddings_consumer"),
        Container.resolve("update_embeddings_sessions_consumer"),
        Container.resolve("delete_embeddings_consumer"),
        Container.resolve("extract_text_consumer"),
        Container.resolve("embed_chunks_consumer"),
        Container.resolve("update_embeddings_status_consumer"),
        Container.resolve("broadcasting_consumer"),
    ]

    for consumer in async_consumers:
        asyncio.create_task(consumer.start())

    logger.info("All consumers started")
