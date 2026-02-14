from src.di.injector import Injector
from src.http.domain import async_http_client
from src.http.infrastructure.httpx.async_http_client import HttpxAsyncHttpClient



def register_shared_dependencies(injector: Injector):
    injector.register(async_http_client.AsyncHttpClient, HttpxAsyncHttpClient)