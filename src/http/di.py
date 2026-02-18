from src.di import Injector
from .domain import async_http_client
from .infrastructure import HttpxAsyncHttpClient

def register_shared_dependencies(injector: Injector):
    injector.register(async_http_client.AsyncHttpClient, HttpxAsyncHttpClient)