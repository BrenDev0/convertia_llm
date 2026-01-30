import logging
import threading
from src.features.embeddings.dependencies.broker import get_embed_chunks_consumer

logger = logging.getLogger(__name__)

def setup_embeddings_consumers():
    try:
        embed_chunks_consumer = get_embed_chunks_consumer()
        thread = threading.Thread(target=embed_chunks_consumer.start, daemon=True)
        thread.start()

        
        logger.info("embedding consumers setup")

    except Exception as e:
        logger.error("Error setting up embeddings consumers")
        raise