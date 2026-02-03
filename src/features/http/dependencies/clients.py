import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.http.domain import async_http_client
from src.features.http.infrastructure.httpx.async_http_client import HttpxAsyncHttpClient

logger = logging.getLogger(__name__)

def get_async_http_client() -> async_http_client.AsyncHttpClient:
    try:
        instance_key = "async_http_client"
        client = Container.resolve(instance_key)

    except DependencyNotRegistered:
        client = HttpxAsyncHttpClient()
        Container.register(instance_key, client)
        logger.debug(f"{instance_key} registered")

    return client