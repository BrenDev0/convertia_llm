import logging
import threading
from src.di.container import Container


logger = logging.getLogger(__name__)

def setup_knowledge_base_consumers():
    try:
        store_embeddings_consumer = Container.resolve("store_embeddings_consumer")
        thread = threading.Thread(target=store_embeddings_consumer.start, daemon=True)
        thread.start()

        logger.info("Knowledge base consumers setup")

        update_embeddings_status_consumer = Container.resolve("update_embeddings_status_consumer")
        thread = threading.Thread(target=update_embeddings_status_consumer.start, daemon=True)
        thread.start()

    except Exception as e:
        logger.error("Error setting up knowledge base consumers")
        raise