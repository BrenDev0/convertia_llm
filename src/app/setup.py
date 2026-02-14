import logging
import asyncio
from src.di.injector import Injector
from src.broker.domain.producer import DocumentsProducer, CommunicationProducer
from src.broker.infrastructure.pikaaio.async_producer import PikaAioCommunicationsProducer, PikaAioDocumentsProducer
from src.http.di import register_shared_dependencies as http_dependencies
from src.persistence.di import register_shared_dependencies as persistance_dependencies
from src.features.communication.di import (
    register_api_dependencies as communication_dependencies,
    register_shared_dependencies as communications_shared_dependencies
)
from src.features.communication.domain import consumers as communications_consumers
from src.features.document_processing.di import (
    register_api_dependencies as documents_dependencies,
    register_shared_dependencies as documents_shared_dependencies
)
from src.features.embeddings.di import (
    register_api_dependencies as embeddings_dependencies,
    register_shared_dependencies as embeddings_shared_dependencies
)
from src.features.sessions.di import (
    register_api_dependencies as sessions_dependencies,
    register_shared_dependencies as sessions_shared_dependencies
)

logger = logging.getLogger(__name__)

def setup_dependencies(injector: Injector):
    injector.register(DocumentsProducer, PikaAioDocumentsProducer)
    injector.register(CommunicationProducer, PikaAioCommunicationsProducer)
    http_dependencies(injector=injector)
    persistance_dependencies(injector=injector)
    communication_dependencies(injector=injector)
    communications_shared_dependencies(injector=injector)
    documents_dependencies(injector=injector)
    documents_shared_dependencies(injector=injector)
    embeddings_dependencies(injector=injector)
    embeddings_shared_dependencies(injector=injector)
    sessions_dependencies(injector=injector)
    sessions_shared_dependencies(injector=injector)


async def setup_consumers(injector: Injector):
    async_consumers =  [
        injector.resolve(communications_consumers.BroadcastingConsumer)
    ]

    for consumer in async_consumers:
        asyncio.create_task(consumer.start())

    logger.info("All consumers started")