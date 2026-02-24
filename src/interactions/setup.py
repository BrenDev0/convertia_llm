import logging
import asyncio
from src.di import Injector
from src.broker import ChatsProducer, CommunicationProducer
from src.broker.infrastructure import PikaAioCommunicationsProducer, PikaAioChatsProducer, get_async_connection
from src.features.chats.domain import CreateChatConsumer, CreateChatQueConfig
from src.features.chats.application import CreateChatHandler
from src.features.chats.infrastructure import PikaaioCreateChatConsumer
from src.features.messages.domain import ChatHistoryConsumer, ChatHistoryQueueConfig, CreateMessageConsumer, CreateMessageQueueConfig
from src.features.messages.application import ChatHistoryHandler, CreateMessageHandler
from src.features.messages.infrastructure import PikaaioChatHistoryConsumer, PikaaioCreateMessageConsumer
from src.features.llm.domain import InvokeClientAgentconsumer, InvokeClientAgentQueueConfig, LlmService
from src.features.llm.application import InvokeClientAgentHandler
from src.features.llm.infrastructure import LangchainLlmService, PikaAioInvokeClientAgentConsumer
from src.persistence import (
    SessionRepository,
    VectorRepository,
)
from src.persistence.infrastructure import RedisSessionRepository, QdrantVectorRepository
from src.http import AsyncHttpClient, HttpxAsyncHttpClient

logger = logging.getLogger(__name__)

def setup_dependencies(injector: Injector):
    injector.register(ChatsProducer, PikaAioChatsProducer)
    injector.register(CommunicationProducer, PikaAioCommunicationsProducer)

    injector.register(SessionRepository, RedisSessionRepository)
    injector.register(VectorRepository, QdrantVectorRepository)
    
    injector.register(AsyncHttpClient, HttpxAsyncHttpClient)

    injector.register(CreateChatQueConfig)
    injector.register(CreateChatHandler)
    injector.register(CreateChatConsumer, PikaaioCreateChatConsumer)

    injector.register(ChatHistoryQueueConfig)
    injector.register(CreateMessageQueueConfig)
    injector.register(ChatHistoryHandler)
    injector.register(CreateMessageHandler)
    injector.register(ChatHistoryConsumer, PikaaioChatHistoryConsumer)
    injector.register(CreateMessageConsumer, PikaaioCreateMessageConsumer)

    injector.register(InvokeClientAgentQueueConfig)
    injector.register(InvokeClientAgentHandler)
    injector.register(LlmService, LangchainLlmService)
    injector.register(InvokeClientAgentconsumer, PikaAioInvokeClientAgentConsumer)



async def __setup_exchanges():
    try:
        conn = await get_async_connection()
        channel = await conn.channel()

        await channel.declare_exchange(
            name="chats",
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

    async_consumers = [
        injector.resolve(CreateChatConsumer),
        injector.resolve(ChatHistoryConsumer),
        injector.resolve(CreateMessageConsumer),
        injector.resolve(InvokeClientAgentconsumer)
    ]

    for consumer in async_consumers:
        asyncio.create_task(consumer.start())

    logger.info("All consumers started")


