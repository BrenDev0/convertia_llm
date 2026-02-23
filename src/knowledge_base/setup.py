import logging
import asyncio
from src.di import Injector
from src.broker.infrastructure.pikaaio import connection, async_producer
from src.broker.domain.producer import DocumentsProducer, CommunicationProducer
from src.http import AsyncHttpClient, HttpxAsyncHttpClient
from src.persistence import (
    SessionRepository,
    VectorRepository,
)
from src.persistence.infrastructure import RedisSessionRepository, QdrantVectorRepository
from src.features.document_processing.domain import (
    TextChunker,
    PdfProcessor,
    ChunkTextQueueConfig,
    ChunkTextConsumer,
    ExtractTextQueueConfig,
    ExtractTextConsumer
)
from src.features.document_processing.application import (
    ExtractTextHandler,
    ChunkTextHandler
)
from src.features.document_processing.infrastructure import (
    TiktokenTextChunker,
    PypdfProcessor,
    PikaAioChunkTextConsumer,
    PikaAioExtractTextConsumer
)

from src.features.embeddings.domain import (
    EmbeddingService,
    EbedChunksQueueConfig,
    StoreEmbeddingsQueueConfig,
    UpdateEmbeddingsStatusQueueConfig,
    EmbedChunksConsumer,
    StoreEmbeddingsConsumer,
    UpdateEmbeddingsStatusConsumer
)
from src.features.embeddings.application import (
    EmbedChunksHandler,
    StoreEmbeddingsHandler,
    UpdateEmeddingStatusHandler
)

from src.features.embeddings.infrastructure import (
    OpenAIEmbeddingService,
    PikaAioEmbedChunksConsumer,
    PikaAioStoreEmbeddingsConsumer,
    PikaAioUpdateEmbeddingsStatusConsumer
)

from src.features.sessions.domain import (
    UpdateEmbeddingsSessionConsumer,
    UpdateEmbeddingsSessionQueueConfig
)
from src.features.sessions.application import UpdateEmbeddingSession
from src.features.sessions.infrastructure import PikaAioUpdateEmbeddingsSessionConsumer

logger = logging.getLogger(__name__)

def setup_dependencies(injector: Injector):
    injector.register(DocumentsProducer, async_producer.PikaAioDocumentsProducer)
    injector.register(CommunicationProducer, async_producer.PikaAioCommunicationsProducer)
    
    injector.register(SessionRepository, RedisSessionRepository)
    injector.register(VectorRepository, QdrantVectorRepository)
    
    injector.register(AsyncHttpClient, HttpxAsyncHttpClient)

    injector.register(TextChunker, TiktokenTextChunker)
    injector.register(PdfProcessor, PypdfProcessor)
    injector.register(ExtractTextHandler)
    injector.register(ChunkTextHandler)
    injector.register(ChunkTextQueueConfig)
    injector.register(ChunkTextConsumer, PikaAioChunkTextConsumer)
    injector.register(ExtractTextQueueConfig)
    injector.register(ExtractTextConsumer, PikaAioExtractTextConsumer)


    injector.register(EmbeddingService, OpenAIEmbeddingService)
    injector.register(EmbedChunksHandler)
    injector.register(StoreEmbeddingsHandler)
    injector.register(UpdateEmeddingStatusHandler)
    injector.register(EbedChunksQueueConfig)
    injector.register(EmbedChunksConsumer, PikaAioEmbedChunksConsumer)
    injector.register(StoreEmbeddingsQueueConfig)
    injector.register(StoreEmbeddingsConsumer, PikaAioStoreEmbeddingsConsumer)
    injector.register(UpdateEmbeddingsStatusQueueConfig)
    injector.register(UpdateEmbeddingsStatusConsumer, PikaAioUpdateEmbeddingsStatusConsumer)

    injector.register(UpdateEmbeddingSession)
    injector.register(UpdateEmbeddingsSessionQueueConfig)
    injector.register(UpdateEmbeddingsSessionConsumer, PikaAioUpdateEmbeddingsSessionConsumer)



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
        injector.resolve(ExtractTextConsumer),
        injector.resolve(ChunkTextConsumer),
        injector.resolve(StoreEmbeddingsConsumer),
        injector.resolve(UpdateEmbeddingsStatusConsumer),
        injector.resolve(EmbedChunksConsumer),
        injector.resolve(UpdateEmbeddingsSessionConsumer)
    ]

    for consumer in async_consumers:
        asyncio.create_task(consumer.start())

    logger.info("All consumers started")
