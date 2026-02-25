import logging
import asyncio
from src.di import Injector
from src.broker.domain import DocumentsProducer, CommunicationProducer, ChatsProducer
from src.broker.infrastructure.pikaaio import async_producer, connection
from src.http.domain import AsyncHttpClient
from src.http.infrastructure import HttpxAsyncHttpClient
from src.persistence.domain import SessionRepository, VectorRepository
from src.persistence.infrastructure import RedisSessionRepository, QdrantVectorRepository
from src.features.communication.domain import BroadcastingQueueConfig, BroadcastingConsumer
from src.features.communication.application import BroadcastHandler
from src.features.communication.infrastructure import PikaAioBroadcastingConsumer

logger = logging.getLogger(__name__)

def setup_dependencies(injector: Injector):
    injector.register(DocumentsProducer, async_producer.PikaAioDocumentsProducer)
    injector.register(CommunicationProducer, async_producer.PikaAioCommunicationsProducer)
    injector.register(ChatsProducer, async_producer.PikaAioChatsProducer)
    
    
    injector.register(AsyncHttpClient, HttpxAsyncHttpClient)

    injector.register(SessionRepository, RedisSessionRepository)
    injector.register(VectorRepository, QdrantVectorRepository)

    injector.register(BroadcastHandler)
    injector.register(BroadcastingQueueConfig)
    injector.register(BroadcastingConsumer, PikaAioBroadcastingConsumer)


async def __setup_exchanges():
    try:
        conn = await connection.get_async_connection()
        channel = await conn.channel()


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

async def setup_broker(injector: Injector):
    await __setup_exchanges()

    async_consumers =  [
        injector.resolve(BroadcastingConsumer)
    ]

    for consumer in async_consumers:
        asyncio.create_task(consumer.start())

    logger.info("All consumers started")