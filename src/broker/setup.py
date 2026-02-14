import logging
import asyncio
from src.di.injector import Injector
from src.broker.infrastructure.pikaaio import connection, async_producer
from src.broker.domain.producer import DocumentsProducer, CommunicationProducer
from src.http.di import register_shared_dependencies as http_dependencies
from src.persistence.di import register_shared_dependencies as persistance_dependencies
from src.features.communication.di import (
    register_broker_dependencies as communication_dependencies, 
    register_shared_dependencies as commincation_shared_dependencies
)
from src.features.document_processing.domain import consumers as documents_consumers
from src.features.document_processing.di import (
    register_broker_dependencies as documents_dependencies,
    register_shared_dependencies as documents_shared_dependencies
)
from src.features.embeddings.domain import consumers as embeddings_consumers
from src.features.embeddings.di import (
    register_broker_dependencies as embeddings_dependencies,
    register_shared_dependencies as embeddings_shared_dependencies
)
from src.features.sessions.domain import consumers as sessions_consumers
from src.features.sessions.di import (
    register_broker_dependencies as session_dependencies,
    register_shared_dependencies as session_shared_dependencies
)

logger = logging.getLogger(__name__)

def setup_dependencies(injector: Injector):
    injector.register(DocumentsProducer, async_producer.PikaAioDocumentsProducer)
    injector.register(CommunicationProducer, async_producer.PikaAioCommunicationsProducer)
    
    persistance_dependencies(injector=injector)
    http_dependencies(injector=injector)

    communication_dependencies(injector=injector)
    commincation_shared_dependencies(injector=injector)

    documents_dependencies(injector=injector)
    documents_shared_dependencies(injector=injector)

    embeddings_dependencies(injector=injector)
    embeddings_shared_dependencies(injector=injector)

    session_dependencies(injector=injector)
    session_shared_dependencies(injector=injector)



async def __setup_exchanges():
    try:
        conn = await connection.get_async_connection()
        channel = await conn.channel()

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

async def setup_broker(injector: Injector):
    await __setup_exchanges()

    async_consumers = [
        injector.resolve(documents_consumers.ExtractTextConsumer),
        injector.resolve(documents_consumers.ChunkTextConsumer),
        injector.resolve(embeddings_consumers.StoreEmbeddingsConsumer),
        injector.resolve(embeddings_consumers.UpdateEmbeddingsStatusConsumer),
        injector.resolve(embeddings_consumers.EmbedChunksConsumer),
        injector.resolve(sessions_consumers.UpdateEmbeddingsSessionConsumer)
    ]

    for consumer in async_consumers:
        asyncio.create_task(consumer.start())

    logger.info("All consumers started")
