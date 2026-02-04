import logging
from src.di.container import Container
from src.features.http.infrastructure.httpx.async_http_client import HttpxAsyncHttpClient

logger = logging.getLogger(__name__)

def register_client_dependencies():
    Container.register_factory(
        key="async_http_client",
        factory=lambda: HttpxAsyncHttpClient()
    )

