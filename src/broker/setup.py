import logging
from src.broker.infrastructure.rabbitmq.connection import create_connection
from src.features.embeddings.broker import consumers_setup as embeddings_consumers, queues_setup as embeddings_queues
from src.features.document_processing.broker import consumers_setup as document_processing_consumers, queues_setup as document_processesing_queues
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

        logger.info("Exchanges setup")
    
    except Exception as e:
        logger.error(str(e))
        raise

    finally:
        channel.close()
        connection.close()

def setup_broker():
    __setup_exchanges()

    embeddings_queues.setup_embedding_queues()
    document_processesing_queues.setup_document_processing_queues()

    embeddings_consumers.setup_embeddings_consumers()
    document_processing_consumers.setup_document_processing_consumers()