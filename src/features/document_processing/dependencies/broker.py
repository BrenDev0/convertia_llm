import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.broker.dependencies.producers import get_documents_producer
from src.broker.domain import consumer
from src.broker.infrastructure.rabbitmq.consumer import RabbitMqConsumer
from src.features.document_processing.application.event_handlers import chunk_text, extract_text, download_document
from src.features.document_processing.dependencies import chunkers, processors
from src.features.http.dependencies.clients import get_async_http_client

logger = logging.getLogger(__name__)

def get_extract_text_handler() -> extract_text.ExtractTextHandler:
    try:
        instance_key = "extract_text_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = extract_text.ExtractTextHandler(
            pdf_processor=processors.get_pdf_processor(),
            producer=get_documents_producer()
        )
        Container.register(instance_key, handler)
        logger.debug(f"{instance_key} registered")

    return handler


def get_chunk_text_handler() -> chunk_text.ChunkTextHandler:
    try:
        instance_key = "chunk_text_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = chunk_text.ChunkTextHandler(
            text_chunker=chunkers.get_text_chunker(),
            producer=get_documents_producer()
        )
        Container.register(instance_key, handler)
        logger.debug(f"{instance_key} registered")

    return handler

def get_download_document_handler() -> download_document.DownloadDocument:
    try:
        instance_key = "download_document_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = download_document.DownloadDocument(
            async_http_client=get_async_http_client(),
            producer=get_documents_producer()
        )
        Container.register(instance_key, handler)
        logger.debug(f"{instance_key} registered")

    return handler


def get_extract_text_consumer() -> consumer.Consumer:
    try: 
        instance_key = "extraxt_text_consumer"
        consumer = Container.resolve(instance_key)

    except DependencyNotRegistered:
        consumer = RabbitMqConsumer(
            queue_name="documents.extract_text.q",
            handler=get_extract_text_handler()
        )

        Container.register(instance_key, consumer)
        logger.debug(f"{instance_key} register")

    return consumer

def get_chunk_text_consumer() -> consumer.Consumer:
    try: 
        instance_key = "chunk_text_consumer"
        consumer = Container.resolve(instance_key)

    except DependencyNotRegistered:
        consumer = RabbitMqConsumer(
            queue_name="documents.chunk_text.q",
            handler=get_chunk_text_handler()
        )

        Container.register(instance_key, consumer)
        logger.debug(f"{instance_key} register")

    return consumer

def get_download_document_consumer() -> consumer.Consumer:
    try: 
        instance_key = "download_document_consumer"
        consumer = Container.resolve(instance_key)

    except DependencyNotRegistered:
        consumer = RabbitMqConsumer(
            queue_name="documents.download.q",
            handler=get_download_document_handler()
        )

        Container.register(instance_key, consumer)
        logger.debug(f"{instance_key} register")

    return consumer