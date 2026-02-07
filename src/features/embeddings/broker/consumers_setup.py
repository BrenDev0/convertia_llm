import logging
import asyncio
from src.di.container import Container

logger = logging.getLogger(__name__)

def setup_embeddings_consumers():
    try:        
        async def start_async_consumers():
            embed_chunks_consumer = Container.resolve("embed_chunks_consumer")
            await asyncio.gather(
                embed_chunks_consumer.start()
            )

        asyncio.run(start_async_consumers())

        
        logger.info("embedding consumers setup")

    except Exception as e:
        logger.error("Error setting up embeddings consumers")
        raise