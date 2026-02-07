import logging
import threading
import asyncio
from src.di.container import Container


logger = logging.getLogger(__name__)

def setup_document_processing_consumers():
    try:
        chunk_text_consumer = Container.resolve("chunk_text_consumer")
        threading.Thread(target=chunk_text_consumer.start, daemon=True).start()

        async def start_async_consumers():
            extract_text_consumer = Container.resolve("extract_text_consumer")
            await asyncio.gather(
                extract_text_consumer.start()
            )

        asyncio.run(start_async_consumers())

        logger.info("Document processing consumers setup")

    except Exception as e:
        logger.error(f"Error setting up document processing consumers: {e}")
        raise