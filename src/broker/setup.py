import logging
import threading
import asyncio
from src.di.container import Container
from src.broker.infrastructure.pika.connection import create_connection
from src.features.embeddings.broker import setup as embeddings_setup
from src.features.document_processing.broker import  setup as document_processesing_setup
from src.features.knowledge_base.broker import setup as knowledge_base_setup
from src.features.sessions.broker import setup as sessions_setup
from src.features.websocket.broker import setup
logger = logging.getLogger(__name__)

def __setup_exchanges():
    try:
        connection = create_connection()
        channel = connection.channel()

        channel.exchange_declare(
            exchange="documents",
            exchange_type="topic",
            durable=True
        )

        channel.exchange_declare(
            exchange="communication",
            exchange_type="topic",
            durable=True
        )

        logger.info("Exchanges setup")
    
    except Exception as e:
        logger.error(str(e))
        raise

    finally:
        channel.close()
        connection.close()

def setup_broker():
    __setup_exchanges()

    embeddings_setup.setup_embedding_queues()
    document_processesing_setup.setup_document_processing_queues()
    knowledge_base_setup.setup_knowledge_base_queues()
    sessions_setup.setup_sessions_queues()
    setup.setup_websocket_queues()

    consumers = [
        Container.resolve("chunk_text_consumer"),
        Container.resolve("store_embeddings_consumer"),
        Container.resolve("update_embeddings_sessions_consumer")
    ]

    async_consumers = [
        Container.resolve("extract_text_consumer"),
        Container.resolve("embed_chunks_consumer"),
        Container.resolve("update_embeddings_status_consumer"), 
        Container.resolve("broadcasting_consumer")
    ]

    for consumer in consumers:
        thread = threading.Thread(target=consumer.start, daemon=True)
        thread.start()

    def start_async_loop():
        async def run_async_consumers():
            tasks = [consumer.start() for consumer in async_consumers]
            await asyncio.gather(*tasks)
        asyncio.run(run_async_consumers())

    threading.Thread(target=start_async_loop, daemon=True).start()