import threading
import logging
from src.di.container import Container

logger = logging.getLogger(__name__)

def setup_sessions_consumers():
    try:
        update_embeddings_session_consumer = Container.resolve("update_embeddings_sessions_consumer")
        thread = threading.Thread(target=update_embeddings_session_consumer.start, daemon=True)
        thread.start()

        logger.info("session consumers setup")
    except Exception as e:
        logger.error("Error setting up sessions consumers")
        raise

