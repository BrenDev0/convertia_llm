import logging
from src.broker.dependencies.connection import get_broker_connection
from src.features.embeddings.setup import consumers as embeddings_consumers, queues as embeddings_queues
logger = logging.getLogger(__name__)

def __setup_exchanges():
    try:
        connection = get_broker_connection()
        channel = connection.get_channel()

        channel.exchange_declare(
            exchange="documnets",
            exchange_type="topic",
            durable=True
        )
    
    except Exception as e:
        logger.error(str(e))
        raise

    finally:
        channel.close()

def setup_broker():
    __setup_exchanges()


    embeddings_queues.setup_embedding_queues()
    embeddings_consumers.setup_embeddings_consumers()