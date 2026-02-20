import os
from src.broker import AsyncHandler, ChatsProducer
from src.http import AsyncHttpClient, generate_hmac_headers
from ...domain import ChatEvent

class CreateChatHandler(AsyncHandler):
    def __init__(
        self,
        async_http_client: AsyncHttpClient,
        chats_producer: ChatsProducer
    ):
        self.__async_http_client = async_http_client
        self.__chats_producer = chats_producer

    async def handle(self, event):
        parsed_event = ChatEvent(**event)

        app_host = os.getenv("APP_HOST")

        headers = generate_hmac_headers()

        req_body = {
            "chat_id": parsed_event.chat_id,
            "agent_id": parsed_event.agent_id
        }

        await self.__async_http_client.request(
            endpoint=f"{app_host}/chats/",
            method="POST",
            headers=headers,
            req_body=req_body
        )